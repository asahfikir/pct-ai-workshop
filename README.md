# Palembang Agentic Workshop — Starter Kit

> **Goal:** Demonstrate how to unlock a legacy PHP monolith by wrapping it with a read-only API and exposing it to AI agents via MCP.
>
> **Caution:** This is a **teaching artifact**, not production code. It intentionally omits authentication, rate limiting, input validation, and scalability considerations so we can focus on concepts. Every shortcut is documented.

---

## Project Structure

```
palembang-workshop/
├── api/
│   ├── mock_database.py      # Creates realistic SQLite academic data
│   ├── database.py           # Database connection & query helpers
│   └── main.py               # FastAPI read-only API
├── mcp/
│   └── server.py             # Simple HTTP MCP server (Option A)
├── tests/
│   └── test_api.py           # Sanity checks
├── docs/
│   ├── WORKSHOP_SCRIPT.md    # Your exact demo script
│   ├── PRD_TEMPLATE.md       # The PRD framework to teach
│   └── CAUTIONARY_TALES.md   # Real-world failure modes
├── requirements.txt
└── README.md                 # This file
```

---

## Quick Start (Your Laptop — Demo Mode)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create mock database
python api/mock_database.py

# 4. Start the API
python api/main.py
# → API running at http://localhost:8000

# 5. In another terminal, start the MCP server
python mcp/server.py
# → MCP running at http://localhost:8001
```

---

## Quick Start (Participant Laptop — Minimal Setup)

If participants don't have Python or can't install packages, they can still:

1. **Watch your demo** on the projector
2. **Use curl** to test the API (no install needed, just curl)
3. **Ask questions via Hermes/Claude/Codex** if they have it installed

For those who want to run locally:
```bash
# Clone the repo
git clone https://github.com/asahfikir/pct-ai-workshop.git
cd palembang-workshop

# Setup (one time)
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate    # Mac
uv pip install -r requirements.txt

# Create database
python api/mock_database.py

# Start API
python api/main.py
```

**Need detailed instructions?** See [PARTICIPANT_GUIDE.md](PARTICIPANT_GUIDE.md) — step-by-step with screenshots.

**Stuck on an error?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — every error with a fix.

**Just want the commands?** See [QUICKSTART.md](QUICKSTART.md) — for experienced developers.

---

## API Endpoints (Read-Only)

| Endpoint | Description | Example |
|----------|-------------|---------|
| `GET /health` | Health check | `curl http://localhost:8000/health` |
| `GET /students` | List all students | `curl http://localhost:8000/students` |
| `GET /students/{id}` | Get student by ID | `curl http://localhost:8000/students/1` |
| `GET /registrations/today` | Count today's registrations | `curl http://localhost:8000/registrations/today` |
| `GET /courses` | List courses | `curl http://localhost:8000/courses` |
| `GET /stats/overview` | Aggregate stats | `curl http://localhost:8000/stats/overview` |

---

## MCP Server (HTTP-based)

The MCP server exposes two endpoints:

```bash
# List available tools
GET http://localhost:8001/tools/list

# Call a tool
POST http://localhost:8001/tools/call
Content-Type: application/json

{
  "name": "get_student_count",
  "arguments": {}
}
```

**Why HTTP-based?** It's just a REST API. No SDK to learn. The official MCP SDK uses stdio/SSE — we mention this as "the production upgrade path."

---

## Caution: What This Is NOT

| Aspect | This Workshop | Production Reality |
|--------|-------------|-------------------|
| **Authentication** | None | OAuth2, JWT, API keys |
| **Authorization** | None | Role-based access control |
| **Rate Limiting** | None | 100 req/min per user |
| **Input Validation** | Minimal | Strict schema validation |
| **SQL Injection** | Protected by ORM | Parameterized queries + WAF |
| **Error Handling** | Basic | Structured logging, alerting |
| **Scalability** | Single process | Load balancer, multiple workers |
| **Database** | SQLite file | MySQL/PostgreSQL with replication |
| **Testing** | Sanity checks | Unit, integration, load, security tests |
| **Deployment** | Localhost | Docker, CI/CD, monitoring |

**Every shortcut is marked with `# CAUTION:` in the code.**

---

## Workshop Narrative

### Session 1: "We Have Data, But It's Trapped"

1. **The Monolith** — Show their PHP app diagram. Data is in MySQL. Only the web app can touch it.
2. **The Question** — "How many students registered today?" Currently: open PHPMyAdmin, write SQL, run query. Tomorrow: ask an agent.
3. **The Bridge** — Build a read-only API. Now ANY authorized tool can ask questions.
4. **The Agent** — Hermes calls the API. Natural language → structured query → answer.

### Session 2: "Standardizing the Bridge"

1. **The Problem** — Every agent needs custom code to talk to our API. Claude needs one script, Codex needs another.
2. **The Solution** — MCP: one standard protocol, any agent.
3. **The Demo** — Same MCP server, three different consumers: Hermes, Claude Code, curl.
4. **The Roadmap** — What comes next: auth, write operations, microservices, monitoring.

---

## Requirements

```
fastapi
uvicorn
requests
```

---

## License

MIT — for teaching purposes only. Not for production use without hardening.
