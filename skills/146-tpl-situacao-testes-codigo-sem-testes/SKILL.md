---
name: tpl-situacao-testes-codigo-sem-testes
description: Adds tests to codebases with zero or very few existing tests — writing characterization tests first, identifying seams, and prioritizing coverage by risk tier. Use when the user needs to add tests to an untested or barely-tested codebase, or mentions characterization tests, test seams, or risk-based test coverage.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: Writing Tests for Untested Code

## Workflow

1. **Identify seams.** Find every place behavior can be substituted without editing code; add minimal seams where none exist.
2. **Write characterization tests first.** Capture current behavior on the riskiest paths before asserting anything "should" happen.
3. **Prioritize by risk tier.** Cover payments, auth, and data mutation before low-risk code.
4. **Test the boundary, one failure at a time.** Add a test, make it pass, commit — keep the feedback loop short.
5. **Mock at the outermost boundary.** Fake the DB, HTTP, and filesystem; never mock your own logic.
6. **Track coverage by risk tier.** Critical paths target 100% line + branch coverage, with the acceptance floor in QUALITY GATES.
7. **Deliver and verify.** Produce the coverage report, test inventory, seams list, and skipped paths; check every QUALITY GATE.

1. **Characterization tests first.** Before writing tests that assert what "should" happen, write tests that assert what DOES happen. Run the code, observe output, write a test that captures it. This is the safety net — even if behavior is wrong, you want to know if it changes.

2. **Start at the highest risk, not the lowest complexity.** High risk = code that handles money, auth, data mutation, external integrations. A complex but low-risk rendering function can wait. Test what breaks the most when wrong.

3. **Test the boundary, not the implementation.** Test inputs and outputs. Don't test internal state or private methods. If you have to, the architecture needs to change later.

4. **Identify seams.** A seam is a place where you can substitute behavior without editing code (constructor injection, module mock, env variable). Find all seams before writing tests. If a class has no seams, you'll need to add a minimal one.

5. **One failing test at a time.** When adding tests, add one, make it pass, commit. Don't write 50 tests then try to make them all pass — the feedback loop is too long.

6. **Mock at the outermost boundary.** Mock database connections, HTTP calls, filesystems. Do not mock your own business logic — those are integration tests in disguise.

7. **Coverage targets by risk tier:**
   - Critical (payments, auth, data deletion): target 100% line + branch coverage (acceptance floor: ≥ 90%)
   - Core business logic: 80%+ coverage
   - Utility functions: 60%+ coverage
   - Simple glue code / configuration: skip or minimal

## ROUTING TABLE

- If you encounter global mutable state, wrap it in a function or class that can be reset, add a `reset()` method, and test in isolation.
- If you encounter `new SomeService()` inside a function (a hardwired dependency), pass it as a parameter with a default; this is the minimal seam you need.
- If you encounter database calls in the middle of business logic, extract the DB calls to a Repository interface and mock the repository in unit tests.
- If you encounter HTTP calls in business logic, extract them to a client class and mock it, or use `nock`/`msw` to intercept at the HTTP layer.
- If you encounter timer-dependent code (`setTimeout`, intervals), use Jest's fake timers (`jest.useFakeTimers()`) or sinon fake timers.
- If you encounter file system operations, mock the `fs` module or use a temp directory with cleanup in `afterEach`.
- If you encounter an untestable legacy function (500 lines, everything mixed), write a characterization test at the top level only, add a TODO comment, and refactor in a separate PR.
- If you encounter a function that's never called in tests (0% coverage), write a smoke test: check whether it runs without throwing, then add edge cases.
- If you encounter async code without proper async/await, convert it to async/await first, then test with async test functions.
- If you encounter a third-party library with complex behavior, test your code's behavior assuming the library works, using stubs/fakes rather than mocks of internals.

## Test Pyramid Strategy

```
E2E Tests (5%)
  → Cover the most critical user journeys only
  → Slow, flaky if overdone. Use sparingly.

Integration Tests (25%)
  → Test how components work together
  → Use real DB (in-memory or test DB), mock external APIs
  → Example: UserService creates a user and can retrieve it

Unit Tests (70%)
  → Test individual functions/classes in isolation
  → Fast, no I/O, fully mocked dependencies
  → Example: validateEmail() returns false for malformed email
```

## Test Naming Convention

Examples use JavaScript/Jest; apply the same patterns with your stack's equivalents (pytest, JUnit, Go testing, etc.).

```javascript
// Pattern: [unit] should [expected behavior] when [condition]
describe('AuthService', () => {
  describe('login()', () => {
    it('should return JWT token when credentials are valid', async () => { ... })
    it('should throw UnauthorizedError when password is wrong', async () => { ... })
    it('should throw UnauthorizedError when user does not exist', async () => { ... })
    it('should lock account after 5 failed attempts', async () => { ... })
  })
})
```

## DO NOT

- **DO NOT** mock what you own — mock external dependencies, not your own services in unit tests
- **DO NOT** test private methods directly — if you feel you need to, the class has too many responsibilities
- **DO NOT** write tests that depend on execution order — each test must be independent
- **DO NOT** use `beforeAll` for mutable state — use `beforeEach` so each test starts clean
- **DO NOT** target 100% line coverage across the board — it leads to testing trivial code while missing critical logic
- **DO NOT** write assertions that test the mock itself (`expect(mockFn).toHaveBeenCalled` only)  — test the outcome
- **DO NOT** leave `console.log` in test files — tests should be silent in CI
- **DO NOT** skip flaky tests with `xtest` or `.skip` — fix the flakiness or delete the test

## OUTPUT FORMAT

When adding tests to an existing codebase, produce:

1. **Coverage Report** — before and after, focusing on critical paths
2. **Test inventory** — list of what's tested and what's intentionally not tested
3. **Seams identified** — places where the code was adjusted (minimally) to be testable
4. **Characterization tests list** — tests that capture current behavior (possibly wrong/to be revisited)
5. **Skipped paths** — what was NOT tested and why (complexity, risk, time)

Template for a characterization test comment:
```javascript
// CHARACTERIZATION TEST: Captures current behavior as of [the date this test is written].
// This behavior may not be correct — see issue #123.
// Do not change this test without first verifying the business requirement.
it('should return null when user not found (current behavior)', () => {
  expect(service.getUser(-1)).toBeNull()
})
```

## SCOPE

This skill adds tests to existing untested or barely-tested code. It does NOT:

- **Write tests for greenfield projects** — for new code with no legacy
  constraints, standard TDD applies; this skill targets existing behavior.
- **Refactor legacy code** — refactoring happens in a separate PR, after
  characterization tests lock in current behavior.
- **Fix bugs** — a failing test reveals a bug; fixing the production code
  is a separate task outside this skill's test-adding scope.
- **Rewrite tests wholesale** — existing passing tests stay; the skill adds
  coverage for untested paths and converts behavior-capturing tests where
  appropriate.
- **Require a specific language or framework** — examples use JS/Jest, but
  the principles apply to any stack; substitute equivalent tools.

## QUALITY GATES

- [ ] Coverage of critical paths (auth, payments, data mutations) is ≥ 90%
- [ ] Every test is independent: passes when run alone and in any order
- [ ] No unit test takes more than 200ms; integration and E2E tests get separate, higher time limits
- [ ] No production code was changed to make tests pass (only minimal seams and readability conversions, e.g. async/await, added)
- [ ] All tests are named with the `should [behavior] when [condition]` pattern
- [ ] Test suite runs cleanly in CI with zero flaky failures
- [ ] Characterization tests are marked as such with a comment
- [ ] Coverage report visible in CI output
- [ ] A new developer can understand what a function does by reading its tests

