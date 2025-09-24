@echo off
REM setup_venv.bat - Script để thiết lập virtual environment trên Windows

echo 🏥 Thiết lập Virtual Environment - Hệ Thống Quản Lý Khám Bệnh
echo ==============================================================

REM Kiểm tra Python version
python --version
if %errorlevel% neq 0 (
    echo ❌ Lỗi: Python không được cài đặt hoặc không có trong PATH
    pause
    exit /b 1
)

REM Tạo virtual environment
echo 🔧 Tạo virtual environment...
python -m venv venv

REM Kích hoạt virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Cập nhật pip...
python -m pip install --upgrade pip

REM Cài đặt dependencies
echo 📦 Cài đặt các thư viện cần thiết...
pip install -r requirements.txt

echo.
echo ✅ Thiết lập hoàn tất!
echo.
echo 🚀 Hướng dẫn sử dụng:
echo ====================
echo.
echo 1. Kích hoạt virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Chạy ứng dụng:
echo    python app.py
echo.
echo 3. Thoát virtual environment:
echo    deactivate
echo.
echo 📝 Lưu ý: Cần cấu hình kết nối SQL Server trong file db.py
pause