# C# & .NET Core

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Nếu Java Spring Boot là một "Tập đoàn khổng lồ với nhiều chi nhánh tự trị", thì **C# và .NET** là một "Đế chế công nghệ do Microsoft độc quyền kiểm soát từ A đến Z". Ra đời với mục đích đánh bại Java, C# mang trong mình thiết kế Hướng đối tượng (OOP) chặt chẽ y hệt Java, nhưng cú pháp lại hiện đại và tinh tế hơn rất nhiều. Ngày xưa, .NET bị ghét vì nó chỉ chạy độc quyền trên Windows (buộc công ty phải mua bản quyền Máy chủ Windows Server đắt đỏ). Nhưng với sự ra đời của **.NET Core** (bây giờ gọi chung là **.NET**), Microsoft đã đập đi xây lại toàn bộ, biến nó thành mã nguồn mở, chạy siêu nhanh trên cả Linux và Docker. Ngày nay, C# .NET là một đối thủ đáng gờm của Java trong các hệ thống Ngân hàng, Doanh nghiệp (Enterprise), và đặc biệt thống trị mảng phát triển Game (Unity).

</details>

> **Summary**: For decades, Enterprise Backend Engineering was dominated by Java. Microsoft engineered **C#** and the **.NET Framework** explicitly to rival Java's monopoly, offering a strictly typed, Object-Oriented language with a highly refined, modern syntax. Historically, .NET was heavily criticized and shunned by startups because it was inextricably locked to the Windows Operating System and IIS Web Servers, requiring expensive licensing. The release of **.NET Core** (now unified as simply **.NET**) executed a monumental paradigm shift. Microsoft completely rewrote the framework to be Open Source, cross-platform (native Linux/macOS support), and aggressively optimized for high-performance Cloud and Container (Docker) deployments. Today, C# .NET stands shoulder-to-shoulder with Java Spring Boot in Tier-1 Enterprise environments, offering arguably superior Developer Experience (DX), LINQ, and asynchronous native primitives.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hãy tưởng tượng bạn đang quản lý một xưởng sản xuất Đồ chơi.
1. **Node.js**: Bạn tự đi mua nhựa, tự mua khuôn đúc, tự thiết kế máy móc. Tự do tuyệt đối nhưng hay bị lỗi vặt.
2. **Java Spring Boot**: Bạn dùng hệ thống máy móc mua từ 10 công ty khác nhau (Hibernate của công ty A, Tomcat của công ty B, Spring của công ty C). Bạn ghép chúng lại với nhau. Chạy rất khỏe, nhưng thi thoảng các máy móc cãi nhau (xung đột phiên bản thư viện).
3. **C# .NET**: Bạn mua toàn bộ Dây chuyền sản xuất độc quyền từ một tập đoàn duy nhất là Microsoft. Khuôn đúc (C#), Băng chuyền (.NET), Màn hình điều khiển (Visual Studio), Kho chứa (SQL Server), Dịch vụ mây (Azure). Mọi thứ đều được thiết kế để khớp với nhau khít khìn khịt. Cực kỳ đồng bộ, cực kỳ trơn tru, không bao giờ có chuyện xung đột hệ thống.

</details>

Imagine outfitting a Professional Tool Workshop.
1. **Node.js**: You buy a generic workbench and custom-order tools from 50 different independent blacksmiths across the world (NPM modules). It's flexible, but sometimes the hammer doesn't fit the nail because they were made by different people.
2. **Java Spring Boot**: You buy high-end heavy machinery. It's incredibly powerful, but you have to buy the engine from Bosch, the drill bits from Makita, and the belts from a third company. Integrating them requires massive configuration manuals.
3. **C# .NET**: You buy the entire Workshop directly from Microsoft. The workbench, the drills, the saws, and the toolboxes are all manufactured by the exact same company. Every tool perfectly locks into every other tool without you having to read a single configuration manual. The ecosystem is flawlessly integrated.

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Hệ sinh thái .NET bao gồm 3 thành phần chính:
1. **C# (C-Sharp)**: Ngôn ngữ lập trình. Nó giống Java đến 80%, nhưng được tích hợp sẵn những "Ma thuật" như LINQ (Viết câu lệnh truy vấn dữ liệu thẳng trong code rất thanh lịch) và Async/Await (Microsoft chính là kẻ phát minh ra Async/Await trước cả JavaScript).
2. **.NET Runtime (CLR)**: Giống như JVM của Java. Code C# sẽ được dịch thành một mã trung gian (IL), sau đó CLR sẽ dịch nó ra mã máy của Windows hoặc Linux.
3. **ASP.NET Core**: Đây là Framework (như Spring Boot của Java hay Express của Node) dùng để xây dựng API Web. Nó nổi tiếng vì cung cấp sẵn mọi thứ: Dependency Injection (DI), bảo mật JWT, và ORM (Entity Framework) hoàn hảo đến từng milimet.

</details>

The Microsoft ecosystem is composed of three tightly integrated pillars:
1. **The C# Language**: A multi-paradigm, statically typed language. It shares profound structural similarities with Java but boasts vastly superior syntactic sugar. It natively integrates Language Integrated Query (**LINQ**), allowing SQL-like declarative querying of in-memory collections, and it pioneered the `async`/`await` asynchronous programming model years before JavaScript adopted it.
2. **The Common Language Runtime (CLR)**: The execution engine (analogous to Java's JVM). C# compiles down to Intermediate Language (IL) code. The CLR executes this IL via its highly tuned Just-In-Time (JIT) compiler, managing memory allocation, garbage collection, and thread execution across Windows, Linux, or macOS targets.
3. **ASP.NET Core**: The web framework framework. It provides a highly modular HTTP request pipeline, native Dependency Injection (DI) without requiring external libraries, and seamlessly integrates with **Entity Framework Core (EF Core)**—arguably the most powerful and developer-friendly Object-Relational Mapper (ORM) in the industry.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Đầu những năm 2000, Microsoft muốn cạnh tranh với Java. Họ tạo ra C# và .NET. Tuy nhiên, suốt nhiều năm, .NET bị gắn mác "Nhà giàu mới chơi được" vì nó ép chạy trên máy chủ Windows Server tốn hàng ngàn đô la tiền bản quyền.
Nhưng thế giới đã thay đổi. Đám mây (Cloud) và Docker nổi lên, Linux thống trị hoàn toàn các máy chủ Backend vì nó miễn phí và nhẹ. Microsoft nhận ra nếu không thay đổi, .NET sẽ chết.
Họ đập đi xây lại ra mắt **.NET Core**. Tại sao .NET Core lại tồn tại? Để chứng minh cho thế giới thấy Microsoft có thể tạo ra một cỗ máy Backend Nhanh hơn Node.js, Chặt chẽ bằng Java, Chạy mượt trên Linux, Hoàn toàn miễn phí (Open Source), và Mở rộng cực đỉnh trên Đám mây (Kubernetes).

</details>

Historically, the .NET Framework was a proprietary, Windows-exclusive monolith. As the industry aggressively pivoted towards Linux-based Cloud infrastructure and Docker containerization, .NET became a severe operational liability due to heavy Windows Server licensing costs.
Microsoft orchestrated an unprecedented pivot by completely rewriting the framework from scratch as **.NET Core** (now unified as .NET 5+). It exists to brutally compete in the modern Cloud-Native era. It completely severed its ties to Windows IIS, adopting the ultra-fast Kestrel cross-platform web server. Today, it exists to provide enterprises with a robust, statically typed alternative to Java that possesses significantly faster startup times, a lower memory footprint, and a more unified, less fragmented open-source ecosystem, all running natively on Ubuntu/Alpine Linux containers.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
So sánh việc thao tác với Dữ liệu (Lấy ra các User trên 18 tuổi và sắp xếp theo Tên).
</details>

Visualizing Data Manipulation (Vanilla Iteration vs C# LINQ).

| Metric | Standard Iteration (Java/JS before Streams) | C# (.NET) with LINQ |
|---|---|---|
| **The Code** | `List<User> adults = new List<>();`<br>`for(User u : users) {`<br>`  if(u.Age >= 18) adults.add(u);`<br>`}`<br>`adults.sort(new Comparator...);` | `var adults = users`<br>`  .Where(u => u.Age >= 18)`<br>`  .OrderBy(u => u.Name)`<br>`  .ToList();` |
| **Developer Effort**| High. Imperative logic requires explicitly writing the loops, managing temporary arrays, and writing verbose custom sorting comparators. | **Elegant**. LINQ (Language Integrated Query) allows SQL-like declarative syntax directly in C#. It is mathematically sound, deeply integrated into the compiler, and highly readable. |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Hệ thống Phần mềm Doanh nghiệp (Enterprise ERPs)**: Cấu trúc của C# giống hệt Java, vô cùng phù hợp để xây các dự án có tuổi thọ chục năm, với hàng ngàn Class và Interface phức tạp. Các công ty truyền thống, Ngân hàng đang xài sẵn hệ sinh thái Windows (Active Directory, Azure) gần như mặc định chọn .NET.
2. **Game Backend (Unity)**: C# là ngôn ngữ chính của Unity - Game Engine phổ biến nhất thế giới. Do đó, các công ty làm Game thường tận dụng luôn C# và .NET để viết API Máy chủ (Backend) cho Game để đội ngũ Frontend (Game Dev) và Backend có thể đọc chéo code của nhau dễ dàng.
3. **Ứng dụng Real-time quy mô lớn (SignalR)**: Trong khi Node.js dùng Socket.io, .NET có một vũ khí hạng nặng tên là **SignalR**. Nó tự động chuyển đổi qua lại giữa WebSockets và Long-polling một cách thông minh, khả năng tự kết nối lại cực đỉnh, thường được dùng trong các bảng giá chứng khoán hoặc ứng dụng Chat ngầm của doanh nghiệp.

</details>

1. **Enterprise Monoliths & Corporate IT**: The traditional stronghold of .NET. Organizations deeply embedded in the Microsoft Ecosystem (Azure Cloud, Active Directory, SQL Server) naturally gravitate towards ASP.NET Core for their internal ERPs, Payroll systems, and Customer Portals. The extreme homogeneity of the toolchain (Visual Studio IDE + C# + SQL Server) ensures unparalleled developer productivity within these corporate silos.
2. **Game Server Architectures**: Because C# is the scripting language of the Unity Game Engine (which commands over 50% of the mobile gaming market), game development studios often utilize ASP.NET Core for their Backend multiplayer servers, matchmaking APIs, and player databases. This allows Studio Engineers to share codebase logic, DTOs, and utility classes flawlessly between the Game Client and the Backend Server.
3. **High-Frequency Real-Time Comms (SignalR)**: While Node.js dominates lightweight WebSockets, ASP.NET Core possesses **SignalR**. SignalR is an incredibly robust real-time library that abstracts transport mechanisms. It gracefully attempts WebSockets, falling back to Server-Sent Events (SSE) or Long-Polling if firewalls block the socket, making it the premier choice for enterprise-grade live dashboards and trading tickers.

---

## Layer 5: Deep Practice

### Best Practices

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Khai thác tối đa Entity Framework (EF Core)**: Trái tim của .NET. Khác với Java Hibernate đôi khi rất khó cấu hình, EF Core là ORM xịn nhất hiện nay. Hãy sử dụng cơ chế `Migrations`: Bạn chỉ việc viết Code C# định nghĩa Bảng (Table), gõ 1 lệnh Terminal, EF Core tự động sinh ra file SQL để tạo Bảng trong Database. Code quản lý Database thay vì Database quản lý Code (Code-First Approach).
2. **Sử dụng Asynchronous từ đầu đến cuối (Async All The Way)**: Trong C#, khi bạn gọi một hàm `Async`, toàn bộ chuỗi các hàm gọi nó cũng phải là `Async`. Đừng bao giờ lười biếng viết `.Wait()` hay `.Result` để ép một hàm Bất đồng bộ chạy Đồng bộ. Việc này sẽ gây ra thảm họa "Chặn luồng" (Deadlock), làm sập Server ngay tức khắc.

</details>

1. **Master Entity Framework Core (Code-First Migrations)**: EF Core is arguably the most polished Object-Relational Mapper in the software industry. Adopt the **Code-First** approach. Developers define their Database Schema using pure C# POCO classes. EF Core automatically generates explicit, version-controlled C# Migration files that translate those classes into raw PostgreSQL/SQL Server queries. This ensures the Database Schema is strictly version-controlled within Git alongside the application code.
2. **Enforce "Async All the Way Down"**: ASP.NET Core is aggressively optimized for asynchronous I/O. Every controller, service, and database call must utilize `async/await`. The most fatal anti-pattern in C# is calling `.Result` or `.Wait()` on an asynchronous `Task` to force it to execute synchronously. This blocks the Thread Pool, rapidly exhausting available threads and causing catastrophic Thread Starvation (Deadlocks) under high network load.

### Common Pitfalls

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Quá phụ thuộc vào Visual Studio**: Visual Studio (VS màu tím) là một IDE tuyệt vời, nhưng nó giấu đi rất nhiều dòng lệnh cấu hình (Magic). Lập trình viên C# thường có thói quen "Bấm nút Play là chạy", mà không hiểu bên dưới máy chủ Linux nó Build (Biên dịch) ra sao. Khi đẩy code lên Docker hoặc Đám mây Linux, app chết mà không biết sửa.
   - *Luật*: Hãy tập xài `dotnet CLI` trên màn hình đen (Terminal). Hiểu rõ lệnh `dotnet build`, `dotnet run`. Hoặc thử chuyển sang xài VSCode nhẹ nhàng để hiểu rõ cấu trúc file thay vì phó mặc cho IDE.
2. **Lạm dụng LINQ quá đà**: LINQ viết rất sướng. Nhưng nếu bạn dùng LINQ để `JOIN` 5 cái bảng lại với nhau cùng hàng đống điều kiện `Where` lồng nhau. EF Core sẽ không dịch nổi ra lệnh SQL tối ưu, mà nó sẽ kéo toàn bộ dữ liệu 5 bảng đó về RAM của Server rồi mới lọc (Client-Side Evaluation). Server sẽ sập vì tràn RAM.
   - *Luật*: Với các truy vấn Thống kê (Báo cáo) cực kì phức tạp, đừng dùng LINQ. Hãy tự viết câu lệnh SQL thuần (Raw SQL) hoặc dùng Stored Procedure.

</details>

1. **The "Visual Studio Magic" Dependency**: Legacy .NET developers often rely entirely on the heavyweight Visual Studio IDE ("Click Play to Run"). They lack fundamental knowledge of the underlying build processes, runtime arguments, and `csproj` configurations. When migrating to Linux-based Docker deployments or configuring CI/CD YAML pipelines, they are completely paralyzed. **The Fix**: Master the `dotnet CLI`. Understand how to execute `dotnet publish`, configure environment variables natively, and explicitly containerize the app via Dockerfiles without relying on IDE GUI wizards.
2. **LINQ-to-SQL Performance Disasters (Client-Side Evaluation)**: LINQ is incredibly expressive. However, if a developer writes an overly complex LINQ query spanning 5 deeply nested tables with complex mathematical string manipulations, Entity Framework Core might fail to translate it into a valid SQL query. Historically, EF would silently pull the *entire* table into Application RAM and filter it there (Client-Side Evaluation), causing instant Out-Of-Memory exceptions. **Rule**: Always profile the generated SQL output in the console. For hyper-complex reporting queries or massive joins, abandon LINQ and execute Raw SQL (`FromSqlRaw`) or utilize Dapper (a Micro-ORM).

---

## Layer 6: Cheatsheet

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>
Tổng hợp cấu trúc chuẩn xác nhất của một ứng dụng ASP.NET Core Minimal API (Cú pháp hiện đại).
</details>

### Server Setup (Minimal APIs in .NET 6+)
Microsoft introduced Minimal APIs to remove the heavy Controller boilerplate, making it look as clean as Node.js/Express.

```csharp
// Program.cs (The entire entry point)
using Microsoft.EntityFrameworkCore;
using MyApi.Data;
using MyApi.Models;

var builder = WebApplication.CreateBuilder(args);

// 1. Dependency Injection Setup (Connecting Database)
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultDB")));

var app = builder.Build();

// 2. ROUTING (Minimal API approach)
// GET ALL
app.MapGet("/api/users", async (AppDbContext db) => {
    // Entity Framework handles the SQL automatically
    return await db.Users.ToListAsync();
});

// GET ONE (With URL Params)
app.MapGet("/api/users/{id}", async (int id, AppDbContext db) => {
    var user = await db.Users.FindAsync(id);
    return user is not null ? Results.Ok(user) : Results.NotFound();
});

// POST (Create)
app.MapPost("/api/users", async (User newUser, AppDbContext db) => {
    db.Users.Add(newUser);
    await db.SaveChangesAsync(); // Commits transaction to DB
    return Results.Created($"/api/users/{newUser.Id}", newUser);
});

// Run the Server
app.Run();
```

### Entity Framework Core (The Database Mapping)
```csharp
namespace MyApi.Models;

// 1. The Entity Class (Maps directly to a SQL Table)
public class User
{
    public int Id { get; set; } // Auto-Increment Primary Key
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}

// 2. The DbContext (The Bridge between C# and the Database)
namespace MyApi.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    // This property represents the exact 'Users' table in SQL
    public DbSet<User> Users { get; set; }
}
```

### Modern C# Syntax Features (LINQ & Records)
```csharp
using System;
using System.Linq;
using System.Collections.Generic;

// 'record' is a modern C# feature for creating immutable DTOs instantly
public record UserDto(int Id, string Name);

public class Program
{
    public static void Main()
    {
        var users = new List<User> {
            new User { Id = 1, Name = "Alice", Age = 25 },
            new User { Id = 2, Name = "Bob", Age = 17 }
        };

        // LINQ: Extremely elegant data manipulation
        var adultDtos = users
            .Where(u => u.Age >= 18)        // Filter
            .OrderBy(u => u.Name)           // Sort
            .Select(u => new UserDto(u.Id, u.Name)) // Map to DTO
            .ToList();
    }
}
```

---

## Related Topics

- For a structurally identical, strictly typed OOP ecosystem, compare with **[Spring Boot (Java)](./spring-boot.md)**.
- For high-performance backend alternatives outside the Microsoft ecosystem, see **[Go](./go.md)**.
- To understand the database layer EF Core interacts with, see **[PostgreSQL](../databases/postgresql.md)**.
