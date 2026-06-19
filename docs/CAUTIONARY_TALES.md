# Cautionary Tales: When Agentic Workflow Goes Wrong

> **Real-world failure modes that happen when people skip the engineering.**
> Tell these stories during the workshop. They stick better than lectures.

---

## Tale 1: The "Works on My Machine" API

**The Setup:**
A developer uses AI to build a REST API for student records. It works perfectly in testing with 10 students. They demo it to the rector. The rector is impressed. They deploy it to production.

**The Failure:**
Registration day. 5,000 students try to register simultaneously. The API — a single Python process with SQLite — locks up. Database is locked. Timeouts everywhere. The developer is called at 2 AM.

**The Root Cause:**
The AI built what was asked for: "a REST API that handles student registration." The developer never specified:
- Expected concurrent users: 5,000
- Database: SQLite (single-writer, file-locked)
- No connection pooling
- No load testing

**The Lesson:**
> "AI built a bicycle. You needed a bus. But you asked for 'a vehicle.'"

**The Fix:**
- Specify load requirements in the PRD
- Use PostgreSQL with connection pooling
- Load test before production
- Implement rate limiting

---

## Tale 2: The Helpful Agent That Deleted Data

**The Setup:**
A university builds an AI assistant that can query AND update the student database. "Make it helpful," they said. The AI generates code with write access. No approval workflow. "It's faster this way."

**The Failure:**
A department head asks: "Remove all students who haven't paid tuition." The agent dutifully deletes 200 records. No backup. No audit trail. No "Are you sure?" The data is gone.

**The Root Cause:**
- Write access without human approval
- No soft deletes (data permanently removed)
- No audit logging (who did what, when)
- No role-based access control

**The Lesson:**
> "An agent with write access is like giving a stranger your bank PIN and saying 'be helpful.'"

**The Fix:**
- Read-only APIs first
- Write operations require human approval
- Soft deletes (mark as deleted, don't remove)
- Immutable audit logs
- Role-based access: who can do what

---

## Tale 3: The "Secure" API With No Auth

**The Setup:**
A team builds an API for internal use. "It's behind the firewall, so it's safe." They use AI to generate the code. The AI includes no authentication because none was requested.

**The Failure:**
A student discovers the API endpoint. They can query any student's GPA, email, and enrollment status. They build a script that downloads all 10,000 student records. They post it on a forum. The university faces a data breach investigation.

**The Root Cause:**
- No authentication (anyone can access)
- No authorization (anyone can see everything)
- No rate limiting (one user can download everything)
- No input validation (SQL injection possible)
- "Security by obscurity" (hoping no one finds the URL)

**The Lesson:**
> "If it doesn't have auth, it's public. The internet is very good at finding things."

**The Fix:**
- API keys or OAuth2 for every endpoint
- Role-based access control (rector sees all, student sees self)
- Rate limiting per user/API key
- Input validation and parameterized queries
- Regular security audits

---

## Tale 4: The Vendor Lock-In Trap

**The Setup:**
A university builds their entire AI workflow around Claude. Custom prompts, custom tools, custom integrations. It works beautifully. The team becomes dependent on Claude's specific features.

**The Failure:**
Anthropic changes pricing. Or Claude is unavailable in their region. Or they need to use a different model for compliance reasons. They try to switch to another agent. Nothing works. Their entire workflow is tied to one vendor's quirks.

**The Root Cause:**
- Custom integration for one tool
- No abstraction layer (like MCP)
- No fallback plan
- "We'll never need to switch" assumption

**The Lesson:**
> "Building on one vendor's platform is like building a house on someone else's land."

**The Fix:**
- Use standards (MCP, OpenAPI, REST)
- Test with multiple agents during development
- Abstract vendor-specific code
- Keep migration path open

---

## Tale 5: The "Vibe Coded" Production System

**The Setup:**
A developer uses AI to build a complete student portal in one weekend. "Vibe coding," they call it. The AI generates thousands of lines of code. It looks impressive. It mostly works.

**The Failure:**
Three months later:
- No one understands the code structure (not even the AI that wrote it)
- No tests exist; every change breaks something
- The original developer left; no one can maintain it
- Performance degrades as data grows
- Security holes are discovered

**The Root Cause:**
- No code review (AI wrote it, no human verified)
- No tests (AI wasn't asked to write tests)
- No documentation (AI wasn't asked to document)
- No architecture decisions recorded ("why did we choose this?")
- No monitoring ("is it working?" — no one knows)

**The Lesson:**
> "AI can write code. It cannot own code. You own it. That means you understand it, test it, and maintain it."

**The Fix:**
- Human code review for every AI-generated file
- Require tests in the prompt
- Document architecture decisions
- Set up monitoring and alerting
- Bus factor > 1 (more than one person understands it)

---

## Tale 6: The PRD That Wasn't

**The Setup:**
A team tells an AI: "Build us a registration system." No PRD. No requirements. Just a vague goal. The AI builds something. It has features no one asked for. It misses features everyone needs.

**The Failure:**
- The system can't handle the actual registration workflow (students need department approval, but the system skips that)
- It has a chatbot feature no one wanted
- It can't export to the existing finance system
- After 3 months of "development," it's scrapped

**The Root Cause:**
- No problem statement (what are we solving?)
- No functional requirements (what must it do?)
- No non-functional requirements (how fast, how secure?)
- No acceptance criteria (how do we know it's done?)
- The AI guessed at requirements instead of implementing specified ones

**The Lesson:**
> "AI is a brilliant implementer and a terrible product manager. You must be the product manager."

**The Fix:**
- Write the PRD BEFORE asking AI to code
- Include non-functional requirements (performance, security, scalability)
- Define acceptance criteria
- Review the PRD with stakeholders
- Update the PRD as you learn

---

## The Meta-Lesson

**AI doesn't make bad engineering go away. It makes bad engineering faster.**

Before AI:
- Bad requirements → slow failure (months of development before discovery)
- Bad architecture → slow failure (scales until it doesn't)
- Bad security → slow failure (breach discovered later)

With AI:
- Bad requirements → fast failure (working code in hours, wrong product)
- Bad architecture → fast failure (scales to 100 users, then collapses)
- Bad security → fast failure (breach happens immediately because it's deployed faster)

**The goal of this workshop is not to build faster. It's to build WELL, with AI as a tool, not a replacement for thinking.**

---

## Discussion Prompts for the Workshop

Ask participants:

1. "Which of these tales have you seen in your own work?"
2. "What's the most expensive mistake you've seen from rushing to code?"
3. "If you had to choose one safeguard (auth, testing, PRD, monitoring), which would you implement first?"
4. "How do you balance 'move fast' with 'don't break things' in your organization?"

---

## The Checklist: Before You Ask AI to Build Anything

- [ ] I can explain the business problem in one sentence
- [ ] I've written a PRD with functional AND non-functional requirements
- [ ] I know the expected load (users, data volume, requests/second)
- [ ] I've considered security (auth, authorization, data sensitivity)
- [ ] I've planned for failure (backups, monitoring, rollback)
- [ ] I have a human review plan for AI-generated code
- [ ] I have a testing plan (unit, integration, load, security)
- [ ] I've considered vendor lock-in and have an exit strategy
- [ ] I know who maintains this when the AI is done
- [ ] I've set a definition of "done" that includes production readiness, not just "it works"

---

> **"The AI will build you a rope bridge. It's your job to decide if that's enough to cross the canyon."**
