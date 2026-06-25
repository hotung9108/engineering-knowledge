# Advanced TypeScript

> A comprehensive guide to TypeScript's advanced type system features including Type Narrowing, Utility Types, Conditional Types with `infer`, constrained Generics, and Branded Types. These techniques are the foundation of type-safe frontend architecture at scale.

---

## 1. What is it? (What)

**TypeScript** is a statically-typed superset of JavaScript that compiles to plain JavaScript. At the advanced level, TypeScript's type system becomes a powerful meta-programming language capable of encoding complex domain constraints directly into the type checker.

### Classification
- **Type**: Programming language / static type system.
- **Superset of**: JavaScript (ES2015+).
- **Runtime**: None — types are erased at compile time.

The advanced features covered here go beyond basic `interface` and `type` declarations into **Type Manipulation**, which enables developers to derive, transform, and constrain types programmatically.

---

## 2. Why does it exist? (Why)

JavaScript's dynamic typing introduces an entire category of bugs that only manifest at runtime: accessing properties on `undefined`, passing arguments in the wrong order, and mismatched API contracts between frontend and backend.

TypeScript's advanced type features exist to:

- **Eliminate entire classes of runtime bugs** at compile time.
- **Encode domain rules** (e.g., "a `UserId` is not interchangeable with a `PostId`") into the type system.
- **Automate type derivation** — instead of manually keeping types in sync, derive one from another.
- **Enable library authors** to provide precise, self-documenting APIs that guide consumers through IntelliSense.

---

## 3. Without vs. With Comparison (Compare)

### Without advanced TypeScript

```typescript
// Loose types — easy to pass the wrong ID
function fetchUser(id: string) { /* ... */ }
function fetchPost(id: string) { /* ... */ }

const userId = "user-123";
const postId = "post-456";

fetchUser(postId); // No compile error — but semantically wrong
```

### With Branded Types

```typescript
type UserId = string & { readonly __brand: unique symbol };
type PostId = string & { readonly __brand: unique symbol };

function createUserId(id: string): UserId { return id as UserId; }
function createPostId(id: string): PostId { return id as PostId; }

function fetchUser(id: UserId) { /* ... */ }

const userId = createUserId("user-123");
const postId = createPostId("post-456");

fetchUser(userId); // Compiles
// fetchUser(postId); // Compile ERROR — PostId is not assignable to UserId
```

| Aspect | Plain `string` IDs | Branded Types |
|---|---|---|
| Type safety | IDs are interchangeable | Distinct at compile time |
| Runtime overhead | None | None (brands are erased) |
| Bug prevention | Runtime-only | Compile-time |
| Developer experience | No IntelliSense hints | Clear domain semantics |

---

## 4. Common Use Cases

1. **API response typing** — Deriving frontend types from backend schemas using Utility Types and `infer`.
2. **State machine modeling** — Using Discriminated Unions to model finite states (idle, loading, success, error).
3. **Design system props** — Polymorphic component types that constrain `as` prop based on the rendered element.
4. **Form validation** — Mapping form field types to their validation schemas using Mapped Types.
5. **Domain-Driven Design** — Branded Types to prevent mixing semantically different values of the same primitive type.

### When not to over-engineer types

- Throwaway scripts and prototypes.
- Internal admin tools where type complexity exceeds its benefit.
- Over-abstracted generic utilities that become unreadable.

---

## 5. Deep Practice

### Type Narrowing and Discriminated Unions

```typescript
// Discriminated Union — the 'status' field serves as the discriminant
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function renderState(state: FetchState<User>): string {
  switch (state.status) {
    case "idle":    return "Waiting to fetch...";
    case "loading": return "Loading...";
    case "success": return `Hello, ${state.data.name}`; // TS knows 'data' exists
    case "error":   return `Error: ${state.error.message}`; // TS knows 'error' exists
  }
}
```

### Utility Types Under the Hood

```typescript
interface User {
  id: string;
  name: string;
  age: number;
  email?: string;
}

// Built-in utilities
type PartialUser = Partial<User>;       // All fields optional
type RequiredUser = Required<User>;     // All fields required
type ReadonlyUser = Readonly<User>;     // All fields readonly
type UserSummary = Pick<User, "id" | "name">;
type UserWithoutEmail = Omit<User, "email">;

// Implementing Omit manually — demonstrates Mapped + Conditional types
type MyOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Custom Mapped Type — convert all fields to string
type Stringify<T> = { [K in keyof T]: string };
```

### Conditional Types and `infer`

```typescript
// Extract the resolved type from a Promise
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type A = UnwrapPromise<Promise<string>>; // string
type B = UnwrapPromise<number>;          // number

// Extract array element type
type Flatten<T> = T extends Array<infer Item> ? Item : T;
type C = Flatten<string[]>; // string

// Implementing ReturnType manually
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

### Constrained Generics

```typescript
// Type-safe property accessor
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // type: string
// getProperty(user, "invalid");        // Compile error
```

### Best Practices

1. **Prefer Discriminated Unions over type casting** — They provide exhaustive checking with `switch` statements.
2. **Use `satisfies` operator** — Validates that a value conforms to a type without widening it: `const config = { ... } satisfies Config`.
3. **Derive types from source of truth** — Use `typeof`, `ReturnType`, `Parameters`, and `Awaited` instead of manually duplicating types.
4. **Avoid `any`; prefer `unknown`** — `unknown` forces explicit narrowing before use.
5. **Use template literal types** for string-based domain modeling: `type Route = \`/api/${string}\``.

### Common Pitfalls

1. **Overuse of `as` type assertions** — Bypasses the type checker entirely; prefer type guards.
2. **Forgetting `readonly`** — Mutable arrays and objects in function signatures allow unintended mutations.
3. **Excessively complex generic types** — If a type is unreadable, it provides negative value; consider simplifying.
4. **Ignoring `strict` mode** — Running without strict mode defeats the purpose of TypeScript.
5. **Type gymnastics in application code** — Advanced types belong in libraries and shared utilities, not in business logic.

### Production Checklist

- [ ] `strict: true` enabled in `tsconfig.json`.
- [ ] No `any` types in production code (enforce via `@typescript-eslint/no-explicit-any`).
- [ ] Discriminated Unions used for all state representations with more than two states.
- [ ] Branded Types used for domain IDs (`UserId`, `OrderId`, etc.).
- [ ] `satisfies` operator used for configuration objects to preserve literal types.

---

## 6. Code Templates and Integration

### Generic API Response Type

```typescript
// Standardized API response wrapper
type ApiResponse<T> =
  | { success: true; data: T; timestamp: number }
  | { success: false; error: { code: string; message: string }; timestamp: number };

// Type-safe fetch wrapper
async function apiFetch<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  const body = await response.json();

  if (!response.ok) {
    return {
      success: false,
      error: { code: String(response.status), message: body.message ?? "Unknown error" },
      timestamp: Date.now(),
    };
  }

  return { success: true, data: body as T, timestamp: Date.now() };
}
```

---

## 7. Cheatsheet

| Feature | Syntax | Purpose |
|---|---|---|
| Discriminated Union | `{ type: "a"; data: X } \| { type: "b"; error: Y }` | Exhaustive state modeling |
| `keyof` | `keyof T` | Union of all keys of `T` |
| Mapped Type | `{ [K in keyof T]: V }` | Transform all properties |
| Conditional Type | `T extends U ? X : Y` | Type-level branching |
| `infer` | `T extends Promise<infer U> ? U : T` | Extract inner types |
| `satisfies` | `const x = { ... } satisfies Type` | Validate without widening |
| Template Literal | `` type Route = `/api/${string}` `` | String pattern types |
| Branded Type | `type Id = string & { __brand: symbol }` | Nominal typing simulation |
| `Readonly<T>` | `Readonly<{ a: 1 }>` | Make all fields readonly |
| `Record<K, V>` | `Record<string, number>` | Dictionary type |
| `Exclude<T, U>` | `Exclude<"a" \| "b", "a">` → `"b"` | Remove members from union |
| `Extract<T, U>` | `Extract<"a" \| "b", "a">` → `"a"` | Keep matching members |
| `NonNullable<T>` | `NonNullable<string \| null>` → `string` | Remove null/undefined |
| `ReturnType<T>` | `ReturnType<typeof fn>` | Get function return type |
| `Awaited<T>` | `Awaited<Promise<string>>` → `string` | Unwrap Promise type |

---

## Related Topics

- [JS Engine Internals](./js-engine-internals.md) — How TypeScript's type erasure interacts with V8 optimization.
- [Advanced Component Patterns](../02-reactjs/advanced-component-patterns.md) — Polymorphic component types in React.
- [State Management Patterns](../02-reactjs/state-management-patterns.md) — Type-safe state management with Zustand and Jotai.
