# PRD Template: Agentic Workflow Projects

> **Use this template for every project, no matter how small.**
> AI will build what you specify. If you don't specify it, it won't exist.

---

## 1. PROBLEM STATEMENT

**What business problem does this solve?**

*Example:*
> Our rector needs daily registration reports but must wait for IT staff to run SQL queries. This causes delays in decision-making.

**Why now?**

*Example:*
> Student registration period starts next month. We need automated reporting before then.

**Success looks like:**

*Example:*
> The rector can ask "How many registrations today?" via any device and get an answer in under 5 seconds.

---

## 2. FUNCTIONAL REQUIREMENTS

**What must the system DO?**

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-1 | Query student count | Must have | Returns total active students |
| FR-2 | Query today's registrations | Must have | Returns count for current date |
| FR-3 | Search students by name | Should have | Returns matching students within 2 seconds |
| FR-4 | Export reports to PDF | Could have | Generates PDF with university branding |

**User Stories:**

*As a [user], I want [feature], so that [benefit].*

- As the rector, I want to ask registration questions in Indonesian, so that I don't need to learn SQL.
- As the IT staff, I want read-only access, so that I don't worry about accidental data changes.

---

## 3. NON-FUNCTIONAL REQUIREMENTS (NFRs)

**The most commonly skipped section. The most important section.**

### Performance
- **Expected concurrent users:** ___ (e.g., 50 during registration period)
- **Requests per second:** ___ (e.g., 10 RPS average, 100 RPS peak)
- **Response time:** ___ (e.g., p95 < 2 seconds for queries)
- **Data volume:** ___ (e.g., 10,000 students, 100,000 grade records)

### Availability
- **Uptime requirement:** ___% (e.g., 99.9% = 8.7 hours downtime/year)
- **Maintenance windows:** ___ (e.g., Sundays 2-4 AM)
- **Disaster recovery:** ___ (e.g., daily backups, 4-hour RTO)

### Security
- **Authentication method:** ___ (e.g., OAuth2, LDAP, API keys)
- **Authorization model:** ___ (e.g., role-based: rector sees all, staff sees department)
- **Data sensitivity:** ___ (e.g., student PII = sensitive, aggregate stats = public)
- **Compliance requirements:** ___ (e.g., GDPR, local data protection laws)
- **Threat model:** ___ (e.g., SQL injection, XSS, unauthorized access)

### Scalability
- **Current load:** ___
- **Expected growth:** ___ (e.g., 20% more students next year)
- **Horizontal scaling needed?** ___ (e.g., can we add more servers?)

### Maintainability
- **Team skills:** ___ (e.g., PHP experts, limited Python experience)
- **Documentation required:** ___ (e.g., API docs, deployment guide)
- **Testing requirements:** ___ (e.g., unit tests, integration tests, load tests)

---

## 4. CONSTRAINTS & ASSUMPTIONS

**What limits our options?**

- **Technology:** Must integrate with existing MySQL database
- **Budget:** No cloud infrastructure budget; must run on-premise
- **Team:** 2 developers, part-time
- **Timeline:** 3 months for Phase 1
- **Regulatory:** Student data cannot leave university network

**What are we assuming?**

- The existing MySQL schema is stable (no major changes expected)
- The university network has reliable internal connectivity
- At least one developer can learn Python/FastAPI

---

## 5. ACCEPTANCE CRITERIA

**How do we KNOW it's done?**

| Criteria | How to Test | Pass/Fail |
|----------|-------------|-----------|
| API returns student count | `curl /stats/overview` returns JSON with total_students | |
| Response time < 2s | Run 100 requests, measure p95 | |
| Read-only protection | Attempt DELETE request, verify 405 error | |
| MCP server lists tools | `curl /tools/list` returns 6+ tools | |
| Agent can answer questions | Ask "How many students?" get correct number | |

---

## 6. RISK REGISTER

**What could go wrong?**

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Database performance degrades | Medium | High | Add read replica, caching layer |
| Unauthorized data access | Medium | Critical | Implement auth before production |
| Team lacks Python skills | High | Medium | Training budget, hire consultant |
| AI gives wrong answers | Medium | High | Human verification for critical decisions |
| Scope creep | High | Medium | Strict phase gates, weekly review |
| Vendor lock-in (one AI model) | Low | Medium | Use MCP, test with multiple agents |

---

## 7. PHASES & MILESTONES

**Never try to build everything at once.**

### Phase 1: Read-Only API (Month 1-2)
- [ ] Mock database with realistic data
- [ ] 4-5 read-only endpoints
- [ ] Basic error handling
- [ ] **Definition of Done:** Non-technical user can ask questions and get answers

### Phase 2: MCP Standardization (Month 2-3)
- [ ] Wrap API in MCP server
- [ ] Test with multiple agents (Hermes, Claude, Codex)
- [ ] Documentation
- [ ] **Definition of Done:** Same API works with any agent

### Phase 3: Production Hardening (Month 4-6)
- [ ] Authentication (OAuth2 or API keys)
- [ ] Rate limiting
- [ ] Input validation
- [ ] Logging and monitoring
- [ ] **Definition of Done:** Security audit passes

### Phase 4: Write Operations (Month 7-12)
- [ ] Admin approval workflow for changes
- [ ] Audit trails
- [ ] Data validation rules
- [ ] **Definition of Done:** Changes are tracked and reversible

### Phase 5: Microservices (Year 2+)
- [ ] Extract student service
- [ ] Extract finance service
- [ ] Extract lecturer service
- [ ] **Definition of Done:** Services deploy independently

---

## 8. AI-SPECIFIC CONSIDERATIONS

**When using AI to build this:**

### Prompt Engineering
- **Be specific:** "Build a FastAPI endpoint that returns student count" not "Build an API"
- **Include constraints:** "Read-only, no authentication, SQLite for now"
- **Request tests:** "Include unit tests for each endpoint"

### Verification Checklist
- [ ] Does it handle empty results gracefully?
- [ ] Does it handle large results (pagination)?
- [ ] Does it validate input types?
- [ ] Does it return proper HTTP status codes?
- [ ] Does it log errors?
- [ ] Can it handle 1000 concurrent requests? (Load test)

### What AI Will NOT Do For You
- **Decide business requirements** — you must specify what matters
- **Choose the right architecture** — you must understand trade-offs
- **Test in production** — you must verify with real data and load
- **Maintain the system** — you must own the code it generates
- **Take responsibility** — when it breaks at 3 AM, you fix it

---

## EXAMPLE: COMPLETED PRD FOR THIS WORKSHOP

### Problem Statement
Teach 20 mixed-skill participants how to unlock legacy data using agentic workflow, without vendor lock-in.

### Functional Requirements
- FR-1: Create realistic academic database
- FR-2: Build read-only API with 5+ endpoints
- FR-3: Build HTTP-based MCP server
- FR-4: Demonstrate multi-agent compatibility
- FR-5: Teach PRD and cautionary practices

### Non-Functional Requirements
- **Performance:** 200 students, 20 courses, <1s response time
- **Availability:** 99% (workshop only, not production)
- **Security:** None (teaching environment, explicitly marked)
- **Scalability:** Single machine, single process
- **Maintainability:** Well-commented code with CAUTION markers

### Constraints
- Must run on Windows laptops without Docker
- Must work offline (SQLite, no external APIs)
- Must be understandable by PHP developers

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Participant laptops can't run Python | Medium | High | Provide cloud alternative, pair programming |
| Live demo fails | Medium | Medium | Screenshots, code walkthrough backup |
| Non-tech participants lost | Medium | Medium | Buddy system, simplified track |
| Time runs short | High | Medium | Strict timekeeping, defer Q&A to breaks |

---

> **Remember:** A PRD is a living document. Update it as you learn. The AI will build what you write — make sure you write what you actually need.
