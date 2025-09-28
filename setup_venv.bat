@echo off
REM setup_venv.bat - Script để thiết lập virtual environment trên Windows

echo 🏥 THIẾT LẬP VIRTUAL ENVIRONMENT
echo 🏥 HỆ THỐNG QUẢN LÝ KHÁM BỆNH - NÂNG CAP  
echo ==============================================================

REM Kiểm tra Python version
echo 📋 Kiểm tra Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Lỗi: Python không được cài đặt hoặc không có trong PATH
    echo 💡 Vui lòng cài đặt Python 3.8+ trước khi tiếp tục
    pause
    exit /b 1
)

REM Kiểm tra và xóa venv cũ nếu có
if exist "venv" (
    echo ⚠️  Virtual environment đã tồn tại, đang xóa để tạo mới...
    rmdir /s /q venv
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
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo ❌ File requirements.txt không tồn tại!
    pause
    exit /b 1
)

REM Kiểm tra cài đặt thành công
echo 🧪 Kiểm tra cài đặt...
python -c "import pyodbc; print('✅ pyodbc: OK')" 2>nul || echo ❌ pyodbc: FAILED
python -c "import pandas; print('✅ pandas: OK (Excel export available)')" 2>nul || echo ⚠️  pandas: Not installed (CSV export only)
python -c "import openpyxl; print('✅ openpyxl: OK (Excel styling available)')" 2>nul || echo ⚠️  openpyxl: Not installed (Basic Excel export)

echo.
echo ✅ THIẾT LẬP HOÀN TẤT!
echo.
echo 🚀 HƯỚNG DẪN SỬ DỤNG:
echo ====================
echo.
echo 1. Kích hoạt virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Chạy ứng dụng:
echo    python app.py
echo    hoặc: run.bat
echo.
echo 3. Thoát virtual environment:
echo    deactivate
echo.
echo 📊 TÍNH NĂNG MỚI:
echo =================
echo • 📈 Báo cáo ^& Xuất Excel nâng cao
echo • 🎨 Excel styling chuyên nghiệp
echo • 📊 Phân tích thống kê ^& doanh thu  
echo • 📁 Quản lý file báo cáo tự động
echo • 💾 Hỗ trợ CSV fallback
echo • 🔍 Hệ thống lịch sử khám nâng cao cho User
echo • 🗓️ Hiển thị ngày khám chính xác
echo • 🔎 Tìm kiếm theo mã tiếp nhận
echo.
echo 📝 LƯU Ý: Cần cấu hình kết nối SQL Server trong file db.py
pause