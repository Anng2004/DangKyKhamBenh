@echo off
REM run.bat - Script chạy ứng dụng trên Windows

cls
echo 🏥 HỆ THỐNG QUẢN LÝ KHÁM BỆNH
echo 📊 Báo cáo Excel + 🔍 Lịch sử khám nâng cao
echo ================================================
echo.

REM Kiểm tra virtual environment
if not exist "venv" (
    echo ❌ Virtual environment chưa được tạo!
    echo 💡 Chạy: setup_venv.bat để thiết lập
    echo.
    set /p answer=Bạn có muốn thiết lập ngay bây giờ? (y/n): 
    if /i "%answer%"=="y" (
        echo 🔄 Đang thiết lập virtual environment...
        call setup_venv.bat
        if %errorlevel% neq 0 (
            echo ❌ Thiết lập thất bại!
            pause
            exit /b 1
        )
        echo ✅ Thiết lập hoàn tất, tiếp tục khởi động app...
    ) else (
        pause
        exit /b 1
    )
)

REM Kích hoạt virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Kiểm tra dependencies
echo 📋 Kiểm tra dependencies...
python -c "import pyodbc" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencies chưa được cài đặt!
    echo 💡 Chạy: pip install -r requirements.txt
    echo.
    set /p answer=Bạn có muốn cài đặt dependencies ngay bây giờ? (y/n): 
    if /i "%answer%"=="y" (
        pip install -r requirements.txt
    ) else (
        pause
        exit /b 1
    )
)

REM Kiểm tra tính năng báo cáo
echo � Kiểm tra tính năng báo cáo...
python -c "import pandas; print('  ✅ Excel export: Có')" 2>nul || echo   ⚠️  Excel export: CSV only
python -c "import openpyxl; print('  ✅ Excel styling: Có')" 2>nul || echo   ⚠️  Excel styling: Cơ bản

echo.
echo 🚀 KHỞI ĐỘNG ỨNG DỤNG...
echo.
python app.py

echo.
echo 👋 Cảm ơn bạn đã sử dụng Hệ Thống Quản Lý Khám Bệnh!

pause