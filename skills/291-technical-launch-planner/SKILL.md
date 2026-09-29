---
name: technical-launch-planner
description: Plan and execute technical product launches for developer tools, APIs, and technical products. Use when the user asks to plan a technical product or API launch, create a launch strategy, coordinate a product release, assess launch tier, prepare for GA or beta launch, draft release notes, or announce a new API version.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Technical Launch Planner


## Overview

Plan and execute successful launches for technical products, developer tools, APIs, SDKs, and platforms. This skill provides frameworks, checklists, and templates specifically designed for technical audiences and developer-focused products.

**Built for:**
- Developer tools and platforms
- APIs and SDKs
- Technical infrastructure products
- B2D (Business-to-Developer) products
- SaaS with technical buyers

## Scope and Limitations

**This skill covers:** launch planning and execution for technical products — tier assessment, launch plans, developer enablement, technical messaging, channels, and readiness checks.

**Out of scope:**
- Consumer (B2C) launches of non-technical products — the tier framework, channels, and messaging here assume developer audiences.
- Budget decisions and PR execution — this skill provides frameworks, checklists, and templates, not approvals or hands-on execution of paid media or press relations.
- Product strategy or pricing — assume the product and pricing decisions are made before the launch is planned.

**Environment:** the three scripts require bash. They are interactive by default; when running as an agent, feed answers through stdin (see Quick Start).

**Timeline note:** the five-phase workflow below uses a Tier 1 calendar (T-12 to T+4 weeks). For Tier 2 (6-8 weeks) and Tier 3 (2-4 weeks) launches, compress the phases proportionally rather than forcing a Tier 1 schedule.

---


## Quick Start

### 1. Assess Your Launch Tier

Run the interactive assessment:

```bash
scripts/assess_launch_tier.sh
```

This determines if your launch is:
- **Tier 1** (Major/GA) - New product, major version, significant expansion
- **Tier 2** (Standard) - New features, integrations, regional expansion
- **Tier 3** (Minor) - Updates, improvements, small features

### 2. Generate Launch Plan

Create your comprehensive launch plan:

```bash
scripts/generate_launch_plan.sh
```

Provides structured plan with:
- Timeline and milestones
- Stakeholder responsibilities
- Developer enablement checklist
- Go-to-market activities
- Launch day playbook

### 3. Validate Readiness

Before launch, check readiness:

```bash
scripts/validate_readiness.sh
```

Validates seven groups: documentation completeness, code assets, technical infrastructure, marketing assets, sales enablement, team readiness, and final checks (stakeholder approval, rollback plan, launch day playbook).

**Note on running the scripts:** all three scripts read answers interactively from stdin. When executing as an agent, pipe the answers in, e.g. `printf '1\n1\n1\n1\n1\n1\n1\nn\n' | bash scripts/assess_launch_tier.sh`, The scripts require a bash environment (Git Bash, WSL, or macOS/Linux).

---


## Output Format

The deliverable for a launch planning request is a markdown launch plan document. When generating it (directly or via `scripts/generate_launch_plan.sh`), include these sections:

1. **Executive Summary** — what is launching, which tier, and the goal of the launch.
2. **Timeline** — phases from planning to post-launch, adapted to the launch tier (see Launch Planning Workflow).
3. **Deliverables** — the documentation, code assets, and marketing assets the launch requires.
4. **Stakeholders** — who owns each workstream (product, engineering, DevRel, sales, marketing).
5. **Success Metrics** — the adoption and usage metrics that define launch success.
6. **Risks** — the main risks and their mitigations.
7. **Post-Launch Plan** — the week 1/2/4 checkpoints and the retrospective.

For an assessment request (tier or readiness), the deliverable is the assessment result with the score or check results and the reasoning behind the conclusion.

---


## Core Launch Framework

### Launch Tiers

Different launches require different levels of investment:

- **Tier 1** is a **Major** launch type, covering GA launches, new products, and major versions, and warrants full GTM, events, and PR investment.
- **Tier 2** is a **Standard** launch type, covering new features, integrations, and SDKs, and warrants selective GTM, blog, and docs investment.
- **Tier 3** is a **Minor** launch type, covering updates, improvements, and patches, and warrants changelog and in-app investment.

See `references/launch_tiers.md` for complete framework.

---


## Developer-Focused Launch Components

### 1. Developer Enablement

**Critical for technical launches:**

**Documentation:**
- Getting started guide
- API reference
- Code samples
- Integration guides
- Migration guides (if applicable)

**Code Assets:**
- SDKs/client libraries
- Sample applications
- Starter templates
- Code snippets

**Developer Experience:**
- Sandbox/playground environment
- Interactive tutorials
- API explorer
- Debugging tools

See `references/developer_enablement.md` for complete checklist.

---

### 2. Technical Messaging

**Speak developer language:**

**Avoid:**
- Marketing jargon
- Vague benefits
- Non-technical superlatives

**Include:**
- Concrete technical details
- Performance metrics
- Code examples
- Architecture diagrams
- Integration patterns

See `references/launch_messaging.md` for templates.

---

### 3. Launch Channels for Developers

**Where developers discover new tools:**

**Primary:**
- Developer documentation
- GitHub/GitLab
- Developer blog
- API changelog
- Release notes

**Secondary:**
- Dev.to, Hacker News, Reddit
- Technical Twitter/X
- Discord/Slack communities
- YouTube (tutorials)
- Developer newsletters

**Tertiary:**
- Webinars/workshops
- Conferences
- Podcasts
- Case studies

---


## Launch Planning Workflow

The five phases below follow the Tier 1 calendar (T-12 to T+4 weeks). Adapt the timeline to the tier: Tier 2 launches compress the phases to roughly T-6/T-4/T-2/Launch week, and Tier 3 launches to a single T-2/Launch week sprint (matching the milestones in `scripts/generate_launch_plan.sh`). The phase order and activities stay the same — only the durations shrink.

### Phase 1: Planning (T-12 to T-8 weeks)

**Objectives:**
- Define launch tier
- Set success criteria
- Align stakeholders
- Create timeline

**Activities:**
1. **Launch Tier Assessment**
   ```bash
   scripts/assess_launch_tier.sh
   ```

2. **Stakeholder Kickoff**
   - Product/Engineering
   - Developer Relations
   - Sales Engineering
   - Marketing/Comms
   - Partners (if applicable)

3. **Define Success Metrics**
   - Developer adoption metrics
   - API usage/calls
   - SDK downloads
   - Documentation traffic
   - Community engagement

4. **Create Launch Timeline**
   ```bash
   scripts/generate_launch_plan.sh
   ```

---

### Phase 2: Build (T-8 to T-4 weeks)

**Objectives:**
- Create all launch assets
- Prepare documentation
- Build demos and samples

**Activities:**

**Documentation:**
- [ ] Getting started guide written
- [ ] API reference complete
- [ ] Integration guides ready
- [ ] Migration guide (if needed)
- [ ] Troubleshooting FAQ

**Code Assets:**
- [ ] SDKs built and tested
- [ ] Sample apps created
- [ ] Code snippets prepared
- [ ] Sandbox environment ready

**Marketing Assets:**
- [ ] Technical blog post written
- [ ] Demo video recorded
- [ ] Announcement email drafted
- [ ] Social media plan
- [ ] Press release (Tier 1)

**Sales Enablement:**
- [ ] Technical battlecard
- [ ] Demo script
- [ ] FAQ/objection handling
- [ ] Pricing materials
- [ ] Competitive positioning

---

### Phase 3: Prepare (T-4 to T-1 weeks)

**Objectives:**
- Review and refine all assets
- Train teams
- Pre-launch validation

**Activities:**

**Internal Enablement:**
- [ ] Sales team training
- [ ] Support team training
- [ ] Partner briefings
- [ ] Internal demo day

**External Prep:**
- [ ] Beta customers briefed
- [ ] Partners coordinated
- [ ] Developer advocates prepared
- [ ] Community moderators ready

**Technical Validation:**
```bash
scripts/validate_readiness.sh
```

**Pre-Launch Checklist:**
- [ ] All docs published to staging
- [ ] SDKs tagged and ready
- [ ] Demo environment tested
- [ ] Monitoring/analytics configured
- [ ] Support escalation path defined

---

### Phase 4: Launch (Launch Day)

**Launch Day Playbook:**

**Morning (9 AM):**
- [ ] Publish documentation
- [ ] Release SDKs/packages
- [ ] Deploy blog post
- [ ] Send announcement email
- [ ] Post to social media
- [ ] Update website/product pages

**Midday (12 PM):**
- [ ] Monitor metrics dashboard
- [ ] Respond to community questions
- [ ] Share to external communities
- [ ] Engage with social mentions

**Afternoon (3 PM):**
- [ ] Post to Hacker News/Reddit (if Tier 1)
- [ ] Developer advocate content
- [ ] Partner announcements

**End of Day:**
- [ ] Day 1 metrics report
- [ ] Team debrief
- [ ] Issue triage

---

### Phase 5: Post-Launch (T+1 week to T+4 weeks)

**Objectives:**
- Monitor adoption
- Gather feedback
- Iterate on messaging
- Report results

**Activities:**

**Week 1:**
- [ ] Daily metrics monitoring
- [ ] Community Q&A
- [ ] Bug fixes prioritized
- [ ] Feedback synthesis

**Week 2:**
- [ ] First adoption metrics
- [ ] Customer feedback interviews
- [ ] Documentation updates
- [ ] Follow-up content

**Week 4:**
- [ ] Launch retrospective
- [ ] Success metrics report
- [ ] Lessons learned doc
- [ ] Update launch playbook

---


## Launch Tier Details

### Tier 1: Major Launch

**When:**
- New product GA
- Major version release (v2.0, v3.0)
- Significant platform expansion
- Transformative new capability

**Timeline:** 12-16 weeks

**Investment:**
- Full cross-functional GTM
- PR/media outreach
- Developer events
- Partner coordination
- Paid promotion

**Deliverables:**
- Complete documentation
- Multiple SDKs
- Sample applications
- Video tutorials
- Interactive demos
- Press release
- Analyst briefings
- Launch event/webinar
- Partner co-marketing

---

### Tier 2: Standard Launch

**When:**
- New features
- New integrations
- Additional SDKs
- Regional expansion

**Timeline:** 6-8 weeks

**Investment:**
- Selective GTM activities
- Blog and social
- Email to developer list
- Documentation updates

**Deliverables:**
- Feature documentation
- Code samples
- Blog post
- Demo video
- Email announcement
- Social media
- Changelog entry

---

### Tier 3: Minor Launch

**When:**
- Incremental improvements
- Bug fixes
- Performance enhancements
- Small feature additions

**Timeline:** 2-4 weeks

**Investment:**
- Minimal marketing
- Documentation only
- Changelog

**Deliverables:**
- Release notes
- Updated docs
- Changelog entry
- In-app notification (if applicable)

---


## Developer Launch Best Practices

### 1. Documentation First

**Launch is NOT ready without:**
- ✅ Getting started guide
- ✅ API reference
- ✅ At least 3 code samples
- ✅ Integration guide

**Developer rule:** "If it's not documented, it doesn't exist"

---

### 2. Show, Don't Tell

**Developers want to see code:**

**Good:**
```python
# Initialize the SDK
import acme_sdk

client = acme_sdk.Client(api_key="your_key")
result = client.widgets.create(name="My Widget")
print(result.id)
```

**Bad:**
"Our SDK makes it easy to create widgets with just a few lines of code"

---

### 3. Interactive > Passive

**Engagement hierarchy:**
1. 🥇 Interactive tutorial/playground
2. 🥈 Live demo
3. 🥉 Demo video
4. ❌ Static screenshots

---

### 4. Honest Technical Communication

**Developers appreciate:**
- Limitations clearly stated
- Performance characteristics
- Pricing transparency
- Migration complexity
- Breaking changes

**Developers hate:**
- Overpromising
- Hidden limitations
- Surprise breaking changes
- Vendor lock-in

---

### 5. Community-First Approach

**Engage where developers are:**
- Answer questions on Stack Overflow
- Be active in GitHub discussions
- Respond on Hacker News
- Join relevant Discord/Slack
- Participate in Reddit AMAs

**Don't:**
- Spam communities
- Ignore negative feedback
- Delete critical comments
- Only show up for launches

---


## Reference Files

**Core frameworks (read these first):**
- **Launch Tiers**: see [references/launch_tiers.md](references/launch_tiers.md)
- **Developer Enablement**: see [references/developer_enablement.md](references/developer_enablement.md)
- **Launch Messaging**: see [references/launch_messaging.md](references/launch_messaging.md)
- **Metrics Frameworks**: see [references/metrics_frameworks.md](references/metrics_frameworks.md)

**Supporting files:**
- **Common Pitfalls**: see [references/common-pitfalls.md](references/common-pitfalls.md)
- **Getting Started**: see [references/getting-started.md](references/getting-started.md)
- **How It Works**: see [references/how-it-works.md](references/how-it-works.md)
- **Launch Retrospective**: see [references/launch-retrospective.md](references/launch-retrospective.md)
- **Launch Templates**: see [references/launch-templates.md](references/launch-templates.md)
- **Partner Integration Launches**: see [references/partner-integration-launches.md](references/partner-integration-launches.md)
- **Real World Examples**: see [references/real-world-examples.md](references/real-world-examples.md)
- **Resources**: see [references/resources.md](references/resources.md)
- **Summary**: see [references/summary.md](references/summary.md)
- **Technical Metrics**: see [references/technical-metrics.md](references/technical-metrics.md)
- **The Problem**: see [references/the-problem.md](references/the-problem.md)
- **The Solution**: see [references/the-solution.md](references/the-solution.md)
- **Changelog Template**: see [references/version---yyyy-mm-dd.md](references/version---yyyy-mm-dd.md)
- **What's Next**: see [references/what-s-next.md](references/what-s-next.md)

