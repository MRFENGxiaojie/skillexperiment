# Reverse Engineering Viral Content — Full Framework

The six-step method from SKILL.md, expanded with the data collection table, pattern encoding template, and playbook document structure.

---

## Step 1: Find creators (10-20 accounts)

Selection criteria — accounts must have:

- High engagement relative to follower count (engagement rate > 5% is a strong signal; > 2% still useful)
- Content in your niche or a directly adjacent niche (your audience overlaps theirs)
- Consistent output (at least 3 posts/week over the last 60 days)
- A mix of sizes: 2-3 micro accounts (< 10k), 5-8 mid accounts (10k-100k), 2-3 large accounts (100k+) — patterns differ by size

Record for each account: name, platform, niche, follower count, posting frequency, and the engagement-rate estimate.

## Step 2: Collect data (500+ posts)

| Field | What to record |
|-------|----------------|
| Account | Creator name |
| Platform | LinkedIn / Twitter/X / Instagram / TikTok / Facebook |
| Date | Post date |
| Type | Post / thread / carousel / reel / video / poll |
| Hook | The first line or first 3 seconds, verbatim |
| Length | Word count or video duration |
| CTA | What the post asked the reader to do |
| Format details | Hashtags, emoji density, line breaks, media count |
| Engagement | Likes, comments, shares/saves (at time of collection) |
| Topic | The subject in one line |
| Notes | Anything else that stands out |

Collect at least 100 posts per platform you target. A spreadsheet with these columns is the working artifact.

## Step 3: Analyze patterns

For each post, code the patterns:

- **Hook type** — which Hook Formula (curiosity / story / value / contrarian / data) does it use?
- **Structure** — the shape of the post after the hook (list? story arc? question then answer? problem-solution?)
- **Pacing** — line breaks per 100 words, sentence length mix, where the emphasis lands
- **CTA style** — direct ask / open question / implied (comment bait) / none

Then group by performance: top 10% by engagement rate vs bottom 50%. The patterns that concentrate in the top 10% and are absent from the bottom 50% are your signals. Patterns that appear in both are noise — discard them.

## Step 4: Codify the playbook

Create a playbook document per platform, using this structure:

```markdown
# [Platform] Playbook — [Date of analysis]

## Top-performing patterns (with evidence)
1. [Pattern] — appears in X of the top 20 posts (examples: [link/screenshot])

## Hook formulas that work here
- [Formula + one verbatim example]

## Structure that works here
- [e.g., hook → 3 bullets → proof → CTA]

## Length and pacing
- [Word count range, line-break rhythm, emoji density]

## CTAs that outperform
- [Direct ask vs question vs none — with evidence]

## What NOT to copy (failed patterns)
- [Patterns from the bottom 50% that look tempting]
```

The playbook is a living document — refresh it when the platform's behavior changes or every 2-3 months.

## Step 5: Add your voice

Patterns are the skeleton, not the content. For each playbook rule, translate it into your own terms:

- Write the hook in your voice, not the creator's (the pattern is the structure; the personality is yours)
- Keep your own topics and expertise — borrowed formats with original substance, never the reverse
- If a pattern requires a persona you don't have (e.g., a story you didn't live), skip it

## Step 6: Convert

Attention without business results is vanity. Connect the playbook to outcomes:

- Track one conversion metric per post type (link clicks, profile visits, DMs, signups)
- Attribute: which playbook patterns drive conversions, not just engagement?
- Double down on the patterns that convert; keep the patterns that only engage for reach campaigns

## Common failure modes

1. **Copying the creator, not the pattern** — imitating a persona you don't have reads as fake.
2. **Sample too small** — under 100 posts per platform, the "patterns" are anecdotes.
3. **Survivorship bias** — only studying top accounts misses what top accounts and small accounts do differently.
4. **Ignoring the bottom** — the bottom 50% is where the failed patterns live; that's half the lesson.
5. **Playbook rot** — a playbook from 12 months ago on a platform that changed is a costume, not a strategy.
