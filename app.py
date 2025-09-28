# app.py
from db import init_db
from mvc import View, Model, Controller
from repositories import UserRepo
from datetime import datetime
import os

from utils.message_utils import (
    success, error, warning, print_header,print_separator
)

# Try to import pandas, set flag if available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class MenuManager:
    def __init__(self, controller: Controller, current_user_id: str, user_role: str, username: str):
        self.controller = controller
        self.current_user_id = current_user_id
        self.user_role = user_role
        self.username = username
        self.user_repo = UserRepo()

    def main_menu(self):
        if self.user_role.upper() == "ADMIN":
            self.admin_main_menu()
        else:
            self.user_main_menu()

    def admin_main_menu(self):
        """Admin main menu with module selection"""
        while True:
            print_header("           HỆ THỐNG QUẢN LÝ KHÁM BỆNH -\n              MENU QUẢN TRỊ VIÊN",50)
            print("1. 📋 Quản lý Tiếp nhận")
            print("2. 🏥 Quản lý Phòng khám")
            print("3. 🩺 Quản lý Dịch vụ")
            print("4. 👳 Quản lý Bệnh nhân")
            print("5. 👨‍⚕️ Quản lý Bác sĩ")
            print("6. 👤 Quản lý Người dùng")
            print("7. 📊 Báo cáo & Xuất Excel")
            print("8. 🏛️ Migration dữ liệu tỉnh bệnh nhân")
            print("0. 🚪 Đăng xuất")
            print_separator(50,"=")
            
            try:
                choice = int(input("Chọn module: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.tiep_nhan_menu()
                case 2: self.phong_kham_menu()
                case 3: self.dich_vu_menu()
                case 4: self.benh_nhan_menu()
                case 5: self.bac_si_menu()
                case 6: self.user_management_menu()
                case 7: self.report_menu()
                case 8: self.migration_menu()
                case 0: print("👋 Đăng xuất..."); break
                case _: error("Chức năng không tồn tại!")

    def user_main_menu(self):
        """User main menu with limited access"""
        while True:
            print("\n" + "="*50)
            print("           HỆ THỐNG ĐĂNG KÝ KHÁM BỆNH")
            print("                MENU BỆNH NHÂN")
            print_separator(50,"=")
            print("1. 👀 Xem thông tin dịch vụ")
            print("2. 🏥 Xem thông tin phòng khám")
            print("3. 📝 Đăng ký khám bệnh")
            print("4. 📋 Xem lịch sử khám")
            print("5. 🔍 Xem lịch sử khám chi tiết")
            print("0. 🚪 Đăng xuất")
            print_separator(50,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_danh_sach_dich_vu_cho_user()
                case 2: self.controller.hien_thi_danh_sach_phong_kham_cho_user()
                case 3: self.user_register_appointment()
                case 4: self.controller.hien_thi_lich_su_kham_cua_user(self.username)
                case 5: self.controller.hien_thi_lich_su_kham_cua_user_chi_tiet(self.username)
                case 0: print("👋 Đăng xuất..."); break
                case _: error("Chức năng không tồn tại!")

    def phong_kham_menu(self):
        """Phòng khám management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ PHÒNG KHÁM")
            print_separator(40,"=")
            print("1. 📋 Danh sách phòng khám")
            print("2. ➕ Thêm phòng khám mới")
            print("3. ❌ Xóa phòng khám")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_danh_sach_phong_kham_cho_user()
                case 2: self.add_phong_kham()
                case 3: self.delete_phong_kham()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def dich_vu_menu(self):
        """Dịch vụ management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ DỊCH VỤ")
            print_separator(40,"=")
            print("1. 📋 Danh sách dịch vụ")
            print("2. ➕ Thêm dịch vụ mới")
            print("3. ❌ Xóa dịch vụ")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_danh_sach_dich_vu_cho_user()
                case 2: self.add_dich_vu()
                case 3: self.delete_dich_vu()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def benh_nhan_menu(self):
        """Bệnh nhân management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ BỆNH NHÂN")
            print_separator(40,"=")
            print("1. 📋 Danh sách bệnh nhân")
            print("2. ➕ Thêm bệnh nhân mới")
            print("3. 🔍 Tìm kiếm bệnh nhân theo CCCD")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_danh_sach_benh_nhan_cho_admin()
                case 2: self.add_benh_nhan()
                case 3: self.search_benh_nhan()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def tiep_nhan_menu(self):
        """Tiếp nhận management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ TIẾP NHẬN")
            print_separator(40,"=")
            print("1. 📱 Quét QR code đăng ký")
            print("2. ➕ Đăng ký tiếp nhận mới")
            print("3. 📋 Danh sách tiếp nhận")
            print("4. ❌ Hủy tiếp nhận")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.qr_scan_tiep_nhan()
                case 2: self.add_tiep_nhan()
                case 3: self.controller.hien_thi_danh_sach_tiep_nhan_cho_admin()
                case 4: self.cancel_tiep_nhan()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def bac_si_menu(self):
        """Bac si management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ BÁC SĨ")
            print_separator(40,"=")
            print("1. 📋 Danh sách bác sĩ")
            print("2. ➕ Thêm bác sĩ mới")
            print("3. 🔄 Gán bác sĩ vào phòng khám")
            print("4. 👨‍⚕️ Danh sách bác sĩ theo phòng khám")
            print("5. ❌ Xóa bác sĩ")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")

            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_danh_sach_bac_si_cho_user()
                case 2: self.add_bac_si()
                case 3: self.assign_bac_si_to_phong_kham()
                case 4: self.list_bac_si_by_phong_kham()
                case 5: self.delete_bac_si()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def user_management_menu(self):
        """User management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ NGƯỜI DÙNG")
            print_separator(40,"=")
            print("1. 📋 Danh sách người dùng")
            print("2. ➕ Tạo tài khoản mới")
            print("3. 🔄 Thay đổi mật khẩu")
            print("4. 🔄 Thay đổi quyền")
            print("5. ❌ Xóa tài khoản")
            print("0. ⬅️  Quay lại menu chính")
            print_separator(40,"=")
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.list_users()
                case 2: self.create_user()
                case 3: self.change_password()
                case 4: self.change_role()
                case 5: self.delete_user()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def report_menu(self):
        """Enhanced Report and Excel export submenu"""
        while True:
            print("\n" + "="*60)
            print("           📊 BÁO CÁO & XUẤT EXCEL - NÂNG CAP")
            print_separator(60,"=")
            print("📋 XUẤT DANH SÁCH CƠ BẢN:")
            print("  1. � Xuất danh sách bệnh nhân")
            print("  2. 🏥 Xuất danh sách tiếp nhận")  
            print("  3. 🩺 Xuất báo cáo dịch vụ")
            print("  4. 🏨 Xuất báo cáo phòng khám")
            print("  5. ⚕️  Xuất báo cáo bác sĩ")
            print()
            print("📊 BÁO CÁO THỐNG KÊ & PHÂN TÍCH:")
            print("  6. 📈 Báo cáo thống kê tổng hợp")
            print("  7. 💰 Báo cáo doanh thu & phân tích")
            print("  8. 📅 Báo cáo hoạt động hôm nay")
            print("  9. 📋 Báo cáo tổng hợp đa trang")
            print()
            print("📁 QUẢN LÝ FILE:")
            print(" 10. 📂 Mở thư mục báo cáo")
            print(" 11. 🧹 Dọn dẹp file cũ")
            print()
            print("  0. ⬅️  Quay lại menu chính")
            print_separator(60,"=")
            print("💡 Tất cả file báo cáo được lưu trong thư mục 'reports'")
            
            try:
                choice = int(input("\n➤ Chọn chức năng: ").strip())
            except ValueError:
                error("Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.export_benh_nhan()
                case 2: self.export_tiep_nhan()
                case 3: self.export_dich_vu_report()
                case 4: self.export_phong_kham_report()
                case 5: self.export_bac_si_report()
                case 6: self.export_statistical_report()
                case 7: self.export_revenue_report()
                case 8: self.export_daily_report()
                case 9: self.export_summary_report()
                case 10: self.open_reports_folder()
                case 11: self.cleanup_old_reports()
                case 0: break
                case _: error("Chức năng không tồn tại!")

    def open_reports_folder(self):
        """Open reports folder in file manager"""
        try:
            import subprocess
            import platform
            reports_path = os.path.abspath("reports")
            
            if not os.path.exists(reports_path):
                error(f"Thư mục báo cáo không tồn tại: {reports_path}")
                return
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", reports_path])
            elif system == "Windows":
                subprocess.run(["explorer", reports_path])
            elif system == "Linux":
                subprocess.run(["xdg-open", reports_path])
            else:
                print(f"📁 Đường dẫn thư mục báo cáo: {reports_path}")
                return
                
            success(f"Đã mở thư mục báo cáo: {reports_path}")
            
        except Exception as e:
            error(f"Không thể mở thư mục: {e}")
            print(f"📁 Đường dẫn thủ công: {os.path.abspath('reports')}")

    def cleanup_old_reports(self):
        """Clean up old report files"""
        try:
            import glob
            from datetime import datetime, timedelta
            
            # Ask for retention days
            try:
                days = int(input("Xóa báo cáo cũ hơn bao nhiêu ngày? (mặc định 30): ").strip() or "30")
            except ValueError:
                days = 30
            
            cutoff_date = datetime.now() - timedelta(days=days)
            reports_path = "reports"
            
            if not os.path.exists(reports_path):
                error("Thư mục báo cáo không tồn tại!")
                return
            
            # Find old files
            old_files = []
            for root, dirs, files in os.walk(reports_path):
                for file in files:
                    if file.endswith(('.xlsx', '.csv')):
                        file_path = os.path.join(root, file)
                        file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                        if file_time < cutoff_date:
                            old_files.append((file_path, file_time))
            
            if not old_files:
                success(f"Không có báo cáo nào cũ hơn {days} ngày!")
                return
            
            print(f"\n📋 Tìm thấy {len(old_files)} file báo cáo cũ:")
            for file_path, file_time in old_files:
                print(f"  • {os.path.basename(file_path)} ({file_time.strftime('%d/%m/%Y')})")
            
            confirm = input(f"\n⚠️  Xác nhận xóa {len(old_files)} file? (y/n): ").strip().lower()
            if confirm == 'y':
                deleted = 0
                for file_path, _ in old_files:
                    try:
                        os.remove(file_path)
                        deleted += 1
                    except Exception as e:
                        error(f"Không thể xóa {os.path.basename(file_path)}: {e}")
                
                success(f"Đã xóa {deleted}/{len(old_files)} file báo cáo cũ!")
            else:
                error("Đã hủy thao tác dọn dẹp.")
                
        except Exception as e:
            error(f"Lỗi khi dọn dẹp báo cáo: {e}")

    # =============== IMPLEMENTATION METHODS ===============

    def add_phong_kham(self):
        """Add new phòng khám"""
        try:
            ma = input("Mã phòng: ").strip()
            ten = input("Tên phòng: ").strip()
            if not ma or not ten:
                error("Mã phòng và tên phòng không được để trống!")
                return
            n = self.controller.model.pk_repo.create(ma, ten, self.current_user_id)
            success(f"Đã thêm phòng khám thành công (ID: {n})")
        except Exception as e:
            error(f"Lỗi khi thêm phòng khám: {e}")

    def delete_phong_kham(self):
        """Delete phòng khám"""
        try:
            ma = input("Nhập mã phòng cần xóa: ").strip()
            if not ma:
                error("Mã phòng không được để trống!")
                return
            n = self.controller.model.pk_repo.delete_by_ma(ma)
            if n > 0:
                success(f"Đã xóa {n} phòng khám")
            else:
                error("Không tìm thấy phòng khám với mã đã nhập")
        except Exception as e:
            error(f"Lỗi khi xóa phòng khám: {e}")

    def add_dich_vu(self):
        """Add new dịch vụ"""
        try:
            ma = input("Mã dịch vụ: ").strip()
            ten = input("Tên dịch vụ: ").strip()
            gia = int(input("Giá dịch vụ: ").strip())
            if not ma or not ten:
                error("Mã và tên dịch vụ không được để trống!")
                return
            n = self.controller.model.dv_repo.create(ma, ten, gia, self.current_user_id)
            success(f"Đã thêm dịch vụ thành công (ID: {n})")
        except ValueError:
            error("Giá dịch vụ phải là số!")
        except Exception as e:
            error(f"Lỗi khi thêm dịch vụ: {e}")

    def delete_dich_vu(self):
        """Delete dịch vụ"""
        try:
            ma = input("Nhập mã dịch vụ cần xóa: ").strip()
            if not ma:
                error("Mã dịch vụ không được để trống!")
                return
            n = self.controller.model.dv_repo.delete_by_ma(ma)
            if n > 0:
                success(f"Đã xóa {n} dịch vụ")
            else:
                error("Không tìm thấy dịch vụ với mã đã nhập")
        except Exception as e:
            error(f"Lỗi khi xóa dịch vụ: {e}")

    def add_benh_nhan(self):
        """Add new bệnh nhân with comprehensive validation"""
        try:
            from utils.validation_utils import (
                input_cccd_with_validation, 
                input_full_name_with_validation,
                input_gender_with_recommendation,
                input_birth_date_with_validation,
                input_ward_commune_with_validation,
                input_province_with_recommendation,
                display_patient_confirmation_info,
                display_existing_patient_info,
                confirm_with_default_yes
            )
            
            print("\n" + "="*50)
            print("           THÊM BỆNH NHÂN MỚI")
            print_separator(50,"=")
            
            # Step 1: Input and validate CCCD (12 digits required)
            so_cccd = input_cccd_with_validation()
            
            # Step 2: Check if CCCD already exists
            existing_patient = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if existing_patient:
                warning("CCCD ĐÃ TỒN TẠI TRONG HỆ THỐNG!")
                display_existing_patient_info(existing_patient)
                error("Không thể tạo bệnh nhân trùng CCCD!")
                print("Vui lòng kiểm tra lại hoặc sử dụng chức năng tìm kiếm bệnh nhân.")
                return
            
            # Step 3: Input other information with validation and recommendations
            ho_ten = input_full_name_with_validation()
            gioi_tinh = input_gender_with_recommendation(so_cccd)
            
            # Step 4: Input and validate birth date (multiple formats supported)
            ngay_sinh = input_birth_date_with_validation()
            
            # Step 5: Input address information with recommendations
            print("\n🏠 Thông tin địa chỉ:")
            phuong_xa = input_ward_commune_with_validation()
            tinh = input_province_with_recommendation(so_cccd)
            
            # Step 6: Display confirmation information (similar to QR creation)
            display_patient_confirmation_info(ho_ten, gioi_tinh, ngay_sinh, so_cccd)
            
            # Step 7: Confirm before saving (default Y)
            if confirm_with_default_yes("\n📝 Bạn có muốn lưu thông tin bệnh nhân này không?"):
                # Create patient with address information
                self.controller.them_benh_nhan_full(ho_ten, gioi_tinh, ngay_sinh, so_cccd, phuong_xa, tinh)
                
                print("\n✅ Đã thêm bệnh nhân thành công!")
                
                # Display created patient information
                created_patient = self.controller.model.bn_repo.get_by_cccd(so_cccd)
                if created_patient:
                    print("\n" + "="*60)
                    print("           THÔNG TIN BỆNH NHÂN VỪA TẠO")
                    print_separator(60,"=")
                    print(f"🆔 Mã BN: {created_patient.ma_bn}")
                    print(f"📋 PID: {created_patient.pid}")
                    print(f"📱 CCCD: {created_patient.so_cccd}")
                    print(f"👤 Họ tên: {created_patient._ho_ten}")
                    print(f"⚤ Giới tính: {created_patient._gioi_tinh}")
                    print(f"🎂 Năm sinh: {created_patient.nam_sinh}")
                    if phuong_xa:
                        print(f"🏘️  Phường/Xã: {phuong_xa}")
                    print(f"🏙️  Tỉnh/TP: {tinh}")
                    print_separator(60,"=")
            else:
                print("\n❌ Đã hủy thêm bệnh nhân.")
                
        except KeyboardInterrupt:
            print("\n\n❌ Đã hủy thêm bệnh nhân.")
        except Exception as e:
            error(f"Lỗi khi thêm bệnh nhân: {e}")

    def search_benh_nhan(self):
        """Search bệnh nhân by CCCD"""
        try:
            so_cccd = input("Nhập số CCCD cần tìm: ").strip()
            if not so_cccd:
                error("Số CCCD không được để trống!")
                return
            bn = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if bn:
                success("Tìm thấy bệnh nhân:")
                print(bn)
            else:
                error("Không tìm thấy bệnh nhân với CCCD đã nhập")
        except Exception as e:
            error(f"Lỗi khi tìm kiếm: {e}")

    def add_tiep_nhan(self):
        """Add new tiếp nhận with enhanced step-by-step display"""
        try:
            print("📋 Đăng ký tiếp nhận - Mã tiếp nhận sẽ được tự động tạo")
            
            # Step 1: Input CCCD and display patient info
            so_cccd = input("CCCD bệnh nhân: ").strip()
            if not so_cccd:
                error("CCCD không được để trống!")
                return
            
            # Get patient info and display
            patient = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if not patient:
                error("Không tìm thấy bệnh nhân với CCCD này!")
                return
            
            # Display patient information
            from utils.validation_utils import display_patient_summary
            print("\n📋 THÔNG TIN BỆNH NHÂN")
            print_separator(50,"=")
            display_patient_summary(patient)
            
            # Step 2: Display service list and get service selection
            print("\n💉 DANH SÁCH DỊCH VỤ KỸ THUẬT")
            print_separator(50,"=")
            self.controller.hien_thi_danh_sach_dich_vu_cho_user()
            
            ma_dv = input("\nMã dịch vụ: ").strip()
            if not ma_dv:
                error("Mã dịch vụ không được để trống!")
                return
            
            # Validate service exists
            dich_vu = self.controller.model.dv_repo.get_by_ma(ma_dv)
            if not dich_vu:
                error("Không tìm thấy dịch vụ với mã này!")
                return
            
            # Step 3: Display clinic list and get clinic selection
            print("\n🏥 DANH SÁCH PHÒNG KHÁM")
            print_separator(50,"=")
            self.controller.hien_thi_danh_sach_phong_kham_cho_user()
            
            ma_pk = input("\nMã phòng khám: ").strip()
            if not ma_pk:
                error("Mã phòng khám không được để trống!")
                return
            
            # Validate clinic exists
            phong_kham = self.controller.model.pk_repo.get_by_ma(ma_pk)
            if not phong_kham:
                error("Không tìm thấy phòng khám với mã này!")
                return
            
            # Step 4: Input reason for examination
            ly_do = input("\nLý do khám: ").strip()
            if not ly_do:
                error("Lý do khám không được để trống!")
                return
            
            ma_bs = input("Mã bác sĩ (để trống để auto-assign): ").strip()
            
            # Step 5: Create reception and display comprehensive summary
            tiep_nhan, cost = self.controller.tiep_nhan_enhanced(so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
            
            if tiep_nhan:
                print("\n✅ THÔNG TIN TỔNG HỢP TIẾP NHẬN")
                print_separator(50,"=")
                from utils.validation_utils import display_reception_summary
                display_reception_summary(tiep_nhan, cost)
                
                from utils.validation_utils import confirm_with_default_yes
                if confirm_with_default_yes("\nXác nhận đăng ký tiếp nhận"):
                    success(f"Đăng ký tiếp nhận thành công! Mã tiếp nhận: {tiep_nhan.ma_tn}")
                else:
                    # Cancel the registration (delete the created record)
                    self.controller.model.tn_repo.delete_by_ma(tiep_nhan.ma_tn)
                    error("Đã hủy đăng ký tiếp nhận!")
            
        except Exception as e:
            error(f"Lỗi khi đăng ký tiếp nhận: {e}")

    def cancel_tiep_nhan(self):
        """Cancel tiếp nhận"""
        try:
            ma_tn = input("Nhập mã tiếp nhận cần hủy: ").strip()
            if not ma_tn:
                error("Mã tiếp nhận không được để trống!")
                return
            self.controller.huy_tiep_nhan(ma_tn)
        except Exception as e:
            error(f"Lỗi khi hủy tiếp nhận: {e}")

    def qr_scan_tiep_nhan(self):
        """QR scan for patient registration and tiếp nhận"""
        try:
            print("\n📱 QUÉT QR CODE ĐĂNG KÝ TIẾP NHẬN")
            print_separator(50,"=")
            print("Vui lòng nhập chuỗi QR code từ CCCD/CMND")
            print("Định dạng: CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi|NgayCap")
            print("Ví dụ: 058090000000|26430000|Nguyễn Văn An|01011990|Nam|Thôn La Vang 1, Ninh Thuận|01012020")
            
            qr_string = input("📱 QR Code: ").strip()
            if not qr_string:
                error("QR code không được để trống!")
                return
            
            # Process QR scan
            patient = self.controller.process_qr_scan(qr_string)
            if not patient:
                return
            
            print(f"\n✅ Sẽ sử dụng bệnh nhân: {patient._ho_ten} ({patient.ma_bn})")
            
            # Continue with tiếp nhận registration
            print("\n📋 THÔNG TIN DỊCH VỤ & PHÒNG KHÁM")
            print_separator(40)
            
            # Show services
            print("Danh sách dịch vụ:")
            self.controller.hien_thi_danh_sach_dich_vu_cho_user()
            
            ma_dv = input("\nMã dịch vụ: ").strip()
            if not ma_dv:
                error("Mã dịch vụ không được để trống!")
                return
            
            # Show clinics
            print("\nDanh sách phòng khám:")
            self.controller.hien_thi_danh_sach_phong_kham_cho_user()
            
            ma_pk = input("\nMã phòng khám: ").strip()
            if not ma_pk:
                error("Mã phòng khám không được để trống!")
                return
                
            ly_do = input("Lý do khám: ").strip()
            if not ly_do:
                error("Lý do khám không được để trống!")
                return
                
            ma_bs = input("Mã bác sĩ (để trống để auto-assign): ").strip()
            
            # Create tiếp nhận
            self.controller.tiep_nhan(patient.so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
            
        except Exception as e:
            error(f"Lỗi khi xử lý QR scan: {e}")

    def user_register_appointment(self):
        """User registration for appointment - Enhanced version with sequential display"""
        try:
            print("\n🏥 ĐĂNG KÝ KHÁM BỆNH")
            print_separator(50,"=")
            print("📋 Hệ thống sẽ tự động lấy thông tin của bạn từ tài khoản")
            print(f"👤 Tài khoản: {self.username}")
            print_separator(50,"=")
            
            # Step 1: Display services list and get service selection
            print("\n🩺 BƯỚC 1: CHỌN DỊCH VỤ KHÁM")
            print_separator(40)
            self.controller.hien_thi_danh_sach_dich_vu_cho_user()
            
            ma_dv = ""
            while not ma_dv.strip():
                ma_dv = input("\n➤ Nhập mã dịch vụ: ").strip()
                if not ma_dv:
                    error("Mã dịch vụ không được để trống! Vui lòng chọn từ danh sách trên.")
            
            # Validate service exists
            dich_vu = self.controller.model.dv_repo.get_by_ma(ma_dv)
            if not dich_vu:
                error(f"Không tìm thấy dịch vụ với mã '{ma_dv}'!")
                return
            
            success(f"Đã chọn dịch vụ: {dich_vu._ma_dv} - {dich_vu._ten_dv} ({dich_vu._gia:,}đ)")
            
            # Step 2: Display clinics list and get clinic selection
            print("\n🏥 BƯỚC 2: CHỌN PHÒNG KHÁM")
            print_separator(40)
            self.controller.hien_thi_danh_sach_phong_kham_cho_user()
            
            ma_pk = ""
            while not ma_pk.strip():
                ma_pk = input("\n➤ Nhập mã phòng khám: ").strip()
                if not ma_pk:
                    error("Mã phòng khám không được để trống! Vui lòng chọn từ danh sách trên.")
            
            # Validate clinic exists
            phong_kham = self.controller.model.pk_repo.get_by_ma(ma_pk)
            if not phong_kham:
                error(f"Không tìm thấy phòng khám với mã '{ma_pk}'!")
                return
            
            success(f"Đã chọn phòng khám: {phong_kham._ma_phong} - {phong_kham._ten_phong}")
            
            # Step 3: Input reason (mandatory)
            print("\n📝 BƯỚC 3: LÝ DO KHÁM BỆNH")
            print_separator(40)
            ly_do = ""
            while not ly_do.strip():
                ly_do = input("➤ Nhập lý do khám: ").strip()
                if not ly_do:
                    error("Lý do khám không được để trống!")
            
            success(f"Lý do khám: {ly_do}")
            
            # Step 4: Optional doctor selection
            print("\n👨‍⚕️ BƯỚC 4: CHỌN BÁC SĨ (TÙY CHỌN)")
            print_separator(40)
            print("💡 Để trống để hệ thống tự động gán bác sĩ theo phòng khám")
            self.controller.hien_thi_danh_sach_bac_si_cho_user()
            
            ma_bs = input("\n➤ Nhập mã bác sĩ (để trống để tự động chọn): ").strip()
            
            if ma_bs:
                # Validate doctor exists if provided
                bac_si = self.controller.model.bs_repo.get_by_ma(ma_bs)
                if not bac_si:
                    error(f"Không tìm thấy bác sĩ với mã '{ma_bs}'! Sẽ tự động gán bác sĩ.")
                    ma_bs = ""
                else:
                    success(f"Đã chọn bác sĩ: {bac_si.ma_bs} - {bac_si.ho_ten} ({bac_si.chuyen_khoa})")
            else:
                success("Sẽ tự động gán bác sĩ theo phòng khám")
            
            # Step 5: Confirm and register
            print("\n🔄 BƯỚC 5: XÁC NHẬN ĐĂNG KÝ")
            print_separator(40)
            print(f"📋 Dịch vụ: {dich_vu._ten_dv} ({dich_vu._gia:,}đ)")
            print(f"🏥 Phòng khám: {phong_kham._ten_phong}")
            print(f"📝 Lý do: {ly_do}")
            print(f"👨‍⚕️ Bác sĩ: {bac_si.ho_ten if ma_bs and 'bac_si' in locals() else 'Tự động gán'}")
            
            confirm = input("\n✅ Xác nhận đăng ký? (y/n): ").strip().lower()
            if confirm == 'y':
                # Use username as CCCD for registration
                self.controller.tiep_nhan_cho_user(self.username, ma_dv, ma_pk, ly_do, ma_bs)
            else:
                error("Đã hủy đăng ký khám bệnh.")
            
        except Exception as e:
            error(f"Lỗi khi đăng ký khám: {e}")

    # =============== USER MANAGEMENT METHODS ===============

    def list_users(self):
        """List all users with enhanced formatting"""
        try:
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT user_id, username, role, pass, created_at FROM [user] ORDER BY created_at DESC")
            users = cur.fetchall()
            conn.close()
            
            if users:
                print("\n� DANH SÁCH NGƯỜI DÙNG")
                print_separator(80,"=")
                print(f"{'STT':<4} {'Username':<20} {'Role':<8} {'Mật khẩu':<12} {'Ngày tạo':<20}")
                print_separator(80)
                for i, user in enumerate(users, 1):
                    created_date = user.created_at.strftime("%d/%m/%Y %H:%M") if user.created_at else "N/A"
                    password = getattr(user, 'pass', 'N/A')
                    # Mask password for security
                    masked_password = '*' * len(password) if password != 'N/A' else 'N/A'
                    print(f"{i:<4} {user.username:<20} {user.role:<8} {masked_password:<12} {created_date:<20}")
                print_separator(80,"=")
                print(f"📊 Tổng cộng: {len(users)} người dùng")
            else:
                error("Không có người dùng nào trong hệ thống")
        except Exception as e:
            error(f"Lỗi khi lấy danh sách người dùng: {e}")

    def create_user(self):
        """Create new user"""
        try:
            username = input("Tên đăng nhập: ").strip()
            password = input("Mật khẩu: ").strip()
            role = input("Quyền (ADMIN/USER): ").strip().upper()
            
            if not all([username, password, role]):
                error("Tất cả thông tin không được để trống!")
                return
                
            if role not in ["ADMIN", "USER"]:
                error("Quyền chỉ có thể là ADMIN hoặc USER!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM [user] WHERE username = ?", (username,))
            if cur.fetchone():
                error("Tên đăng nhập đã tồn tại!")
                conn.close()
                return
                
            cur.execute("INSERT INTO [user](username, role, pass) VALUES (?, ?, ?)", (username, role, password))
            conn.commit()
            conn.close()
            success(f"Đã tạo tài khoản thành công cho {username}")
        except Exception as e:
            error(f"Lỗi khi tạo tài khoản: {e}")

    def change_password(self):
        """Change user password"""
        try:
            username = input("Tên đăng nhập: ").strip()
            new_password = input("Mật khẩu mới: ").strip()
            
            if not all([username, new_password]):
                error("Tên đăng nhập và mật khẩu mới không được để trống!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE [user] SET pass = ? WHERE username = ?", (new_password, username))
            if cur.rowcount > 0:
                success(f"Đã thay đổi mật khẩu cho {username}")
            else:
                error("Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            error(f"Lỗi khi thay đổi mật khẩu: {e}")

    def change_role(self):
        """Change user role"""
        try:
            username = input("Tên đăng nhập: ").strip()
            new_role = input("Quyền mới (ADMIN/USER): ").strip().upper()
            
            if not all([username, new_role]):
                error("Tên đăng nhập và quyền mới không được để trống!")
                return
                
            if new_role not in ["ADMIN", "USER"]:
                error("Quyền chỉ có thể là ADMIN hoặc USER!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE [user] SET role = ? WHERE username = ?", (new_role, username))
            if cur.rowcount > 0:
                success(f"Đã thay đổi quyền cho {username} thành {new_role}")
            else:
                error("Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            error(f"Lỗi khi thay đổi quyền: {e}")

    def delete_user(self):
        """Delete user"""
        try:
            username = input("Tên đăng nhập cần xóa: ").strip()
            if not username:
                error("Tên đăng nhập không được để trống!")
                return
                
            confirm = input(f"Bạn có chắc muốn xóa tài khoản '{username}'? (y/n): ").strip().lower()
            if confirm != 'y':
                error("Đã hủy thao tác xóa")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM [user] WHERE username = ?", (username,))
            if cur.rowcount > 0:
                success(f"Đã xóa tài khoản {username}")
            else:
                error("Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            error(f"Lỗi khi xóa tài khoản: {e}")

    # =============== ENHANCED EXCEL EXPORT METHODS ===============
    
    def __init_report_manager(self):
        """Initialize report manager"""
        if not hasattr(self, 'report_manager'):
            from utils.report_utils import ReportManager
            self.report_manager = ReportManager()
        return self.report_manager

    def export_benh_nhan(self):
        """Export bệnh nhân list to Excel with enhanced features"""
        try:
            benh_nhan_list = self.controller.model.list_benh_nhan()
            if not benh_nhan_list:
                error("Không có dữ liệu bệnh nhân để xuất!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data using utility functions
            from utils.report_utils import format_benh_nhan_data
            data = format_benh_nhan_data(benh_nhan_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("DanhSach_BenhNhan", "xlsx")
            filepath = report_mgr.get_report_path("benh_nhan", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                "Danh sách bệnh nhân",
                "📋 DANH SÁCH BỆNH NHÂN",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất danh sách bệnh nhân: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Tổng số bản ghi: {len(data)}")
            else:
                error("Không thể xuất file!")
                
        except Exception as e:
            error(f"Lỗi khi xuất danh sách bệnh nhân: {e}")

    def export_tiep_nhan(self):
        """Export tiếp nhận list to Excel with enhanced features"""
        try:
            tiep_nhan_list = self.controller.model.list_tiep_nhan()
            if not tiep_nhan_list:
                error("Không có dữ liệu tiếp nhận để xuất!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data using utility functions
            from utils.report_utils import format_tiep_nhan_data
            data = format_tiep_nhan_data(tiep_nhan_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("DanhSach_TiepNhan", "xlsx")
            filepath = report_mgr.get_report_path("tiep_nhan", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                "Danh sách tiếp nhận",
                "🏥 DANH SÁCH TIẾP NHẬN",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất danh sách tiếp nhận: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Tổng số bản ghi: {len(data)}")
            else:
                error("Không thể xuất file!")
                
        except Exception as e:
            error(f"Lỗi khi xuất danh sách tiếp nhận: {e}")

    def export_dich_vu_report(self):
        """Export dịch vụ report to Excel with enhanced features"""
        try:
            dich_vu_list = self.controller.model.list_dich_vu()
            if not dich_vu_list:
                error("Không có dữ liệu dịch vụ để xuất!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data using utility functions
            from utils.report_utils import format_dich_vu_data
            data = format_dich_vu_data(dich_vu_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("BaoCao_DichVu", "xlsx")
            filepath = report_mgr.get_report_path("dich_vu", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                "Báo cáo dịch vụ",
                "🩺 BÁO CÁO DỊCH VỤ",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo dịch vụ: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Tổng số bản ghi: {len(data)}")
            else:
                error("Không thể xuất file!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo dịch vụ: {e}")

    def export_phong_kham_report(self):
        """Export phòng khám report to Excel with enhanced features"""
        try:
            phong_kham_list = self.controller.model.list_phong_kham()
            if not phong_kham_list:
                error("Không có dữ liệu phòng khám để xuất!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data using utility functions
            from utils.report_utils import format_phong_kham_data
            data = format_phong_kham_data(phong_kham_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("BaoCao_PhongKham", "xlsx")
            filepath = report_mgr.get_report_path("phong_kham", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                "Báo cáo phòng khám",
                "🏥 BÁO CÁO PHÒNG KHÁM",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo phòng khám: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Tổng số bản ghi: {len(data)}")
            else:
                error("Không thể xuất file!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo phòng khám: {e}")

    def export_summary_report(self):
        """Export comprehensive summary report with multiple sheets"""
        try:
            # Get all data
            benh_nhan_list = self.controller.model.list_benh_nhan()
            tiep_nhan_list = self.controller.model.list_tiep_nhan()
            dich_vu_list = self.controller.model.list_dich_vu()
            phong_kham_list = self.controller.model.list_phong_kham()
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Prepare data for multiple sheets
            from utils.report_utils import (
                format_benh_nhan_data, format_tiep_nhan_data, 
                format_dich_vu_data, format_phong_kham_data
            )
            
            data_dict = {}
            
            # Summary overview
            summary_data = [
                {'Chỉ số': 'Tổng số bệnh nhân', 'Giá trị': len(benh_nhan_list)},
                {'Chỉ số': 'Tổng số tiếp nhận', 'Giá trị': len(tiep_nhan_list)},
                {'Chỉ số': 'Tổng số dịch vụ', 'Giá trị': len(dich_vu_list)},
                {'Chỉ số': 'Tổng số phòng khám', 'Giá trị': len(phong_kham_list)},
                {'Chỉ số': 'Thời điểm xuất báo cáo', 'Giá trị': datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            ]
            data_dict['Tổng hợp'] = summary_data
            
            # Add detailed sheets
            if benh_nhan_list:
                data_dict['Chi tiết bệnh nhân'] = format_benh_nhan_data(benh_nhan_list)
            if tiep_nhan_list:
                data_dict['Chi tiết tiếp nhận'] = format_tiep_nhan_data(tiep_nhan_list)
            if dich_vu_list:
                data_dict['Chi tiết dịch vụ'] = format_dich_vu_data(dich_vu_list)
            if phong_kham_list:
                data_dict['Chi tiết phòng khám'] = format_phong_kham_data(phong_kham_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("BaoCao_TongHop_ChiTiet", "xlsx")
            filepath = report_mgr.get_report_path("tong_hop", filename)
            
            # Create summary report
            result_path = report_mgr.create_summary_report(
                data_dict, 
                filepath,
                "📊 BÁO CÁO TỔNG HỢP HỆ THỐNG",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo tổng hợp: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📄 Số sheets: {len(data_dict)}")
                for sheet_name, sheet_data in data_dict.items():
                    print(f"   • {sheet_name}: {len(sheet_data) if isinstance(sheet_data, list) else 'N/A'} bản ghi")
            else:
                error("Không thể xuất báo cáo tổng hợp!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo tổng hợp: {e}")

    # =============== NEW STATISTICAL REPORTS ===============
    
    def export_statistical_report(self):
        """Export comprehensive statistical report"""
        try:
            report_mgr = self.__init_report_manager()
            result_path = report_mgr.export_statistical_report(
                self.controller.model, 
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo thống kê: {os.path.basename(result_path)}")
                print(f"📁 Vị trí file: {result_path}")
            else:
                error("Không thể xuất báo cáo thống kê!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo thống kê: {e}")

    def export_revenue_report(self):
        """Export revenue analysis report"""
        try:
            report_mgr = self.__init_report_manager()
            result_path = report_mgr.export_revenue_report(
                self.controller.model, 
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo doanh thu: {os.path.basename(result_path)}")
                print(f"📁 Vị trí file: {result_path}")
            else:
                error("Không thể xuất báo cáo doanh thu!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo doanh thu: {e}")

    def export_bac_si_report(self):
        """Export bác sĩ report with clinic assignments"""
        try:
            # Get bác sĩ data
            try:
                bac_si_list = self.controller.model.list_bac_si()
            except:
                error("Không thể lấy danh sách bác sĩ!")
                return
            
            if not bac_si_list:
                error("Không có dữ liệu bác sĩ để xuất!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data using utility functions
            from utils.report_utils import format_bac_si_data
            data = format_bac_si_data(bac_si_list)
            
            # Generate filename and path
            filename = report_mgr.generate_filename("BaoCao_BacSi", "xlsx")
            filepath = report_mgr.get_report_path("phong_kham", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                "Báo cáo bác sĩ",
                "⚕️ BÁO CÁO BÁC SĨ",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo bác sĩ: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Tổng số bản ghi: {len(data)}")
            else:
                error("Không thể xuất file!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo bác sĩ: {e}")

    def export_daily_report(self):
        """Export daily activity report"""
        try:
            from datetime import date
            today = date.today()
            
            # Filter today's tiếp nhận
            tiep_nhan_list = self.controller.model.list_tiep_nhan()
            today_tiep_nhan = []
            
            for tn in tiep_nhan_list:
                # Giả sử có thuộc tính ngay_tao
                if hasattr(tn, 'ngay_tao') and tn.ngay_tao:
                    tn_date = tn.ngay_tao.date() if hasattr(tn.ngay_tao, 'date') else tn.ngay_tao
                    if tn_date == today:
                        today_tiep_nhan.append(tn)
            
            if not today_tiep_nhan:
                error(f"Không có dữ liệu tiếp nhận ngày {today.strftime('%d/%m/%Y')}!")
                return
            
            # Initialize report manager
            report_mgr = self.__init_report_manager()
            
            # Format data
            from utils.report_utils import format_tiep_nhan_data
            data = format_tiep_nhan_data(today_tiep_nhan)
            
            # Generate filename and path
            filename = report_mgr.generate_filename(
                "BaoCao_NgayHienTai", "xlsx", 
                suffix=today.strftime('%Y%m%d')
            )
            filepath = report_mgr.get_report_path("thong_ke", filename)
            
            # Create Excel with styling
            result_path = report_mgr.create_excel_with_styling(
                data, 
                filepath,
                f"Báo cáo ngày {today.strftime('%d/%m/%Y')}",
                f"📅 BÁO CÁO HOẠT ĐỘNG NGÀY {today.strftime('%d/%m/%Y')}",
                f"{self.user_role} - {self.username}"
            )
            
            if result_path:
                success(f"Đã xuất báo cáo ngày {today.strftime('%d/%m/%Y')}: {filename}")
                print(f"📁 Vị trí file: {filepath}")
                print(f"📊 Số tiếp nhận trong ngày: {len(data)}")
            else:
                error("Không thể xuất báo cáo ngày!")
                
        except Exception as e:
            error(f"Lỗi khi xuất báo cáo ngày: {e}")


    # ===== BÁC SĨ MANAGEMENT METHODS =====
    def add_bac_si(self):
        """Add new bac si"""
        try:
            ma_bs = input("Mã bác sĩ: ").strip()
            ho_ten = input("Họ tên bác sĩ: ").strip()
            chuyen_khoa = input("Chuyên khoa: ").strip()
            so_dt = input("Số điện thoại: ").strip()
            email = input("Email: ").strip()
            
            if not all([ma_bs, ho_ten]):
                error("Mã bác sĩ và họ tên không được để trống!")
                return
                
            self.controller.them_bac_si(ma_bs, ho_ten, chuyen_khoa, so_dt, email)
            print("💡 Gợi ý: Sau khi thêm bác sĩ, bạn có thể gán bác sĩ vào phòng khám bằng chức năng 'Gán bác sĩ vào phòng khám'")
        except Exception as e:
            error(f"Lỗi khi thêm bác sĩ: {e}")

    def delete_bac_si(self):
        """Delete bac si"""
        try:
            ma_bs = input("Nhập mã bác sĩ cần xóa: ").strip()
            if not ma_bs:
                error("Mã bác sĩ không được để trống!")
                return
            
            confirm = input(f"Bạn có chắc chắn muốn xóa bác sĩ {ma_bs}? (y/n): ").strip().lower()
            if confirm == 'y':
                self.controller.xoa_bac_si(ma_bs)
            else:
                error("Đã hủy thao tác xóa.")
        except Exception as e:
            error(f"Lỗi khi xóa bác sĩ: {e}")

    def assign_bac_si_to_phong_kham(self):
        """Assign bac si to phong kham"""
        try:
            print("📋 Danh sách bác sĩ hiện tại:")
            self.controller.hien_thi_danh_sach_bac_si_cho_user()
            print("\n📋 Danh sách phòng khám:")
            self.controller.hien_thi_danh_sach_phong_kham_cho_user()
            
            ma_bs = input("\nNhập mã bác sĩ: ").strip()
            ma_phong = input("Nhập mã phòng khám (để trống để hủy gán): ").strip()
            
            if not ma_bs:
                error("Mã bác sĩ không được để trống!")
                return
                
            self.controller.gan_bac_si_phong_kham(ma_bs, ma_phong)
        except Exception as e:
            error(f"Lỗi khi gán bác sĩ vào phòng khám: {e}")

    def list_bac_si_by_phong_kham(self):
        """List bac si by phong kham"""
        try:
            print("📋 Danh sách phòng khám:")
            phong_kham_list = self.controller.model.list_phong_kham()
            for i, pk in enumerate(phong_kham_list, 1):
                print(f"{i}. {pk}")
            
            if not phong_kham_list:
                error("Không có phòng khám nào!")
                return
            
            choice = input("\nNhập số thứ tự phòng khám: ").strip()
            try:
                index = int(choice) - 1
                if 0 <= index < len(phong_kham_list):
                    pk = phong_kham_list[index]
                    print(f"\n👨‍⚕️ Danh sách bác sĩ tại {pk}:")
                    bac_si_list = self.controller.model.bs_repo.get_by_phong_kham(pk.pk_id)
                    if bac_si_list:
                        for bs in bac_si_list:
                            print(f"  {bs}")
                    else:
                        print("  ❌ Không có bác sĩ nào tại phòng khám này!")
                else:
                    error("Số thứ tự không hợp lệ!")
            except ValueError:
                error("Vui lòng nhập số hợp lệ!")
        except Exception as e:
            error(f"Lỗi khi liệt kê bác sĩ theo phòng khám: {e}")

    def migration_menu(self):
        """Migration dữ liệu tỉnh bệnh nhân theo NQ 202/2025/QH15"""
        try:
            from migration_hanh_chinh import run_full_migration, check_migration_status
            
            print("\n" + "="*60)
            print("🏛️  MIGRATION DỮ LIỆU TỈNH BỆNH NHÂN (NQ 202/2025/QH15)")
            print_separator(60,"=")
            print("📋 Chức năng này sẽ:")
            print("   • Tạo các bảng hành chính mới theo NQ 202/2025/QH15")
            print("   • Mapping dữ liệu từ 63 tỉnh cũ sang 34 đơn vị mới")
            print("   • Cập nhật thông tin tỉnh của tất cả bệnh nhân")
            print_separator(60,"=")
            
            check_migration_status()
            
            print("\n" + "⚠️ " + "="*58)
            print("  CẢNH BÁO: Thao tác này sẽ thay đổi cấu trúc database!")
            print("  Nên backup database trước khi thực hiện migration!")
            print_separator(60,"=")
            
            confirm = input("Bạn có chắc chắn muốn thực hiện migration? (y/n): ").strip().lower()
            
            if confirm == 'y':
                success = run_full_migration()
                if success:
                    print("\n✅ Migration hoàn thành thành công!")
                    print("💡 Từ giờ hệ thống sẽ sử dụng cấu trúc hành chính mới")
                else:
                    print("\n❌ Migration gặp lỗi!")
            else:
                error("Đã hủy thao tác migration.")
                
        except ImportError as e:
            error(f"Không thể import module migration: {e}")
        except Exception as e:
            error(f"Lỗi khi thực hiện migration: {e}")


def main():
    init_db(seed=True)

    view = View()
    model = Model()
    controller = Controller(view, model)
    user_repo = UserRepo()

    print_header("HỆ THỐNG QUẢN LÝ KHÁM BỆNH - ĐĂNG NHẬP",60)
    username = input("👤 Username: ").strip()
    password = input("🔒 Password: ").strip()
    print(username, password)
    user = user_repo.auth(username, password)

    if not user:
        error("Sai tài khoản hoặc mật khẩu!")
        return

    print(f"👋 Xin chào {'Quản trị viên' if user._role == 'ADMIN' else f'Bệnh nhân {username}'}! Quyền: {user._role}")
    
    # Initialize menu manager and start
    menu_manager = MenuManager(controller, user._user_id, user._role, username)
    menu_manager.main_menu()


if __name__ == "__main__":
    main()
