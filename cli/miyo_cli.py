import requests
import time
import json
import os
import sys

# Optional: Syntax highlighting and autocomplete
try:
    from pygments import highlight
    from pygments.lexers import guess_lexer, TextLexer
    from pygments.formatters import TerminalFormatter
except ImportError:
    highlight = None
    guess_lexer = None
    TextLexer = None
    TerminalFormatter = None

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.styles import Style
except ImportError:
    prompt = None
    WordCompleter = None
    Style = None

import configparser

CONFIG_PATH = os.path.expanduser("~/.miyo_code_cli.ini")

MODELS = ["gpt-oss-120b", "zai-glm-4.7", "qwen-3-235b"]
MODES = ["low", "pro", "max"]

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    return config

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def get_backend_url(config):
    return os.environ.get("FIREBASE_FUNCTION_URL", config.get("DEFAULT", "backend_url", fallback="https://YOUR_PROJECT.cloudfunctions.net/miyo_request"))

def print_header():
    print("\033[1;36m╔══════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║           MIYO CODE - Claude Style CLI              ║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════════════════════╝\033[0m")

def print_status(model, mode, session_id, backend_url):
    print(f"\033[1;33m[Model: {model}] [Mode: {mode}] [Session: {session_id}]\033[0m")
    print(f"\033[1;34m[Backend: {backend_url}]\033[0m")

def print_help():
    print("\033[1;32mCommands:\033[0m")
    print(":model <name>         - Set model (gpt-oss-120b, zai-glm-4.7, qwen-3-235b)")
    print(":mode <name>          - Set mode (low, pro, max)")
    print(":session <id>         - Set session ID")
    print(":run <file.py>        - Run a Python script (simulated)")
    print(":read <file>          - Read a file and send contents to backend")
    print(":write <file>         - Write backend response to file")
    print(":config [key] [val]   - Show or set config (backend_url)")
    print(":clear                - Clear screen")
    print(":help                 - Show this help")
    print(":exit, :quit          - Exit CLI")

def typewriter_print(text, delay=0.01, highlight_code=False):
    if highlight_code and highlight and guess_lexer and TerminalFormatter:
        try:
            lexer = guess_lexer(text)
        except Exception:
            lexer = TextLexer()
        text = highlight(text, lexer, TerminalFormatter())
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def send_request(prompt_text, model, mode, session_id, backend_url):
    payload = {
        "prompt": prompt_text,
        "model": model,
        "mode": mode,
        "session_id": session_id
    }
    try:
        res = requests.post(backend_url, json=payload)
        return res.json().get("response", "[No response from backend]")
    except Exception as e:
        return f"[Backend error: {e}]"

def main():
    config = load_config()
    model = config.get("DEFAULT", "model", fallback=MODELS[0])
    mode = config.get("DEFAULT", "mode", fallback=MODES[1])
    session_id = config.get("DEFAULT", "session_id", fallback="default")
    backend_url = get_backend_url(config)
    commands = [":model", ":mode", ":session", ":run", ":read", ":write", ":config", ":clear", ":help", ":exit", ":quit"]
    completer = WordCompleter(commands + MODELS + MODES, ignore_case=True) if WordCompleter else None
    style = Style.from_dict({"prompt": "ansicyan bold"}) if Style else None
    print_header()
    print_status(model, mode, session_id, backend_url)
    print("Type ':help' for commands.\n")
    while True:
        try:
            if prompt and completer:
                user_input = prompt("\033[1;35mClaude> \033[0m", completer=completer, style=style)
            else:
                user_input = input("Claude> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        cmd = user_input.strip()
        if not cmd:
            continue
        if cmd in [":exit", ":quit", "exit", "quit"]:
            print("Goodbye!")
            break
        if cmd == ":help":
            print_help()
            continue
        if cmd == ":clear":
            os.system("clear" if os.name == "posix" else "cls")
            print_header()
            print_status(model, mode, session_id, backend_url)
            continue
        if cmd.startswith(":model "):
            m = cmd.split(" ", 1)[1].strip()
            if m in MODELS:
                model = m
                config["DEFAULT"]["model"] = model
                save_config(config)
                print(f"[Model set to {model}]")
            else:
                print(f"[Unknown model. Available: {', '.join(MODELS)}]")
            continue
        if cmd.startswith(":mode "):
            m = cmd.split(" ", 1)[1].strip().lower()
            if m in MODES:
                mode = m
                config["DEFAULT"]["mode"] = mode
                save_config(config)
                print(f"[Mode set to {mode}]")
            else:
                print(f"[Unknown mode. Available: {', '.join(MODES)}]")
            continue
        if cmd.startswith(":session "):
            session_id = cmd.split(" ", 1)[1].strip()
            config["DEFAULT"]["session_id"] = session_id
            save_config(config)
            print(f"[Session set to {session_id}]")
            continue
        if cmd.startswith(":config"):
            parts = cmd.split()
            if len(parts) == 1:
                print(f"backend_url = {backend_url}")
            elif len(parts) == 3:
                key, val = parts[1], parts[2]
                if key == "backend_url":
                    config["DEFAULT"]["backend_url"] = val
                    save_config(config)
                    backend_url = val
                    print(f"[backend_url set to {val}]")
                else:
                    print("[Unknown config key]")
            else:
                print("Usage: :config [key] [value]")
            continue
        if cmd.startswith(":run "):
            file = cmd.split(" ", 1)[1].strip()
            if not os.path.exists(file):
                print(f"[File not found: {file}]")
                continue
            print(f"[Simulating run of {file}]")
            with open(file) as f:
                code = f.read()
            response = send_request(f"Run this code and explain:\n{code}", model, mode, session_id, backend_url)
            typewriter_print(response, highlight_code=True)
            continue
        if cmd.startswith(":read "):
            file = cmd.split(" ", 1)[1].strip()
            if not os.path.exists(file):
                print(f"[File not found: {file}]")
                continue
            with open(file) as f:
                content = f.read()
            response = send_request(f"Analyze this file:\n{content}", model, mode, session_id, backend_url)
            typewriter_print(response, highlight_code=True)
            continue
        if cmd.startswith(":write "):
            file = cmd.split(" ", 1)[1].strip()
            print("[Writing backend response to file]")
            response = send_request("Suggest code for this file.", model, mode, session_id, backend_url)
            with open(file, "w") as f:
                f.write(response)
            print(f"[Wrote response to {file}]")
            continue
        # Default: send as prompt
        typewriter_print("MIYO CODE is thinking...\n")
        response = send_request(cmd, model, mode, session_id, backend_url)
        highlight_code = response.strip().startswith("def ") or response.strip().startswith("class ")
        typewriter_print(response, highlight_code=highlight_code)

if __name__ == "__main__":
    main()
