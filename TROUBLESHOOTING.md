# Troubleshooting Guide

> **Every error I've seen, with copy-paste fixes.**
> 
> If your error isn't here, take a screenshot and ask the instructor.

---

## Installation Errors

### Error: "python is not recognized as an internal or external command"

**What it means:** Python isn't in your system PATH.

**Fix for Windows:**
1. Try `py --version` instead
2. If that works, use `py` instead of `python` for all commands
3. If neither works, reinstall Python and check "Add Python to PATH"

**Fix for Mac:**
1. Try `python3 --version` instead
2. Use `python3` instead of `python` for all commands

**Quick workaround:**
```bash
# Windows
py api/mock_database.py
py api/main.py

# Mac
python3 api/mock_database.py
python3 api/main.py
```

---

### Error: "uv is not recognized"

**What it means:** UV wasn't installed or the terminal needs to be restarted.

**Fix:**
1. Close ALL terminal windows
2. Open a new terminal
3. Try `uv --version` again

**If still not working:**
- Windows: Check if `uv.exe` is in `C:\Users\YOURNAME\.local\bin\`
- Mac: Check if `uv` is in `~/.local/bin/`

**Alternative:** Use `pip` instead of `uv`:
```bash
python -m venv .venv
.venv\Scripts\activate     (Windows)
source .venv/bin/activate  (Mac)
pip install -r requirements.txt
```

---

### Error: "No module named pip" (when using python -m pip)

**What it means:** Your Python installation is minimal and doesn't include pip.

**Fix:**
```bash
# Download get-pip.py
python -m ensurepip --upgrade

# Or use uv (which doesn't need pip):
uv venv
uv pip install -r requirements.txt
```

---

## Git Errors

### Error: "fatal: not a git repository"

**What it means:** You're trying to run git commands but you're not in a git folder.

**Fix:**
```bash
# Make sure you're in the right folder
cd Documents\palembang-workshop

# Check if .git folder exists
ls .git   (Mac)
dir .git  (Windows)

# If not, clone again:
cd ..
git clone https://github.com/YOUR_USERNAME/palembang-workshop.git
cd palembang-workshop
```

---

### Error: "fatal: unable to access"

**What it means:** Network issue or wrong URL.

**Fix:**
1. Check your internet connection
2. Make sure the URL is correct (ask instructor)
3. Try again — sometimes it's just a temporary glitch

---

## Virtual Environment Errors

### Error: "No such file or directory: '.venv'"

**What it means:** The virtual environment wasn't created or you're in the wrong folder.

**Fix:**
```bash
# Make sure you're in the project folder
pwd                    (Mac)
cd                     (Windows)

# You should see the palembang-workshop path

# Create the venv
uv venv

# If uv doesn't work, use python:
python -m venv .venv
```

---

### Error: "Cannot activate: .venv\Scripts\activate is not recognized"

**What it means:** Windows PowerShell execution policy is blocking the script.

**Fix for Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```bash
.venv\Scripts\activate
```

**Alternative:** Use Command Prompt instead of PowerShell:
1. Press Win+R, type `cmd`, press Enter
2. Navigate to the project folder
3. Run `.venv\Scripts\activate.bat`

---

### Error: "source: no such file or directory: .venv/bin/activate"

**What it means:** You're on Mac/Linux but the venv was created with Windows paths, or vice versa.

**Fix:**
```bash
# Check if .venv exists
ls -la .venv

# If it exists but structure is wrong, recreate it:
rm -rf .venv
uv venv
source .venv/bin/activate
```

---

## Database Errors

### Error: "sqlite3.OperationalError: no such table: students"

**What it means:** The database file exists but doesn't have the tables, or the database file is missing.

**Fix:**
```bash
# Recreate the database
python api/mock_database.py
```

**If that fails:**
```bash
# Delete the old database and recreate
rm academic.db          (Mac)
del academic.db         (Windows)
python api/mock_database.py
```

---

### Error: "sqlite3.IntegrityError: UNIQUE constraint failed"

**What it means:** The mock data generator tried to create duplicate data.

**Fix:**
```bash
# Delete and recreate
del academic.db         (Windows)
rm academic.db          (Mac)
python api/mock_database.py
```

---

## API Server Errors

### Error: "Address already in use" (Port 8000)

**What it means:** Something else is using port 8000.

**Fix Option 1: Find and kill the process**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac:
lsof -i :8000
kill -9 <PID_NUMBER>
```

**Fix Option 2: Use a different port**
Edit `api/main.py` and change the last line:
```python
uvicorn.run(app, host="0.0.0.0", port=8002)  # Changed from 8000
```

Then access the API at `http://localhost:8002`

---

### Error: "ModuleNotFoundError: No module named 'database'"

**What it means:** Python can't find the database module.

**Fix:**
```bash
# Make sure you're in the project root folder
pwd

# Make sure .venv is activated
# You should see (.venv) in your prompt

# Try running from the project root:
python api/main.py

# NOT from inside the api folder:
# cd api          <-- DON'T DO THIS
# python main.py  <-- THIS WILL FAIL
```

---

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**What it means:** Dependencies aren't installed in the virtual environment.

**Fix:**
```bash
# Make sure .venv is activated
.venv\Scripts\activate     (Windows)
source .venv/bin/activate  (Mac)

# Install dependencies
uv pip install -r requirements.txt

# Or with pip:
pip install -r requirements.txt
```

---

## MCP Server Errors

### Error: "ModuleNotFoundError: No module named 'database'" (from mcp/server.py)

**What it means:** The MCP server can't find the database module because the path isn't set up.

**Fix:**
```bash
# Make sure you're in the project root folder
# Make sure .venv is activated
python mcp/server.py
```

**If still failing:**
The `mcp/server.py` already has `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))` which should work. If it doesn't:

```bash
# Set PYTHONPATH explicitly (Windows)
set PYTHONPATH=%CD%\api
python mcp/server.py

# Set PYTHONPATH explicitly (Mac)
export PYTHONPATH=$PWD/api
python mcp/server.py
```

---

## curl Errors

### Error: "curl is not recognized"

**What it means:** Windows doesn't have curl installed by default (older versions).

**Fix Option 1: Use PowerShell**
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing
```

**Fix Option 2: Use Browser**
Open `http://localhost:8000/docs` in your browser and test the API there.

**Fix Option 3: Install curl**
Download from https://curl.se/windows/

---

### Error: "Failed to connect to localhost port 8000"

**What it means:** The API server isn't running.

**Fix:**
1. Check if Terminal 2 (the API server) is still open
2. If it crashed, restart it: `python api/main.py`
3. Wait 5 seconds for it to start
4. Try the curl command again

---

### Error: "curl: (6) Could not resolve host"

**What it means:** You have a typo in the URL.

**Fix:**
```bash
# Make sure it's localhost (not localhos or localhot)
curl http://localhost:8000/health

# Make sure it's http (not https)
curl http://localhost:8000/health
```

---

## Windows-Specific Issues

### Issue: Backslash vs Forward Slash

**What it means:** Windows uses backslash (`\`) but sometimes forward slash (`/`) works too.

**Fix:**
```bash
# Both of these work in most modern Windows terminals:
cd Documents\palembang-workshop
cd Documents/palembang-workshop

# For paths with spaces, use quotes:
cd "My Documents/palembang-workshop"
```

---

### Issue: Terminal Opens in Wrong Directory

**What it means:** Your terminal starts in `C:\Users\You` but the project is in `Documents`.

**Fix:**
```bash
# Always navigate first
cd Documents
cd palembang-workshop

# Or in one line:
cd Documents\palembang-workshop
```

---

## Mac-Specific Issues

### Issue: "Permission denied" when activating venv

**What it means:** The activate script doesn't have execute permission.

**Fix:**
```bash
chmod +x .venv/bin/activate
source .venv/bin/activate
```

---

### Issue: "zsh: command not found: python"

**What it means:** Mac uses `python3` by default, not `python`.

**Fix:**
```bash
# Use python3 instead of python
python3 api/mock_database.py
python3 api/main.py

# Or create an alias:
alias python=python3
```

---

## The "Nuclear Option" (When Nothing Works)

If you've tried everything and nothing works:

```bash
# 1. Delete everything and start fresh
cd Documents
rm -rf palembang-workshop       (Mac)
rmdir /s /q palembang-workshop  (Windows)

# 2. Clone again
git clone https://github.com/YOUR_USERNAME/palembang-workshop.git

# 3. Recreate venv
cd palembang-workshop
uv venv
.venv\Scripts\activate     (Windows)
source .venv/bin/activate  (Mac)

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Create database
python api/mock_database.py

# 6. Start API
python api/main.py
```

---

## Still Stuck?

**Before asking for help, gather this information:**

1. What command did you run?
2. What error message did you see? (copy-paste the exact text)
3. What folder are you in? (run `pwd` or `cd` and tell us the output)
4. Is `(.venv)` showing in your prompt?
5. What operating system are you using? (Windows 10/11, Mac, etc.)

**The instructor needs this information to help you quickly.**

---

## Prevention Checklist

Before you start, make sure:

- [ ] Python installed and working (`python --version` or `python3 --version`)
- [ ] Git installed and working (`git --version`)
- [ ] UV installed and working (`uv --version`)
- [ ] Repository cloned (`ls` shows `api/`, `mcp/`, `docs/`)
- [ ] Virtual environment created (`ls .venv` shows folders)
- [ ] Dependencies installed (`uv pip list` shows fastapi, uvicorn, etc.)
- [ ] Database created (`academic.db` exists in the project folder)

If all of these are checked, 90% of problems are avoided.
