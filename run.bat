@echo off
REM run.bat - Script chạy ứng dụng trên Windows

echo 🏥 Khởi động Hệ Thống Quản Lý Khám Bệnh
echo ================================================

REM Kiểm tra virtual environment
if not exist "venv" (
    echo ❌ Virtual environment chưa được tạo!
    echo 💡 Chạy: setup_venv.bat để thiết lập
    pause
    exit /b 1
)

REM Kích hoạt virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Chạy ứng dụng
echo 🚀 Khởi động ứng dụng...
python app.py

pause