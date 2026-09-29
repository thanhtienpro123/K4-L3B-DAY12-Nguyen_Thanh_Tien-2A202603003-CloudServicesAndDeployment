# Thông Tin Deploy — Checkpoint 5

> Phương án dự phòng được chọn vì môi trường hiện tại không có quyền truy cập cloud provider hoặc không thể đăng ký tài khoản cho deploy thực tế. Theo quy định lab, `LOCAL_FALLBACK=true` sẽ kích hoạt kiểm tra trên Docker local.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Nguyễn Thành Tiến |
| Mã học viên | 2A202603003 |
| Repo | https://github.com/your-user/K4-L3B-DAY12-Nguyen_Thanh_Tien-2A202603003-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | http://localhost:8000 |
| Platform | Railway / Render fallback via Docker Compose (local fallback because cloud access was unavailable) |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set

Ghi tên biến và nguồn giá trị, không ghi giá trị secret:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | local Docker Compose dùng 8000 |
| `AGENT_API_KEY` | ✅ | đặt trong file `.env` cho local fallback, không commit vào repo |
| `REDIS_URL` | ✅ | Redis service `redis` trong Docker Compose |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |
| `LOCAL_FALLBACK` | ✅ | true |

## Lệnh Kiểm Tra

```bash
# 1. Liveness — mong đợi 200 {"status":"ok"}
curl -i http://localhost:8000/health

# 2. Readiness — mong đợi 200 {"status":"ready"}
curl -i http://localhost:8000/ready

# 3. Không có API key — mong đợi 401
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# 4. Có API key — mong đợi 200 kèm câu trả lời
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AGENT_API_KEY" \
  -H "X-User-Id: sv-test" \
  -d '{"question":"Deploy là gì?"}'
```

## Kết Quả Chạy Thật

```text
HTTP/1.1 200 OK
{"status":"ok","service":"day12-agent","version":"1.0.0"}

HTTP/1.1 200 OK
{"status":"ready","redis":true}

HTTP/1.1 401 Unauthorized
{"detail":"invalid or missing API key"}
```

## Ảnh Chụp Màn Hình

Ảnh đã lưu trong thư mục `screenshots/`:

- `screenshots/dashboard.png`
- `screenshots/health.png`

---

## Lý Do Dùng Phương Án Dự Phòng

Không khả dụng để đăng ký hoặc truy cập nền tảng cloud từ môi trường hiện tại. Vì vậy ứng dụng được chạy local bằng Docker Compose, với Redis service trong mạng Compose và health/readiness được kiểm tra bằng curl từ máy chủ local. Đây là phương án fallback cho phép nộp bài nhưng tối đa 60% điểm theo quy định của lab.
