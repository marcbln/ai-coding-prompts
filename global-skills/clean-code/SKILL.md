---
name: clean-code
description: Guidelines, best practices, and heuristics derived from Robert C. Martin's "Clean Code" for writing readable, maintainable, and robust code.
---

# Clean Code Skill & Reference Guide

This guide provides core principles, rules, and heuristics from Robert C. Martin's (*Uncle Bob*) book **Clean Code: A Handbook of Agile Software Craftsmanship**.

---

## 1. The Boy Scout Rule
> *"Always leave the campground cleaner than you found it."*
- Check in code that is cleaner than when you checked it out.
- Continuously refactor: fix bad names, break up bloated functions, remove dead code, and eliminate duplication incrementally.

---

## 2. Meaningful Names
- **Reveal Intent**: A variable, function, or class name should answer why it exists, what it does, and how it is used.
  - *Bad:* `int d;` -> *Good:* `int elapsedTimeInDays;`
- **Avoid Disinformation**: Do not encode types in names (e.g., avoid `accountList` if it’s actually a `Map` or `Set`).
- **Make Meaningful Distinctions**: Avoid noise words (`Data`, `Info`, `The`, `Object`, `Manager`).
- **Use Pronounceable & Searchable Names**: Single-letter variables should only be used as local loop counters in very short scopes.
- **Avoid Encodings**: No Hungarian notation, no member prefixes (`m_`).
- **Class Names**: Should be nouns or noun phrases (`Customer`, `Account`, `WikiPageParser`). Avoid verbs.
- **Method Names**: Should be verbs or verb phrases (`postPayment`, `deletePage`, `save`).
  - Accessors: `getName()`, Mutators: `setName()`, Predicates: `isPosted()`.

---

## 3. Functions & Methods
- **Small!**: Functions should rarely exceed 20 lines, ideally under 10.
- **Do One Thing**: A function should do one thing, do it well, and do it only.
- **One Level of Abstraction (SLAP)**: Every statement in a function must be at the same level of abstraction.
- **Stepdown Rule**: Code should read top-to-bottom like a narrative.
- **Function Arguments**:
  - Ideal: 0 (niladic) > 1 (monadic) > 2 (dyadic) > 3 (triadic).
  - 4+ (polyadic) requires a strong justification or parameter object wrapper.
  - **Flag Arguments Are Ugly**: Passing a boolean argument means the function does more than one thing (split into two functions).
- **No Side Effects**: A function must not silently alter global/passed state unless explicitly declared in its name.
- **Command-Query Separation (CQS)**: A function should either do something (*command*) or answer something (*query*), never both.
- **DRY (Don't Repeat Yourself)**: Eliminate duplicated logic relentlessly.

---

## 4. Comments
- **Comments Do Not Make Up for Bad Code**: Explain yourself in code, not in comments.
- **Good Comments**:
  - Legal comments / copyright.
  - Informative comments (e.g., regex pattern explanation).
  - Explanation of intent (why a non-obvious decision was made).
  - Clarification / Warning of consequences.
  - `TODO` notes (keep minimal and actionable).
- **Bad Comments**:
  - Mumbling / rambling / redundant explanations.
  - Misleading / outdated comments.
  - Journal/history comments (use Git instead).
  - Commented-out code (delete it immediately; source control will remember it).

---

## 5. Formatting
- **The Newspaper Metaphor**: The top of a source file should provide high-level concepts/algorithm, with details increasing as you scroll down.
- **Vertical Density**: Keep closely related concepts vertically close.
- **Variable Declarations**: Declare variables close to their usage.
- **Instance Variables**: Declare at the top of the class.
- **Dependent Functions**: If function A calls function B, function B should be placed vertically below function A.
- **Horizontal Formatting**: Keep line lengths reasonable (80–120 characters). Maintain consistent indentation.

---

## 6. Objects and Data Structures
- **Data Abstraction**: Hide implementation behind abstract interfaces. Don't just slap getters/setters on private fields.
- **Objects vs. Data Structures**:
  - *Objects* hide their data behind abstractions and expose functions that operate on that data.
  - *Data Structures* expose their data and have no meaningful functions (e.g., DTOs).
- **The Law of Demeter**: A method $f$ of class $C$ should only call methods of:
  1. $C$ itself
  2. An object created by $f$
  3. An object passed as an argument to $f$
  4. An object held in an instance variable of $C$
  - Avoid train wrecks: `ctxt.getOptions().getScratchDir().getAbsolutePath()`

---

## 7. Error Handling
- **Prefer Exceptions to Return Error Codes** *(in exception-capable languages)*: Separates business logic from error-handling logic.
- **Language-Appropriate Error Semantics** — the "exceptions everywhere" rule is Java-centric; adapt it to the stack:
  - **Go**: No exceptions. Return explicit errors (`if err != nil`), define custom domain error types, unwrap with `errors.Is` / `errors.As`, and add context via `fmt.Errorf("...: %w", err)`. Never swallow errors; never return `(nil, nil)`.
  - **TypeScript / Python / PHP**: Use typed domain exceptions or monadic `Result<T, E>` types for *expected* domain branches (validation failures, not-found, conflicts). Reserve raw runtime exceptions for *unexpected* system failures (network, I/O, bugs). At microservice boundaries, translate downstream error payloads into typed domain errors instead of re-throwing HTTP error objects.
- **Write `try-catch-finally` Statements First**: Defines what the caller of the code can expect.
- **Use Unchecked Exceptions**: Checked exceptions violate the Open/Closed Principle when thrown deep in the stack.
- **Provide Context with Exceptions**: Include informative error messages and the failing operation.
- **Don't Return Null**: Return empty collections/objects or use `Optional` / `NullObject` pattern to avoid `NullPointerException` clutter.
- **Don't Pass Null**: Forbid passing `null` into methods unless explicitly required by an external API.

---

## 7b. Modern Language Idioms

The 2008 Java heuristics translate into these current idioms per language:

* **PHP 8.3**:
  * Constructor promotion (`public function __construct(private readonly Foo $foo)`) instead of manual property + assignment boilerplate.
  * `readonly` classes/properties and DTOs for immutable value objects.
  * `declare(strict_types=1);` at the top of every file.
  * `match` expressions over `switch`, enums over constants.
* **TypeScript**:
  * Strict null checking (`strict: true`); model state with **discriminated unions** instead of boolean flag soup.
  * Immutability via `Readonly<T>` / `readonly` modifiers; avoid `any` and loose `as` assertions.
* **Python**:
  * Full type annotations; `dataclasses(frozen=True)` for value objects.
  * Avoid mutable default arguments (`def f(x=[])` is a bug — use `field(default_factory=list)` or `None`).
  * `match`/`case` (3.10+) over if-chains where it reads better.

---

## 8. Boundaries & Third-Party Code
- **Encapsulate Boundaries**: Wrap third-party APIs / libraries in your own domain-specific adapters/interfaces.
- **Learning Tests**: Write unit tests to explore and verify third-party APIs before integrating them.
- **Adapters**: Keep a clean separation between your core business logic and external dependencies to ease future migrations.

---

## 9. Unit Tests & TDD
- **Three Laws of TDD**:
  1. You may not write production code until you have written a failing unit test.
  2. You may not write more of a unit test than is sufficient to fail.
  3. You may not write more production code than is sufficient to pass the currently failing test.
- **Test Cleanliness**: Test code is just as important as production code; it requires readability and refactoring.
- **F.I.R.S.T. Principles**:
  - **F**ast: Tests should run quickly so you run them frequently.
  - **I**ndependent: Tests should not depend on other tests or run order.
  - **R**epeatable: Tests should pass in any environment (dev, CI, offline).
  - **S**elf-Validating: Tests output a boolean pass/fail, not manual log checks.
  - **T**imely: Written just before the production code that makes them pass.
- **Single Concept per Test**: Test one logical concept per test function.

---

## 10. Classes & SOLID Principles
- **Class Organization**: Public static constants $\rightarrow$ Private static variables $\rightarrow$ Private instance variables $\rightarrow$ Public functions $\rightarrow$ Private utilities.
- **Small Classes**: Measure class size by its **responsibilities** (Single Responsibility Principle).
- **High Cohesion**: Classes should have a small number of instance variables, and methods should manipulate one or more of those variables.
- **SOLID Principles**:
  - **S** - Single Responsibility Principle (SRP): A class should have one, and only one, reason to change.
  - **O** - Open/Closed Principle (OCP): Classes should be open for extension, closed for modification.
  - **L** - Liskov Substitution Principle (LSP): Subtypes must be substitutable for their base types.
  - **I** - Interface Segregation Principle (ISP): Prefer many client-specific interfaces over one general-purpose interface.
  - **D** - Dependency Inversion Principle (DIP): Depend upon abstractions, not concretions.

---

## 11. Code Smells Checklist
- [ ] **Rigidity**: Hard to change because every change forces many other changes.
- [ ] **Fragility**: Code breaks in unexpected places when changed.
- [ ] **Immobility**: Parts cannot be reused in other projects because of tight coupling.
- [ ] **Viscosity**: Doing things right is harder than doing hacks/workarounds.
- [ ] **Needless Complexity**: Over-engineering and premature optimization.
- [ ] **Dead Code**: Uncalled methods, unused parameters, unreachable branches.
- [ ] **Feature Envy**: A method makes heavy calls on another object's data instead of its own.
- [ ] **Primitive Obsession**: Using raw primitives instead of small domain objects (e.g., `String` for phone numbers/money).
