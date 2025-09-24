# 📦 HƯỚNG DẪN DEPLOYMENT

## 🎯 Để triển khai hệ thống trên máy khác

### 1. Copy source code
```bash
# Nén và copy toàn bộ thư mục cli_khambenh
# Hoặc push lên Git repository
```

### 2. Cài đặt Python 3.8+
- **Windows**: Tải từ python.org
- **Linux**: `sudo apt install python3 python3-pip python3-venv`
- **macOS**: `brew install python3`

### 3. Chạy setup
```bash
# Linux/macOS
./setup_venv.sh

# Windows
setup_venv.bat
```

### 4. Cấu hình Database
Sửa file `db.py`:
```python
SERVER = 'your-sql-server'
DATABASE = 'your-database'  
USERNAME = 'your-username'
PASSWORD = 'your-password'
```

### 5. Import dữ liệu mẫu
```bash
# Kích hoạt venv trước
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Import dữ liệu
python import_data.py
```

### 6. Chạy ứng dụng
```bash
# Sử dụng script tiện lợi
./run.sh        # Linux/macOS
run.bat         # Windows

# Hoặc chạy thủ công
source venv/bin/activate
python app.py
```

## 🔧 Troubleshooting

### ODBC Driver Issues
**Linux Ubuntu/Debian:**
```bash
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql17
```

**CentOS/RHEL:**
```bash
sudo curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/mssql-release.repo
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel
sudo ACCEPT_EULA=Y yum install msodbcsql17
```

**macOS:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17
```

### Permission Issues (Linux/macOS)
```bash
chmod +x setup_venv.sh run.sh
```

### Virtual Environment Issues
```bash
# Xóa và tạo lại
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📋 Checklist Deployment

- [ ] Python 3.8+ installed
- [ ] SQL Server accessible
- [ ] ODBC Driver installed  
- [ ] Source code copied
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database configured
- [ ] Sample data imported
- [ ] Application tested
- [ ] User accounts created

## 🚀 Production Notes

1. **Security**: Thay đổi mật khẩu admin mặc định
2. **Database**: Backup định kỳ
3. **Logs**: Monitor log files
4. **Updates**: Kiểm tra updates thường xuyên
5. **Performance**: Monitor database performance