# API Layer Design (Advanced)

Xây dựng API Layer tốt ở Frontend giúp chống lại các lỗi mất kết nối mạng, hết hạn Token, trùng lặp request, và tạo ra một codebase dễ maintain.

## 1. Thiết kế Axios Interceptors (Cấp độ Enterprise)

Khi gọi API, bạn cần một nơi duy nhất để đính kèm Token (Request Interceptor) và bắt lỗi global/refresh token (Response Interceptor).

```typescript
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000, // Bắt buộc phải có timeout để tránh treo UI
});

// REQUEST INTERCEPTOR
apiClient.interceptors.request.use((config) => {
  const token = getAccessToken(); // Lấy từ memory hoặc cookie
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// RESPONSE INTERCEPTOR (Bắt lỗi & Refresh Token)
let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: Error | null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Lỗi 401 (Hết token) và chưa từng thử refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Nếu đang refresh dở, các request khác đưa vào hàng đợi
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers.Authorization = 'Bearer ' + token;
          return apiClient(originalRequest);
        }).catch(err => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newAccessToken = await callRefreshTokenAPI(); // Gọi API refresh
        saveAccessToken(newAccessToken);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
        
        processQueue(null, newAccessToken);
        
        // Chạy lại request bị lỗi ban đầu với token mới
        return apiClient(originalRequest);
      } catch (err) {
        processQueue(err as Error, null);
        // Force logout user
        forceLogout();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);
```

---

## 2. API Code Generation (Swagger/OpenAPI)

Đừng bao giờ tự định nghĩa TypeScript interface cho API response bằng tay (vừa mệt, vừa dễ lỗi thời khi Backend đổi specs). Hãy tự động sinh mã!

Sử dụng **Orval** hoặc **OpenAPI-Typescript-Codegen**.

```bash
# Ví dụ cấu hình Orval (orval.config.ts)
export default {
  myApi: {
    input: 'https://my-backend.com/api-docs/swagger.json',
    output: {
      mode: 'tags-split',
      target: 'src/api/endpoints',
      client: 'react-query', # Tự sinh mã React Query Hooks siêu xịn!
      mock: true,            # Tự sinh mock data bằng MSW
    },
  },
};
```
Kết quả, bạn sẽ có thẳng Hook như thế này:
```tsx
const { data, isLoading } = useGetUserById(userId); // Type-safe 100%
```

---

## 3. Server State vs API Client

React Query / SWR / Apollo không phải là công cụ thay thế cho Axios. 
- **Axios / Fetch** là tầng **Transport** (Cách bạn gọi mạng).
- **React Query** là tầng **Cache & State** (Cách bạn lưu và sử dụng dữ liệu).

### Tại sao bắt buộc dùng React Query/SWR thay vì `useEffect + fetch`?
- **Deduping:** 5 component gọi cùng 1 API, chỉ 1 request mạng bay ra.
- **Background Fetching:** Tự động gọi lại API khi user chuyển tab trở về (Focus) hoặc bật lại mạng (Reconnect) để dữ liệu luôn mới.
- **Optimistic Updates:** Bấm "Like", lập tức cho UI đỏ tim (Optimistic) trước khi chờ API trả kết quả. Giúp app phản hồi tức thì.
- **Pagination / Infinite Scroll:** Hỗ trợ sẵn API siêu mạnh.

> [!TIP]
> Việc tách rõ **API Transport Layer** (axios instance) và **Caching Layer** (React Query) giúp bạn có thể dễ dàng đổi từ REST sang GraphQL hoặc đổi HTTP client (Fetch) mà không phải sửa UI components.
