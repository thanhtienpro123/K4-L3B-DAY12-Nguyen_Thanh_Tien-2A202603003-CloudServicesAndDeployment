# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng placeholder bên dưới từng câu bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Nguyễn Thành Tiến Mã học viên: 2A202603003

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

Nếu deploy lên server mới mà quên cấu hình `AGENT_API_KEY`, app sẽ dừng ngay khi khởi động và báo thiếu cấu hình. Nhờ vậy mình biết phải sửa secret trước khi nhận traffic. Nếu mặc định là `changeme`, app vẫn chạy và có thể vô tình cho người khác dùng một khóa dễ đoán.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

Ví dụ log JSON từ một lần gọi `/ask`:

```json
{"event": "ask_completed", "level": "info", "timestamp": "2026-09-29T10:07:16.444621+00:00", "user_id": "sv-test", "tokens_in": 4, "tokens_out": 36, "cost_usd": 2.22e-05}
```

Từ các trường có cấu trúc, mình có thể lọc request theo `user_id` hoặc `event`, và cộng tổng token/chi phí để theo dõi mức sử dụng. Một câu `print("đã trả lời xong")` không có trường để lọc hay tổng hợp tự động.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1,727.9 MB |
| Multi-stage | 288.4 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

Mình build Dockerfile 1-stage ban đầu lấy từ Git và Dockerfile multi-stage hiện tại trên cùng build context. Số đo lấy từ Docker image metadata (bytes đổi sang MB thập phân); bản 1-stage lớn hơn khoảng 1,439.5 MB. Phần lớn chênh lệch đến từ base image `python:3.11` đầy đủ ở bản đầu so với `python:3.11-slim` ở runtime multi-stage; multi-stage chỉ đưa dependencies và source cần chạy vào image cuối, không đưa nguyên stage builder vào.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

Khi chỉ sửa `app/main.py`, layer cài dependencies vẫn dùng cache vì `requirements.txt` không đổi. Các layer tạo user và copy dependencies sang runtime cũng có thể dùng lại; layer `COPY app ./app` phải chạy lại vì source đổi. `COPY utils ./utils` không đổi nên có thể dùng cache riêng. Nếu đưa `COPY . .` lên trước `pip install`, sửa một file bất kỳ cũng làm layer copy đổi, khiến bước cài dependencies phía sau phải chạy lại.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

Nếu tiến trình trong container chạy bằng root, khai thác được lỗ hổng Python có thể cho kẻ tấn công quyền root bên trong container; nếu tiếp tục khai thác lỗi cấu hình hoặc lỗ hổng container/kernel thì rủi ro ảnh hưởng host tăng lên. `USER app` giảm quyền của tiến trình ngay từ đầu, nên kẻ tấn công không mặc nhiên có quyền root trong container. Đây là giảm thiểu rủi ro, không thay thế việc vá lỗi hay cô lập container.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

Với giới hạn 10 request/phút theo phút đồng hồ, có thể gửi 10 request ngay trước mốc chuyển phút, rồi thêm 10 request ngay sau mốc đó. Như vậy có 20 request trong khoảng xấp xỉ 2 giây mà cả hai nhóm vẫn nằm trong hai phút lịch khác nhau. Sliding window tránh lỗ hổng này vì luôn đếm 60 giây gần nhất.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

Rate limit giới hạn số request trong một khoảng thời gian; cost guard giới hạn tổng tiền của user trong tháng. Nếu user còn quota request nhưng đã dùng hết ngân sách tháng, rate limit vẫn cho qua còn cost guard chặn với HTTP 402. Ngược lại, user có thể còn nhiều ngân sách nhưng gửi request vượt giới hạn trong 60 giây; rate limiter chặn với HTTP 429 dù cost guard vẫn cho phép.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

Đầu tiên Redis mất kết nối nên probe kiểm tra Redis trên cả ba container đều thất bại. Nếu endpoint chung được dùng làm readiness, orchestrator đánh dấu cả ba instance không sẵn sàng và ngừng gửi traffic tới chúng. Nếu cũng dùng kết quả đó làm liveness, nó còn restart cả ba container dù tiến trình ứng dụng vẫn sống; Redis vẫn lỗi nên các container lại fail probe, gây restart lặp và kéo dài gián đoạn. Tách `/health` khỏi Redis giúp liveness vẫn đạt, còn `/ready` chỉ tạm ngừng nhận traffic.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

Với Redis dùng chung, mỗi request đọc lịch sử do replica trước ghi nên `history_length` trước lượt mới tăng theo 0, 2, 4, ... (mỗi lượt thêm một message user và một message assistant). Nếu lưu trong dict Python, mỗi container có dict riêng; request chuyển sang replica khác có thể lại thấy lịch sử ngắn hoặc bằng 0. Khi thử scale bằng Compose, cấu hình hiện tại cùng publish host port 8000 cho từng replica nên lệnh scale gặp xung đột port; vì vậy đây là kết quả mong đợi theo thiết kế, chưa phải số đo quan sát được từ ba replica chạy đồng thời.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

Mình chưa deploy lên cloud vì môi trường không có quyền truy cập hoặc khả năng đăng ký platform, nên không có lỗi deploy cloud thật để ghi. Khi kiểm tra phương án local, có lần `curl` ngay sau `docker compose up -d` báo `Empty reply from server`; `docker compose ps` cho thấy agent còn ở trạng thái `health: starting`. Mình xem log container, xác nhận Uvicorn khởi động và health check nội bộ trả 200, sau đó chạy lại CP5 trên stack đã ổn định và nhận 8 passed, 5 skipped. Đây là sự cố lúc kiểm tra local, không phải lỗi cloud; phương án cloud vẫn cần được thử riêng.
