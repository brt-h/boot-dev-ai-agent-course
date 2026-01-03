# AI Coding Agent

A CLI tool that uses Google's Gemini API to autonomously explore and interact with a codebase — essentially a toy version of Cursor/Zed's agent mode or Claude Code. Built as part of the [Boot.dev Build an AI Agent in Python course](https://www.boot.dev/courses/build-ai-agent-python).

## How It Works

The agent takes a natural language prompt and iteratively:
1. Sends the prompt (and conversation history) to Gemini
2. If Gemini requests a tool call → executes it and feeds results back
3. If Gemini has a final answer → prints it and exits

The agent can list directories, read files, execute Python scripts, and write files — all sandboxed to the `calculator/` directory.

## Setup

```bash
# Install dependencies
uv sync

# Set your Gemini API key
echo "GEMINI_API_KEY=your-key-here" > .env
```

## Usage

```bash
# Ask a question about the codebase
uv run main.py "Explain how the calculator renders results to the console"

# Run with verbose output
uv run main.py "List the contents of the pkg directory" --verbose

# Have it execute code
uv run main.py "Run the calculator tests and tell me if they pass"
```

## Project Structure

```
main.py              # Entry point and agent loop
call_function.py     # Tool registry and function dispatcher
prompts.py           # System prompt for Gemini
config.py            # Constants (MAX_CHARS, MAX_ITERATIONS)
functions/
  get_files_info.py  # List directory contents
  get_file_content.py # Read file contents
  run_python_file.py # Execute Python scripts
  write_file.py      # Write/overwrite files
calculator/          # Sandboxed target codebase
```

## Notable Implementation Details

**Gemini Function Calling** — Tools are defined using `types.FunctionDeclaration` schemas that describe parameters, types, and requirements. Gemini returns structured `function_call` objects rather than text, enabling reliable tool execution.

**Path Traversal Prevention** — Each tool validates paths using `os.path.commonpath()` to ensure requests can't escape the sandboxed `calculator/` directory.

**Subprocess Isolation** — Python scripts run via `subprocess.run()` with `capture_output=True`, `timeout=30`, and command-as-list pattern to prevent hangs, capture output for the LLM, and avoid shell injection.

**Conversation History as State** — The model is stateless; each API call sends the full conversation history (user prompt, model responses, tool results). The agent maintains state by accumulating messages and replaying them on every iteration.

## Caution

Be very cautious about giving an LLM access to your filesystem and Python interpreter. This project sandboxes operations to the `calculator/` directory, but production tools require much more robust security measures.
