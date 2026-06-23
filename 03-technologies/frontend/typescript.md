# TypeScript

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: JavaScript là một ngôn ngữ "gõ phím nhanh nhưng dễ gãy". Trình duyệt không quan tâm bạn gán một biến bằng chữ hay bằng số, nó cứ nhắm mắt chạy, cho đến khi khách hàng thao tác và màn hình... văng lỗi đỏ chót (Runtime Error). **TypeScript (TS)** được Microsoft tạo ra để trị căn bệnh này. Nó là một siêu tập hợp (Superset) của JS. Nói nôm na, TS dán nhãn mác (Type) lên mọi biến trong code của bạn. Nếu bạn quy định `age` là một con số, mà bạn lỡ tay gán `age = "hai mươi"`, trình soạn thảo (VSCode) sẽ gạch dưới màu đỏ và cấm bạn chạy code ngay lập tức (Compile-time Error). Bắt lỗi ngay lúc đang gõ phím, thay vì để khách hàng là người lãnh đạn.

</details>

> **Summary**: JavaScript is a dynamically, weakly typed language. It defers type checking entirely to execution time (Runtime). This structural freedom enables rapid prototyping but becomes a catastrophic liability in massive, enterprise-scale codebases, where passing the wrong object shape throws a fatal `Cannot read properties of undefined` in Production. **TypeScript (TS)**, developed by Microsoft, is a strict syntactical superset of JavaScript that introduces **Static Typing**. It acts as a pre-compilation Linting engine. By explicitly declaring the structural shape of Variables, Functions, and APIs (Types/Interfaces), the TypeScript Compiler (`tsc`) mathematically verifies the codebase *before* execution (Compile-time). It physically prevents developers from deploying type-mismatched bugs, fundamentally transforming JS from a chaotic scripting tool into a rigorous software engineering language.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn điều hành một xưởng đóng hộp trái cây.
1. **JavaScript (JS)**: Một công nhân (Hàm) nhận lệnh: "Đóng nắp cái hộp này lại". Anh ta nhắm mắt làm. Nếu bạn vô tình đưa cho anh ta quả sầu riêng chưa gọt vỏ (Dữ liệu sai), anh ta vẫn cố lấy cái nắp ép xuống. Hậu quả là nát bét cả sầu riêng lẫn nắp hộp ngay giữa dây chuyền (Lỗi Runtime).
2. **TypeScript (TS)**: Bạn chế tạo ra cái khuôn đúc bằng thép (Interface). Cái khuôn này có hình Quả Táo. Công nhân phải nhét trái cây lọt qua cái khuôn đó thì mới được đóng nắp. Ngay khi bạn vừa cầm quả sầu riêng lên định bỏ vào, cái khuôn đã chặn lại và kêu BÍP BÍP (Lỗi Compile-time). Dây chuyền không bao giờ bị gián đoạn vì lỗi đã bị chặn ngay từ đầu.

</details>

Imagine plugging a cable into a socket.
1. **JavaScript**: The socket accepts any shape. You can plug a round TV cable into a square toaster socket. The system lets you do it. But when you turn on the power, the toaster explodes. (This is a Runtime Error).
2. **TypeScript**: The socket is explicitly molded as a Triangle (`Type = Triangle`). The cable is molded as a Square (`Type = Square`). The moment you *try* to push the square cable into the triangle socket, the plastic physically blocks you. You cannot even turn on the power. You are forced to fix the cable *before* running the system. (This is a Compile-time Error).

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Superset (Siêu tập hợp)**: Bất kỳ code JS nào cũng là code TS hợp lệ. TS chỉ thêm các cú pháp về Type (kiểu dữ liệu) đè lên trên JS.
**2. Biên dịch (Compilation / Transpilation)**: Trình duyệt (Chrome) KHÔNG BIẾT đọc TypeScript. Vì vậy, trước khi chạy web, bộ biên dịch `tsc` (TypeScript Compiler) sẽ:
- Bóc tách toàn bộ code để tìm lỗi (Type Checking).
- Nếu không có lỗi, nó sẽ gọt sạch toàn bộ các từ khóa TypeScript đi, và ói ra một file JavaScript thuần túy. File JS này mới là thứ được gửi xuống trình duyệt.

</details>

**1. A Syntactic Superset**: TypeScript is entirely backward compatible with JavaScript. Every valid JS program is a valid TS program. TypeScript simply layers a static type system (Interfaces, Generics, Enums) on top of standard JS syntax.
**2. Zero Runtime Overhead (Transpilation)**: Browsers (V8 Engine) and Node.js *cannot* natively execute TypeScript. TS is strictly a Developer Tool. During the build step, the TypeScript Compiler (`tsc`) executes rigorous Type Checking. If the code passes the mathematical proofs, the compiler completely strips away all Type Annotations (Erasure) and outputs vanilla, standard-compliant JavaScript. TypeScript leaves exactly zero footprint in the final production bundle.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Khi công ty bạn có 5 Dev, JS rất tuyệt. Khi công ty bạn có 500 Dev và 2 triệu dòng code, JS là ác mộng.
Một kĩ sư viết hàm `calculateDiscount(user)`. Hai năm sau, một kĩ sư khác gọi hàm đó. Vì viết bằng JS, kĩ sư số 2 không thể biết cái biến `user` cần truyền vào là một chữ cái `(String)`, một con số `(ID)` hay một đối tượng `(Object có chứa tên và tuổi)`. Kĩ sư số 2 phải mất nửa tiếng lội code cũ để đọc.
TS sinh ra để tự động hóa tài liệu (Self-documenting code). Khi bạn rê chuột vào hàm `calculateDiscount`, VSCode (được tích hợp engine TS) sẽ hiện ra cái khung báo cho bạn biết: "Hàm này bắt buộc phải truyền vào 1 Object có chứa 2 trường: `id (số)` và `isPremium (boolean)`". Lập trình viên mới vào công ty có thể code nhanh gấp 10 lần nhờ bộ gợi ý tự động (IntelliSense) siêu đẳng của TS.

</details>

TypeScript was created to solve the fundamental scaling limits of JavaScript in enterprise organizations.
In a massive monolithic JS codebase, API contracts are implicit. If a developer writes `function processOrder(order)`, the consumer of that function has absolutely no idea what properties the `order` object must possess. Does it need `order.id`? Or `order.orderId`? The only way to find out is to mentally parse the function's internal logic or rely on outdated documentation.
TypeScript makes API contracts explicit and enforceable. By defining `function processOrder(order: OrderPayload)`, the IDE acts as a built-in encyclopedia. As soon as the developer types `order.`, the IDE (powered by the TS Language Server) instantly provides autocomplete for all strictly verified properties. It drastically accelerates developer velocity, eliminates trivial `undefined` property crashes, and acts as a living, compile-time verified documentation layer.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cảnh tượng viết 1 hàm tính tổng tiền Giỏ hàng bằng JS thuần và TS.
</details>

Visualizing the structural safety gap between Vanilla JS and TypeScript.

| Metric | Vanilla JavaScript | TypeScript |
|---|---|---|
| **The Code** | `function add(a, b) { return a + b; }` | `function add(a: number, b: number): number { ... }` |
| **Accidental Bad Call**| `add(10, "5")` | `add(10, "5")` |
| **Editor Warning** | Silence. Everything looks fine. | 🛑 Red Squiggly Line: `Argument of type 'string' is not assignable to parameter of type 'number'.` |
| **Production Result**| Evaluates to `"105"`. Customer is charged $105 instead of $15. | **Code refuses to build.** Bug is destroyed before it ever reaches the server. |
| **IntelliSense** | You type `user.`. IDE guesses wildly. | You type `user.`. IDE shows exactly `id`, `name`, `email`. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Enterprise Frontend (React/Angular)**: Gần như 100% các dự án React mới hiện nay (Next.js) đều mặc định dùng TypeScript. Nó giúp kiểm soát chặt chẽ dữ liệu truyền (Props) giữa các Cục Lego (Component). Angular thậm chí ép buộc phải xài TS từ cốt lõi.
2. **Backend API (Node.js/NestJS)**: Khi làm Backend API bằng Express hoặc NestJS, TS giúp đảm bảo Dữ liệu JSON từ khách hàng gửi lên (Payload) hoàn toàn khớp với Cấu trúc Dữ liệu (Schema) của Database.
3. **Viết Thư viện (NPM Packages)**: Nếu bạn viết một thư viện mã nguồn mở cho người khác xài, bạn phải viết bằng TS để khi người khác cài vào máy, trình soạn thảo của họ sẽ tự động gợi ý cách dùng (Thông qua file `.d.ts`).

</details>

1. **Enterprise React/Next.js Applications**: The modern industry standard. Defining React Component `Props` using TS Interfaces completely eradicates prop-drilling errors. If a Parent component forgets to pass the required `title` prop to a Child component, the CI/CD pipeline immediately fails the build, preventing a broken UI deployment.
2. **Robust Backend Engineering (NestJS/Express)**: TypeScript enforces strict Data Transfer Object (DTO) validation. When an HTTP POST request hits the server, TS ensures the JSON body perfectly aligns with the Database Schema models (e.g., Prisma or TypeORM) before any database write operations occur.
3. **Open-Source Library Publishing**: Distributing a library to NPM without Type Definitions (`.d.ts` files) is heavily discouraged today. Writing the library in TS automatically generates these definition files, granting downstream consumers perfect autocomplete and type safety when utilizing your library's APIs.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Bật chế độ `strict: true`**: Khi cấu hình file `tsconfig.json`, luôn luôn bật `strict: true`. Nó ép bạn phải kiểm tra các biến có khả năng bị `null` hoặc `undefined`. Nếu tắt đi, TS sẽ dễ dãi như JS, mất hoàn toàn tác dụng.
2. **Phân biệt `interface` và `type`**: 
   - Dùng `interface` để định nghĩa Cấu trúc Dữ liệu (Ví dụ: Class, Object User, Product).
   - Dùng `type` để gom nhóm các kiểu dữ liệu lẻ tẻ hoặc hàm (Ví dụ: `type Status = "OK" | "FAIL"`).
3. **Sử dụng Generics (`<T>`)**: Khi bạn viết một cái hàm "Nhập gì xuất nấy" (Ví dụ hàm Fetch API chung). Đừng để Type là `any`. Hãy dùng Generic `<T>` để TS tự động giữ nguyên Type của biến từ lúc chui vào hàm đến lúc chui ra.

</details>

1. **Enable Strict Mode (`"strict": true`)**: The most critical configuration in `tsconfig.json`. This enforces `strictNullChecks`. Without it, TypeScript allows assigning `null` to a `number` variable, completely defeating the purpose of static typing and re-introducing the "Billion Dollar Mistake" (Null Pointer Exceptions).
2. **Interface vs. Type Aliases**: 
   - Prefer `interface` for declaring object shapes, data models, and class contracts. Interfaces support Declaration Merging and are generally better optimized by the compiler for massive structures.
   - Prefer `type` for defining Primitives, Unions (e.g., `type Role = 'Admin' | 'User'`), Intersections, and complex utility types (e.g., `Omit`, `Pick`).
3. **Leverage Generics (`<T>`)**: Avoid hardcoding types for reusable utility functions. A function like `fetchData(url)` shouldn't return `any`. It should be `async function fetchData<T>(url: string): Promise<T>`. This allows the caller to explicitly inject the expected return type (e.g., `fetchData<User>('/user/1')`), ensuring end-to-end type safety across network boundaries.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Lạm dụng từ khóa `any` (Sát thủ thầm lặng)**: Khi TS báo lỗi đỏ chóe vì bạn lười tìm hiểu cấu trúc dữ liệu, bạn tức giận gõ `let data: any = ...`. Xin chúc mừng, chữ `any` tắt hoàn toàn hệ thống kiểm tra của TS trên biến đó. Nó biến code TS đắt tiền của bạn quay về JS cùi bắp.
   - *Luật*: Tuyệt đối cấm dùng `any`. Nếu chưa biết dữ liệu trả về hình dạng ra sao, hãy dùng `unknown` (TS sẽ ép bạn phải dùng if/else kiểm tra trước khi sử dụng).
2. **Ảo tưởng "An toàn tuyệt đối" (Trusting Network Data)**: TS chỉ kiểm tra code LÚC GÕ PHÍM (Compile-time). Nếu bạn khai báo `user: User`, TS sẽ tin bạn. NHƯNG, nếu dữ liệu đó tải từ API trên mạng về, và API đó vô tình trả về một danh sách Gà Vịt (Không phải User). TS KHÔNG HỀ BIẾT điều đó (Vì TS đã bị xóa sạch lúc chạy ở Trình duyệt).
   - *Luật*: Ở biên giới mạng (Gọi API), Type của TS là vô dụng. Bắt buộc phải dùng các thư viện Runtime Validation (như **Zod** hoặc **Yup**) để xác minh cục JSON lúc nó vừa bay tới trình duyệt.

</details>

1. **The `any` Escape Hatch Anti-Pattern**: When developers struggle to satisfy the Compiler, they lazily explicitly cast a variable as `any` (e.g., `const payload: any`). This completely silences the compiler, physically bypassing the entire type-checking engine for that tree of code. The codebase regresses to Vanilla JS. **Rule**: Ban `any` using ESLint. If you genuinely cannot predict a payload's structure, type it as `unknown`. TypeScript will strictly force you to execute runtime Type Narrowing (e.g., `typeof val === 'string'`) before permitting you to manipulate it.
2. **The Compile-Time Illusion (Runtime Blindness)**: The most dangerous misconception. TypeScript *does not exist at Runtime*. If you assert an incoming API JSON payload as a specific type: `const user = response.data as User;`. You are lying to the compiler. If the backend actually returned an array of `Cats`, the TypeScript compiled code will blindly attempt to read `user.email`, and silently crash the application. **The Fix**: TypeScript cannot validate network data. You MUST execute explicit Runtime Validation at the network boundary using libraries like **Zod** or **Joi** to parse the raw JSON and guarantee it mathematically matches the TS Interface.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các khai báo Type phổ biến trong TypeScript.
</details>

### Basic Types & Unions
```typescript
let isDone: boolean = false;
let lines: number = 42;
let name: string = "Alice";
let list: number[] = [1, 2, 3]; // Array of numbers

// Union Type (Can be one or the other)
let status: "loading" | "success" | "error" = "loading";

// Optional parameter (?)
function printName(first: string, last?: string) { ... }
```

### Interfaces & Types
```typescript
interface User {
  id: number;
  email: string;
  isAdmin?: boolean; // Optional property
  readonly createdAt: string; // Cannot be modified after creation
}

type ID = string | number;

// Intersection (Merging types)
type Employee = User & { salary: number }; 
```

### Functions
```typescript
// Typing parameters and return value
const calculateTax = (amount: number, taxRate: number): number => {
  return amount + (amount * taxRate);
};

// Function returning nothing
function logMessage(msg: string): void {
  console.log(msg);
}
```

### Generics
```typescript
// <T> captures the type passed in, and uses it for the return type
function wrapInArray<T>(value: T): T[] {
  return [value];
}

const numArr = wrapInArray(5); // Inferred as number[]
const strArr = wrapInArray("hello"); // Inferred as string[]
```

### Utility Types (Built-in Magic)
```typescript
interface Todo {
  title: string;
  description: string;
  completed: boolean;
}

// Partial: Makes all properties optional (Great for update APIs)
type UpdateTodoInput = Partial<Todo>; 

// Pick: Creates a new type picking only specific properties
type TodoPreview = Pick<Todo, "title" | "completed">;

// Omit: Creates a new type excluding specific properties
type TodoCreate = Omit<Todo, "completed">; 
```

---

## Related Topics

- For how TS interacts with the frontend logic, read **[JavaScript](./javascript.md)**.
- For building strict TS architectures on the server, read **[Node.js / Express](../backend/nodejs-express.md)**.
- For combining TS with Component libraries, explore **[React](./react.md)**.
