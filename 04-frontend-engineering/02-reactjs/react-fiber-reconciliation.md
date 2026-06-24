# React Fiber & Reconciliation (Advanced)

Hiểu React hoạt động dưới nắp capo là chìa khoá để viết các ứng dụng siêu tốc và tránh những bug re-render khó hiểu.

## 1. Vấn đề của Stack Reconciler (React 15 trở về trước)

Trước React 16, React dùng "Stack Reconciler". Quá trình render và diffing DOM là **đồng bộ (Synchronous)** và đệ quy. 
- Khi một update lớn xảy ra, React sẽ khóa Main Thread (block UI) cho đến khi quá trình diffing hoàn tất.
- Trình duyệt không thể xử lý user input (typing, clicking) hoặc animation, dẫn đến giật lag (dropped frames).

## 2. React Fiber (React 16+)

React 16 đập đi xây lại core bằng **Fiber Reconciler**.

**Fiber là gì?** 
Nó là một Plain JavaScript Object đại diện cho một đơn vị công việc (unit of work). Mỗi React Element tương ứng với một Fiber Node.

### Tính chất cốt lõi của Fiber
- **Tạm dừng và tiếp tục (Pause & Resume):** Có thể dừng việc render để nhường Main Thread cho các task khẩn cấp hơn (như user input).
- **Phân loại độ ưu tiên (Prioritization):** VD: Animation và typing (High priority) sẽ ngắt ngang quá trình render Data List (Low priority).
- **Concurrency (Đồng thời):** Trọng tâm của React 18, render nhiều UI states cùng lúc trong background mà không block main thread.

---

## 3. Quá trình Render 2 Phase của React

React chia một "Update" thành 2 phases:

### Phase 1: Render Phase (Asynchronous, Interruptible)
1. Bắt đầu từ Root, React duyệt qua Fiber Tree (Singly Linked List) bằng thuật toán Depth-First.
2. Gọi hàm `render()` của component (hoặc Function Component body).
3. So sánh VDOM mới với VDOM cũ (Diffing).
4. Đánh dấu (Tag) các thay đổi (Placement, Update, Deletion) vào các Fiber Nodes - gọi là **Effect List**.
> [!IMPORTANT]
> **Phase này có thể bị tạm dừng, huỷ bỏ, hoặc chạy lại từ đầu.** Do đó, KHÔNG ĐƯỢC để side-effects (API calls, DOM mutation) trong Function Body. (Đó là lý do ta cần `useEffect`).

### Phase 2: Commit Phase (Synchronous, Uninterruptible)
1. Duyệt qua **Effect List** đã tạo ở Phase 1.
2. Áp dụng các thay đổi đó vào thực tế (Real DOM).
3. Chạy `useLayoutEffect` (trước khi browser paint).
4. Chạy `useEffect` (sau khi browser paint).
> [!IMPORTANT]
> **Phase này không thể dừng lại.** Khi đã chạm vào Real DOM, nó phải chạy một lèo để tránh UI bị hiển thị nửa vời (inconsistent state).

---

## 4. WorkLoop & `requestIdleCallback` (Cơ chế Time Slicing)

React tự viết lại một Scheduler tương tự `requestIdleCallback` của browser để thực hiện **Time Slicing** (Cắt lát thời gian).
- Thay vì duyệt toàn bộ 10,000 components một lúc.
- React duyệt 5 components -> Hết 5ms -> Nhường quyền cho trình duyệt vẽ UI, bắt sự kiện chuột.
- Trình duyệt rảnh -> React duyệt tiếp 5 components tiếp theo.

Đó chính là sức mạnh của tính năng **Concurrent Rendering** thông qua `useTransition` và `useDeferredValue` ở React 18.
