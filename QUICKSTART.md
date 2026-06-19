# Quick Start (For Advanced Participants)

> **If you're comfortable with terminals and want to skip the detailed guide.**
>
> If anything here fails, switch to `PARTICIPANT_GUIDE.md` for detailed steps.

---

## Prerequisites

- Python 3.11+
- Git
- UV (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

---

## One-Command Setup

```bash
git clone https://github.com/asahfikir/pct-ai-workshop.git
cd pct-ai-workshop
uv venv && uv pip install -r requirements.txt
python api/mock_database.py
```

---

## Run Everything

**Terminal 1 — API Server:**
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac
python api/main.py
```

**Terminal 2 — MCP Server:**
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac
python mcp/server.py
```

**Terminal 3 — Testing:**
```bash
# API health
curl http://localhost:8000/health

# Stats
curl http://localhost:8000/stats/overview

# MCP tools list
curl http://localhost:8001/tools/list

# MCP tool call
curl -X POST http://localhost:8001/tools/call -H "Content-Type: application/json" -d "{\"name\":\"get_student_count\",\"arguments\":{}}"
```

---

## Hermes Integration

In Hermes Desktop, use these prompts:

```
Call the API at http://localhost:8000/stats/overview and summarize the statistics.
```

```
Call the MCP server at http://localhost:8001/tools/list and tell me what tools are available.
```

```
Call the MCP tool "get_today_registrations" at http://localhost:8001/tools/call and report the result.
```

---

## File Structure

```
palembang-workshop/
├── api/
│   ├── mock_database.py      # Generate mock data
│   ├── database.py             # Query helpers
│   └── main.py                 # FastAPI (port 8000)
├── mcp/
│   └── server.py               # MCP server (port 8001)
├── docs/
│   ├── WORKSHOP_SCRIPT.md      # Instructor script
│   ├── PRD_TEMPLATE.md         # PRD framework
│   ├── CAUTIONARY_TALES.md     # Failure stories
│   └── HANDOUT.html            # Visual handout
├── PARTICIPANT_GUIDE.md        # Step-by-step guide
├── TROUBLESHOOTING.md          # Error fixes
└── QUICKSTART.md               # This file
```

---

## Common Issues (Quick Fixes)

| Issue | Fix |
|-------|-----|
| Port 8000 in use | Change port in `api/main.py` or kill existing process |
| `python` not found | Use `python3` (Mac) or `py` (Windows) |
| `uv` not found | Close and reopen terminal |
| Module not found | Make sure `(.venv)` is activated |
| Database missing | Run `python api/mock_database.py` |

---

## Need More Help?

- **Detailed steps:** See `PARTICIPANT_GUIDE.md`
- **Error fixes:** See `TROUBLESHOOTING.md`
- **Instructor script:** See `docs/WORKSHOP_SCRIPT.md`
