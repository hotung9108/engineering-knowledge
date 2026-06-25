# YAGNI Principle (You Aren't Gonna Need It)

> A foundational software engineering principle from Extreme Programming (XP) that states developers should not add functionality until it is deemed necessary.

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**YAGNI (Bạn sẽ không cần đến nó đâu)** là một nguyên tắc cơ bản trong kỹ nghệ phần mềm xuất phát từ Extreme Programming (XP). Nguyên tắc này chỉ ra rằng lập trình viên không nên thêm bất kỳ tính năng hay chức năng nào vào mã nguồn cho đến khi điều đó thực sự cần thiết.

Việc dự đoán tương lai và viết code "phòng hờ" thường dẫn đến mã nguồn phức tạp, lãng phí thời gian và khó bảo trì. Bạn chỉ nên tập trung giải quyết đúng vấn đề hiện tại thay vì xây dựng những hệ thống khổng lồ cho những trường hợp có thể không bao giờ xảy ra.

</details>

---

## 1. What is it? (What)

**YAGNI (You Aren't Gonna Need It)** is a principle of Extreme Programming (XP) that advises against adding code, features, or architectural complexity based on presumed future needs. 

### Classification
- **Type**: Software Engineering / Agile Principle.
- **Origin**: Extreme Programming (XP) methodology.
- **Core Philosophy**: Always implement things when you actually need them, never when you just foresee that you need them.

---

## 2. Why does it exist? (Why)

Developers often fall into the trap of speculative generalization—building frameworks, adding extra parameters, or designing database tables for features they "might need later." YAGNI exists to combat:

- **Wasted Time**: Time spent building unused features is time stolen from delivering actual business value.
- **Maintenance Burden**: Every line of code must be tested, reviewed, and maintained. Unused code is a liability.
- **Design Complexity**: Premature abstractions make the codebase harder to understand and adapt when actual requirements change.
- **Wrong Guesses**: When the future requirement actually arrives, the preemptively built solution is often wrong anyway because business needs shift.

---

## 3. Without vs. With Comparison (Compare)

### Without YAGNI (Speculative Design)

```java
// Adding multiple layers of abstraction for a simple file export
public interface Exporter {
    void export(String data);
}

// Developer thinks: "We only need CSV now, but maybe we will need PDF, XML, and JSON later! I will build them all."
public class CsvExporter implements Exporter { /* ... */ }
public class PdfExporter implements Exporter { /* ... */ } // Never used
public class XmlExporter implements Exporter { /* ... */ } // Never used

public class ExportFactory {
    public static Exporter getExporter(String type) {
        if (type.equals("CSV")) return new CsvExporter();
        if (type.equals("PDF")) return new PdfExporter(); // Dead code
        if (type.equals("XML")) return new XmlExporter(); // Dead code
        throw new IllegalArgumentException("Unknown type");
    }
}
```

### With YAGNI (Lean Implementation)

```java
// Just implement exactly what is needed today
public class CsvExporter {
    public void export(String data) {
        // Implementation for CSV export
    }
}
// When (and IF) PDF is requested, THEN we refactor to an interface and factory.
```

| Aspect | Without YAGNI | With YAGNI |
|---|---|---|
| Development Time | High (building "what ifs") | Low (building what is needed) |
| Codebase Size | Bloated | Lean and focused |
| Refactoring Effort | Hard (entangled speculative code) | Easy (simple, direct code) |
| Business Alignment | Low (building unrequested features) | High (delivering immediate value) |

---

## 4. Common Use Cases

### When to apply YAGNI
1. **Feature Implementation**: A stakeholder asks for a simple text field; do not build a rich text editor "just in case."
2. **Database Design**: Do not add extra columns or tables for features that are only in the "ideas" phase.
3. **Abstractions and Interfaces**: Do not extract interfaces or base classes if there is only one implementation.
4. **Library Selection**: Do not install heavy enterprise frameworks if a lightweight library solves the current problem.
5. **Infrastructure**: Do not provision a Kubernetes cluster if a single VPS is sufficient for the current load.

### When NOT to apply YAGNI (Anti-patterns)
- **Security**: "We aren't gonna need input sanitization yet." (Security must be built-in from day one).
- **Core Architecture Constraints**: Choosing a NoSQL database when you know the data is highly relational, just because it's "easier to set up right now."
- **Testing**: "We aren't gonna need unit tests until we launch." (Testing is a fundamental practice, not a speculative feature).

---

## 5. Deep Practice — Real-world Experience

### Best Practices
1. **Refactor mercilessly**: YAGNI relies heavily on the ability to refactor later. If you keep the code clean and simple now, it will be easy to extend when the time comes.
2. **Focus on the present**: Only write code that is required to pass the current sprint's acceptance criteria.
3. **Use the "Rule of Three"**: Don't extract a reusable component or abstraction until you have duplicated the code three times.
4. **Delete dead code**: If you find speculative code that is currently unused, delete it. It lives in source control history if you ever need it.
5. **Challenge requirements**: If a feature seems overly complex, ask stakeholders if a simpler version delivers 80% of the value.

### Common Pitfalls
1. **Confusing YAGNI with Technical Debt**: Writing messy, unmaintainable code and claiming "YAGNI" is a misuse of the principle. The code must still be clean and well-tested.
2. **Over-abstracting early**: Building complex generic functions before having concrete use cases.
3. **Fear of rewriting**: Developers over-engineer because they fear touching the code again. Cultivate a culture where refactoring is safe and routine.
4. **Ignoring known imminent requirements**: If a feature is definitively scheduled for the next sprint, it is acceptable to leave a small architectural hook for it (though still risky).
5. **Database schema rigidity**: It can be hard to change schemas later. Use migrations (e.g., Flyway, Liquibase) to make database evolution painless, enabling YAGNI for data.

---

## 6. Code Templates & Integration

### Progressive Refactoring (The YAGNI Approach)

**Step 1: The simple requirement (Current Need)**
```typescript
interface User {
    id: string;
    isActive: boolean;
    role: string;
}

// Requirement: Filter active users
export function getActiveUsers(users: User[]): User[] {
    return users.filter(u => u.isActive);
}
```

**Step 2: A new requirement arrives (Future Need Becomes Current)**
```typescript
// New Requirement: Now we also need to filter by role
// We refactor to a more generic approach ONLY when needed

type FilterPredicate = (user: User) => boolean;

export function filterUsers(users: User[], predicate: FilterPredicate): User[] {
    return users.filter(predicate);
}

// Usage:
// const activeUsers = filterUsers(users, u => u.isActive);
// const adminUsers = filterUsers(users, u => u.role === 'ADMIN');
```

---

## Related Topics

- [Clean Code](./clean-code.md) — The foundation that makes YAGNI possible through easy refactoring.
- [SOLID Principles](./solid-principles.md) — How to balance YAGNI with the Open/Closed Principle.
- [Design Patterns](./design-patterns.md) — Patterns to apply *when the need arises*, not before.
