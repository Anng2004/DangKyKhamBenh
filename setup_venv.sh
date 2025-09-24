#!/bin/bash
# setup_venv.sh - Script để thiết lập virtual environment cho hệ thống quản lý khám bệnh

echo "🏥 Thiết lập Virtual Environment - Hệ Thống Quản Lý Khám Bệnh"
echo "=============================================================="

# Kiểm tra Python version
python_version=$(python3 --version 2>&1)
echo "📋 Phiên bản Python: $python_version"

# Tạo virtual environment
echo "🔧 Tạo virtual environment..."
python3 -m venv venv

# Kiểm tra OS để activate venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🪟 Phát hiện hệ điều hành Windows"
    source venv/Scripts/activate
else
    # Unix/Linux/macOS
    echo "🐧 Phát hiện hệ điều hành Unix/Linux/macOS"
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️  Cập nhật pip..."
pip install --upgrade pip

# Cài đặt dependencies
echo "📦 Cài đặt các thư viện cần thiết..."
pip install -r requirements.txt

echo ""
echo "✅ Thiết lập hoàn tất!"
echo ""
echo "🚀 Hướng dẫn sử dụng:"
echo "===================="
echo ""
echo "1. Kích hoạt virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   Windows: source venv/Scripts/activate"
else
    echo "   Unix/Linux/macOS: source venv/bin/activate"
fi
echo ""
echo "2. Chạy ứng dụng:"
echo "   python3 app.py"
echo ""
echo "3. Thoát virtual environment:"
echo "   deactivate"
echo ""
echo "📝 Lưu ý: Cần cấu hình kết nối SQL Server trong file db.py"