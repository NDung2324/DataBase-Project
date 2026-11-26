# Mini-Netflix Phase 4 — Client Demo (Flask + MySQL)

Dự án giữ nguyên 9 bảng MySQL của Phase 3, không thêm bảng hay vai trò admin.

## Các chức năng
- Đăng nhập bằng `username` và `password` đã có trong bảng `users`.
- My Profiles: chỉ hiện profile của user đang đăng nhập; tạo profile tự gắn đúng user (trigger kiểm tra giới hạn).
- Chọn profile, xem Movies, TV Series → Season → Episode.
- Xem nội dung **mô phỏng**: mỗi 1 giây thực = 1 phút phim. Bấm `Stop & Lưu Watch History` để Flask tự INSERT vào MySQL. Không phát video thật.
- My Watch History: chỉ xem lịch sử của profile đang chọn.
- My Subscriptions: chỉ xem gói của tài khoản đang đăng nhập.

## Chạy trên Windows
1. File `.env` trên máy này đã chọn `DB_NAME=mini_netflix_check`. Mật khẩu MySQL được lưu riêng trong file này.
2. Bấm đúp **CHAY_WEB.bat**. Chương trình kiểm tra MySQL rồi mở `http://127.0.0.1:5000/login`.
3. Giữ cửa sổ chương trình mở trong lúc dùng web. Nhấn **Ctrl+C** trong cửa sổ đó để dừng.
4. Nếu chưa biết tài khoản website, bấm **XEM_TAI_KHOAN_MAU.bat** để xem tài khoản mẫu đang có profile và gói ACTIVE còn hiệu lực.
5. Login → My Profiles → chọn profile → Movies hoặc TV Series → chọn nội dung → Play → Dừng và lưu tiến độ → My History.

Các nút hỗ trợ:
- **KIEM_TRA_DATABASE.bat**: kiểm tra kết nối, số dòng của 9 bảng và hai trigger.
- **MO_CAU_HINH.bat**: mở `.env` bằng Notepad để sửa thông tin MySQL.
- **CAI_DAT_MOI_TRUONG.bat**: tạo hoặc sửa môi trường Python riêng và cài `requirements.txt`. Ưu tiên Python đã cài; trên máy có Codex có thể dùng runtime đi kèm.

Nếu chuyển project sang máy khác, cài MySQL và nạp database trước, chép `.env.example` thành `.env`, điền mật khẩu MySQL của máy đó rồi chạy `CAI_DAT_MOI_TRUONG.bat`. Các lệnh thủ công vẫn dùng được:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_local.py
```

## Chuẩn bị dữ liệu để thử
Phải có user mà bạn **biết mật khẩu** và có subscription `ACTIVE` hợp lệ theo ngày hiện tại:
```sql
SELECT u.user_id, u.username, s.status, s.start_date, s.end_date,
       sp.plan_name
FROM users u
JOIN subscription s ON s.user_id=u.user_id
JOIN subscription_plan sp ON sp.plan_id=s.plan_id
WHERE s.status='ACTIVE' AND s.start_date<=CURDATE()
  AND (s.end_date IS NULL OR s.end_date>=CURDATE())
LIMIT 20;
```
Nếu không biết mật khẩu tài khoản mẫu, chỉ dùng tài khoản thử nghiệm và đặt mật khẩu thử trong Workbench, ví dụ:
```sql
UPDATE users SET password='demo123' WHERE user_id='USER_ID_THAT';
```
Lệnh trên thay đổi DB thật: chỉ dùng cho tài khoản kiểm thử và backup dữ liệu trước.

## Kiểm tra MySQL sau khi xem
```sql
SELECT w.watch_history_id, p.profile_name, c.title, w.watch_duration, w.completed
FROM watch_history w
JOIN profile p ON p.profile_id=w.profile_id
JOIN content c ON c.content_id=w.content_id
ORDER BY w.watch_history_id DESC LIMIT 30;
```
`watch_history_id` dùng UUID dạng `WHxxxxxxxxxxxxxx` nên sắp xếp theo ID **không tương ứng thời điểm tạo**. Schema hiện tại không có `watched_at`.

## Giới hạn quan trọng
- Chỉ demo trên `localhost`, **không public** bản dùng mật khẩu plaintext hoặc dùng tài khoản root MySQL.
- Trang Plans có thể kích hoạt gói mô phỏng trong một tháng; không tích hợp thanh toán thật.
- Trình xem chỉ là **mô phỏng**, thời gian do trình duyệt gửi, không phải hệ thống phát video thật.
- `watch_history` không có timestamp. Tiến độ của lượt chưa hoàn thành được cập nhật; xem lại nội dung đã hoàn thành tạo lượt xem mới. Thứ tự UUID không biểu thị thời điểm tạo.
- Nếu user không có gói ACTIVE còn hiệu lực, website sẽ từ chối xem nội dung. Có thể kiểm tra `start_date`, `end_date` bằng Workbench.
