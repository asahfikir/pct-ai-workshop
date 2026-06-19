# Workshop Demo Script

> **Your exact talking points and prompts for each segment.**
> Print this or keep it on a second screen.

---

## PRE-WORKSHOP CHECKLIST

- [ ] Laptop charged, projector tested
- [ ] `python api/mock_database.py` ran successfully
- [ ] `python api/main.py` running on port 8000
- [ ] `python mcp/server.py` running on port 8001
- [ ] Hermes Desktop open, new session ready
- [ ] Browser open to `http://localhost:8000/docs` (FastAPI Swagger)
- [ ] Terminal ready with curl commands
- [ ] Backup plan: screenshots if live demo fails

---

## SESSION 1: "We Have Data, But It's Trapped" (3 hours)

### Segment 1: The Problem (0:00-0:20)

**You say:**
> "You have a PHP application. It's been running for years. It has student data, grades, registrations — everything. But there's a problem: only the web application can talk to the database. If your rector asks 'How many students registered today?' at 10 PM, what do you do?"

**Let them answer.** Guide them to: "Open PHPMyAdmin, write SQL, run query."

**You say:**
> "That's fine for you. But what if the rector wants to ask that question every day? What if 10 department heads want different reports? What if you want an AI assistant to help generate those reports?"

**Show the monolith diagram** (draw on whiteboard or show slide):
```
[Browser] → [PHP App] → [MySQL Database]
              ↑
         Only this can ask questions
```

---

### Segment 2: What Is an Agent? (0:20-0:50)

**You say:**
> "An agent is not just a chatbot. A chatbot answers from what it already knows. An agent can DO things — call APIs, read files, run code — to find answers it doesn't already have."

**Live Demo 1: Hermes without tools**

Open Hermes. Type:
```
How many students registered today?
```

**Hermes will say something like:** "I don't have access to your database."

**You say:**
> "See? It WANTS to help, but it has no way to reach your data. It's like a smart person locked in a room with no phone."

**Live Demo 2: Hermes with a simple calculation**

Type:
```
What is 2 + 2?
```

**You say:**
> "This it can answer — it knows math. But your student data? It has no idea. We need to give it a tool."

---

### Segment 3: Build the Bridge — The API (0:50-1:30)

**You say:**
> "The solution is to build a bridge between the database and the outside world. Not the whole PHP app — just a read-only window. Think of it as a librarian who can look up books but can't burn the library."

**Show the new architecture:**
```
[Browser] → [PHP App] → [MySQL Database]
              ↑
         [NEW: Read-Only API] → [Same Database]
              ↑
         [Hermes / Claude / Codex]
```

**Run the API live:**

```bash
cd /d/Teaching/palembang-workshop
python api/mock_database.py
python api/main.py
```

**Show the Swagger docs:** Open browser to `http://localhost:8000/docs`

**Test with curl:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/students | head -c 500
curl http://localhost:8000/stats/overview
```

**You say:**
> "This API has no authentication. Anyone on the network can access it. In production, this is a disaster. But for learning, it lets us focus on the concept."

**Point out the CAUTION comments in the code.**

---

### Segment 4: Connect to Hermes (1:30-2:15)

**You say:**
> "Now we give Hermes the ability to call this API. There are two ways: custom code, or a standard protocol. Let's start with custom code — then you'll appreciate why standards matter."

**In Hermes, type:**

```
I have an API running at http://localhost:8000. Please call the /stats/overview endpoint and tell me what you find.
```

**Hermes should use the web tool** to fetch the data and summarize it.

**You say:**
> "Great! But notice what just happened: I had to TELL Hermes about the API. If I switch to Claude Code, I have to tell Claude too. If I switch to Codex, I tell Codex. Every agent needs custom instructions. This doesn't scale."

---

### Segment 5: The "Aha" Moment — Non-Tech Participants Ask (2:15-2:45)

**You say:**
> "Now, the important part. I want the non-technical participants to try. You don't need to know SQL. You don't need to know Python. You just need to ask questions in Indonesian or English."

**Invite a non-tech participant to suggest a question.** Examples:
- "Berapa jumlah mahasiswa aktif?"
- "What's the average GPA?"
- "How many students are in Teknik Informatika?"

**Type their question into Hermes.** Let everyone see the answer.

**You say:**
> "This person just queried a database without learning SQL. That's the power. But remember — this is read-only. The agent cannot delete, cannot modify. That's intentional."

---

### Segment 6: The Cautionary Moment (2:45-3:00)

**You say:**
> "Before we break, I need to show you something. This API has no authentication. Watch."

**In a new terminal, type:**
```bash
curl http://localhost:8000/students | wc -c
```

**You say:**
> "I just downloaded all student data. Names, emails, GPAs — everything. In a real system, this would be behind login, rate limits, and encryption. This is why we say 'teaching artifact, not production.'"

**Show the PRD template** (briefly, tease Session 2):
> "Tomorrow, we'll learn how to write requirements that prevent these problems."

---

## SESSION 2: "Standardizing with MCP" (3 hours)

### Segment 1: Recap + MCP Concept (0:00-0:30)

**You say:**
> "Yesterday we built a custom bridge. It worked, but it was bespoke — custom for Hermes, custom for our API. Today we learn MCP: Model Context Protocol. Think of it as USB for AI agents."

**Draw the analogy:**
```
Before MCP:
[Hermes] → [custom code] → [Your API]
[Claude] → [different code] → [Your API]
[Codex]  → [different code] → [Your API]

After MCP:
[Hermes] → [MCP] → [Your API]
[Claude] → [MCP] → [Your API]
[Codex]  → [MCP] → [Your API]
```

**You say:**
> "MCP is a standard. You build it once, any agent can use it."

---

### Segment 2: Build the MCP Server (0:30-1:30)

**Show the MCP server code:**

```bash
cat mcp/server.py
```

**Highlight the key parts:**
- `GET /tools/list` — what can this server do?
- `POST /tools/call` — do it

**You say:**
> "This is a simplified HTTP version. The official MCP SDK uses stdio or SSE — more complex, more robust. But the concepts are identical: list tools, call tools, return results."

**Start the MCP server:**
```bash
python mcp/server.py
```

**Test it with curl:**
```bash
curl http://localhost:8001/tools/list

curl -X POST http://localhost:8001/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_student_count", "arguments": {}}'
```

---

### Segment 3: Multi-Tool Demo (1:30-2:15)

**You say:**
> "Now the proof. Same MCP server, three different consumers."

**Demo 1: Hermes**

In Hermes, explain that you'll use the MCP server. Since Hermes doesn't have native MCP client built-in (yet), show how you'd conceptually connect it — or use the `web` tool to call the MCP HTTP endpoints directly.

Type:
```
Call the MCP server at http://localhost:8001/tools/list and tell me what tools are available.
```

Then:
```
Call the tool "get_stats_overview" on the MCP server at http://localhost:8001/tools/call
```

**Demo 2: curl**

```bash
curl -X POST http://localhost:8001/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_today_registrations", "arguments": {}}'
```

**You say:**
> "Same server. Different client. No custom code for each. That's the power of standardization."

**Demo 3: Mention Claude Code / Codex**

**You say:**
> "If you have Claude Code or Codex installed, the same MCP server works. You'd configure it in their settings. The server doesn't care who's asking."

---

### Segment 4: The PRD Framework (2:15-2:45)

**You say:**
> "Now, the most important part. AI makes coding easy. But easy coding is not the same as good engineering. Let me show you why."

**Show the PRD template:**

```markdown
# Project Requirements Document

## 1. PROBLEM STATEMENT
What business problem does this solve?

## 2. FUNCTIONAL REQUIREMENTS
What must it DO?

## 3. NON-FUNCTIONAL REQUIREMENTS
- Expected load: ___ concurrent users
- Data volume: ___ records
- Availability: ___% uptime
- Security: ___

## 4. CONSTRAINTS
- Must work with existing MySQL
- Budget: ___
- Team skills: ___

## 5. ACCEPTANCE CRITERIA
How do we KNOW it's done?

## 6. RISK REGISTER
What could go wrong?
```

**You say:**
> "Yesterday we built an API. But we never asked: How many users? What's the uptime requirement? What if someone tries SQL injection? AI will happily build you something that works on your laptop and collapses in production."

**Give a concrete example:**

> "Let's say your rector asks: 'Can this handle 10,000 students registering at the same time?' Our SQLite API? It would probably lock up. That's not the AI's fault — the AI built what we asked for. We didn't specify the load requirement."

**Show the cautionary tales** (see CAUTIONARY_TALES.md).

---

### Segment 5: Roadmap Discussion (2:15-2:45)

**You say:**
> "So what comes next? You're not going to rebuild your PHP monolith in one weekend. But you CAN do this in phases."

**Show the phased roadmap:**

```
Phase 1: Read-Only APIs (3 months)
- Student lookup
- Grade reports
- Registration statistics
- NO writes, NO auth complexity

Phase 2: Write APIs with Approval Gates (6 months)
- Update student info (with admin approval)
- Process registrations (with validation rules)
- Audit trails for every change

Phase 3: Microservices by Domain (12 months)
- Student portal service
- Finance service
- Lecturer service
- Each has its own database, its own API

Phase 4: Agentic Layer (ongoing)
- Management asks questions via WhatsApp
- Automated report generation
- Predictive analytics (which students are at risk?)
```

**You say:**
> "Phase 1 alone gives your rector the 'How many registrations today?' answer. That's immediate value. You don't need to rebuild everything."

---

### Segment 6: Close (2:45-3:00)

**You say:**
> "Two days ago, you thought AI would replace programmers. Now you see: AI is a tool. A powerful one, but it needs direction. The programmer who knows how to ask the right questions, set the right constraints, and verify the results — that programmer is more valuable than ever."

**Resources:**
- GitHub repo with all code
- PRD template
- Your contact for follow-up

**Q&A**

---

## EMERGENCY BACKUP PLANS

### If mock_database.py fails
```bash
# Just create a minimal database manually
python -c "
import sqlite3
conn = sqlite3.connect('academic.db')
c = conn.cursor()
c.execute('CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)')
c.execute(\"INSERT INTO students VALUES (1, 'Budi Santoso')\")
conn.commit()
"
```

### If API won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python api/main.py  # edit to use port 8002
```

### If Hermes can't reach localhost
```bash
# Test connectivity
curl http://localhost:8000/health

# If curl works but Hermes doesn't, the issue is Hermes's network access
# Try using 127.0.0.1 instead of localhost
```

### If everything fails
- Have screenshots of successful outputs ready
- Walk through code instead of live demo
- Emphasize: "This is why we test before presenting to the rector"

---

## KEY MESSAGES TO REPEAT

1. **"Read-only first."** Never give an agent write access until you've tested read-only extensively.

2. **"The AI built what you asked for, not what you needed."** PRDs exist to close that gap.

3. **"Standards matter."** MCP means you don't rewrite integration code for every new tool.

4. **"This is a teaching artifact."** Every `# CAUTION:` in the code is a real production requirement.

5. **"Phase-wise, not big bang."** You don't need to rebuild the monolith. One API endpoint is a win.

---

## PARTICIPANT TAKEAWAYS

By the end of this workshop, participants should be able to:

**Technical:**
- Explain what an agent is vs. a chatbot
- Build a simple read-only API
- Understand why authentication and rate limiting matter
- Describe what MCP is and why it matters

**Non-Technical:**
- Ask natural language questions of a database via an agent
- Understand why PRDs need non-functional requirements (load, security)
- Describe a phased roadmap for modernizing a legacy system
- Know what questions to ask technical teams

**Everyone:**
- Recognize that AI-assisted coding is not the same as engineering
- Understand the difference between "works on my machine" and "production ready"
