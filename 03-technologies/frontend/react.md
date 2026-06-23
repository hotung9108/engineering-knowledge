# React

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Trước khi có React, lập trình viên tạo giao diện web bằng cách chèn HTML vào những chuỗi văn bản khổng lồ, sau đó dùng jQuery để dò tìm từng cái ID trên màn hình và sửa lại chữ. Khi ứng dụng lớn lên (như Facebook), việc quản lý "cái nút nào đang nhấp nháy, tin nhắn nào vừa tới" trở thành một đống rác code (Spaghetti code) cực kì dễ lỗi. **React**, sinh ra từ Facebook, đã thay đổi hoàn toàn cách chúng ta làm web. Nó đưa ra hai khái niệm vĩ đại: **Component** (Chia giao diện thành các cục Lego nhỏ tự quản lý) và **Virtual DOM** (Cập nhật giao diện siêu tốc mà không cần tải lại toàn bộ trang).

</details>

> **Summary**: Prior to React, Frontend architecture relied on imperative DOM manipulation (e.g., jQuery) tightly coupled with raw HTML strings. As web applications scaled into complex Single Page Applications (SPAs) like Facebook, manually orchestrating complex state transitions across thousands of DOM nodes resulted in catastrophic architectural fragility and unmaintainable spaghetti code. **React**, open-sourced by Facebook, revolutionized the UI landscape by introducing a declarative, Component-based architecture. It shifted the paradigm from "manipulating the DOM" to "rendering State". React's core innovation is the **Virtual DOM**—an in-memory representation of the UI that rigorously calculates the minimal diff required to update the actual browser DOM, ensuring high performance regardless of data complexity.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang vẽ một bức tranh phong cảnh có 100 cái cây và 1 ông mặt trời. Đột nhiên ông mặt trời chuyển sang màu đỏ.
1. **Cách làm cũ (jQuery)**: Bạn phải lấy cục tẩy, bôi xóa thật cẩn thận đúng cái hình ông mặt trời trên tờ giấy, rồi lấy bút màu đỏ vẽ lại vào chỗ đó. Nếu lỡ tay, bạn bôi nhầm luôn cái cây bên cạnh (Lỗi code rác).
2. **Cách làm của React (Virtual DOM)**: Trí não bạn (React) tưởng tượng ra một bức tranh mới toanh có mặt trời màu đỏ. Sau đó, não bạn tự so sánh bức tranh tưởng tượng đó với bức tranh thật trên bàn. Nó nhận ra: "À, 100 cái cây giữ nguyên, chỉ có mặt trời là khác". React sẽ CẦM TAY BẠN, tự động lấy bút đỏ tô đè lên đúng cái mặt trời mà không bao giờ đụng vào cái cây. (Bạn không cần tự tay xóa hay vẽ, bạn chỉ cần ra lệnh: "Tao muốn mặt trời màu đỏ").

</details>

Imagine directing an Orchestra of 100 musicians.
1. **Imperative (jQuery/Vanilla JS)**: You (the developer) must walk up to every single musician individually and tell them exactly what to play, when to breathe, and how loud to be. If the song suddenly changes, you must frantically run around to all 100 musicians telling them to stop and play the new notes.
2. **Declarative (React)**: You simply hand out a piece of Sheet Music (the State) to the Orchestra. You don't tell them *how* to play it. If the song changes, you just hand them a new piece of Sheet Music. The Orchestra (React) automatically figures out who needs to stop, who needs to start, and perfectly transitions the music. You only manage the Sheet Music; React manages the musicians.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

React được xây dựng dựa trên 3 khái niệm cốt lõi:
1. **JSX (JavaScript XML)**: Cho phép bạn viết code HTML lai với JavaScript. Nhìn nó giống HTML, nhưng bên trong nó là sức mạnh tính toán của JS (`<h1>{user.name}</h1>`).
2. **Components**: Bẻ gãy một trang web khổng lồ thành các mảnh Lego tái sử dụng được (Header, Footer, Button, Card). Mỗi Component là một Hàm JS, nhận dữ liệu đầu vào (Props) và trả về một đoạn giao diện (JSX).
3. **State & Props (Trạng thái và Thuộc tính)**: 
   - *State* là trí nhớ bí mật của riêng một Component (Ví dụ: Nút Like nhớ rằng nó đang được bấm hay chưa). Nếu State thay đổi, Component tự động vẽ lại chính nó (Re-render).
   - *Props* là dữ liệu do "Cha" truyền xuống "Con". Khác với State, Props là đọc-chỉ (Read-only), Con không được quyền sửa Props của Cha.

</details>

React's architectural foundation rests on three primary pillars:
1. **JSX (JavaScript Syntax Extension)**: A syntactic sugar that allows developers to write XML/HTML-like structures directly within JavaScript logic. It bridges the traditional gap between View logic and Business logic, compiling down to `React.createElement()` calls.
2. **Component-Based Architecture**: React enforces extreme modularity. A UI is deconstructed into independent, reusable Functions (Components) that return JSX. Components completely encapsulate their own layout, styling, and behavior logic.
3. **Unidirectional Data Flow (State & Props)**: 
   - *State* (`useState`) represents mutable, component-internal memory. When State mutates, React automatically triggers a reconciliation cycle to re-render the component tree.
   - *Props* (Properties) are strictly read-only data payloads passed downwards from Parent to Child components. Children cannot directly mutate their Props, ensuring predictable, highly traceable data flows.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Bạn đang lướt Facebook. Có hộp Chat ở góc phải, Bảng tin ở giữa, Danh sách bạn online ở bên trái.
Đột nhiên, bạn của bạn nhắn tin tới. Chữ "Bạn có 1 tin nhắn mới" hiện lên ở 3 nơi khác nhau: Trên thanh tiêu đề, ở cục Chat màu đỏ, và ở danh sách bạn bè.
Nếu làm bằng JS thuần: Bạn sẽ phải viết 3 dòng code `document.getElementById('header').innerHTML = 1; document.getElementById('chat').innerHTML = 1...`. Càng nhiều tính năng, số lượng dòng code "tìm và sửa" này càng phình to đến mức không thể kiểm soát.
React giải quyết triệt để vấn đề này. Dữ liệu (State) được gán làm NGUỒN CHÂN LÝ DUY NHẤT. Khi biến `unread_messages = 1`, React tự động lan truyền con số 1 đó tới cả 3 chỗ trên màn hình cùng một lúc. Lập trình viên không cần đụng tay vào DOM nữa. 

</details>

React was engineered to solve the "Cascading Updates" problem inherent in highly dynamic Web 2.0 applications.
In MVC architectures (like Backbone.js), bidirectional data binding was common. If Model A updated, it triggered View B. View B's update triggered Model C, which cascaded back to View A. Debugging a layout bug required tracing an infinite loop of mutated event listeners.
React enforced **Declarative Rendering** and **Unidirectional Data Flow**. Developers declare: "Given this JSON Data (State), the UI should look exactly like this JSX." React's Virtual DOM engine assumes full responsibility for the DOM mutations. By making the UI a pure mathematical function of State (`UI = f(State)`), React eradicated manual DOM tracking, drastically reducing cognitive load and eliminating entire classes of DOM-synchronization bugs.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc tạo ra một cái Nút "Bấm để Tăng số" (Counter Button).
</details>

Visualizing Imperative DOM Mutation vs. Declarative React State.

| Metric | Vanilla JavaScript (Imperative) | React (Declarative) |
|---|---|---|
| **HTML Setup** | `<button id="btn">0</button>` | (None. Handled in JS) |
| **Logic Code** | `let count = 0;`<br>`const btn = document.getElementById('btn');`<br>`btn.addEventListener('click', () => {`<br>`  count++;`<br>`  btn.innerText = count;`<br>`});` | `const [count, setCount] = useState(0);`<br>`return (`<br>`  <button onClick={() => setCount(count + 1)}>`<br>`    {count}`<br>`  </button>`<br>`);` |
| **Mental Model**| **Tell the browser EXACTLY WHAT TO DO.** "Find button. Listen to click. Do math. Update text." | **Tell React WHAT TO BE.** "Render a button. If clicked, update my State. React, handle the text update for me." |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Single Page Applications (SPA)**: Các hệ thống quản trị (Admin Dashboard), CRM, ERP nội bộ. Nơi người dùng bấm chuyển trang liên tục nhưng trình duyệt không hề chớp màn hình (Vì mọi HTML đã được tải sẵn 1 lần duy nhất từ đầu).
2. **Hệ thống Design System (UI Kit)**: Khi công ty bạn lớn, bạn cần 1 thư viện chuẩn chung cho toàn công ty (Ví dụ: Màu nút bấm, font chữ, kích cỡ hộp thoại). React Component là công cụ hoàn hảo để đóng gói các UI này thành các thư viện NPM nội bộ cho mọi team dùng chung.
3. **Kết hợp với SSR (Next.js/Remix)**: React thuần túy cực kỳ tồi tệ cho SEO vì Google Bot chỉ thấy 1 trang trắng bóc lúc đầu. Do đó, người ta thường bọc React bên trong Next.js để máy chủ kết xuất sẵn HTML rồi mới gửi cho trình duyệt, giải quyết triệt để bài toán SEO.

</details>

1. **Complex Single Page Applications (SPAs)**: B2B SaaS platforms, rich internal Admin Dashboards, and Web-based Editors (e.g., Notion, Spotify Web). Scenarios where highly complex, deeply nested Client-Side state must persist without triggering full browser navigation reloads.
2. **Component Libraries / Design Systems**: Large organizations (e.g., Uber, Airbnb) require extreme visual consistency across 50 different micro-frontends. React's component boundaries make it the perfect vehicle to build centralized, version-controlled UI component libraries (`<Button />`, `<Modal />`) distributed via private NPM registries.
3. **The Foundation for Meta-Frameworks**: Pure Client-Side React (Create React App/Vite) suffers from massive SEO penalties and slow First Contentful Paint (FCP) because the browser must download the massive JS bundle before rendering a single pixel. Consequently, React is now predominantly used as the UI rendering engine *underneath* robust Server-Side Rendering frameworks like **Next.js** and **Remix**.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hiểu rõ Vòng đời Component (Lifecycle)**: Trong React Hooks, `useEffect` là con dao hai lưỡi. Đừng dùng `useEffect` để tính toán lại dữ liệu (Ví dụ: `fullName = firstName + lastName`), hãy tính nó trực tiếp trong hàm. Chỉ dùng `useEffect` để gọi API, tương tác với hệ thống ngoài (Browser APIs), hoặc đăng ký sự kiện (Sockets).
2. **Sử dụng Custom Hooks**: Đừng viết một cái Component có 500 dòng code. Giao diện (JSX) và Logic (API, tính toán) phải tách biệt. Hãy gom nhóm các biến State và hàm `useEffect` có liên quan đẩy ra một file riêng (Ví dụ: `useFetchData()`). Lúc này file giao diện của bạn sẽ cực kỳ sạch sẽ và dễ đọc.

</details>

1. **Master the Rules of Hooks (Specifically `useEffect`)**: `useEffect` is strictly an escape hatch to synchronize React State with external systems (e.g., Network Requests, WebSockets, or raw DOM events). The most common React anti-pattern is using `useEffect` to derive internal state (e.g., updating a `fullName` state whenever `firstName` changes). **Rule**: If a value can be computed directly from existing state during the render cycle, compute it directly. Do not chain `useEffect` calls.
2. **Abstract Logic into Custom Hooks**: A React component rendering UI should not contain 200 lines of complex data fetching and state mutation logic. This violates Separation of Concerns. Extract cohesive business logic into highly testable Custom Hooks (e.g., `useCartManagement()`). The presentation component should simply consume the hook: `const { cart, addItem } = useCartManagement(); return <UI />`.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Cơn ác mộng "Prop Drilling" (Khoan giếng)**: Bạn có biến dữ liệu ở Component Ông Nội. Bạn muốn truyền cho Component Cháu Cố. Bạn phải truyền nó qua Cha, rồi truyền qua Con, rồi mới tới Cháu (Truyền 4 tầng liên tiếp). Việc này làm rác code ở những Component trung gian không dùng đến biến đó.
   - *Cách giải quyết*: Đừng truyền Props cho những thứ sâu quá 3 tầng. Hãy dùng React `Context API` hoặc thư viện Quản lý State toàn cục như **Zustand** hoặc **Redux**.
2. **Bỏ quên Dependency Array trong `useEffect`**: Khi viết `useEffect(() => { ... }, [])`, nếu bạn quên khai báo cái biến vào trong cái mảng vuông `[]` ở cuối, code của bạn sẽ bị "nhớ dai" dữ liệu cũ rích từ lần chạy đầu tiên (Stale Closure). Nếu bạn không bỏ dấu `[]` vào luôn, API của bạn sẽ bị gọi lặp lại hàng triệu lần (Infinite Loop) làm sập Server ngay lập tức.

</details>

1. **Catastrophic Prop Drilling**: Passing data from a top-level `<App />` component down through 6 layers of intermediate wrapper components just to reach a tiny `<Avatar />` component at the bottom of the tree. The intermediate components are polluted with unused props, destroying their reusability. **The Fix**: Limit Prop passing to 2-3 levels deep. For global data (Themes, User Sessions), utilize the native `React Context API`. For complex, high-frequency global state, utilize lightweight Atomic state managers like **Zustand** or **Jotai** (avoiding the boilerplate of legacy Redux).
2. **`useEffect` Dependency Array Disasters (Infinite Loops)**: The single largest source of bugs in React Hooks. If you omit the dependency array entirely `useEffect(() => { fetch() })`, the effect runs after *every single render*, causing an infinite loop that instantly DDOSes your backend API. If you pass an empty array `[]` but utilize state inside the effect, the effect traps a "Stale Closure" and operates on outdated memory. **Absolute Rule**: Always install and rigorously obey the `eslint-plugin-react-hooks` linter rule (`exhaustive-deps`). Never ignore its warnings.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp các Hooks và cú pháp React phổ biến nhất.
</details>

### Component Skeleton (Functional Component)
```tsx
import React, { useState, useEffect } from 'react';

// Define Props Interface (using TypeScript)
interface UserCardProps {
  userId: string;
  onFollow: (id: string) => void;
}

const UserCard: React.FC<UserCardProps> = ({ userId, onFollow }) => {
  // JSX must return a single parent element (or a Fragment <></>)
  return (
    <div className="card">
      <h2>User: {userId}</h2>
      <button onClick={() => onFollow(userId)}>Follow</button>
    </div>
  );
};

export default UserCard;
```

### React Hooks: `useState` (Local Memory)
```tsx
const [count, setCount] = useState<number>(0);

const handleIncrement = () => {
  // CORRECT WAY: If next state depends on previous state, use callback function
  setCount((prevCount) => prevCount + 1); 
};
```

### React Hooks: `useEffect` (Side Effects)
```tsx
// 1. Run ONCE when component mounts (Empty dependency array)
useEffect(() => {
  console.log("Component Mounted. Fetch initial data here.");
}, []);

// 2. Run EVERY TIME a specific variable changes
const [userId, setUserId] = useState(1);
useEffect(() => {
  fetch(`/api/users/${userId}`);
}, [userId]); // Dependency array

// 3. CLEANUP function (Runs right before component is destroyed or re-runs)
useEffect(() => {
  const interval = setInterval(() => console.log('Tick'), 1000);
  
  // Return a cleanup function to prevent memory leaks!
  return () => clearInterval(interval);
}, []);
```

### Conditional Rendering & Mapping Arrays
```tsx
const [isLoading, setIsLoading] = useState(true);
const [items, setItems] = useState([{id: 1, name: 'Apple'}, {id: 2, name: 'Banana'}]);

return (
  <>
    {/* 1. Ternary Operator for if/else */}
    {isLoading ? <Spinner /> : <Dashboard />}
    
    {/* 2. Logical AND for if (without else) */}
    {items.length === 0 && <p>No items found</p>}
    
    {/* 3. Array.map() for rendering lists. CRITICAL: MUST provide unique 'key' */}
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  </>
);
```

### React Hooks: `useRef` (Direct DOM Access & Persistent Mutables)
```tsx
const inputRef = useRef<HTMLInputElement>(null);

const focusInput = () => {
  // Safely access the actual DOM node
  inputRef.current?.focus(); 
};

// Also used to store a variable that DOES NOT trigger a re-render when changed
const renderCount = useRef(0);
renderCount.current++; // Will not trigger UI update

return <input ref={inputRef} placeholder="Type here..." />;
```

---

## Related Topics

- React compiles down to heavily optimized **[JavaScript](./javascript.md)**.
- For building production-ready apps with SEO, wrap React in **[Next.js](./nextjs.md)**.
- For styling React components rapidly, use **[TailwindCSS](./tailwindcss.md)**.
