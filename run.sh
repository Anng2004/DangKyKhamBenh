#!/bin/bash
# run.sh - Script chạy ứng dụng với virtual environment

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🏥 Khởi động Hệ Thống Quản Lý Khám Bệnh${NC}"
echo "================================================"

# Kiểm tra virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment chưa được tạo!${NC}"
    echo -e "${YELLOW}💡 Chạy: ./setup_venv.sh để thiết lập${NC}"
    exit 1
fi

# Kích hoạt virtual environment
echo "🔄 Kích hoạt virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Kiểm tra dependencies
echo "📋 Kiểm tra dependencies..."
pip freeze | grep -q "pyodbc" || {
    echo -e "${RED}❌ Dependencies chưa được cài đặt!${NC}"
    echo -e "${YELLOW}💡 Chạy: pip install -r requirements.txt${NC}"
    exit 1
}

# Chạy ứng dụng
echo "🚀 Khởi động ứng dụng..."
python3 app.py