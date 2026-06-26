# Advanced TypeScript

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Hướng dẫn toàn diện về các tính năng kiểu hệ thống (type system) nâng cao của TypeScript, bao gồm Type Narrowing, Utility Types, Conditional Types với `infer`, Generics, và Branded Types. Đây là nền tảng để xây dựng kiến trúc frontend an toàn kiểu dữ liệu (type-safe) ở quy mô lớn.

</details>

> **Summary**: A comprehensive guide to TypeScript's advanced type system features including Type Narrowing, Utility Types, Conditional Types with `infer`, constrained Generics, and Branded Types. These techniques are the foundation of type-safe frontend architecture at scale.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang phân loại đồ chơi vào các hộp:
- **JS cơ bản**: Bạn vứt tất cả đồ chơi (xe hơi, búp bê, khối xếp hình) vào một thùng lớn. Bất kỳ ai cũng có thể lấy ra bất kỳ thứ gì, rất dễ lấy nhầm.
- **TS cơ bản**: Bạn dán nhãn "Hộp Xe Hơi", "Hộp Búp Bê". Mọi người phải lấy đúng đồ chơi.
- **TS nâng cao**: Bạn không chỉ dán nhãn, mà còn chế tạo ra một cái máy tự động: "Nếu đồ chơi có bánh xe (Conditional Type), tự động bỏ vào hộp Xe Hơi; Nếu không, bỏ vào hộp Khác". Bạn tạo ra các luật lệ thông minh tự động thay đổi dựa trên đồ vật bạn có.

</details>

Imagine you are organizing toys into boxes:
- **Basic JavaScript**: You throw all toys (cars, dolls, blocks) into a massive bin. Anyone can pull out anything; it's easy to grab the wrong toy.
- **Basic TypeScript**: You label boxes "Car Box" and "Doll Box." People must put the correct toys in the correct boxes.
- **Advanced TypeScript**: You don't just label boxes; you build an automated sorting machine. "If a toy has wheels (Conditional Type), automatically put it in the Car Box. Otherwise, put it in the Other Box." You create smart rules that automatically adapt based on what you put into them.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**TypeScript** là một tập hợp siêu dữ liệu (superset) tĩnh của JavaScript. Ở cấp độ nâng cao, hệ thống kiểu của TypeScript trở thành một ngôn ngữ lập trình siêu cấp (meta-programming language), có khả năng mã hóa các ràng buộc phức tạp của miền dữ liệu (domain constraints) trực tiếp vào trình kiểm tra kiểu (type checker).

**Phân loại:**
- **Loại**: Ngôn ngữ lập trình / Hệ thống kiểu tĩnh.
- **Bản chất**: Tập hợp mở rộng của JavaScript.
- **Thời điểm chạy**: Không có — các kiểu bị xóa sạch khi biên dịch (compile time).

</details>

**TypeScript** is a statically-typed superset of JavaScript that compiles to plain JavaScript. At the advanced level, TypeScript's type system becomes a powerful meta-programming language capable of encoding complex domain constraints directly into the type checker.

### Classification
- **Type**: Programming language / static type system.
- **Superset of**: JavaScript (ES2015+).
- **Runtime**: None — types are erased at compile time.

The advanced features covered here go beyond basic `interface` and `type` declarations into **Type Manipulation**, which enables developers to derive, transform, and constrain types programmatically.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tính linh hoạt của JavaScript sinh ra một loạt các lỗi chỉ xuất hiện khi chạy thực tế (runtime). Các tính năng kiểu nâng cao của TypeScript ra đời nhằm:
- **Tiêu diệt hoàn toàn nhiều loại lỗi runtime** ngay từ lúc viết code.
- **Mã hóa các luật nghiệp vụ** vào hệ thống (ví dụ: `UserId` không bao giờ được dùng lẫn lộn với `PostId`).
- **Tự động hóa việc suy diễn kiểu dữ liệu** — thay vì phải sửa thủ công nhiều nơi, kiểu này có thể tự sinh ra từ kiểu khác.
- **Giúp người viết thư viện** tạo ra các API tự viết tài liệu thông qua IntelliSense (gợi ý code).

</details>

JavaScript's dynamic typing introduces an entire category of bugs that only manifest at runtime: accessing properties on `undefined`, passing arguments in the wrong order, and mismatched API contracts between frontend and backend.

TypeScript's advanced type features exist to:

- **Eliminate entire classes of runtime bugs** at compile time.
- **Encode domain rules** (e.g., "a `UserId` is not interchangeable with a `PostId`") into the type system.
- **Automate type derivation** — instead of manually keeping types in sync, derive one from another.
- **Enable library authors** to provide precise, self-documenting APIs that guide consumers through IntelliSense.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi dùng chuỗi `string` thông thường cho mọi ID, TypeScript không thể phân biệt được `UserId` và `PostId`. Nhưng khi áp dụng **Branded Types**, bạn tạo ra các nhãn ảo (ảo vì chúng bị xóa khi chạy) để ép trình biên dịch phải báo lỗi nếu bạn vô tình truyền sai loại ID.

</details>

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

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khớp kiểu dữ liệu API**: Suy diễn kiểu dữ liệu Frontend tự động từ các Schema Backend.
2. **Mô hình máy trạng thái (State machine)**: Sử dụng Discriminated Unions để mô phỏng trạng thái (idle, loading, success, error).
3. **Props trong Design System**: Ràng buộc các tham số của Component linh hoạt (Polymorphic).
4. **Validation Form**: Map các kiểu form tự động với Mapped Types.
5. **Domain-Driven Design (DDD)**: Sử dụng Branded Types để tránh nhầm lẫn giữa các ID.

**Anti-patterns (Khi nào KHÔNG nên dùng)**:
- Các script tạm thời (Throwaway scripts).
- Lạm dụng việc trừu tượng hóa (Over-abstraction) làm code không thể đọc được.

</details>

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

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Thực tiễn cốt lõi:**
1. Ưu tiên **Discriminated Unions** thay vì ép kiểu thủ công (`as`).
2. Dùng toán tử `satisfies` để kiểm tra kiểu mà không làm mất đi giá trị gốc.
3. Tránh dùng `any`; hãy dùng `unknown` vì nó bắt buộc bạn phải kiểm tra kiểu trước khi sử dụng.
4. KHÔNG lạm dụng các Types phức tạp trong code ứng dụng kinh doanh, hãy để chúng nằm gọn trong các thư viện tiện ích (utilities).

</details>

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

## Layer 6: Code Templates and Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Mẫu code dưới đây trình bày cách dùng Discriminated Union cho một API Response an toàn. Khi `success: true`, bạn chắc chắn lấy được `data`. Khi `success: false`, bạn chắc chắn lấy được `error`.

</details>

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

## Layer 7: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bảng tóm tắt các tính năng nâng cao và cú pháp thường dùng nhất của TypeScript.

</details>

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
