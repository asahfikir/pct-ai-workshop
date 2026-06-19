# Participant Guide: Step-by-Step

> **For everyone, especially those who need extra guidance.**
>
> If you get stuck at ANY step, raise your hand. We won't leave you behind.

---

## BEFORE THE WORKSHOP (Do This at Home)

### Step 1: Install Python

**Windows:**
1. Go to https://python.org/downloads
2. Click "Download Python 3.11.x"
3. Run the installer
4. **IMPORTANT:** Check the box "Add Python to PATH" at the bottom
5. Click "Install Now"

**Mac:**
1. Open Terminal (Cmd+Space, type "Terminal")
2. Type: `python3 --version`
3. If you see a version number (like `Python 3.11.4`), you're done
4. If not, go to https://python.org/downloads and install Python 3.11

**Verify it works:**
```bash
python --version
```
You should see something like `Python 3.11.4`.

**If you see an error:**
- Windows: Try `py --version` instead of `python --version`
- Mac: Try `python3 --version` instead of `python --version`

---

### Step 2: Install Git

**Windows:**
1. Go to https://git-scm.com/download/win
2. Download and run the installer
3. Accept all defaults (just click Next, Next, Next...)

**Mac:**
1. Open Terminal
2. Type: `git --version`
3. If you see a version number, you're done
4. If not, you'll see a prompt to install Xcode Command Line Tools. Click "Install"

**Verify it works:**
```bash
git --version
```

---

### Step 3: Install UV (Package Manager)

UV is a fast Python package manager. We'll use it instead of `pip`.

**Windows:**
Open PowerShell and run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac:**
Open Terminal and run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify it works:**
```bash
uv --version
```
You should see something like `uv 0.11.x`.

**If you see "command not found":**
- Close and reopen your terminal/PowerShell
- Try again

---

## DAY 1: BEFORE SESSION 1 STARTS

### Step 4: Clone the Repository

Open your terminal (Windows: PowerShell or Git Bash; Mac: Terminal) and run:

```bash
cd Documents
```

```bash
git clone https://github.com/asahfikir/pct-ai-workshop.git
```

**Replace `YOUR_USERNAME` with the actual GitHub username.**

**If you don't know the exact URL:** Ask the instructor or look at the QR code on the projector.

**Verify it worked:**
```bash
cd palembang-workshop
ls
```

You should see folders like `api/`, `mcp/`, `docs/`.

**If `git clone` fails:**
- Check your internet connection
- Try again — sometimes it's just a temporary glitch
- Ask your neighbor or the instructor

---

### Step 5: Create the Virtual Environment

In the same terminal (you should be in `palembang-workshop` folder):

```bash
uv venv
```

You should see:
```
Using CPython 3.x.x
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate  (Windows)
```

**Activate the virtual environment:**

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac:**
```bash
source .venv/bin/activate
```

**How do you know it's activated?** Your terminal prompt will show `(.venv)` at the beginning.

Example:
```
(.venv) C:\Users\You\Documents\palembang-workshop>
```

**If activation fails:**
- Windows: Try `\.venv\Scripts\activate` (with backslash)
- Mac: Make sure you typed `source` before the path

---

### Step 6: Install Dependencies

With the virtual environment activated (you see `(.venv)` in your prompt):

```bash
uv pip install -r requirements.txt
```

You should see a list of packages being installed:
```
 + fastapi==0.x.x
 + uvicorn==0.x.x
 + requests==2.x.x
 + pydantic==2.x.x
```

**If this fails:**
- Make sure you're in the `palembang-workshop` folder
- Make sure `(.venv)` is showing in your prompt
- Try again — sometimes network hiccups happen

---

### Step 7: Create the Database

Still with `(.venv)` in your prompt:

```bash
python api/mock_database.py
```

You should see:
```
Creating mock academic database...
Generated 200 students
Generated 20 courses
Generated 868 registrations
Generated 5243 grade records

==================================================
DATABASE SUMMARY
==================================================
Students: 200
Courses: 20
Registrations: 868
Grades: 5243
Today's registrations: 34
```

**If you see an error:**
- Make sure you're in the `palembang-workshop` folder
- Make sure `(.venv)` is showing
- Ask for help — don't spend more than 2 minutes trying to fix it alone

---

## DURING SESSION 1

### Step 8: Start the API Server

Open a **NEW terminal window** (don't close the old one).

**Windows:** Right-click the terminal icon and open a new window.
**Mac:** Press Cmd+N in Terminal.

Navigate to the project:
```bash
cd Documents\palembang-workshop
```

Activate the virtual environment again:
```bash
.venv\Scripts\activate     (Windows)
source .venv/bin/activate    (Mac)
```

Start the API:
```bash
python api/main.py
```

You should see:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to stop)
```

**IMPORTANT:** This terminal is now running the server. Don't close it. Don't type anything else in it. Just leave it open.

**To stop the server later:** Press `CTRL+C` in this terminal.

---

### Step 9: Test the API (Quick Check)

Open a **THIRD terminal window** (yes, you'll have three terminals open).

Navigate and activate:
```bash
cd Documents\palembang-workshop
.venv\Scripts\activate     (Windows)
source .venv/bin/activate    (Mac)
```

Test with curl:
```bash
curl http://localhost:8000/health
```

You should see:
```json
{"status":"healthy","database":"connected"}
```

**If you see "Failed to connect":**
- Make sure the API server is still running (check Terminal 2)
- Make sure you typed `localhost` not `localhos`
- Wait 5 seconds and try again — sometimes it takes a moment to start

---

### Step 10: Try the Endpoints

In the same terminal (Terminal 3), try these one by one:

```bash
curl http://localhost:8000/stats/overview
```

You should see a JSON with statistics. It will look messy in the terminal. That's normal.

```bash
curl http://localhost:8000/students | findstr /c:"first_name"    (Windows)
curl http://localhost:8000/students | grep "first_name"          (Mac)
```

This shows just the first names from the student list.

**If curl is not found (Windows):**
- Use your browser instead: open `http://localhost:8000/docs`
- You'll see a nice web interface to test the API
- Click on any endpoint, then click "Try it out", then "Execute"

---

## DURING SESSION 2

### Step 11: Start the MCP Server

You'll need the API server still running (Terminal 2).

Open a **FOURTH terminal window**.

Navigate and activate:
```bash
cd Documents\palembang-workshop
.venv\Scripts\activate     (Windows)
source .venv/bin/activate    (Mac)
```

Start the MCP server:
```bash
python mcp/server.py
```

You should see:
```
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to stop)
```

**Leave this terminal open.** Now you have:
- Terminal 1: Original (for creating database, etc.)
- Terminal 2: API server (port 8000)
- Terminal 3: Testing commands
- Terminal 4: MCP server (port 8001)

---

### Step 12: Test the MCP Server

In Terminal 3 (or open a fifth one), test:

```bash
curl http://localhost:8001/tools/list
```

You should see a list of available tools like `get_student_count`, `get_today_registrations`, etc.

Test calling a tool:
```bash
curl -X POST http://localhost:8001/tools/call -H "Content-Type: application/json" -d "{\"name\":\"get_student_count\",\"arguments\":{}}"
```

**Windows users:** If the above doesn't work, try:
```bash
curl -X POST http://localhost:8001/tools/call -H "Content-Type: application/json" -d "{\"name\":\"get_student_count\",\"arguments\":{}}"
```

You should see:
```json
{"content":[{"type":"text","text":"There are 200 students in the database."}],"data":{"count":200}}
```

---

## IF YOU'RE STUCK

### Common Problems and Solutions

#### Problem: "python is not recognized"
**Solution:**
- Windows: Try `py` instead of `python`
- Mac: Try `python3` instead of `python`

#### Problem: "uv is not recognized"
**Solution:**
- Close ALL terminal windows
- Open a new one
- Try again
- If still not working, ask the instructor

#### Problem: "No module named 'database'"
**Solution:**
- Make sure you're in the `palembang-workshop` folder
- Make sure `(.venv)` is showing in your prompt
- Try: `python -c "import api.database; print('OK')"`

#### Problem: Port 8000 is already in use
**Solution:**
```bash
# Find what's using it (Windows):
netstat -ano | findstr :8000

# Or just use a different port by editing api/main.py:
# Change port=8000 to port=8002
```

#### Problem: "I don't see (.venv) in my prompt"
**Solution:**
- You forgot to activate the virtual environment
- Run the activate command again (see Step 5)

#### Problem: "curl is not recognized" (Windows)
**Solution:**
- Use your browser instead: `http://localhost:8000/docs`
- Or install curl: https://curl.se/windows/
- Or ask the instructor for an alternative

#### Problem: Everything worked yesterday but not today
**Solution:**
- Make sure you're in the right folder
- Make sure `(.venv)` is activated
- The database file (`academic.db`) might be missing — run `python api/mock_database.py` again

---

## FOR NON-TECHNICAL PARTICIPANTS

### You Don't Need to Run Code

If you're not comfortable with terminals and code, **that's okay**. Here's what you can do:

1. **Watch the instructor's screen** — everything will be projected
2. **Use the browser interface** — go to `http://localhost:8000/docs` and click buttons
3. **Ask questions** — your perspective (management, finance, etc.) is valuable
4. **Focus on concepts** — you don't need to understand Python to understand "data that was locked is now accessible"

### What You Should Understand by the End

- [ ] What is an agent vs. a chatbot?
- [ ] Why is read-only access safer than write access?
- [ ] What is MCP and why does it matter for avoiding vendor lock-in?
- [ ] What questions should I ask my technical team?
- [ ] What are the risks of rushing to production?

---

## QUICK REFERENCE CARD

### Commands You Need

```bash
# Activate virtual environment
.venv\Scripts\activate          (Windows)
source .venv/bin/activate      (Mac)

# Create database
python api/mock_database.py

# Start API server
python api/main.py

# Start MCP server (in another terminal)
python mcp/server.py

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/stats/overview

# Test MCP
curl http://localhost:8001/tools/list
curl -X POST http://localhost:8001/tools/call -H "Content-Type: application/json" -d "{\"name\":\"get_student_count\",\"arguments\":{}}"
```

### URLs to Remember

| Service | URL | What It Does |
|---------|-----|--------------|
| API Docs | http://localhost:8000/docs | Interactive API testing |
| API Health | http://localhost:8000/health | Check if API is running |
| MCP Tools | http://localhost:8001/tools/list | See available MCP tools |

---

## AFTER THE WORKSHOP

### Keep Learning

1. **Try modifying the code:**
   - Add a new endpoint in `api/main.py`
   - Add a new tool in `mcp/server.py`
   - See what breaks and why

2. **Connect to different AI agents:**
   - Try Claude Code with the MCP server
   - Try asking questions in Indonesian
   - See how different agents handle the same data

3. **Read the cautionary tales:**
   - Open `docs/CAUTIONARY_TALES.md`
   - Think about which ones apply to your organization
   - Discuss with your team

### Get Help

- **GitHub Issues:** If you find a bug, open an issue at the repo
- **Email the instructor:** For questions about concepts
- **Your technical team:** For implementation questions

---

> **Remember:** The goal is not to become a programmer in 6 hours. The goal is to understand what's possible, what the risks are, and what questions to ask.
>
> **If you're stuck, ask. If you're confused, ask. If you're bored, help your neighbor.**
