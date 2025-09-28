#!/bin/bash
# run.sh - Script chạy ứng dụng với virtual environment

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${GREEN}🏥 HỆ THỐNG QUẢN LÝ KHÁM BỆNH${NC}"
echo -e "${CYAN}📊 Báo cáo Excel + 🔍 Lịch sử khám nâng cao${NC}"
echo "================================================"
echo ""

# Kiểm tra virtual environment
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment chưa được tạo!${NC}"
    echo -e "${YELLOW}💡 Chạy: ./setup_venv.sh để thiết lập${NC}"
    echo ""
    read -p "Bạn có muốn thiết lập ngay bây giờ? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🔄 Đang thiết lập virtual environment...${NC}"
        ./setup_venv.sh
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Thiết lập hoàn tất, tiếp tục khởi động app...${NC}"
        else
            echo -e "${RED}❌ Thiết lập thất bại!${NC}"
            exit 1
        fi
    else
        exit 1
    fi
fi

# Kích hoạt virtual environment
echo -e "${YELLOW}🔄 Kích hoạt virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Kiểm tra dependencies
echo -e "${YELLOW}📋 Kiểm tra dependencies...${NC}"
python3 -c "import pyodbc" 2>/dev/null || {
    echo -e "${RED}❌ Dependencies chưa được cài đặt!${NC}"
    echo -e "${YELLOW}💡 Chạy: pip install -r requirements.txt${NC}"
    echo ""
    read -p "Bạn có muốn cài đặt dependencies ngay bây giờ? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install -r requirements.txt
    else
        exit 1
    fi
}

# Kiểm tra tính năng báo cáo
echo -e "${BLUE}📊 Kiểm tra tính năng báo cáo...${NC}"
python3 -c "import pandas; print('  ✅ Excel export: Có')" 2>/dev/null || echo -e "${YELLOW}  ⚠️  Excel export: CSV only${NC}"
python3 -c "import openpyxl; print('  ✅ Excel styling: Có')" 2>/dev/null || echo -e "${YELLOW}  ⚠️  Excel styling: Cơ bản${NC}"

echo ""
echo -e "${GREEN}🚀 KHỞI ĐỘNG ỨNG DỤNG...${NC}"
echo ""
python3 app.py

# Thông báo khi thoát
echo ""
echo -e "${CYAN}👋 Cảm ơn bạn đã sử dụng Hệ Thống Quản Lý Khám Bệnh!${NC}"