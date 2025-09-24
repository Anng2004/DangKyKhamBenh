# 🏥 Hệ Thống Quản Lý Khám Bệnh

Hệ thống quản lý khám bệnh với giao diện CLI, hỗ trợ quét QR code đăng ký bệnh nhân và quản lý tiếp nhận.

## 🚀 Tính Năng

- ✅ Quản lý bệnh nhân, bác sĩ, phòng khám, dịch vụ
- ✅ Đăng ký tiếp nhận khám bệnh 
- ✅ Quét QR code từ CCCD để tự động tạo bệnh nhân
- ✅ Tự động gán bác sĩ theo phòng khám
- ✅ Xuất báo cáo Excel
- ✅ Hệ thống phân quyền (Admin/User)

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.8 hoặc cao hơn
- **Database**: Microsoft SQL Server
- **OS**: Windows, macOS, Linux

## ⚡ Cài Đặt Nhanh

### 1. Clone/Download source code
```bash
# Download và giải nén source code vào thư mục cli_khambenh
```

### 2. Chạy script setup

**Trên Linux/macOS:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

**Trên Windows:**
```cmd
setup_venv.bat
```

### 3. Cấu hình Database
Chỉnh sửa file `db.py` để cấu hình kết nối SQL Server:
```python
SERVER = 'your-server-name'
DATABASE = 'your-database-name'
USERNAME = 'your-username'
PASSWORD = 'your-password'
```

### 4. Khởi tạo Database
```bash
# Kích hoạt virtual environment trước
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate     # Windows

# Chạy script khởi tạo
python import_data.py
```

### 5. Chạy ứng dụng
```bash
python app.py
```

## 🔧 Cài Đặt Thủ Công

Nếu script tự động không hoạt động, bạn có thể cài đặt thủ công:

### 1. Tạo Virtual Environment
```bash
python3 -m venv venv

# Kích hoạt
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Cài đặt dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Cài đặt ODBC Driver (nếu cần)

**Windows:**
- Tải SQL Server ODBC Driver từ Microsoft

**Linux (Ubuntu/Debian):**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

**macOS:**
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17
```

## 🎯 Sử Dụng

### Đăng nhập
- **Admin**: username=`admin`, password=`admin`
- **User**: Sử dụng CCCD và mật khẩu được tạo tự động

### Quét QR Code
1. Vào menu "Quản lý Tiếp nhận" → "Quét QR code đăng ký"
2. Nhập chuỗi QR theo định dạng: 
   ```
   CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi
   ```
3. Hệ thống sẽ tự động tạo bệnh nhân và tài khoản

### Định dạng QR Code
```
058090007045|264362146|Nguyễn Gio An|20041990|Nam|Thôn La Vang 1, Quảng Sơn, Ninh Sơn, Ninh Thuận
```

## 📁 Cấu Trúc Project

```
cli_khambenh/
├── app.py              # Giao diện chính
├── db.py               # Kết nối database
├── models.py           # Định nghĩa models
├── repositories.py     # Data access layer
├── mvc.py              # Controllers
├── qr_utils.py         # Xử lý QR code
├── import_data.py      # Khởi tạo dữ liệu
├── requirements.txt    # Dependencies
├── setup_venv.sh       # Setup script Linux/macOS
├── setup_venv.bat      # Setup script Windows
└── README.md           # Hướng dẫn này
```

## 🔍 Troubleshooting

### Lỗi kết nối Database
```
pyodbc.Error: ('01000', "[01000] [unixODBC]...")
```
**Giải pháp:** Kiểm tra cấu hình server, username, password trong `db.py`

### Lỗi ODBC Driver
```
pyodbc.Error: ('01000', "Can't open lib 'ODBC Driver 17 for SQL Server'")
```
**Giải pháp:** Cài đặt ODBC Driver theo hướng dẫn trên

### Lỗi import pandas
```
ModuleNotFoundError: No module named 'pandas'
```
**Giải pháp:** 
```bash
pip install pandas openpyxl
```

## 🤝 Đóng Góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 📞 Hỗ Trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub hoặc liên hệ developer.