#!/bin/bash
# setup_venv.sh - Script để thiết lập virtual environment cho hệ thống quản lý khám bệnh

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🏥 THIẾT LẬP VIRTUAL ENVIRONMENT${NC}"
echo -e "${GREEN}🏥 HỆ THỐNG QUẢN LÝ KHÁM BỆNH - NÂNG CAP${NC}"
echo "=============================================================="

# Kiểm tra Python version
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
    echo -e "${BLUE}📋 Phiên bản Python: $python_version${NC}"
else
    echo -e "${RED}❌ Python3 không được tìm thấy!${NC}"
    echo -e "${YELLOW}💡 Vui lòng cài đặt Python 3.8+ trước khi tiếp tục${NC}"
    exit 1
fi

# Tạo virtual environment
echo -e "${YELLOW}🔧 Tạo virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment đã tồn tại, đang xóa để tạo mới...${NC}"
    rm -rf venv
fi

python3 -m venv venv

# Kiểm tra OS để activate venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo -e "${BLUE}🪟 Phát hiện hệ điều hành Windows${NC}"
    source venv/Scripts/activate
else
    # Unix/Linux/macOS  
    echo -e "${BLUE}🐧 Phát hiện hệ điều hành Unix/Linux/macOS${NC}"
    source venv/bin/activate
fi

# Upgrade pip
echo -e "${YELLOW}⬆️  Cập nhật pip...${NC}"
pip install --upgrade pip

# Cài đặt dependencies
echo -e "${YELLOW}📦 Cài đặt các thư viện cần thiết...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${RED}❌ File requirements.txt không tồn tại!${NC}"
    exit 1
fi

# Kiểm tra cài đặt thành công
echo -e "${YELLOW}🧪 Kiểm tra cài đặt...${NC}"
python3 -c "import pyodbc; print('✅ pyodbc: OK')" 2>/dev/null || echo -e "${RED}❌ pyodbc: FAILED${NC}"
python3 -c "import pandas; print('✅ pandas: OK (Excel export available)')" 2>/dev/null || echo -e "${YELLOW}⚠️  pandas: Not installed (CSV export only)${NC}"
python3 -c "import openpyxl; print('✅ openpyxl: OK (Excel styling available)')" 2>/dev/null || echo -e "${YELLOW}⚠️  openpyxl: Not installed (Basic Excel export)${NC}"

echo ""
echo -e "${GREEN}✅ THIẾT LẬP HOÀN TẤT!${NC}"
echo ""
echo -e "${BLUE}🚀 HƯỚNG DẪN SỬ DỤNG:${NC}"
echo "===================="
echo ""
echo -e "${YELLOW}1. Kích hoạt virtual environment:${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   source venv/Scripts/activate"
else  
    echo "   source venv/bin/activate"
fi
echo ""
echo -e "${YELLOW}2. Chạy ứng dụng:${NC}"
echo "   python3 app.py"
echo -e "${BLUE}   hoặc: ./run.sh${NC}"
echo ""
echo -e "${YELLOW}3. Thoát virtual environment:${NC}"
echo "   deactivate"
echo ""
echo -e "${GREEN}� TÍNH NĂNG MỚI:${NC}"
echo "================="
echo "• 📈 Báo cáo & Xuất Excel nâng cao"
echo "• 🎨 Excel styling chuyên nghiệp" 
echo "• 📊 Phân tích thống kê & doanh thu"
echo "• 📁 Quản lý file báo cáo tự động"
echo "• 💾 Hỗ trợ CSV fallback"
echo ""
echo -e "${YELLOW}�📝 LƯU Ý:${NC} Cần cấu hình kết nối SQL Server trong file db.py"