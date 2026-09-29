# How I Used 3 Custom Commands to Speed Up My Terminal Workflow by 50%

Let me state the conclusion first: I didn't buy a faster computer, and I didn't install any fancy terminal theme. I just took the few commands I typed over and over every day, broke them down, observed them, and packaged them into 3 custom commands. Subjectively, my daily operations feel about 50% faster.

## The Reason: the Most Annoying 10 Minutes of the Day

My daily workflow is pretty ordinary: editing code, running tests, committing, pushing, reading logs, checking git history. Each thing sounds fast, but if you actually count, there are quite a lot of repetitive things I do in the terminal every day. Just the single thing of "see which branch I'm on, what files I've changed, and whether the remote has new commits" — I do it a dozen-plus times a day.

Each time takes about 30 seconds. That adds up to five or six minutes a day, and over half an hour a week, and none of that time produces any value. Worse, every extra command I type is one more chance to typo, one more wait, one more interruption of my train of thought.

So I decided to run an experiment: compress high-frequency operations into a single command. The rule is simple — any operation I manually execute more than 5 times in a week must be worth an alias or a function.

## Command 1: `st` — view the full git status with one command

The first command solves the "where exactly am I right now" problem.

```bash
st() {
  echo "== branch =="
  git branch --show-current
  echo "== status =="
  git status -s
  echo "== log =="
  git log --oneline -5
  echo "== remote =="
  git fetch -q && git log --oneline HEAD..@{u} -- 2>/dev/null || echo "up to date"
}
```

I wrote this function into `.zshrc` and call it with `st`. It prints the branch name, the working tree status, the latest 5 commits, and whether the remote has new commits, all at once.

Previously I had to type the three command groups `git status`, `git log`, and `git fetch` every day; now a single `st` is enough. I use this command dozens of times a day — it is the highest-return custom command I've ever used.

## Command 2: `wip` — experiment boldly, save state anytime

The second command solves the "too scared to commit when I'm half-finished" problem.

```bash
wip() {
  git add -A
  git commit -m "wip: $(date +%m-%d_%H:%M)"
  git push -q
}
```

`wip` means Work In Progress: it archives all current changes into a timestamped commit and pushes it up. The name isn't pretty, but that doesn't matter — it was never meant for human eyes.

With it, I can archive half an idea, a bad idea, or a piece of experimental code at any time, then confidently continue. I used to be afraid of committing half-finished work — afraid of dirtying the history, afraid of others seeing it. Now I'm not afraid at all: archiving is free; the real cost is losing a train of thought.

Risk note: this command does `add -A`, so be careful in a repository and don't drag in things that shouldn't be committed. I handle sensitive files in `.gitignore` first, and use `wip` only on repositories already under control.

## Command 3: `f` — replace memory with fuzzy search

The third command solves the "where is the file, where is the content" problem.

```bash
f() {
  local file
  file=$(fd --type f -0 . | fzf --read0 --preview 'bat --color=always --line-range=:60 {}')
  [[ -n "$file" ]] && $EDITOR "$file"
}
```

It chains fd (fast file finder), fzf (fuzzy selector), and bat (syntax-highlighted preview): type a few letters, preview the file content in real time, press Enter and it opens in the editor. For finding configs, code, or logs, I no longer rely on memory and luck with `grep -r`.

The payoff of this step is hard to measure in seconds — it eliminates not "a few seconds," but "the few failed attempts before finding the file." For me, that is precisely the part that is easiest to get distracted and to break your flow.

## What I Got Beyond the Three Commands

The side effect of doing this was: I started examining what I actually do in the terminal every day. Those repetitive actions often aren't an "efficiency problem" but a "not taking it seriously" problem — too lazy to wrap, too lazy to name, too lazy to remember.

Also, these three commands are all plain, with no black magic; anyone with six months of terminal experience can write them. Their value isn't in technical sophistication, but in observing your own usage habits and turning high-frequency actions into muscle memory.

If you want to try it too, I suggest starting with the single command you use most, not doing the whole set at once. Stick with it for a week, then decide whether it is worth continuing.