# WebSocket STOMP Scaling

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

> **Tóm tắt**: Thiết kế kiến trúc mở rộng ngang (horizontal scaling) cho các kết nối WebSockets thời gian thực bằng cách sử dụng giao thức STOMP trên WebSockets kết hợp với Redis Pub/Sub (hoặc RabbitMQ) làm backplane trong Spring Boot.

</details>

> **Summary**: Architecting horizontal scaling for real-time WebSockets using STOMP over WebSockets and a Redis Pub/Sub backplane in Spring Boot.

---

## ELI5 (Explain Like I'm 5)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Tưởng tượng công ty bạn có 2 tòa nhà (Server 1 và Server 2).
- Nhân viên A ngồi ở Tòa 1. Nhân viên B ngồi ở Tòa 2.
- WebSockets giống như việc mỗi nhân viên nối một sợi dây điện thoại cố định (stateful) vào tòa nhà của mình.
- Nhân viên A nói: "Gửi tin nhắn cho B". Tòa nhà 1 không biết B là ai vì B cắm dây ở Tòa 2. Kết quả: Tin nhắn bị rớt!
- **Giải pháp (Backplane)**: Xây một cái Loa Phóng Thanh trung tâm (Redis Pub/Sub). Khi Tòa 1 nhận tin nhắn từ A, nó đọc lên Loa Phóng Thanh. Tòa 2 nghe được từ Loa, lập tức truyền vào dây điện thoại của B. Thế là A và B chat được với nhau dù ngồi ở 2 máy chủ khác nhau!

</details>

Imagine your company has 2 buildings (Server 1 and Server 2).
- Employee A sits in Building 1. Employee B sits in Building 2.
- WebSockets are like each employee plugging a physical landline cord (stateful) into their respective building.
- Employee A says: "Send a message to B". Building 1 doesn't know who B is because B plugged their cord into Building 2. Result: Message dropped!
- **Solution (Backplane)**: Build a central Megaphone (Redis Pub/Sub). When Building 1 gets a message from A, it shouts it into the Megaphone. Building 2 hears the Megaphone and immediately passes the message down B's landline. Now A and B can chat even though they are on different servers!

---

## Layer 1: What is it? (What)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**Mở rộng WebSocket STOMP** là mô hình kiến trúc bắt buộc để phân tán hàng chục ngàn kết nối WebSocket qua nhiều máy chủ (backend instances).
- **WebSocket**: Giao thức mạng cho phép kết nối 2 chiều liên tục.
- **STOMP**: Giao thức tin nhắn chạy trên nền WebSocket, giúp định tuyến (routing) tin nhắn dễ dàng như gửi mail (Gửi vào `/topic/chat`).
- **Redis Pub/Sub (hoặc RabbitMQ)**: Đóng vai trò là hệ thống thần kinh trung ương (Backplane) kết nối tất cả các máy chủ độc lập lại với nhau.

**Phân loại:**
- **Loại**: Kiến trúc Backend / Hệ thống thời gian thực.
- **Giao thức**: STOMP trên nền WebSocket (ws:// hoặc wss://).
- **Cơ chế mở rộng**: Pub/Sub Message Broker.

</details>

**WebSocket STOMP Scaling** refers to the architectural pattern required to distribute stateful WebSocket connections across multiple backend instances.
- **WebSocket**: The TCP-based protocol for full-duplex communication.
- **STOMP (Simple Text Oriented Messaging Protocol)**: A sub-protocol layered over WebSockets to provide routing mechanisms (publish/subscribe semantics).
- **Redis Pub/Sub (or RabbitMQ)**: The centralized message broker (backplane) that connects all stateless backend instances.

### Classification
- **Type**: Backend Architecture / Real-time systems.
- **Protocol**: STOMP over WebSocket (ws:// or wss://).
- **Scaling Mechanism**: Pub/Sub Message Broker.

---

## Layer 2: Why does it exist? (Why)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Các request HTTP REST thông thường là **không lưu trạng thái (stateless)**. Load balancer có thể ném request cho bất kỳ máy chủ nào xử lý.
Nhưng WebSockets là **lưu trạng thái (stateful)**. Khi client kết nối, nó tạo ra một đường ống cố định (TCP) nối thẳng vào MỘT máy chủ duy nhất.

**Vấn đề khi mở rộng (Scaling):**
1. **User A** kết nối vào **Server 1**.
2. **User B** kết nối vào **Server 2**.
3. User A gửi tin nhắn chat cho User B.
4. **Server 1** nhận tin nhắn nhưng nó không hề kết nối với User B. Tin nhắn bị vứt bỏ.

Để sửa lỗi này, **Server 1** phải chuyển tiếp tin nhắn đó vào một bộ não trung tâm (Redis hoặc RabbitMQ), bộ não này sẽ phát loa báo cho **Server 2** biết để đẩy tin nhắn xuống cho User B.

</details>

Standard REST HTTP requests are **stateless**. Load balancers can route any HTTP request to any server.
WebSockets are **stateful**. A client establishes a persistent TCP connection to a specific physical server instance.

### The Scaling Problem
1. **User A** connects to **Server Node 1**.
2. **User B** connects to **Server Node 2**.
3. User A sends a chat message intended for User B.
4. **Node 1** receives the message but does not have a WebSocket connection to User B. The message is dropped.

To fix this, **Node 1** must forward the message to a central nervous system (Redis or RabbitMQ) so that **Node 2** can receive it and push it to User B.

---

## Layer 3: Without vs. With Comparison (Compare)

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Không có Backplane: Spring Boot dùng RAM cục bộ (In-Memory Broker) để nhớ xem ai đang kết nối. Nếu bạn chạy 2 server, User A và User B bị cô lập hoàn toàn.
Có Backplane: Spring Boot cấu hình `StompBrokerRelay` chỉ thẳng vào RabbitMQ/Redis. Không lưu RAM nữa, mọi tin nhắn đều ném vào Broker. Scale 100 server vẫn chạy mượt.

</details>

### Without a Broker Backplane (Single Instance Only)
```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // Uses in-memory broker. Will break immediately if deployed to >= 2 instances.
        config.enableSimpleBroker("/topic", "/queue");
        config.setApplicationDestinationPrefixes("/app");
    }
}
```

### With a Redis/RabbitMQ Backplane (Horizontally Scalable)
```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // All WebSocket nodes connect to a central RabbitMQ/Redis instance
        config.enableStompBrokerRelay("/topic", "/queue")
              .setRelayHost("rabbitmq-service")
              .setRelayPort(61613)
              .setClientLogin("guest")
              .setClientPasscode("guest");
        config.setApplicationDestinationPrefixes("/app");
    }
}
```

| Aspect | In-Memory Simple Broker | STOMP Relay (RabbitMQ/Redis) |
|---|---|---|
| Horizontal Scaling | Impossible (State is locked to 1 node) | Seamlessly scalable |
| Memory Usage | High (Server stores all subscriptions) | Low (Offloaded to external broker) |
| Message Routing | Basic | Advanced (Topic routing, dead-lettering) |
| Infrastructure Complexity| Low | High (Requires external broker setup) |

---

## Layer 4: Common Use Cases

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

1. **Ứng dụng Chat (Zalo/Messenger)**: Gửi tin nhắn 1-1 hoặc Group Chat cho hàng triệu user phân tán ở khắp các cụm Server.
2. **Sàn giao dịch chứng khoán/Coin**: Bắn giá real-time cho toàn bộ người dùng đang mở app (Dùng Pub/Sub Fanout cực kỳ hiệu quả).
3. **Chỉnh sửa tài liệu chung**: Hiển thị con trỏ chuột của người khác như Google Docs.
4. **Thông báo trực tiếp (Live Notifications)**: Hiện popup "Bạn có đơn hàng mới" ngay lập tức mà không cần F5.

**Không nên làm**:
- Dùng WebSockets để gửi form hoặc lấy dữ liệu thông thường. WebSocket rất tốn tài nguyên và khó scale, hãy dùng REST HTTP bình thường.
- Dùng kỹ thuật Polling (gọi API liên tục mỗi giây) cho 100,000 user. Nó sẽ đánh sập Database của bạn. Lúc này BẮT BUỘC phải dùng WebSockets.

</details>

1. **Real-time Chat Applications**: Sending 1-to-1 or group messages across thousands of users connected to different nodes.
2. **Live Trading Platforms**: Broadcasting stock ticker updates to millions of clients simultaneously (Pub/Sub fanout).
3. **Collaborative Editing**: Google Docs style real-time cursor updates.
4. **Live Notifications**: Sending targeted toast notifications to specific users when events occur in the backend.

### Anti-Patterns
- **Using WebSockets for standard CRUD**: WebSockets add massive infrastructure complexity. Do not use them for standard forms or data fetching; use standard HTTP REST.
- **Polling instead of WebSockets at scale**: Having 100,000 clients poll a REST endpoint every 1 second will destroy your database. Use WebSockets.

---

## Layer 5: Deep Practice

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

**1. Vấn đề bảo mật (Authentication)**:
Không truyền JWT qua Header của HTTP khi mở WebSocket vì trình duyệt không hỗ trợ. Thay vào đó, nhét JWT vào Header của bản tin STOMP `CONNECT` đầu tiên. Backend dùng `ChannelInterceptor` để bắt lấy, giải mã JWT và gán user đó vào Session.

**2. Rớt kết nối tĩnh lặng (Silent Drop)**:
Nginx (Load Balancer) tự động ngắt các kết nối không có dữ liệu trao đổi trong 60 giây. Bắt buộc phải bật tính năng Heartbeat (Ping/Pong) của STOMP (Client gửi Ping mỗi 20s) để giữ kết nối luôn sống.

**3. Giới hạn tài nguyên (File Descriptors)**:
Mỗi kết nối WebSocket ăn 1 File Descriptor trên hệ điều hành Linux. Nếu server có 100,000 user, Linux sẽ cạn kiệt tài nguyên (lỗi `Too many open files`). Bạn phải cấu hình lại `ulimit -n` trên Linux lên con số vài trăm ngàn.

</details>

### Best Practices
1. **Use Load Balancer Sticky Sessions**: While not strictly required for STOMP, using sticky sessions prevents the initial WebSocket HTTP handshake from failing if the Load Balancer routes the upgrade request to a different node.
2. **Authentication via Tokens**: Do not use HTTP Cookies for WebSocket auth. Pass a JWT token in the initial STOMP `CONNECT` frame header, and intercept it using a `ChannelInterceptor` in Spring Boot.
3. **Connection Limits**: Configure maximum connection limits and idle timeouts at the Load Balancer layer (e.g., Nginx, AWS ALB) to prevent zombie connections from exhausting server file descriptors.
4. **Targeted Messaging**: Use `SimpMessagingTemplate.convertAndSendToUser()` to route messages to specific users. Spring maps the username to specific session IDs automatically.

### Common Pitfalls
1. **Nginx Connection Drops**: By default, Nginx drops idle WebSocket connections after 60 seconds (`proxy_read_timeout`). You must implement Heartbeats (Ping/Pong) in STOMP to keep the connection alive.
2. **Memory Leaks**: If clients disconnect ungracefully (e.g., losing internet), the server might keep the session alive in memory. Ensure proper disconnected event listeners (`SessionDisconnectEvent`) clean up resources.
3. **Message Ordering**: In a distributed setup, message ordering is not strictly guaranteed. If ordering is critical, include a timestamp or sequence number in the payload for the client to sort.

---

## Layer 6: Code Templates & Integration

<details>
<summary>🇻🇳 <b>Hiển thị bản dịch Tiếng Việt</b></summary>
<br>

Cấu hình Spring Boot kết nối RabbitMQ làm Broker, đồng thời tích hợp bộ lọc bảo mật JWT. Khi Client kết nối, nó truyền token `Bearer ...` vào header. Hệ thống móc lấy token, xác thực và lưu user vào Session.

</details>

### Securing WebSockets with JWT (Spring Boot)

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.config.ChannelRegistration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.messaging.support.MessageHeaderAccessor;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import java.util.List;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketSecurityConfig implements WebSocketMessageBrokerConfigurer {

    private final JwtService jwtService;

    public WebSocketSecurityConfig(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws-connect")
                .setAllowedOriginPatterns("*")
                .withSockJS(); // Fallback mechanism
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableStompBrokerRelay("/topic", "/queue") // Use RabbitMQ/ActiveMQ for scaling
                .setRelayHost("broker.internal")
                .setRelayPort(61613);
        registry.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        registration.interceptors(new ChannelInterceptor() {
            @Override
            public Message<?> preSend(Message<?> message, MessageChannel channel) {
                StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);
                
                // Intercept the initial CONNECT frame
                if (StompCommand.CONNECT.equals(accessor.getCommand())) {
                    List<String> authorization = accessor.getNativeHeader("Authorization");
                    
                    if (authorization != null && !authorization.isEmpty()) {
                        String token = authorization.get(0).replace("Bearer ", "");
                        
                        // Validate JWT and set User Principal
                        if (jwtService.isValid(token)) {
                            String username = jwtService.extractUsername(token);
                            var auth = new UsernamePasswordAuthenticationToken(username, null, List.of());
                            accessor.setUser(auth);
                        } else {
                            throw new IllegalArgumentException("Invalid JWT Token");
                        }
                    }
                }
                return message;
            }
        });
    }
}
```

---

## Related Topics

- [Kafka vs RabbitMQ at Scale](../04-distributed-async/kafka-vs-rabbitmq-at-scale.md) — Comparing brokers to use as your WebSocket backplane.
- [Advanced Redis Patterns](../03-high-performance-data/advanced-redis-patterns.md) — Using Redis Pub/Sub as an alternative to RabbitMQ.
