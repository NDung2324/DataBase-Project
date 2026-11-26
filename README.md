# MiniNetflix Phase 4

README dự án và hướng dẫn cài đặt vận hành

MiniNetflix là ứng dụng minh họa quản lý dịch vụ xem phim bằng Flask và MySQL. Dự án kết nối giao diện web với chín bảng dữ liệu của Phase 3, hỗ trợ tài khoản, profile, gói đăng ký, danh mục phim và lịch sử xem. Trình xem mô phỏng thời gian xem; ứng dụng không phát video thật.

### Thông tin repository và học phần

| Thông tin | Nội dung |
| --- | --- |
| Repository | [NDung2324/DataBase-Project](https://github.com/NDung2324/DataBase-Project) |
| Học phần | Cơ sở dữ liệu  |
| Lớp học phần | E24CQCE02-N |
| Nhóm | Ba chang linh ngu lam |
| Phạm vi | Phase 3 database và Phase 4 Flask client demo |

### Thành viên thực hiện

| Họ và tên | Mã sinh viên | Email sinh viên |
| --- | --- | --- |
| Lê Ngọc Dũng | N24DECE065 | n24dece065@student.ptithcm.edu.vn |
| Lê Phạm Khánh Huy | N24DECE072 | n24dece072@student.ptithcm.edu.vn |
| Phan Giảng Bình | N24DECE056 | n24dece056@student.ptithcm.edu.vn |

### Phân công công việc

| Giai đoạn | Thành viên thực hiện |
| --- | --- |
| Phase 1 | Lê Ngọc Dũng, Lê Phạm Khánh Huy, Phan Giảng Bình |
| Phase 2 | Lê Ngọc Dũng, Lê Phạm Khánh Huy, Phan Giảng Bình |
| Phase 3 | Lê Phạm Khánh Huy, Phan Giảng Bình |
| Phase 4 | Lê Ngọc Dũng, Lê Phạm Khánh Huy, Phan Giảng Bình |

### Công nghệ và chức năng

Python 3.12, Flask, Jinja2, HTML, CSS, JavaScript, MySQL 8.0 và mysql-connector-python. Phiên bản kiểm tra trên máy: Flask 3.1.3, Connector/Python 9.7.0 và MySQL Server 8.0.46.

Người dùng có thể đăng nhập, tìm và chọn profile của mình, tạo profile trong giới hạn gói, xem phim hoặc series theo mùa và tập, kích hoạt gói mô phỏng, lưu tiến độ xem và xem lịch sử của profile đang chọn.

## 1 Mã nguồn và tài liệu trong repository

Cấu trúc đề xuất cho repository gồm mã nguồn Flask, tài nguyên giao diện, database và tài liệu bên dưới. Các thư mục database và docs cần chứa các file tương ứng khi đóng gói bản nộp.

```text
MiniNetflix_Phase4/
  README.md
  app.py
  run_local.py
  requirements.txt
  requirements.lock.txt
  .env.example
  .gitignore
  templates/
  static/
  CHAY_WEB.bat
  CAI_DAT_MOI_TRUONG.bat
  KIEM_TRA_DATABASE.bat
  MO_CAU_HINH.bat
  XEM_TAI_KHOAN_MAU.bat
  kiem_tra_database.py
  tai_khoan_mau.py
  database/
    project.sql
  docs/
    report_phase_3_final.docx
    kiem_thu_validation.sql
    kiem_tra_11_truy_van.sql
    ket_qua_11_truy_van_project1.csv
    ket_qua_kiem_thu_project_sql.json
    README_MiniNetflix_Phase4_da_chinh.docx
```

### Vai trò các thành phần

app.py chứa kết nối MySQL, xác thực, xử lý profile, gói đăng ký và lịch sử xem. templates chứa giao diện Jinja2; static chứa tài nguyên giao diện. run_local.py kiểm tra kết nối, khởi động web và mở trình duyệt. requirements.txt mô tả thư viện cần cài; requirements.lock.txt ghi phiên bản đã dùng trên máy kiểm tra.

project.sql chứa đầy đủ cấu trúc database và dữ liệu mẫu của chín bảng, ba view và hai trigger. Báo cáo Phase 3 trình bày mô hình ER/EER, schema, PK/FK, chuẩn hóa, data dictionary, DDL, DML và truy vấn.

### Cấu hình riêng của máy

Giữ .env ở máy cá nhân; chỉ đưa .env.example không chứa mật khẩu thật vào repository. Không đưa .venv, __pycache__ hoặc các file cấu hình riêng của máy lên repository. Dữ liệu tài khoản trong dump chỉ dùng cho bài tập và demo.

## 2 Cài đặt và nạp database

### Yêu cầu trên máy mới

Cài Python 3.12 có hỗ trợ pip, MySQL Server 8.0 và MySQL Workbench. MySQL Server phải đang chạy. Workbench là công cụ giao diện để kết nối và chạy SQL; Flask dùng MySQL Server để lưu và đọc dữ liệu.

### Nạp file project sql bằng Workbench

1. Mở kết nối MySQL trên máy, thường là 127.0.0.1, cổng 3306. Nhập mật khẩu MySQL đã đặt khi cài máy đó.

2. Chọn Server → Data Import → Import from Self-Contained File. Chọn file database/project.sql trong repository.

3. Chọn Start Import và đợi Import Completed. Mở tab Schemas bên trái rồi bấm Refresh để thấy project1.

4. File dump chứa CREATE DATABASE project1 và USE project1. Vì vậy tên database sau khi nạp là project1; lựa chọn Default Target Schema không đổi tên này. Dump có các lệnh DROP TABLE để khôi phục bảng, nên chỉ nạp vào môi trường demo phù hợp và sao lưu nếu project1 đã có dữ liệu cần giữ.

### Số dòng của file mới trước khi thao tác trên UI

| Bảng | Số dòng trong project.sql | Bảng | Số dòng trong project.sql |
| --- | --- | --- | --- |
| users | 1000 | profile | 2000 |
| content | 1123 | movies | 723 |
| episode | 400 | tv_series | 8 |
| subscription | 1000 | subscription_plan | 3 |
| watch_history | 5000 |  |  |

Cấu trúc còn có ba view và hai trigger. Đây là số liệu đã khôi phục thử từ project.sql ngày 25/11/2026. Sau khi tạo profile, đổi gói hoặc lưu lịch sử bằng UI, số dòng có thể thay đổi.

### Nạp dữ liệu đầy đủ

Chỉ cần nạp project.sql để có toàn bộ cấu trúc và dữ liệu mẫu. Không chạy thêm các file INSERT rời trên cùng database đã nạp đầy đủ vì có thể trùng khóa hoặc làm thay đổi dataset dùng để đối chiếu kết quả.

## 3 Cấu hình và khởi động website

### Tạo file cấu hình

Mở thư mục mã nguồn. Chép .env.example thành .env nếu chưa có. Đặt DB_NAME=project1 và sửa thông tin kết nối theo MySQL của máy đang chạy. Thay các giá trị trong dấu ngoặc nhọn bằng thông tin thực tế.

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=<tai_khoan_mysql>
DB_PASSWORD=<mat_khau_mysql_tren_may>
DB_NAME=project1
FLASK_SECRET_KEY=<chuoi_ngau_nhien_rieng_cua_may>
```

Sau khi nạp project.sql, lưu .env với DB_NAME=project1 rồi khởi động lại website. Nếu .env.example trong mã nguồn còn tên database khác, thay tên đó bằng project1 khi tạo .env. Tài khoản MySQL dùng để kết nối database khác với tài khoản đăng nhập website trong bảng users.

### Chạy nhanh trên Windows

1. Bấm CAI_DAT_MOI_TRUONG.bat để tạo môi trường Python và cài thư viện khi chạy lần đầu hoặc chuyển sang máy khác. run_local.py và các file .bat nêu trong hướng dẫn đã được xác nhận có trong thư mục MiniNetflix_Phase4 ngày 26/11/2026.

2. Bấm KIEM_TRA_DATABASE.bat để kiểm tra kết nối, số dòng các bảng và hai trigger. Nếu báo lỗi, sửa .env bằng MO_CAU_HINH.bat.

3. Bấm CHAY_WEB.bat. Trình duyệt sẽ mở [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login). Giữ chương trình đang chạy trong lúc trình bày; nhấn Ctrl+C trong cửa sổ chạy để dừng.

### Các lệnh cài và chạy thủ công

Mở PowerShell tại thư mục MiniNetflix_Phase4. Nếu máy đã có môi trường .venv hoạt động thì bỏ qua dòng tạo môi trường.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe kiem_tra_database.py
.\.venv\Scripts\python.exe run_local.py
```

Nếu máy không có lệnh py, dùng python -m venv .venv sau khi cài Python và kiểm tra python --version. Có thể dùng requirements.lock.txt thay requirements.txt khi cần cài đúng phiên bản đã kiểm tra.

### Triển khai để trình bày

Bản bàn giao chạy cục bộ trên 127.0.0.1:5000, debug tắt. Mỗi máy thuyết trình cần MySQL, database đã nạp và .env riêng. Bản này chưa có cấu hình triển khai Internet; hướng dẫn trên là quy trình triển khai demo tại máy.

## 4 Vận hành và luồng trình bày

| Bước | Thao tác | Kết quả cần quan sát |
| --- | --- | --- |
| 1 | Mở XEM_TAI_KHOAN_MAU.bat | Xem tài khoản mẫu của dữ liệu hiện tại trên máy. |
| 2 | Đăng nhập website | Vào trang chính bằng tài khoản trong bảng users. |
| 3 | Mở My Profiles và chọn profile | Chỉ hiện profile thuộc tài khoản đang đăng nhập. |
| 4 | Mở Movies hoặc TV Series | Tìm phim; với series chọn mùa và tập. |
| 5 | Mở nội dung và bấm Play | Bộ đếm mô phỏng chạy; 1 giây thực tương ứng 1 phút xem. |
| 6 | Bấm dừng và lưu lịch sử | Tiến độ được gửi về Flask và lưu vào MySQL. |
| 7 | Mở My Watch History | Xem lịch sử của profile vừa chọn. |
| 8 | Mở Plans và My Subscriptions | Xem gói và lịch sử; kích hoạt gói là thao tác mô phỏng. |

### Điều kiện để xem và tạo profile

Tài khoản cần gói ACTIVE còn hiệu lực theo ngày hiện tại để xem nội dung. Việc tạo profile bị giới hạn theo max_profiles của gói. Ba gói trong dữ liệu là FREE, STANDARD và PRO, có giới hạn tương ứng 1, 3 và 5 profile. Kích hoạt gói qua UI tạo thời hạn một tháng và không thu tiền thật.

### Luồng dữ liệu

Trình duyệt gửi yêu cầu tới Flask. Flask kiểm tra phiên đăng nhập, quyền sở hữu profile và dữ liệu đầu vào, sau đó dùng câu SQL có tham số để đọc hoặc ghi MySQL. Database kiểm tra PK, FK, UNIQUE, CHECK, NOT NULL và các trigger trước khi chấp nhận dữ liệu.

Trigger trg_validate_watch_duration chạy trước INSERT vào watch_history để từ chối thời gian xem vượt thời lượng nội dung. Trigger trg_validate_profile_limit chạy trước INSERT vào profile để kiểm tra gói đang hoạt động và số profile tối đa. Trigger INSERT không tự bao phủ mọi trường hợp UPDATE hoặc thao tác đồng thời.

### Xem lại dữ liệu đã lưu

```sql
USE project1;
SELECT w.watch_history_id, p.profile_name, c.title,
       w.watch_duration, w.completed
FROM watch_history w
JOIN profile p ON p.profile_id=w.profile_id
JOIN content c ON c.content_id=w.content_id
WHERE p.profile_id = '<profile_id_vua_chon>';
```

Thay profile_id bằng ID profile thực tế vừa chọn trên UI. ID lịch sử dùng UUID và bảng không có watched_at, nên thứ tự ID không thể hiện thời điểm xem.

## 5 Kiểm tra và kết quả đã xác nhận

Ngày 25/11/2026, project.sql được khôi phục vào database thử riêng. Bộ validation, các truy vấn và kiểm tra tích hợp Flask dùng bản sao này, sau đó bản sao được dọn. Tên database thử chỉ phục vụ kiểm tra; tên database chuẩn trong hướng dẫn cài đặt là project1.

### Kết quả kiểm tra database và giao diện

Khôi phục đủ chín bảng, ba view, hai trigger và CHECK duration &gt; 0. Bộ validation đạt 11/11 PASS: hai trường hợp hợp lệ được nhận và chín trường hợp không hợp lệ bị từ chối đúng cơ chế mong đợi.

Các trường hợp gồm thời gian xem hợp lệ, profile trong giới hạn, thời gian xem vượt nội dung, vượt số profile, thiếu gói ACTIVE, giá âm, thời lượng bằng 0, trùng vị trí tập, FK nội dung không tồn tại, completed NULL và ngày kết thúc trước ngày bắt đầu.

Kiểm tra tích hợp với dump mới đã xác nhận đăng nhập, chọn profile và các trang dashboard, profile, gói, đăng ký, phim, series, lịch sử, trang xem mô phỏng trả về thành công. Bằng chứng được lưu trong docs/ket_qua_kiem_thu_project_sql.json. Đây là kiểm tra bằng Flask test client, không thay thế kiểm tra toàn bộ thao tác trên mọi trình duyệt.

### Số dòng kết quả của 11 truy vấn trên file mới

| STT | Truy vấn | Số dòng |
| --- | --- | --- |
| 1 | Top 10 most watched movies | 10 |
| 2 | Total watch time per profile | 2000 |
| 3 | Profiles without watch history | 300 |
| 4 | Most watched TV series | 8 |
| 5 | Users with active subscriptions | 970 |
| 6 | Nominal active subscription value by plan | 3 |
| 7 | Most popular content categories | 11 |
| 8 | Users who watched more than 5 movies | 145 |
| 9 | Movies longer than the average movie duration | 326 |
| 10 | Most active users by watch time | 10 |
| 11 | Users with above average watch time | 459 |

Bảng trên ghi số dòng thực tế của các truy vấn ngày 25/11/2026; dữ liệu tương ứng nằm trong docs/ket_qua_11_truy_van_project1.csv. Số dòng không chứng minh từng giá trị expected result cũ còn đúng. Các truy vấn có CURDATE phụ thuộc ngày chạy và dữ liệu có thể thay đổi sau thao tác UI; cần xuất lại kết quả khi đổi dataset.

## 6 Tự kiểm tra và xử lý lỗi

### Kiểm tra đúng database và các thành phần

```sql
USE project1;
SELECT DATABASE() AS database_dang_dung;
SHOW FULL TABLES;
SHOW TRIGGERS;
SELECT COUNT(*) AS so_view
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA=DATABASE();
SELECT COUNT(*) AS so_trigger
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA=DATABASE();
```

Kết quả của dump mới trước thao tác demo: 9 bảng dữ liệu, 3 view, 2 trigger. KIEM_TRA_DATABASE.bat in số dòng của cả chín bảng theo database trong .env. Có thể kiểm tra từng bảng bằng SELECT COUNT(*) FROM ten_bang; và đối chiếu bảng số dòng trong phần Cài đặt và nạp database.

Mở docs/kiem_thu_validation.sql trong Workbench rồi chạy toàn bộ file. Bản SQL trong thư mục docs đã dùng USE project1. Bộ kiểm thử tạo procedure phụ, dùng dữ liệu thử trong transaction, rollback dữ liệu thử và xóa procedure phụ. Chạy riêng khi không có transaction đang làm dở. Mở docs/kiem_tra_11_truy_van.sql để chạy 11 truy vấn và xuất kết quả đối chiếu. Cả hai file SQL cần được đưa vào repository cùng dữ liệu kiểm thử đã lưu.

### Các lỗi thường gặp

| Hiện tượng | Cách xử lý |
| --- | --- |
| Access denied hoặc lỗi 1045 | Kiểm tra DB_USER và DB_PASSWORD trong .env; dùng mật khẩu MySQL của chính máy. |
| Unknown database hoặc lỗi 1049 | Nạp dump, Refresh Schemas và đối chiếu DB_NAME; dump mới tạo project1. |
| Không kết nối được hoặc lỗi 2003 | Kiểm tra MySQL Server đang chạy, DB_HOST và DB_PORT. |
| Không tìm thấy Python hoặc thiếu thư viện | Cài Python; chạy CAI_DAT_MOI_TRUONG.bat hoặc các lệnh trong phần Cấu hình và khởi động website. |
| Không đăng nhập được website | Dùng tài khoản mẫu trong users, không dùng mật khẩu root MySQL làm tài khoản web. |
| Bị chặn xem hoặc tạo profile | Kiểm tra gói ACTIVE, ngày hiệu lực và max_profiles. |
| Cổng 5000 đang được dùng | Mở URL của bản đang chạy hoặc dừng phiên chạy cũ rồi khởi động lại. |

### Xử lý lỗi DEFINER khi import

Dump có DEFINER=`root`@`localhost` cho view và trigger. Nếu gặp lỗi 1227 khi import bằng tài khoản khác, hoặc lỗi 1449 vì tài khoản DEFINER không tồn tại, dùng tài khoản quản trị được phép tạo các đối tượng đó hoặc nhờ quản trị viên chuẩn bị bản dump phù hợp. Trên bản sao của file SQL, có thể bỏ riêng thuộc tính DEFINER=`root`@`localhost` để người import trở thành definer mặc định; giữ nguyên phần CREATE, nội dung view/trigger và SQL SECURITY. Không xóa toàn bộ dòng có DEFINER vì dòng đó có thể chứa cả định nghĩa đối tượng. Tài khoản import vẫn phải có quyền tạo bảng, view và trigger. Sau khi nạp, kiểm tra lại đủ ba view, hai trigger và chạy validation.

Tham khảo MySQL 8.0 Stored Object Access Control: https://dev.mysql.com/doc/refman/8.0/en/stored-objects-security.html

### Giới hạn và tài liệu tham khảo

Ứng dụng minh họa dùng mật khẩu dạng văn bản theo dataset, không có phát video thật, thanh toán thật hay vai trò quản trị. Không coi đây là cấu hình sản phẩm công khai. Khi phát triển tiếp cần lưu mật khẩu bằng hash, tài khoản database phù hợp, máy chủ triển khai chuyên dụng và kiểm tra quyền cùng thao tác đồng thời.

Tài liệu chính thức: Flask Installation — https://flask.palletsprojects.com/en/stable/installation/ ; MySQL Workbench Data Export and Import — https://dev.mysql.com/doc/workbench/en/wb-admin-export-import-management.html ; Connector/Python Multiple Statements — https://dev.mysql.com/doc/connector-python/en/connector-python-multi.html
