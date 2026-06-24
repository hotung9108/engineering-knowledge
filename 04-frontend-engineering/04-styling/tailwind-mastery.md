# Tailwind Mastery (Advanced)

Tailwind CSS không chỉ là "inline styles bằng classes". Ở mức nâng cao, nó là một công cụ cấu hình Design System toàn diện.

## 1. Tuỳ biến cấu hình sâu (tailwind.config.js)

Không nên lạm dụng Arbitrary values `text-[#ff0000]`. Hãy đưa nó vào Design Tokens.

### Mở rộng (Extend) vs Cầm trịch (Override)
- Nằm trong `theme.extend`: Thêm màu mới, giữ nguyên màu mặc định của Tailwind.
- Nằm ngoài `theme.extend` (ngay trong `theme`): XÓA SẠCH toàn bộ màu/font mặc định và chỉ dùng thiết lập của bạn. Rất tốt cho Enterprise Design System.

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    // Override: Bỏ hết font chuẩn, ép dùng font này
    fontFamily: {
      sans: ['Inter', 'sans-serif'], 
    },
    extend: {
      // Extend: Giữ nguyên dải màu chuẩn, thêm brand color
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9', // bg-brand-500
          900: '#0c4a6e',
        }
      }
    }
  }
}
```

---

## 2. Vấn đề "Nối chuỗi Class" trong React

Đây là lỗi phổ biến nhất khi build Component bằng Tailwind: Xung đột class khi component nhận prop className từ cha truyền xuống.

Ví dụ: Component mặc định có `px-4 py-2 bg-blue-500`. Bạn gọi `<Button className="bg-red-500" />`. 
Chuỗi sinh ra: `px-4 py-2 bg-blue-500 bg-red-500`. 
Trình duyệt sẽ áp dụng class nào? CSS ưu tiên theo thứ tự **khai báo trong file CSS**, không phải thứ tự chuỗi! Do đó kết quả sẽ cực kỳ hên xui.

### Giải pháp 1: `tailwind-merge` + `clsx` (Chuẩn mực hiện nay)
Thư viện `tailwind-merge` hiểu rõ logic Tailwind để triệt tiêu class cũ.

```tsx
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

// Hàm cn (classnames) huyền thoại (Shadcn UI sử dụng)
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// CÁCH DÙNG
function Button({ className }) {
  return <button className={cn("bg-blue-500 text-white p-2", className)} />
}
// Nếu truyền className="bg-red-500", twMerge sẽ xoá bg-blue-500 đi.
```

### Giải pháp 2: CVA (Class Variance Authority)
Cách tuyệt vời nhất để tạo Design System với các "Variants" (kiểu như `variant="outline"`, `size="lg"`).

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors", // Base classes
  {
    variants: {
      variant: {
        default: "bg-blue-500 text-white hover:bg-blue-600",
        outline: "border border-gray-300 bg-transparent hover:bg-gray-100",
        destructive: "bg-red-500 text-white hover:bg-red-600",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        default: "h-10 px-4 py-2",
        lg: "h-12 px-8 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

// Tạo Component Type-safe hoàn toàn!
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}
```

---

## 3. Viết Tailwind Plugin tự tạo (Advanced)

Thay vì dùng `@apply` trong file `.css` (điều mà chính tác giả Tailwind khuyên hạn chế dùng), hãy viết Plugin JS để tái sử dụng component toàn cục.

```javascript
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addComponents, theme }) {
      addComponents({
        '.card': {
          backgroundColor: theme('colors.white'),
          borderRadius: theme('borderRadius.lg'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.xl'),
        }
      })
    })
  ]
}
```
Khi này bạn chỉ cần dùng class `card` ở khắp nơi trong HTML.
