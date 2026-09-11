You can install **uv** in one line:

**macOS / Linux (official installer):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**macOS (Homebrew):**
```bash
brew install uv
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After install, restart your terminal (or run `source ~/.zshrc`), then check:
```bash
uv --version
```

Docs: https://docs.astral.sh/uv/getting-started/installation/