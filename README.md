# 🏥 Hệ Thống Quản Lý Khám Bệnh# 🏥### ✨ Tính Năng Nổi Bật



Hệ thống quản lý khám bệnh chuyên nghiệp với giao diện CLI, hỗ trợ quét QR code, báo cáo Excel và hệ thống lịch sử khám nâng cao.### 🎯 Core Features:

- ✅ **Quản lý đầy đủ**: Bệnh nhân, bác sĩ, phòng khám, dịch vụ, tiếp nhận

## ✨ Tính Năng Chính- ✅ **QR Code thông minh**: Tự động tạo bệnh nhân từ CCCD với phân tích thông minh

- ✅ **Phân quyền nâng cao**: Hệ thống Admin/User với menu riêng biệt và tính năng chuyên biệt

### 🎯 Core Features:- ✅ **Tự động hóa**: Gán bác sĩ theo chuyên khoa, tạo tài khoản bệnh nhân

- ✅ **Quản lý toàn diện**: Bệnh nhân, bác sĩ, phòng khám, dịch vụ, tiếp nhận- ✅ **🆕 Lịch sử khám nâng cao**: Xem chi tiết, tìm kiếm, thống kê cho User role

- ✅ **QR Code thông minh**: Tự động tạo bệnh nhân từ CCCD với phân tích CCCD 12 số

- ✅ **Phân quyền hoàn chỉnh**: Admin (quản lý) và User (bệnh nhân) với menu chuyên biệt### 🚀 NEW: Báo Cáo & Xuất Excel Chuyên Nghiệp

- ✅ **Tự động hóa**: Gán bác sĩ theo chuyên khoa, tạo tài khoản tự động- 📊 **11 loại báo cáo** đa dạng (danh sách, thống kê, phân tích)

- 📈 **Báo cáo thống kê tổng hợp** với phân tích chi tiết

### 📊 Hệ Thống Báo Cáo Chuyên Nghiệp:- 💰 **Báo cáo doanh thu** theo dịch vụ với ranking

- 📈 **11 loại báo cáo** đa dạng với Excel styling- 📅 **Báo cáo hoạt động hàng ngày** 

- 💰 **Báo cáo doanh thu** theo dịch vụ với ranking- 📋 **Báo cáo tổng hợp đa trang** (5 sheets trong 1 file)

- 📋 **Báo cáo tổng hợp** đa trang (5 sheets trong 1 file)- 🎨 **Excel styling chuyên nghiệp** với openpyxl

- 🗂️ **Tự động quản lý file** và dọn dẹp- 📁 **Quản lý file tự động** (mở thư mục, dọn dẹp file cũ)

- 💾 **CSV fallback** khi không có pandas

### 🔍 Hệ Thống Lịch Sử Khám Nâng Cao (User):- 🗂️ **Cấu trúc thư mục** có tổ chức (reports/benh_nhan/, tiep_nhan/, etc.)

- 📋 **Xem lịch sử cơ bản**: Bảng thông tin với thống kê tổng hợp

- 🔍 **Xem chi tiết nâng cao**: Tìm kiếm, lọc và xem từng lần khám### 🆕 NEW: Hệ Thống Lịch Sử Khám Nâng Cao (User Role)

- 📊 **Thống kê cá nhân**: Tổng số lần khám, chi phí- 📋 **Xem lịch sử cơ bản**: Hiển thị danh sách với bảng định dạng chuyên nghiệp

- 🗓️ **Thông tin thời gian**: Ngày khám chính xác từ database- 🔍 **Xem lịch sử chi tiết**: Menu con với nhiều tùy chọn tìm kiếm và lọc

- 📊 **Thống kê cá nhân**: Tổng số lần khám, tổng chi phí đã thanh toán

## 📋 Yêu Cầu Hệ Thống- 🗓️ **Hiển thị ngày khám**: Thông tin thời gian chính xác từ database

- 🔎 **Tìm kiếm theo mã**: Tra cứu nhanh theo mã tiếp nhận

- **Python**: 3.8+ (khuyến nghị 3.10+)- 📝 **Chi tiết từng lần khám**: Xem đầy đủ thông tin bệnh nhân, dịch vụ, bác sĩ

- **Database**: Microsoft SQL Server (LocalDB, Express, hoặc Full)- 🎨 **Giao diện thân thiện**: Text formatting thông minh, cắt ngắn text dài

- **Dependencies**: `pyodbc` (bắt buộc), `pandas + openpyxl` (khuyến nghị)- 💡 **Interactive**: Nhập STT để xem chi tiết, menu điều hướng trực quanKhám Bệnh - NÂNG CAP



## ⚡ Cài Đặt Nhanh# 🏥 Hệ Thống Quản Lý Khám Bệnh - NÂNG CAP



### 🚀 Auto Setup (Khuyến nghị)Hệ thống quản lý khám bệnh với giao diện CLI, hỗ trợ quét QR code đăng ký bệnh nhân, **tính năng báo cáo xuất Excel chuyên nghiệp**, và **hệ thống lịch sử khám nâng cao cho bệnh nhân**.



**Linux/macOS:**## ✨ Tính Năng Nổi Bật

```bash

chmod +x setup_venv.sh run.sh### 🎯 Core Features:

./setup_venv.sh    # Thiết lập một lần- ✅ **Quản lý đầy đủ**: Bệnh nhân, bác sĩ, phòng khám, dịch vụ, tiếp nhận

./run.sh           # Chạy ứng dụng- ✅ **QR Code thông minh**: Tự động tạo bệnh nhân từ CCCD với phân tích thông minh

```- ✅ **Phân quyền**: Hệ thống Admin/User với menu riêng biệt

- ✅ **Tự động hóa**: Gán bác sĩ theo chuyên khoa, tạo tài khoản bệnh nhân

**Windows:**

```cmd### 🚀 NEW: Báo Cáo & Xuất Excel Chuyên Nghiệp

setup_venv.bat     - 📊 **11 loại báo cáo** đa dạng (danh sách, thống kê, phân tích)

run.bat           - 📈 **Báo cáo thống kê tổng hợp** với phân tích chi tiết

```- 💰 **Báo cáo doanh thu** theo dịch vụ với ranking

- 📅 **Báo cáo hoạt động hàng ngày** 

### ⚙️ Cấu hình Database- 📋 **Báo cáo tổng hợp đa trang** (5 sheets trong 1 file)

Chỉnh sửa file `db.py`:- 🎨 **Excel styling chuyên nghiệp** với openpyxl

```python- 📁 **Quản lý file tự động** (mở thư mục, dọn dẹp file cũ)

conn_str = (- 💾 **CSV fallback** khi không có pandas

    "DRIVER={ODBC Driver 13 for SQL Server};"- 🗂️ **Cấu trúc thư mục** có tổ chức (reports/benh_nhan/, tiep_nhan/, etc.)

    "SERVER=HOME\\GIOAN\\SQLEXPRESS;"    # Thay đổi server

    "DATABASE=DangKyKhamBenh;"### 🧠 QR Code Analysis:

    "Trusted_Connection=yes;"- 🔍 **Phân tích CCCD 12 số** tự động trích xuất tỉnh, giới tính, năm sinh

    "TrustServerCertificate=yes;"- 📱 **Multiple formats** hỗ trợ nhiều định dạng QR khác nhau

)- ⚡ **Validation** thông minh với error handling

```

## 📋 Yêu Cầu Hệ Thống

## 🎯 Hướng Dẫn Sử Dụng

- **Python**: 3.8+ (khuyến nghị 3.10+)

### 🔐 Đăng nhập:- **Database**: Microsoft SQL Server (LocalDB, Express, hoặc Full)

- **👨‍💼 Admin**: `admin` / `admin` - Quản lý toàn hệ thống + Báo cáo- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)

- **👤 User**: CCCD/password tự động - Đăng ký khám + Xem lịch sử

### Dependencies:

### 👨‍💼 Admin Menu:- **Bắt buộc**: `pyodbc` (database connection)

```- **Khuyến nghị**: `pandas + openpyxl` (Excel export với styling)

🏥 MENU QUẢN TRỊ VIÊN:- **Tùy chọn**: `numpy, matplotlib` (advanced analytics)

  1. 📋 Quản lý Tiếp nhận

  2. 🏥 Quản lý Phòng khám  ## ⚡ Cài Đặt Siêu Nhanh

  3. 🩺 Quản lý Dịch vụ

  4. 👳 Quản lý Bệnh nhân### 🚀 Auto Setup (Khuyến nghị)

  5. 👨‍⚕️ Quản lý Bác sĩ

  6. 👤 Quản lý Người dùng**Trên Linux/macOS:**

  7. 📊 Báo cáo & Xuất Excel```bash

  8. 🏛️ Migration dữ liệu# Clone/download project

```chmod +x setup_venv.sh run.sh

./setup_venv.sh    # Thiết lập một lần (auto-install dependencies)

### 👤 User Menu:./run.sh           # Chạy ứng dụng (với giao diện đẹp)

``````

🏥 MENU BỆNH NHÂN:

  1. 👀 Xem thông tin dịch vụ**Trên Windows:**

  2. 🏥 Xem thông tin phòng khám  ```cmd

  3. 📝 Đăng ký khám bệnhREM Clone/download project  

  4. 📋 Xem lịch sử khámsetup_venv.bat     REM Thiết lập một lần

  5. 🔍 Xem lịch sử khám chi tiếtrun.bat           REM Chạy ứng dụng

``````



### 🔍 Tính Năng Lịch Sử Khám (User):### ⚙️ Cấu hình Database

Chỉnh sửa file `db.py` để cấu hình kết nối SQL Server:

**📋 Lịch sử cơ bản (Option 4):**```python

- Bảng formatted: STT, Mã TN, Ngày khám, Dịch vụ, Phòng khám, Bác sĩ, Chi phí# Cấu hình connection string

- Thống kê: Tổng lần khám, tổng chi phíconn_str = (

- Xem chi tiết: Nhập STT để xem thông tin đầy đủ    "DRIVER={ODBC Driver 13 for SQL Server};"

    "SERVER=HOME\\GIOAN\\SQLEXPRESS;"    # Thay đổi server tại đây

**🔍 Lịch sử chi tiết (Option 5):**    "DATABASE=DangKyKhamBenh;"

- Xem tất cả lịch sử    "Trusted_Connection=yes;"

- Tìm theo mã tiếp nhận    "TrustServerCertificate=yes;"      # Cho SQL Server 2022+

- Lọc theo thời gian (sắp có))

```

## 📱 QR Code Thông Minh

### 🎯 Sẵn sáng sử dụng!

Hệ thống hỗ trợ nhiều định dạng QR và **tự động phân tích CCCD 12 số**:- ✅ **Database tự động**: Khởi tạo schema + dữ liệu mẫu khi chạy lần đầu

- ✅ **Reports folder**: Tự động tạo cấu trúc thư mục báo cáo

### Định dạng đầy đủ:- ✅ **Login ready**: `admin/admin` để bắt đầu

```

CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi---

058186000028|2345678|Nguyễn Thị Linh|15071986|Nữ|Ninh Thuận

```## 📊 TÍNH NĂNG MỚI: BÁO CÁO & XUẤT EXCEL



### Định dạng tối thiểu:### 🎨 Professional Reports System:

``````

CCCD||HoTen|||📋 XUẤT DANH SÁCH CƠ BẢN:

058186000028||Nguyễn Thị Linh|||  • Xuất danh sách bệnh nhân      

```  • Xuất danh sách tiếp nhận

  • Xuất báo cáo dịch vụ

**🧠 Phân tích thông minh CCCD `058186000028`:**  • Xuất báo cáo phòng khám  

- `058`: Ninh Thuận (3 số đầu)  • Xuất báo cáo bác sĩ

- `1`: Nữ, thế kỷ 20 (số thứ 4)

- `86`: Năm sinh 1986 (số 5-6)📊 BÁO CÁO THỐNG KÊ & PHÂN TÍCH:

  • Báo cáo thống kê tổng hợp

## 📊 Hệ Thống Báo Cáo  • Báo cáo doanh thu & phân tích  

  • Báo cáo hoạt động hôm nay

### Báo cáo cơ bản:  • Báo cáo tổng hợp đa trang

- Danh sách bệnh nhân, tiếp nhận

- Báo cáo dịch vụ, phòng khám, bác sĩ📁 QUẢN LÝ FILE:

  • Mở thư mục báo cáo

### Báo cáo nâng cao:  • Dọn dẹp file cũ (auto-cleanup)

- Thống kê tổng hợp```

- Doanh thu & phân tích  

- Hoạt động hàng ngày### 🗂️ Reports Folder Structure:

- Báo cáo đa trang (multi-sheet)```

reports/

### Quản lý file:├── benh_nhan/          # Báo cáo bệnh nhân

- Mở thư mục báo cáo├── tiep_nhan/          # Báo cáo tiếp nhận  

- Tự động dọn dẹp file cũ├── dich_vu/            # Báo cáo dịch vụ

- CSV fallback khi không có pandas├── phong_kham/         # Báo cáo phòng khám

├── tong_hop/           # Báo cáo tổng hợp (multi-sheet)

## 🗂️ Cấu Trúc Project├── thong_ke/           # Báo cáo thống kê & doanh thu

└── README.md           # Hướng dẫn sử dụng thư mục

``````

cli_khambenh/

├── 🏠 Core Application### ✨ Excel Features:

│   ├── app.py              # Main application- 🎨 **Professional styling**: Headers, borders, colors

│   ├── db.py               # Database connection- 📏 **Auto-fit columns**: Tự động điều chỉnh độ rộng

│   ├── models.py           # Data models- 📊 **Multiple sheets**: Báo cáo đa trang trong 1 file

│   ├── repositories.py     # Data access layer- 📈 **Data analysis**: Thống kê, ranking, tổng hợp

│   └── mvc.py              # Controllers- 💾 **CSV fallback**: Tự động chuyển CSV nếu không có pandas

│- 🏷️ **Metadata**: Author, creation date, file info

├── 🎯 Features  

│   ├── qr_utils.py         # QR code processing## 🔧 Manual Installation (Alternative)

│   ├── report_utils.py     # Reporting system

│   └── utils/              # Validation, messagesNếu auto-setup không hoạt động, bạn có thể cài đặt thủ công:

│

├── 📊 Setup & Data### 1. Virtual Environment

│   ├── requirements.txt    # Dependencies```bash

│   ├── setup_venv.sh/.bat  # Auto setuppython3 -m venv venv

│   ├── run.sh/.bat         # App launcher

│   └── import_data.py      # Sample data# Activate

│source venv/bin/activate          # Linux/macOS  

└── 📁 reports/             # Generated reportsvenv\Scripts\activate            # Windows

    ├── benh_nhan/```

    ├── tiep_nhan/

    ├── dich_vu/### 2. Install Dependencies

    └── thong_ke/```bash

```pip install --upgrade pip

pip install -r requirements.txt

## 🔧 Troubleshooting

# Verify installation

### Database Connection:python3 -c "import pyodbc; print('✅ pyodbc OK')"

```bashpython3 -c "import pandas; print('✅ pandas OK')" 2>/dev/null || echo "⚠️  pandas missing"

# Kiểm tra SQL Server chạy: services.msc → SQL Serverpython3 -c "import openpyxl; print('✅ openpyxl OK')" 2>/dev/null || echo "⚠️  openpyxl missing"

# Test connection: sqlcmd -S HOME\\GIOAN\SQLEXPRESS```

# Xác nhận connection string trong db.py

```### 3. ODBC Driver Installation



### ODBC Driver:**Windows**: Download từ Microsoft

```bash**Linux**: 

# Install ODBC Driver 13 for SQL Server```bash

# Windows: Download từ Microsoft# Ubuntu/Debian

# macOS: brew install msodbcsql17curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Linux: apt-get install msodbcsql17curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

```apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

```

### Excel Export:

```bash**macOS**:

# Install dependencies```bash

pip install pandas openpyxlbrew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release  

HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17

# Nếu lỗi: hệ thống tự chuyển CSV```

```

---

## 🚀 Hiệu Suất

## 🎯 Hướng Dẫn Sử Dụng

- **Small data** (<1K records): ~1-2s  

- **Medium data** (1K-10K): ~3-5s## 🎯 Hướng Dẫn Sử Dụng

- **Large data** (>10K): ~10-30s

- **Medical history**: ~0.5-2s (optimized)### 🔐 Đăng nhập:

- **👨‍💼 Admin**: `admin` / `admin` (Full access + Reports + Management)

## 📄 License- **👤 User**: Sử dụng CCCD/password được tạo tự động (Enhanced medical history access)



MIT License - Professional healthcare management system.### �‍💼 Admin Role Features:

```

---🏥 HỆ THỐNG QUẢN LÝ KHÁM BỆNH - MENU QUẢN TRỊ VIÊN:

  1. 📋 Quản lý Tiếp nhận

**🏥 Hệ Thống Quản Lý Khám Bệnh** - Production-ready với comprehensive features.  2. 🏥 Quản lý Phòng khám  

  3. 🩺 Quản lý Dịch vụ

*Sẵn sàng triển khai! 🚀*  4. 👳 Quản lý Bệnh nhân
  5. 👨‍⚕️ Quản lý Bác sĩ
  6. 👤 Quản lý Người dùng
  7. 📊 Báo cáo & Xuất Excel
  8. 🏛️ Migration dữ liệu tỉnh bệnh nhân
  0. 🚪 Đăng xuất
```

### �👤 User Role Features (Bệnh nhân):
```
🏥 HỆ THỐNG ĐĂNG KÝ KHÁM BỆNH - MENU BỆNH NHÂN:
  1. 👀 Xem thông tin dịch vụ
  2. 🏥 Xem thông tin phòng khám  
  3. 📝 Đăng ký khám bệnh
  4. 📋 Xem lịch sử khám
  5. 🔍 Xem lịch sử khám chi tiết
  0. 🚪 Đăng xuất
```

#### **🆕 Tính năng Lịch sử khám nâng cao:**

**📋 Xem lịch sử khám cơ bản (Option 4):**
- Hiển thị bảng formatted với thông tin: STT, Mã tiếp nhận, Ngày khám, Dịch vụ, Phòng khám, Bác sĩ, Chi phí
- Thống kê tổng số lần khám và tổng chi phí
- Tùy chọn nhập STT để xem chi tiết từng lần khám
- Thông tin bệnh nhân ở header (tên, giới tính, năm sinh, CCCD)

**🔍 Xem lịch sử khám chi tiết (Option 5):**
- Menu con với 3 tùy chọn:
  - 📋 Xem tất cả lịch sử
  - 🔍 Tìm theo mã tiếp nhận cụ thể  
  - 📅 Lọc theo khoảng thời gian (coming soon)

**📝 Chi tiết từng lần khám:**
- Thông tin đầy đủ: bệnh nhân, dịch vụ, phòng khám, bác sĩ
- Mã tiếp nhận, lý do khám, ngày giờ chính xác
- Giao diện thân thiện với emoji và formatting

### 📱 QR Code Thông Minh:

#### **Cách 1: Through Menu**
```
Admin Menu → Quản lý Tiếp nhận → Quét QR code đăng ký
```

#### **Cách 2: User Registration** 
```
User Menu → Đăng ký khám bệnh → Nhập QR code
```

### 📊 Báo Cáo & Excel Export:
```
Admin Menu → Báo cáo & Xuất Excel → [Chọn loại báo cáo]
```
- 📈 **Thống kê tổng hợp**: Overview toàn hệ thống
- 💰 **Doanh thu phân tích**: Revenue by services + ranking  
- 📅 **Hoạt động hàng ngày**: Daily operations report
- 📋 **Multi-sheet reports**: Comprehensive analysis

### 📁 File Management:
- **Mở thư mục**: Trực tiếp mở folder reports từ app
- **Cleanup**: Tự động dọn dẹp file cũ theo ngày

---

## 🔍 QR Code Formats

**🔥 Tính năng mới: Phân tích thông minh CCCD 12 số**

Hệ thống hỗ trợ nhiều định dạng QR code:

#### **1. Định dạng đầy đủ:**
```
CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi
```
Ví dụ:
```
058186000028|2345678|Nguyễn Thị Linh|15071986|Nữ|Ninh Thuận
```

#### **2. Định dạng tối thiểu (✨ Mới):**
```
CCCD||HoTen|||
```
Ví dụ:
```
058186000028||Nguyễn Thị Linh|||
```

**🧠 Phân tích thông minh:** Khi thông tin QR không đầy đủ, hệ thống sẽ **tự động phân tích số CCCD 12 chữ số** để trích xuất:
- 🗺️ **Tỉnh/TP khai sinh** (3 số đầu)
- 👫 **Giới tính** (số thứ 4: 0/2=Nam, 1/3=Nữ)  
- 🎂 **Năm sinh** (số thứ 5-6 + thế kỷ từ số thứ 4)

**Ví dụ CCCD `058186000028`:**
- `058`: Ninh Thuận
- `1`: Nữ, thế kỷ 20 (1900-1999)
- `86`: Năm sinh 1986
- `000028`: Số định danh cá nhân

📁 **Cấu Trúc Project**

```
cli_khambenh/
├── 🏠 Core Application
│   ├── app.py              # Main application với enhanced UI + User menu nâng cao
│   ├── db.py               # Database connection & init
│   ├── models.py           # ORM models với validation + TiepNhan with timestamps
│   ├── repositories.py     # Data access layer + Enhanced medical history queries
│   ├── mvc.py              # MVC controllers + Advanced medical history views
│   └── validation_utils.py # Input validation helpers
│
├── 🎯 Features  
│   ├── qr_utils.py         # QR code processing + CCCD analysis
│   ├── report_utils.py     # 🆕 Professional reporting system
│   ├── migration_hanh_chinh.py # Admin data migration
│   └── admin_migration_menu.py # Migration UI
│
├── 📊 Data & Config
│   ├── database_schema.sql # Complete DB schema
│   ├── import_data.py      # Sample data initialization  
│   ├── requirements.txt    # Enhanced dependencies
│   └── DEPLOYMENT.md       # Deployment guide
│
├── 🚀 Setup & Run
│   ├── setup_venv.sh       # 🆕 Enhanced Linux/macOS setup
│   ├── setup_venv.bat      # 🆕 Enhanced Windows setup  
│   ├── run.sh              # 🆕 Smart app launcher (Unix)
│   ├── run.bat             # 🆕 Smart app launcher (Windows)
│   └── README_SETUP.md     # 🆕 Detailed setup guide
│
└── 📁 Generated
    └── reports/            # 🆕 Auto-created reports folder
        ├── benh_nhan/
        ├── tiep_nhan/ 
        ├── dich_vu/
        ├── phong_kham/
        ├── tong_hop/
        ├── thong_ke/
        └── README.md       # Reports usage guide
```

### 🆕 New Files (Recent Updates):
- ✨ **Enhanced mvc.py**: Advanced medical history controllers with detail views
- ✨ **Updated models.py**: TiepNhan model with timestamp support
- ✨ **Enhanced repositories.py**: Optimized queries for medical history
- ✨ **report_utils.py**: Comprehensive reporting engine
- 🎨 **Enhanced setup scripts**: Interactive, colorful, smart error handling
- 📊 **Reports system**: Auto-organized file structure  
- 🛠️ **README_SETUP.md**: Detailed setup instructions

## �️ Troubleshooting

### ❌ Database Connection Issues:
```bash
# Error: "Can't connect to SQL Server"
# Solutions:
1. Kiểm tra SQL Server đã chạy: services.msc → SQL Server
2. Xác nhận connection string trong db.py  
3. Test connection: sqlcmd -S HOME\\GIOAN\SQLEXPRESS
4. Firewall: Allow SQL Server port 1433
```

### ❌ ODBC Driver Issues:
```bash
# Error: "Can't open lib 'ODBC Driver 13 for SQL Server'"
# Solutions:
1. Install ODBC Driver 17 (hướng dẫn trên)
2. macOS: brew install unixodbc
3. Linux: apt-get install unixodbc unixodbc-dev
```

### ❌ Excel Export Issues:
```bash  
# Error: "No module named 'pandas'" 
pip install pandas openpyxl

# Error: "Excel styling not working"
# Check: Nếu không có openpyxl, hệ thống sẽ tự chuyển CSV

# Error: "Cannot save file into non-existent directory" 
# Fix: Đã được fix trong phiên bản hiện tại (auto-create directories)
```

### ❌ Permission Issues:
```bash
# Linux/macOS: Make scripts executable  
chmod +x setup_venv.sh run.sh

# Windows: Run as Administrator nếu cần
```

### 🔍 Debug Mode:
```python
# Thêm vào db.py để debug connection
print(f"Connecting to: {conn_str}")
```

## 🚀 Performance & Features

### ⚡ System Requirements:
- **RAM**: 2GB+ (4GB+ khuyến nghị cho large reports)
- **Storage**: 500MB+ (reports có thể tốn nhiều dung lượng)
- **CPU**: Any modern CPU (Excel generation có thể tốn CPU)

### 📊 Reporting Performance:
- **Small data** (< 1000 records): ~1-2 seconds  
- **Medium data** (1000-10000 records): ~3-5 seconds
- **Large data** (10000+ records): ~10-30 seconds
- **Multi-sheet reports**: Add ~2-3 seconds per sheet
- **Medical history queries**: ~0.5-2 seconds (optimized with proper indexing)

### 🔄 Data Limits:
- **Bệnh nhân**: Unlimited (limited by SQL Server)
- **Medical history records**: Unlimited với pagination support
- **Excel sheets**: ~1M rows per sheet (Excel limit)
- **CSV files**: Unlimited  
- **File cleanup**: Auto-delete files >30 days (configurable)
- **Search results**: Optimized for fast retrieval với database indexing

---

## 🤝 Contributing & Development

### 🔧 Development Setup:
```bash
# Clone + setup development environment
git clone [repository]
cd cli_khambenh
./setup_venv.sh
# Start coding!
```

### 📝 Code Structure:
- **MVC Pattern**: Separation of concerns
- **Repository Pattern**: Data access abstraction  
- **Validation Layer**: Input sanitization & validation
- **Error Handling**: Comprehensive try-catch với user-friendly messages

### 🧪 Testing:
- **Manual testing**: Use sample data  
- **QR Code testing**: Use provided examples
- **Excel testing**: Check với/không pandas
- **Database testing**: Multiple SQL Server versions

### 🎯 Future Enhancements:
- [ ] Web UI (Flask/FastAPI)
- [ ] REST API endpoints
- [ ] Advanced analytics (charts, graphs)
- [ ] Email reports scheduling  
- [ ] Multi-language support
- [ ] Mobile QR scanning app integration
- [ ] **✅ Enhanced User Medical History** (Completed)
- [ ] Time-based filtering for medical history
- [ ] Medical history export for users
- [ ] Appointment scheduling system
- [ ] SMS/Email notifications

---

## 📄 License & Support

### 📜 License:
MIT License - Xem file LICENSE để biết thêm chi tiết.

### 📞 Hỗ Trợ:
- 🐛 **Bug Reports**: Tạo issue trên GitHub với detailed description
- 💡 **Feature Requests**: GitHub discussions hoặc issues  
- 📧 **Email Support**: Contact repository owner
- 📚 **Documentation**: README.md + README_SETUP.md + inline comments

### 🎯 Quick Links:
- **Setup Guide**: `README_SETUP.md` (detailed installation)
- **Database Schema**: `database_schema.sql`
- **Sample Data**: `import_data.py`  
- **Migration Tools**: `migration_hanh_chinh.py`

---

## 🎉 Changelog & Updates

### 🆕 Recent Updates (Latest):
- ✅ **Enhanced User Medical History System**: Professional medical history viewing with detailed information
  - 📋 Formatted table display with comprehensive information
  - 🔍 Advanced detail view with search and filter capabilities
  - 📊 Personal statistics (total visits, total costs)
  - 🗓️ Accurate date/time information from database
  - 🔎 Search by appointment code functionality
  - 📝 Detailed individual visit information
  - 🎨 Smart text formatting and user-friendly interface
- ✅ **Professional Reporting System**: 11 report types với Excel styling
- ✅ **Enhanced Setup Scripts**: Interactive, colorful, smart error handling
- ✅ **Auto Directory Creation**: Fix for "non-existent directory" errors
- ✅ **File Management**: Auto cleanup, open folder from app  
- ✅ **CSV Fallback**: Graceful degradation when pandas unavailable
- ✅ **Multi-sheet Reports**: Comprehensive analysis in single file
- ✅ **Revenue Analysis**: Detailed service-based revenue reports

### 🔄 Previous Updates:
- ✅ QR Code intelligent analysis (CCCD parsing)
- ✅ Enhanced user registration flow
- ✅ Admin/User role separation with specialized menus
- ✅ Comprehensive validation system
- ✅ MVC architecture implementation
- ✅ Database schema optimization
- ✅ Professional UI/UX improvements

---

**🏥 Hệ Thống Quản Lý Khám Bệnh** - Professional healthcare management với modern reporting capabilities và enhanced user experience.

*Ready for production use! 🚀*

### 🎯 Key Highlights:
- ✅ **Dual-role system**: Comprehensive admin tools + Enhanced patient portal
- ✅ **Smart medical history**: Advanced viewing, searching, and statistics
- ✅ **Professional reporting**: 11 types of Excel reports with styling
- ✅ **QR code intelligence**: Automatic patient data extraction
- ✅ **User-friendly interface**: Intuitive menus with emoji and formatting
- ✅ **Production-ready**: Comprehensive error handling and validation