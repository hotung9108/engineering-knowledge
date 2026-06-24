# Advanced TypeScript

TypeScript là tiêu chuẩn công nghiệp cho Frontend. Ở level Senior, bạn cần nắm vững Type Manipulation, Generics, và Inference thay vì chỉ dùng `interface` và `any`.

## 1. Union, Intersection & Type Narrowing

### Type Guarding
Việc kiểm tra type tại runtime để TypeScript tự động hiểu type hẹp hơn.
- Dùng `typeof`, `instanceof`, `in`.
- **Custom Type Predicate:**

```typescript
type Fish = { swim: () => void };
type Bird = { fly: () => void };

// 'pet is Fish' là Type Predicate
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}

const myPet: Fish | Bird = getPet();
if (isFish(myPet)) {
  myPet.swim(); // TS hiểu myPet là Fish
}
```

### Discriminated Unions
Pattern cực mạnh trong React State (Redux actions, Fetching state).

```typescript
type FetchState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function render(state: FetchState<User>) {
  if (state.status === 'success') {
    console.log(state.data); // TS biết chắc chắn có 'data'
  }
}
```

---

## 2. Utility Types & Keyof

Các utility types có sẵn và cách tự build:

```typescript
interface User { id: string; name: string; age: number; email?: string }

// 1. Partial, Required, Readonly
type PartialUser = Partial<User>; // Tất cả optional
type RequiredUser = Required<User>; // Tất cả bắt buộc
type ReadonlyUser = Readonly<User>; // Tất cả readonly

// 2. Pick & Omit
type UserSummary = Pick<User, 'id' | 'name'>;
type UserWithoutEmail = Omit<User, 'email'>;

// 3. Record
type UserRoleDict = Record<string, 'admin' | 'user' | 'guest'>;

// 4. keyof & Mapped Types (Under the hood)
// Đây là cách Omit hoạt động
type MyOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Tạo type biến mọi thứ thành string
type Stringify<T> = {
  [K in keyof T]: string;
};
```

---

## 3. Conditional Types & `infer`

Cú pháp: `T extends U ? X : Y`

```typescript
// Type nhận biết có phải mảng không
type IsArray<T> = T extends any[] ? true : false;
```

### Sức mạnh của `infer`
Dùng để "móc" ra một type con từ bên trong một type phức tạp.

```typescript
// Trích xuất kiểu trả về của một Promise
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type A = UnwrapPromise<Promise<string>>; // string
type B = UnwrapPromise<number>; // number

// Lấy type phần tử của mảng
type Flatten<T> = T extends Array<infer Item> ? Item : T;
type Str = Flatten<string[]>; // string

// ReturnType (Built-in)
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : any;
```

---

## 4. Advanced Generics & Constraints

Ràng buộc (Constraints) Generics bằng `extends`.

```typescript
// Hàm lấy value theo key, type-safe 100%
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
getProperty(user, "name"); // type = string
// getProperty(user, "invalid"); // Error
```

## 5. Branded Types (Opaque Types)

Dùng để tránh việc truyền nhầm các ID string khác loại cho nhau.

```typescript
type UserId = string & { readonly __brand: unique symbol };
type PostId = string & { readonly __brand: unique symbol };

function getUserId(id: string): UserId {
  return id as UserId;
}

const uid = getUserId("123");
const pid = "456" as PostId;

// function fetchUser(id: UserId)
// fetchUser(pid); // LỖI biên dịch, dù cả 2 là string, chống bug cực tốt!
```
