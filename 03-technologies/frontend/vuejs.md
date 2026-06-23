# Vue.js

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Giới Frontend thường hay nói: "Angular là một công trường xây dựng khổng lồ do tập đoàn Google quy hoạch, React là một thư viện linh hoạt nhưng phải tự chắp vá do Facebook tạo ra, còn **Vue.js** là một kiệt tác cân bằng kết hợp những gì tinh túy nhất của cả hai". Vue được tạo ra bởi Evan You (cựu kĩ sư Google). Nó nổi tiếng vì đường cong học tập (learning curve) cực kỳ thấp: Bạn có thể nhúng Vue vào một file HTML cũ kĩ bằng 1 dòng `<script>` và chạy ngay lập tức, nhưng nó cũng đủ mạnh để xây dựng một Hệ thống Single Page Application (SPA) khổng lồ phức tạp chẳng kém gì React.

</details>

> **Summary**: The Frontend ecosystem is famously polarized between the rigid, enterprise-heavy Angular (Google) and the highly unopinionated, functional-first React (Facebook). **Vue.js**, created by Evan You, positions itself as the "Progressive Framework", offering the best of both paradigms. It combines the declarative template syntax and Two-Way Data Binding concepts of Angular with the Virtual DOM and Component-based architecture of React. Its defining architectural trait is its true progressiveness: Vue can gracefully scale from a simple `<script>` tag drop-in to replace jQuery on a single legacy HTML page, all the way up to a massive, statically-typed, CLI-generated Single Page Application ecosystem.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn muốn lắp một chiếc Xe Đạp (Web App).
1. **Angular**: Mua một bộ máy bay Boeing. Nó có sẵn mọi thứ, từ động cơ phản lực đến hệ thống radar. Rất xịn, nhưng quá sức rườm rà nếu bạn chỉ muốn đi chợ mua rau.
2. **React**: Mua 1000 cái ống sắt, bánh xe, ốc vít riêng lẻ. Bạn phải tự tay hàn khung, tự thiết kế hệ thống xích. Tự do tuyệt đối, nhưng rất mệt và dễ làm sai.
3. **Vue**: Mua một chiếc Xe Đạp cơ bản nhưng thiết kế cực kỳ thông minh. Bạn có thể đạp ngay lập tức. Nếu muốn đi nhanh hơn, bạn có thể mua thêm một cái Động cơ điện (Vue Router, Pinia) gắn vào nó rất mượt mà. Nó "lớn lên" cùng với nhu cầu của bạn (Progressive).

</details>

Imagine outfitting a Kitchen.
1. **Angular**: Buying an industrial-grade restaurant kitchen. It comes pre-installed with massive fryers, walk-in freezers, and a strict 500-page manual on exactly how to boil water. (Overkill for a small apartment).
2. **React**: Buying an empty room and a box of tools. You must custom-build your own oven from scratch using parts from different stores (React Router, Redux, Axios). Extremely flexible, but requires high architectural discipline.
3. **Vue.js**: Buying a beautiful, highly functional home kitchen. It has exactly what you need to cook a great meal immediately (Reactivity, Templates). If you later decide to run a bakery, you can seamlessly add professional equipment (Vue CLI, Pinia) without tearing down the walls. It is purely "Progressive".

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Vue hoạt động dựa trên cấu trúc **Single-File Component (SFC)**. Khác với React trộn lẫn HTML vào trong code JS (JSX), Vue tôn trọng sự rạch ròi truyền thống của Web. Một file `.vue` luôn chia làm 3 tầng rõ rệt:
1. `<template>`: Nơi viết HTML (Giao diện). Hỗ trợ các thẻ điều kiện thông minh như `v-if`, `v-for`.
2. `<script>`: Nơi viết JavaScript (Logic và State).
3. `<style>`: Nơi viết CSS. Cực kỳ an toàn vì có thẻ `<style scoped>`, giúp CSS ở file này không bao giờ lây lan làm hỏng giao diện ở file khác.

</details>

Vue's architectural signature is the **Single-File Component (SFC)**, typically ending in `.vue`. Unlike React, which tightly couples markup and logic using JSX, Vue enforces a modernized separation of concerns within a single cohesive file:
1. `<template>`: HTML-based declarative rendering. It utilizes highly readable Directives (e.g., `v-if`, `v-for`, `v-model`) to bind DOM attributes to the underlying component state.
2. `<script>`: The JS/TS execution context. In Vue 3, this utilizes the **Composition API** (`<script setup>`), allowing developers to logically group reactive state and side-effects elegantly.
3. `<style scoped>`: The CSS layer. Adding the `scoped` attribute guarantees that the CSS written here is mathematically sandboxed via dynamic data attributes, physically preventing CSS specificity leaks to other components.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Evan You từng làm việc cho Google và sử dụng AngularJS. Ông nhận thấy Angular rất mạnh nhưng thiết kế quá nặng nề và lộn xộn. Ông tự hỏi: *"Chuyện gì sẽ xảy ra nếu mình trích xuất phần giao diện (Reactivity) xịn xò nhất của Angular, vứt bỏ toàn bộ những cái rườm rà, và tạo ra một thư viện siêu nhẹ?"*. Đó là lý do Vue ra đời.
Vue tồn tại để cung cấp một Trải nghiệm Lập trình viên (Developer Experience - DX) hoàn hảo. Trong React, việc quản lý State đòi hỏi bạn phải nắm vững các định lý về "Bất biến" (Immutability), phải dùng hàm `setCount` chứ không được `count++`. Trong Vue, Hệ thống Phản ứng (Reactivity System) dùng `Proxy` của JavaScript sẽ âm thầm theo dõi mọi biến. Bạn cứ gõ `count++`, Vue sẽ tự động biết giao diện nào cần vẽ lại. Code Vue ngắn gọn và giống với JS tự nhiên hơn React rất nhiều.

</details>

Vue was explicitly engineered to optimize **Developer Experience (DX)** by abstracting the cognitive overhead of Reactivity.
In React, state is strictly Immutable. To update an array, a developer cannot simply `array.push()`; they must mathematically map/clone the array into a new memory reference (`setArray([...array, newItem])`) to trigger a re-render. This functional rigidity prevents bugs but steepens the learning curve.
Vue fundamentally rejects this boilerplate. Under the hood, Vue 3 utilizes native ES6 `Proxy` objects. When a developer declares a reactive variable `const user = reactive({ name: 'Alice' })`, Vue intercepts all property access. The developer can mutate the object imperatively (`user.name = 'Bob'`). Vue's proxy intercepts this mutation, mathematically calculates the exact DOM node bound to `user.name`, and surgical updates only that text node. The developer writes simple, mutable JavaScript, while the framework handles the complex Virtual DOM reconciliation invisibly.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh cú pháp Xử lý Form Input (Ràng buộc 2 chiều - Two-way Binding) giữa React và Vue.
</details>

Visualizing Two-Way Data Binding (Form Inputs).

| Metric | React (One-Way Binding) | Vue (Two-Way Binding with `v-model`) |
|---|---|---|
| **State Declaration** | `const [text, setText] = useState('');` | `const text = ref('');` |
| **DOM Element** | `<input value={text} onChange={(e) => setText(e.target.value)} />` | `<input v-model="text" />` |
| **Developer Effort**| High. You must explicitly wire the `value` to the state, and manually write an `onChange` event listener to mutate the state. | **Zero**. The `v-model` directive is syntactic sugar that automatically wires the input to the reactive variable in both directions seamlessly. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nâng cấp dự án Web cũ (Legacy Migration)**: Có một hệ thống bán hàng viết bằng PHP từ 10 năm trước. Sếp muốn thêm tính năng Giỏ hàng mượt mà (Không tải lại trang). Nếu dùng React, bạn phải đập bỏ xây lại toàn bộ bằng Node.js/API. Nếu dùng Vue, bạn chỉ việc dán 1 đường link CDN vào file HTML PHP cũ, và viết code Vue chỉ riêng cho cái góc Màn hình Giỏ hàng đó.
2. **Dashboard / CMS nội bộ (Vite + Vue 3)**: Vue rất mạnh trong việc quản lý Form, Bảng biểu (Table) và các hệ thống quản trị nhờ vào khả năng Two-way Binding (`v-model`), giúp tiết kiệm 50% số dòng code so với việc viết hàm onChange() liên tục trong React.
3. **Các dự án mã nguồn mở (Open Source) & Laravel**: Laravel (Framework số 1 của PHP) mặc định chọn Vue làm Frontend chính thức trong một thời gian dài. Cộng đồng sử dụng Vue ở Châu Á (Trung Quốc, Việt Nam) cực kỳ đông đảo, được sử dụng rộng rãi bởi Alibaba, Tencent.

</details>

1. **Progressive Enhancement of Legacy Systems (PHP/Java)**: The most potent architectural advantage of Vue over React/Angular. If a company possesses a massive monolithic Laravel or Spring Boot application rendering raw HTML, they cannot afford a $1M total rewrite to a React SPA. Vue can be imported via a `<script>` CDN link directly into a `.jsp` or `.blade.php` file. Developers can mount Vue to a specific `<div id="shopping-cart">`, progressively converting small components of the legacy app into modern Reactive SPAs without disrupting the core routing.
2. **Form-Heavy B2B Dashboards**: Internal tools requiring hundreds of inputs, checkboxes, and deeply nested object mutations. React's unidirectional flow requires monumental boilerplate (or heavy libraries like Formik/React-Hook-Form) to manage massive forms. Vue's native `v-model` directive achieves this effortlessly, cutting UI boilerplate code in half.
3. **The Nuxt.js Ecosystem (SSR/SEO)**: Just as React has Next.js, Vue has **Nuxt.js**. For high-traffic SEO-dependent platforms (E-commerce, Media), Nuxt provides identical Server-Side Rendering (SSR) and Static Site Generation (SSG) capabilities, matching the performance metrics of Next.js while retaining Vue's superior Developer Experience.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Sử dụng `<script setup>` (Composition API)**: Vue 2 ngày xưa dùng Options API (`data()`, `methods: {}`), khi file dài ra, code bị phân mảnh rất khó đọc. Vue 3 giới thiệu Composition API. Hãy luôn dùng `<script setup>`. Nó giúp bạn nhóm các biến và hàm liên quan đến 1 tính năng lại chung một chỗ, code nhìn y hệt như đang viết JavaScript thuần.
2. **Quản lý State Toàn cục bằng Pinia**: Đừng dùng Vuex (đã lỗi thời). Pinia là thư viện quản lý State chính thức mới của Vue. Nó nhẹ hơn, hỗ trợ TypeScript hoàn hảo 100%, và bỏ đi hoàn toàn cái khái niệm `Mutations` lằng nhằng của Vuex ngày xưa.

</details>

1. **Strictly Adopt the Composition API (`<script setup>`)**: In Vue 2 (Options API), logic was segregated by technical type (`data`, `methods`, `computed`). In a 1000-line component, logic for the "Search Feature" was physically scattered across 5 different objects. Vue 3's Composition API (`<script setup>`) allows developers to colocate reactive state (`ref`), computed properties, and lifecycle hooks functionally. It makes extracting and reusing logic across components infinitely easier (similar to React Custom Hooks).
2. **Utilize Pinia for Global State Management**: Historically, Vue relied on Vuex. Vuex suffered from verbose boilerplate (Mutations vs Actions) and terrible TypeScript inference. **Pinia** is the modern, official State Store for Vue. It eradicates `Mutations`, treats stores as standard TS modules, and provides flawless autocompletion without magic strings.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Nhầm lẫn giữa `ref` và `reactive`**: Vue 3 cung cấp 2 cách để khai báo biến. 
   - `ref()` dùng cho mọi thứ (Số, Chuỗi, Array, Object). Khi dùng trong thẻ `<script>`, BẮT BUỘC phải gõ thêm đuôi `.value` (Ví dụ: `count.value++`). Nếu quên `.value`, code sẽ lỗi.
   - `reactive()` chỉ dùng cho Object. Gõ rất sướng vì không cần `.value`. NHƯNG nếu bạn gán lại cả cái Object đó (`user = { name: 'Mới' }`), nó sẽ mất hoàn toàn kết nối với giao diện (Mất Reactivity).
   - *Luật*: Để an toàn tuyệt đối, cứ dùng `ref()` cho tất cả mọi thứ.
2. **Thay đổi trực tiếp Props của Cha**: Con nhận dữ liệu (Props) từ Cha. Con tự ý gán `props.title = "Đổi tên"`. Màn hình sẽ văng lỗi đỏ chót.
   - *Luật*: Giống React, luồng dữ liệu là Một chiều (One-Way Data Flow). Con muốn đổi dữ liệu, phải dùng `emit('updateTitle')` để la lên cho Cha biết. Cha nghe thấy sẽ tự tay đổi biến của Cha.

</details>

1. **The `ref()` vs `reactive()` Ambiguity**: The most common point of confusion for developers migrating to Vue 3. 
   - `reactive()` is designed for nested Objects, allowing seamless access (`user.name`), but if you destructure it (`const { name } = user`) or reassign the object completely, you instantly destroy the Proxy tracking; the UI will stop updating.
   - `ref()` works for primitives and objects. It creates a robust object wrapper. You MUST append `.value` to mutate it in JS (`count.value++`), but it gracefully survives destructuring and reassignment. **Best Practice**: Default to using `ref()` for everything to prevent Reactivity loss bugs, relying on Volar (the VSCode Vue extension) to automatically append `.value` for you.
2. **Mutating Props Directly (Reactivity Violations)**: A child component receives an `item` object via Props. The child directly executes `props.item.price = 99`. Vue will explicitly emit a runtime warning. While Vue supports Two-Way binding via `v-model`, underlying architectures still mandate **Unidirectional Data Flow**. If a child needs to mutate parent state, it must strictly use `emit('update:item', newValue)` to request the Parent component to perform the mutation itself, preserving a traceable source of truth.

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cấu trúc cơ bản của một File Vue 3 (`.vue`) sử dụng Composition API mới nhất.
</details>

### The Vue 3 Single-File Component (SFC) Structure
```html
<!-- 1. SCRIPT (Logic) -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// PROPS (Data from Parent)
const props = defineProps<{ title: string }>();

// EMITS (Events sent to Parent)
const emit = defineEmits<{ (e: 'submit', id: number): void }>();

// REACTIVE STATE
const count = ref(0);         // Primitives MUST use ref
const user = ref({ name: '' }); // Objects can use ref too

// COMPUTED (Auto-caches derived data)
const doubleCount = computed(() => count.value * 2);

// METHODS
const increment = () => {
  count.value++; // MUST use .value inside <script>
  if (count.value === 5) emit('submit', 123);
};

// LIFECYCLE HOOK
onMounted(() => {
  console.log('Component is ready on the screen!');
});
</script>

<!-- 2. TEMPLATE (HTML View) -->
<template>
  <div class="card">
    <!-- Interpolation -->
    <h1>{{ props.title }}</h1>
    
    <!-- v-if (Conditional Rendering) -->
    <p v-if="count > 10">You clicked many times!</p>
    <p v-else>Keep clicking</p>

    <!-- v-on or @ (Event Listeners) -->
    <button @click="increment">Count is: {{ count }} (Double: {{ doubleCount }})</button>

    <!-- v-model (Two-way binding for Inputs) -->
    <!-- Typing here automatically updates user.name in the script, and vice versa! -->
    <input v-model="user.name" placeholder="Enter your name" />
  </div>
</template>

<!-- 3. STYLE (Scoped CSS) -->
<style scoped>
/* 'scoped' ensures this CSS ONLY affects this specific component, no CSS bleeding! */
.card {
  border: 1px solid #ccc;
  padding: 20px;
}
h1 {
  color: #42b883; /* Vue Green */
}
</style>
```

---

## Related Topics

- Vue transpiles down to highly efficient **[JavaScript](./javascript.md)**.
- For managing scalable state in Vue, explore the **Pinia** store paradigm.
- To compare Vue's approach with Facebook's architecture, read **[React](./react.md)**.
