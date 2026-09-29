---
name: tpl-situacao-sprint-planning-tecnico
description: Break down features into vertical slices, build a sprint plan with capacity, acceptance criteria, story-point estimates, dependency and risk declarations, and a 20% tech-debt budget. Use when the user is breaking down features into tasks for sprint planning, refining a backlog, estimating effort, or facilitating technical planning sessions.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: Technical Sprint Planning

## Workflow

1. **Break features into vertical slices.** Ensure every story delivers end-to-end value; split stories over 8 points or touching more than 3 layers.
2. **Write testable acceptance criteria.** Given/When/Then format, error cases, and a performance check where it matters.
3. **Estimate by complexity.** Compare each story against the reference scale — never against hours or days.
4. **Declare dependencies and risks.** Surface blockers, and route uncertain stories to spikes or back to the backlog before planning.
5. **Plan capacity.** Apply the 60-70% rule to theoretical capacity and reserve 20% for technical debt.
6. **Prioritize and finalize.** Order the stories, state the sprint goal as one business outcome, and verify the plan against QUALITY GATES.

1. **Vertical slices, not horizontal layers.** A vertical slice delivers end-to-end functionality (UI + API + DB) for a narrow user scenario. A horizontal layer (e.g., "build the entire data model") is not a user story — it's a task that rarely delivers value on its own.

2. **If a story touches more than 3 layers, split it.** Backend integration, frontend, tests, and documentation should rarely all be in one story unless the scope is very small.

3. **Technical debt gets a budget, not a sprint.** Reserve 20% of sprint capacity for technical debt. Do not postpone it indefinitely. Do not let it consume the whole sprint. Negotiate explicitly.

4. **Acceptance criteria must be testable.** "Works correctly" is not an acceptance criterion. "User can submit the form with valid data and sees a success message" is. Every AC should be falsifiable.

5. **Estimate by complexity, not by time.** Story points measure relative complexity compared to a reference story. Never say "this is 3 points because it takes 3 hours." That anchors estimates to ideal time and ignores unknowns.

6. **Dependencies are risks.** Any story that depends on another story, external team, or external service is at risk. Surface all dependencies. Either resolve them before the sprint starts or flag the story as blocked.

7. **Capacity ≠ Sprint Length × Team Size.** Account for: meetings, code reviews, incidents, holidays, onboarding. Real capacity is typically 60-70% of theoretical capacity.

## ROUTING TABLE

- A story estimated over 8 points: split it. Stories over 8 points are too uncertain to estimate accurately. Find a vertical slice.
- A story with no acceptance criteria: do not take it into the sprint. Write AC in refinement.
- "Also include X while we're at it": scope creep. Create a new ticket. Keep the current story focused.
- A story blocked by another team: flag it. Move to the backlog unless the blocker resolves before sprint starts.
- A story touching database AND UI AND external API: likely 3 stories. Split into 3 vertical slices, each delivering end-to-end value: (1) user can view records end-to-end, (2) user can create a record end-to-end, (3) user can manage records end-to-end.
- A technical debt story with no concrete impact: reframe as "Refactor X to enable Y" or "Reduce deploy time from 15min to 5min." Impact must be measurable.
- A stakeholder requesting an estimate in hours/days: convert to a range, e.g. "Given our velocity, this is likely 3-5 business days." Never commit to hours publicly.
- A story that depends on design that isn't ready: block the story. Design must be definition-of-ready before a story enters sprint planning.
- A story re-estimated 3+ times: it needs a spike (research task) to reduce uncertainty first. Cap spike at 1-2 days.
- A story with "let's figure it out as we go": red flag. Discovery tasks exist. Write a spike story. Never put an unscoped story in a sprint.

## Story Template

```markdown
## [Story Title]

**Type:** Feature / Bug / Tech Debt / Spike

**As a** [type of user]
**I want** [some goal]
**So that** [some reason / business value]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Error cases: [what happens on validation failure, network error, etc.]
- [ ] [Performance] Response time < 500ms under normal load

**Technical Notes:**
- Affected files/services: [list]
- Dependencies: [other stories, external services]
- Known risks: [what could go wrong]

**Definition of Done:**
- [ ] Code merged to main
- [ ] Tests written and passing (coverage ≥ 80% on new code)
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Acceptance criteria verified by PO or QA

**Estimate:** [story points]
```

Note: a Spike is estimated as a 1-2 day time box, not in story points, and carries no acceptance criteria — list it in the backlog or a separate research section and exclude it from sprint story point totals.

## Story Point Reference Scale

- 1 point: trivial, zero unknowns — e.g. change a label, update a config value.
- 2 points: simple, well-understood change — e.g. add a new field to an existing form + save to DB.
- 3 points: standard, some design needed — e.g. new CRUD endpoint with validation.
- 5 points: complex, significant design work — e.g. new OAuth integration.
- 8 points: very complex, multiple unknowns — e.g. real-time feature with WebSockets.
- 9-13 points: over the 8-point ceiling — must be split into vertical slices.

## Technical Debt Categories

- Security debt (e.g. unvalidated user input): priority Critical — fix immediately.
- Reliability debt (e.g. no error handling in payment flow): priority High.
- Test debt (e.g. critical path with 0% coverage): priority High.
- Performance debt (e.g. N+1 query in hot path): priority Medium.
- Maintainability debt (e.g. 500-line god function): priority Low-Medium.
- Documentation debt (e.g. undocumented architecture): priority Low.

## DO NOT

- **DO NOT** let a sprint start with undefined acceptance criteria on any story
- **DO NOT** carry over more than 20% of stories from the previous sprint — investigate why
- **DO NOT** assign stories by seniority only — knowledge silos kill team velocity
- **DO NOT** create a "Miscellaneous" or "Chores" story as a catch-all
- **DO NOT** interleave open-ended requirements clarification with estimation in the same meeting — close out requirements (AC defined) first, then estimate
- **DO NOT** add stories to an active sprint without removing equal points — protect the sprint
- **DO NOT** use sprint planning to make architectural decisions — that's a separate RFC/ADR session

## SCOPE

This skill covers sprint planning as a technical exercise: breaking features into vertical slices, writing testable acceptance criteria, estimating by complexity, declaring dependencies and risks, and planning capacity with a 20% tech-debt budget.

It does NOT cover: sprint execution, stand-ups, or retrospectives; architectural decisions (those belong in a separate RFC/ADR session); release planning or cross-team combined planning; or committing to hour-level estimates. For those, say so and route the work to the appropriate session instead.

## OUTPUT FORMAT

Sprint planning output should produce:

```markdown
## Sprint [N] Plan — [start date] to [end date]

### Capacity
- Team: 4 developers
- Working days: 10
- Theoretical: 40 points (4 devs × 10 days — a velocity reference, not a promise; points come from historical velocity, not from days)
- Estimated capacity: 26 points (60-70% of theoretical, after meetings, reviews, incidents, holidays, onboarding)
- Reserved for tech debt: 5 points

### Stories (by priority)
- Story 1: "User can reset password via email" — 3 points, owner Dev A, depends on email service configured.
- Story 2: "Add rate limiting to auth endpoints" — 5 points, owner Dev B, no dependencies.

### Risks & Blockers
- [Story X] depends on design mockups not yet ready
- [Story Y] requires access to staging payment gateway

### Tech Debt Budget
- Refactor AuthMiddleware (enables easier testing) — 3 points, impact: unblocks 3 future stories.
- Remove deprecated API v1 endpoints — 2 points, impact: reduces maintenance surface.

### Sprint Goal
[One sentence describing the main user-facing outcome of this sprint]
```

## QUALITY GATES

- [ ] Every story has at least 2 acceptance criteria in testable format
- [ ] No story estimated above 8 points (split if so)
- [ ] All dependencies between stories identified and declared
- [ ] Sprint capacity calculated with realistic overhead (not 100% of working hours)
- [ ] 20% capacity reserved for technical debt
- [ ] Sprint goal stated in one sentence (business outcome, not task list)
- [ ] All team members voiced concerns or questions before plan is finalized
- [ ] Stories marked "blocked" have blocking condition and resolution owner

