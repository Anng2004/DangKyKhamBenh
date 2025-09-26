# app.py
from db import init_db
from mvc import View, Model, Controller
from repositories import UserRepo
from datetime import datetime
import os

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
        """Main menu dispatcher based on user role"""
        if self.user_role.upper() == "ADMIN":
            self.admin_main_menu()
        else:
            self.user_main_menu()

    def admin_main_menu(self):
        """Admin main menu with module selection"""
        while True:
            print("\n" + "="*50)
            print("           HỆ THỐNG QUẢN LÝ KHÁM BỆNH")
            print("              MENU QUẢN TRỊ VIÊN")
            print("="*50)
            print("1. 🏥 Quản lý Phòng khám")
            print("2. 🩺 Quản lý Dịch vụ")
            print("3. 👥 Quản lý Bệnh nhân")
            print("4. 📋 Quản lý Tiếp nhận")
            print("5. �‍⚕️ Quản lý Bác sĩ")
            print("6. �👤 Quản lý Người dùng")
            print("7. 📊 Báo cáo & Xuất Excel")
            print("8. 🏛️ Migration dữ liệu tỉnh bệnh nhân")
            print("0. 🚪 Đăng xuất")
            print("="*50)
            
            try:
                choice = int(input("Chọn module: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.phong_kham_menu()
                case 2: self.dich_vu_menu()
                case 3: self.benh_nhan_menu()
                case 4: self.tiep_nhan_menu()
                case 5: self.bac_si_menu()
                case 6: self.user_management_menu()
                case 7: self.report_menu()
                case 8: self.migration_menu()
                case 0: print("👋 Đăng xuất..."); break
                case _: print("❌ Chức năng không tồn tại!")

    def user_main_menu(self):
        """User main menu with limited access"""
        while True:
            print("\n" + "="*50)
            print("           HỆ THỐNG ĐĂNG KÝ KHÁM BỆNH")
            print("                MENU BỆNH NHÂN")
            print("="*50)
            print("1. 👀 Xem thông tin dịch vụ")
            print("2. 🏥 Xem thông tin phòng khám")
            print("3. 📝 Đăng ký khám bệnh")
            print("4. 📋 Xem lịch sử khám")
            print("0. 🚪 Đăng xuất")
            print("="*50)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_dich_vu()
                case 2: self.controller.hien_thi_ds_phong_kham()
                case 3: self.user_register_appointment()
                case 4: self.controller.hien_thi_lich_su_kham_cua_user(self.username)
                case 0: print("👋 Đăng xuất..."); break
                case _: print("❌ Chức năng không tồn tại!")

    def phong_kham_menu(self):
        """Phòng khám management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ PHÒNG KHÁM")
            print("="*40)
            print("1. 📋 Danh sách phòng khám")
            print("2. ➕ Thêm phòng khám mới")
            print("3. ❌ Xóa phòng khám")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_phong_kham()
                case 2: self.add_phong_kham()
                case 3: self.delete_phong_kham()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def dich_vu_menu(self):
        """Dịch vụ management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ DỊCH VỤ")
            print("="*40)
            print("1. 📋 Danh sách dịch vụ")
            print("2. ➕ Thêm dịch vụ mới")
            print("3. ❌ Xóa dịch vụ")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_dich_vu()
                case 2: self.add_dich_vu()
                case 3: self.delete_dich_vu()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def benh_nhan_menu(self):
        """Bệnh nhân management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ BỆNH NHÂN")
            print("="*40)
            print("1. 📋 Danh sách bệnh nhân")
            print("2. ➕ Thêm bệnh nhân mới")
            print("3. 🔍 Tìm kiếm bệnh nhân theo CCCD")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_benh_nhan()
                case 2: self.add_benh_nhan()
                case 3: self.search_benh_nhan()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def tiep_nhan_menu(self):
        """Tiếp nhận management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ TIẾP NHẬN")
            print("="*40)
            print("1. 📋 Danh sách tiếp nhận")
            print("2. ➕ Đăng ký tiếp nhận mới")
            print("3. 📱 Quét QR code đăng ký")
            print("4. ❌ Hủy tiếp nhận")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_tiep_nhan()
                case 2: self.add_tiep_nhan()
                case 3: self.qr_scan_tiep_nhan()
                case 4: self.cancel_tiep_nhan()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def bac_si_menu(self):
        """Bac si management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ BÁC SĨ")
            print("="*40)
            print("1. 📋 Danh sách bác sĩ")
            print("2. ➕ Thêm bác sĩ mới")
            print("3. 🔄 Gán bác sĩ vào phòng khám")
            print("4. 👨‍⚕️ Danh sách bác sĩ theo phòng khám")
            print("5. ❌ Xóa bác sĩ")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)

            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.controller.hien_thi_ds_bac_si()
                case 2: self.add_bac_si()
                case 3: self.assign_bac_si_to_phong_kham()
                case 4: self.list_bac_si_by_phong_kham()
                case 5: self.delete_bac_si()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def user_management_menu(self):
        """User management submenu"""
        while True:
            print("\n" + "="*40)
            print("         QUẢN LÝ NGƯỜI DÙNG")
            print("="*40)
            print("1. 📋 Danh sách người dùng")
            print("2. ➕ Tạo tài khoản mới")
            print("3. 🔄 Thay đổi mật khẩu")
            print("4. 🔄 Thay đổi quyền")
            print("5. ❌ Xóa tài khoản")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.list_users()
                case 2: self.create_user()
                case 3: self.change_password()
                case 4: self.change_role()
                case 5: self.delete_user()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    def report_menu(self):
        """Report and Excel export submenu"""
        while True:
            print("\n" + "="*40)
            print("       BÁO CÁO & XUẤT EXCEL")
            print("="*40)
            print("1. 📊 Xuất danh sách bệnh nhân")
            print("2. 📊 Xuất danh sách tiếp nhận")
            print("3. 📊 Xuất báo cáo dịch vụ")
            print("4. 📊 Xuất báo cáo phòng khám")
            print("5. 📊 Báo cáo tổng hợp")
            print("0. ⬅️  Quay lại menu chính")
            print("="*40)
            
            try:
                choice = int(input("Chọn chức năng: ").strip())
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!"); continue

            match choice:
                case 1: self.export_benh_nhan()
                case 2: self.export_tiep_nhan()
                case 3: self.export_dich_vu_report()
                case 4: self.export_phong_kham_report()
                case 5: self.export_summary_report()
                case 0: break
                case _: print("❌ Chức năng không tồn tại!")

    # =============== IMPLEMENTATION METHODS ===============

    def add_phong_kham(self):
        """Add new phòng khám"""
        try:
            ma = input("Mã phòng: ").strip()
            ten = input("Tên phòng: ").strip()
            if not ma or not ten:
                print("❌ Mã phòng và tên phòng không được để trống!")
                return
            n = self.controller.model.pk_repo.create(ma, ten, self.current_user_id)
            print(f"✅ Đã thêm phòng khám thành công (ID: {n})")
        except Exception as e:
            print(f"❌ Lỗi khi thêm phòng khám: {e}")

    def delete_phong_kham(self):
        """Delete phòng khám"""
        try:
            ma = input("Nhập mã phòng cần xóa: ").strip()
            if not ma:
                print("❌ Mã phòng không được để trống!")
                return
            n = self.controller.model.pk_repo.delete_by_ma(ma)
            if n > 0:
                print(f"✅ Đã xóa {n} phòng khám")
            else:
                print("❌ Không tìm thấy phòng khám với mã đã nhập")
        except Exception as e:
            print(f"❌ Lỗi khi xóa phòng khám: {e}")

    def add_dich_vu(self):
        """Add new dịch vụ"""
        try:
            ma = input("Mã dịch vụ: ").strip()
            ten = input("Tên dịch vụ: ").strip()
            gia = int(input("Giá dịch vụ: ").strip())
            if not ma or not ten:
                print("❌ Mã và tên dịch vụ không được để trống!")
                return
            n = self.controller.model.dv_repo.create(ma, ten, gia, self.current_user_id)
            print(f"✅ Đã thêm dịch vụ thành công (ID: {n})")
        except ValueError:
            print("❌ Giá dịch vụ phải là số!")
        except Exception as e:
            print(f"❌ Lỗi khi thêm dịch vụ: {e}")

    def delete_dich_vu(self):
        """Delete dịch vụ"""
        try:
            ma = input("Nhập mã dịch vụ cần xóa: ").strip()
            if not ma:
                print("❌ Mã dịch vụ không được để trống!")
                return
            n = self.controller.model.dv_repo.delete_by_ma(ma)
            if n > 0:
                print(f"✅ Đã xóa {n} dịch vụ")
            else:
                print("❌ Không tìm thấy dịch vụ với mã đã nhập")
        except Exception as e:
            print(f"❌ Lỗi khi xóa dịch vụ: {e}")

    def add_benh_nhan(self):
        """Add new bệnh nhân with comprehensive validation"""
        try:
            from validation_utils import (
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
            print("="*50)
            
            # Step 1: Input and validate CCCD (12 digits required)
            so_cccd = input_cccd_with_validation()
            
            # Step 2: Check if CCCD already exists
            existing_patient = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if existing_patient:
                print("\n⚠️  CCCD ĐÃ TỒN TẠI TRONG HỆ THỐNG!")
                display_existing_patient_info(existing_patient)
                print("❌ Không thể tạo bệnh nhân trùng CCCD!")
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
                    print("="*60)
                    print(f"🆔 Mã BN: {created_patient.ma_bn}")
                    print(f"📋 PID: {created_patient.pid}")
                    print(f"📱 CCCD: {created_patient.so_cccd}")
                    print(f"👤 Họ tên: {created_patient._ho_ten}")
                    print(f"⚤ Giới tính: {created_patient._gioi_tinh}")
                    print(f"🎂 Năm sinh: {created_patient.nam_sinh}")
                    if phuong_xa:
                        print(f"🏘️  Phường/Xã: {phuong_xa}")
                    print(f"🏙️  Tỉnh/TP: {tinh}")
                    print("="*60)
            else:
                print("\n❌ Đã hủy thêm bệnh nhân.")
                
        except KeyboardInterrupt:
            print("\n\n❌ Đã hủy thêm bệnh nhân.")
        except Exception as e:
            print(f"❌ Lỗi khi thêm bệnh nhân: {e}")

    def search_benh_nhan(self):
        """Search bệnh nhân by CCCD"""
        try:
            so_cccd = input("Nhập số CCCD cần tìm: ").strip()
            if not so_cccd:
                print("❌ Số CCCD không được để trống!")
                return
            bn = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if bn:
                print("✅ Tìm thấy bệnh nhân:")
                print(bn)
            else:
                print("❌ Không tìm thấy bệnh nhân với CCCD đã nhập")
        except Exception as e:
            print(f"❌ Lỗi khi tìm kiếm: {e}")

    def add_tiep_nhan(self):
        """Add new tiếp nhận with enhanced step-by-step display"""
        try:
            print("📋 Đăng ký tiếp nhận - Mã tiếp nhận sẽ được tự động tạo")
            
            # Step 1: Input CCCD and display patient info
            so_cccd = input("CCCD bệnh nhân: ").strip()
            if not so_cccd:
                print("❌ CCCD không được để trống!")
                return
            
            # Get patient info and display
            patient = self.controller.model.bn_repo.get_by_cccd(so_cccd)
            if not patient:
                print("❌ Không tìm thấy bệnh nhân với CCCD này!")
                return
            
            # Display patient information
            from validation_utils import display_patient_summary
            print("\n📋 THÔNG TIN BỆNH NHÂN")
            print("="*50)
            display_patient_summary(patient)
            
            # Step 2: Display service list and get service selection
            print("\n💉 DANH SÁCH DỊCH VỤ KỸ THUẬT")
            print("="*50)
            self.controller.hien_thi_ds_dich_vu()
            
            ma_dv = input("\nMã dịch vụ: ").strip()
            if not ma_dv:
                print("❌ Mã dịch vụ không được để trống!")
                return
            
            # Validate service exists
            dich_vu = self.controller.model.dv_repo.get_by_ma(ma_dv)
            if not dich_vu:
                print("❌ Không tìm thấy dịch vụ với mã này!")
                return
            
            # Step 3: Display clinic list and get clinic selection
            print("\n🏥 DANH SÁCH PHÒNG KHÁM")
            print("="*50)
            self.controller.hien_thi_ds_phong_kham()
            
            ma_pk = input("\nMã phòng khám: ").strip()
            if not ma_pk:
                print("❌ Mã phòng khám không được để trống!")
                return
            
            # Validate clinic exists
            phong_kham = self.controller.model.pk_repo.get_by_ma(ma_pk)
            if not phong_kham:
                print("❌ Không tìm thấy phòng khám với mã này!")
                return
            
            # Step 4: Input reason for examination
            ly_do = input("\nLý do khám: ").strip()
            if not ly_do:
                print("❌ Lý do khám không được để trống!")
                return
            
            ma_bs = input("Mã bác sĩ (để trống để auto-assign): ").strip()
            
            # Step 5: Create reception and display comprehensive summary
            tiep_nhan, cost = self.controller.tiep_nhan_enhanced(so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
            
            if tiep_nhan:
                print("\n✅ THÔNG TIN TỔNG HỢP TIẾP NHẬN")
                print("="*50)
                from validation_utils import display_reception_summary
                display_reception_summary(tiep_nhan, cost)
                
                from validation_utils import confirm_with_default_yes
                if confirm_with_default_yes("\nXác nhận đăng ký tiếp nhận"):
                    print(f"✅ Đăng ký tiếp nhận thành công! Mã tiếp nhận: {tiep_nhan.ma_tn}")
                else:
                    # Cancel the registration (delete the created record)
                    self.controller.model.tn_repo.delete_by_ma(tiep_nhan.ma_tn)
                    print("❌ Đã hủy đăng ký tiếp nhận!")
            
        except Exception as e:
            print(f"❌ Lỗi khi đăng ký tiếp nhận: {e}")

    def cancel_tiep_nhan(self):
        """Cancel tiếp nhận"""
        try:
            ma_tn = input("Nhập mã tiếp nhận cần hủy: ").strip()
            if not ma_tn:
                print("❌ Mã tiếp nhận không được để trống!")
                return
            self.controller.huy_tiep_nhan(ma_tn)
        except Exception as e:
            print(f"❌ Lỗi khi hủy tiếp nhận: {e}")

    def qr_scan_tiep_nhan(self):
        """QR scan for patient registration and tiếp nhận"""
        try:
            print("\n📱 QUÉT QR CODE ĐĂNG KÝ TIẾP NHẬN")
            print("=" * 50)
            print("Vui lòng nhập chuỗi QR code từ CCCD/CMND")
            print("Định dạng: CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi")
            print("Ví dụ: 058090007045|264362146|Nguyễn Gio An|20041990|Nam|Thôn La Vang 1...")
            
            qr_string = input("📱 QR Code: ").strip()
            if not qr_string:
                print("❌ QR code không được để trống!")
                return
            
            # Process QR scan
            patient = self.controller.process_qr_scan(qr_string)
            if not patient:
                return
            
            print(f"\n✅ Sẽ sử dụng bệnh nhân: {patient._ho_ten} ({patient.ma_bn})")
            
            # Continue with tiếp nhận registration
            print("\n📋 THÔNG TIN DỊCH VỤ & PHÒNG KHÁM")
            print("-" * 40)
            
            # Show services
            print("Danh sách dịch vụ:")
            self.controller.hien_thi_ds_dich_vu()
            
            ma_dv = input("\nMã dịch vụ: ").strip()
            if not ma_dv:
                print("❌ Mã dịch vụ không được để trống!")
                return
            
            # Show clinics
            print("\nDanh sách phòng khám:")
            self.controller.hien_thi_ds_phong_kham()
            
            ma_pk = input("\nMã phòng khám: ").strip()
            if not ma_pk:
                print("❌ Mã phòng khám không được để trống!")
                return
                
            ly_do = input("Lý do khám: ").strip()
            if not ly_do:
                print("❌ Lý do khám không được để trống!")
                return
                
            ma_bs = input("Mã bác sĩ (để trống để auto-assign): ").strip()
            
            # Create tiếp nhận
            self.controller.tiep_nhan(patient.so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý QR scan: {e}")

    def user_register_appointment(self):
        """User registration for appointment"""
        try:
            print("📋 Đăng ký khám - Mã tiếp nhận sẽ được tự động tạo")
            so_cccd = input("CCCD của bạn: ").strip()
            ma_dv = input("Mã dịch vụ: ").strip()
            ma_pk = input("Mã phòng khám: ").strip()
            ly_do = input("Lý do khám: ").strip()
            ma_bs = input("Mã bác sĩ (để trống nếu chưa chọn): ").strip()
            
            if not all([so_cccd, ma_dv, ma_pk, ly_do]):
                print("❌ CCCD, mã dịch vụ, mã phòng khám và lý do khám không được để trống!")
                return
                
            self.controller.tiep_nhan(so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
        except Exception as e:
            print(f"❌ Lỗi khi đăng ký khám: {e}")

    # =============== USER MANAGEMENT METHODS ===============

    def list_users(self):
        """List all users"""
        try:
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT user_id, username, role, pass, created_at FROM [user] ORDER BY created_at DESC")
            users = cur.fetchall()
            conn.close()
            
            if users:
                print("\n📋 DANH SÁCH NGƯỜI DÙNG:")
                print("-" * 80)
                print(f"{'STT':<5} {'Username':<20} {'Role':<10} {'Mật khẩu':<10} {'Ngày tạo':<20}")
                print("-" * 80)
                for i, user in enumerate(users, 1):
                    created_date = user.created_at.strftime("%d/%m/%Y %H:%M") if user.created_at else "N/A"
                    print(users)
                    print(f"{i:<5} {user.username:<20} {user.role:<10} {user:<10} {created_date:<20}")
                print("-" * 80)
            else:
                print("❌ Không có người dùng nào trong hệ thống")
        except Exception as e:
            print(f"❌ Lỗi khi lấy danh sách người dùng: {e}")

    def create_user(self):
        """Create new user"""
        try:
            username = input("Tên đăng nhập: ").strip()
            password = input("Mật khẩu: ").strip()
            role = input("Quyền (ADMIN/USER): ").strip().upper()
            
            if not all([username, password, role]):
                print("❌ Tất cả thông tin không được để trống!")
                return
                
            if role not in ["ADMIN", "USER"]:
                print("❌ Quyền chỉ có thể là ADMIN hoặc USER!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM [user] WHERE username = ?", (username,))
            if cur.fetchone():
                print("❌ Tên đăng nhập đã tồn tại!")
                conn.close()
                return
                
            cur.execute("INSERT INTO [user](username, role, pass) VALUES (?, ?, ?)", (username, role, password))
            conn.commit()
            conn.close()
            print(f"✅ Đã tạo tài khoản thành công cho {username}")
        except Exception as e:
            print(f"❌ Lỗi khi tạo tài khoản: {e}")

    def change_password(self):
        """Change user password"""
        try:
            username = input("Tên đăng nhập: ").strip()
            new_password = input("Mật khẩu mới: ").strip()
            
            if not all([username, new_password]):
                print("❌ Tên đăng nhập và mật khẩu mới không được để trống!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE [user] SET pass = ? WHERE username = ?", (new_password, username))
            if cur.rowcount > 0:
                print(f"✅ Đã thay đổi mật khẩu cho {username}")
            else:
                print("❌ Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Lỗi khi thay đổi mật khẩu: {e}")

    def change_role(self):
        """Change user role"""
        try:
            username = input("Tên đăng nhập: ").strip()
            new_role = input("Quyền mới (ADMIN/USER): ").strip().upper()
            
            if not all([username, new_role]):
                print("❌ Tên đăng nhập và quyền mới không được để trống!")
                return
                
            if new_role not in ["ADMIN", "USER"]:
                print("❌ Quyền chỉ có thể là ADMIN hoặc USER!")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE [user] SET role = ? WHERE username = ?", (new_role, username))
            if cur.rowcount > 0:
                print(f"✅ Đã thay đổi quyền cho {username} thành {new_role}")
            else:
                print("❌ Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Lỗi khi thay đổi quyền: {e}")

    def delete_user(self):
        """Delete user"""
        try:
            username = input("Tên đăng nhập cần xóa: ").strip()
            if not username:
                print("❌ Tên đăng nhập không được để trống!")
                return
                
            confirm = input(f"Bạn có chắc muốn xóa tài khoản '{username}'? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Đã hủy thao tác xóa")
                return
            
            from db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM [user] WHERE username = ?", (username,))
            if cur.rowcount > 0:
                print(f"✅ Đã xóa tài khoản {username}")
            else:
                print("❌ Không tìm thấy người dùng!")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Lỗi khi xóa tài khoản: {e}")

    # =============== EXCEL EXPORT METHODS ===============

    def export_benh_nhan(self):
        """Export bệnh nhân list to Excel"""
        try:
            benh_nhan_list = self.controller.model.list_benh_nhan()
            if not benh_nhan_list:
                print("❌ Không có dữ liệu bệnh nhân để xuất!")
                return
            
            # Prepare data for Excel
            data = []
            for bn in benh_nhan_list:
                data.append({
                    'STT': len(data) + 1,
                    'Mã BN': bn.ma_bn,
                    'PID': bn.pid,
                    'Họ tên': bn._ho_ten,
                    'Giới tính': bn._gioi_tinh,
                    'Năm sinh': bn._nam_sinh,
                    'CCCD': bn._so_cccd
                })
            
            # Create Excel file
            filename = f"DanhSach_BenhNhan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_excel(filepath, index=False, sheet_name='Danh sách bệnh nhân')
                print(f"✅ Đã xuất file Excel: {filename}")
            except ImportError:
                # Fallback to CSV if pandas not available
                import csv
                csv_filename = filename.replace('.xlsx', '.csv')
                csv_filepath = os.path.join(os.getcwd(), csv_filename)
                with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    if data:
                        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                print(f"✅ Đã xuất file CSV: {csv_filename} (pandas không khả dụng)")
                
        except Exception as e:
            print(f"❌ Lỗi khi xuất file: {e}")

    def export_tiep_nhan(self):
        """Export tiếp nhận list to Excel"""
        try:
            tiep_nhan_list = self.controller.model.list_tiep_nhan()
            if not tiep_nhan_list:
                print("❌ Không có dữ liệu tiếp nhận để xuất!")
                return
            
            # Prepare data for Excel
            data = []
            for tn in tiep_nhan_list:
                data.append({
                    'STT': len(data) + 1,
                    'Mã tiếp nhận': tn._ma_tn,
                    'Mã BN': tn._bn.ma_bn,
                    'PID': tn._bn.pid,
                    'Tên bệnh nhân': tn._bn._ho_ten,
                    'CCCD': tn._bn._so_cccd,
                    'Dịch vụ': tn._dv._ten_dv if tn._dv else "N/A",
                    'Phòng khám': tn._pk._ten_phong if tn._pk else "N/A",
                    'Lý do khám': tn._ly_do
                })
            
            # Create Excel file
            filename = f"DanhSach_TiepNhan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_excel(filename, index=False, sheet_name='Danh sách tiếp nhận')
                print(f"✅ Đã xuất file Excel: {filename}")
            except ImportError:
                # Fallback to CSV
                import csv
                csv_filename = filename.replace('.xlsx', '.csv')
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    if data:
                        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                print(f"✅ Đã xuất file CSV: {csv_filename}")
                
        except Exception as e:
            print(f"❌ Lỗi khi xuất file: {e}")

    def export_dich_vu_report(self):
        """Export dịch vụ report to Excel"""
        try:
            dich_vu_list = self.controller.model.list_dich_vu()
            if not dich_vu_list:
                print("❌ Không có dữ liệu dịch vụ để xuất!")
                return
            
            data = []
            for dv in dich_vu_list:
                data.append({
                    'STT': len(data) + 1,
                    'Mã dịch vụ': dv._ma_dv,
                    'Tên dịch vụ': dv._ten_dv,
                    'Giá (VNĐ)': dv._gia
                })
            
            filename = f"BaoCao_DichVu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_excel(filename, index=False, sheet_name='Báo cáo dịch vụ')
                print(f"✅ Đã xuất file Excel: {filename}")
            except ImportError:
                import csv
                csv_filename = filename.replace('.xlsx', '.csv')
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    if data:
                        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                print(f"✅ Đã xuất file CSV: {csv_filename}")
                
        except Exception as e:
            print(f"❌ Lỗi khi xuất file: {e}")

    def export_phong_kham_report(self):
        """Export phòng khám report to Excel"""
        try:
            phong_kham_list = self.controller.model.list_phong_kham()
            if not phong_kham_list:
                print("❌ Không có dữ liệu phòng khám để xuất!")
                return
            
            data = []
            for pk in phong_kham_list:
                data.append({
                    'STT': len(data) + 1,
                    'Mã phòng': pk._ma_phong,
                    'Tên phòng': pk._ten_phong
                })
            
            filename = f"BaoCao_PhongKham_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                df.to_excel(filename, index=False, sheet_name='Báo cáo phòng khám')
                print(f"✅ Đã xuất file Excel: {filename}")
            except ImportError:
                import csv
                csv_filename = filename.replace('.xlsx', '.csv')
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    if data:
                        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                print(f"✅ Đã xuất file CSV: {csv_filename}")
                
        except Exception as e:
            print(f"❌ Lỗi khi xuất file: {e}")

    def export_summary_report(self):
        """Export summary report to Excel"""
        try:
            # Get all data
            benh_nhan_list = self.controller.model.list_benh_nhan()
            tiep_nhan_list = self.controller.model.list_tiep_nhan()
            dich_vu_list = self.controller.model.list_dich_vu()
            phong_kham_list = self.controller.model.list_phong_kham()
            
            # Summary data
            summary_data = [{
                'Chỉ số': 'Tổng số bệnh nhân',
                'Giá trị': len(benh_nhan_list)
            }, {
                'Chỉ số': 'Tổng số tiếp nhận',
                'Giá trị': len(tiep_nhan_list)
            }, {
                'Chỉ số': 'Tổng số dịch vụ',
                'Giá trị': len(dich_vu_list)
            }, {
                'Chỉ số': 'Tổng số phòng khám',
                'Giá trị': len(phong_kham_list)
            }]
            
            filename = f"BaoCao_TongHop_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            try:
                import pandas as pd
                
                # Create Excel writer
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    # Summary sheet
                    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Tổng hợp', index=False)
                    
                    # Detailed sheets
                    if benh_nhan_list:
                        bn_data = [{'Mã BN': bn.ma_bn, 'PID': bn.pid, 'Họ tên': bn._ho_ten, 
                                   'Giới tính': bn._gioi_tinh, 'Năm sinh': bn._nam_sinh, 'CCCD': bn._so_cccd} 
                                   for bn in benh_nhan_list]
                        pd.DataFrame(bn_data).to_excel(writer, sheet_name='Bệnh nhân', index=False)
                    
                    if tiep_nhan_list:
                        tn_data = [{'Mã TN': tn._ma_tn, 'Tên BN': tn._bn._ho_ten, 
                                   'Dịch vụ': tn._dv._ten_dv if tn._dv else "N/A",
                                   'Phòng': tn._pk._ten_phong if tn._pk else "N/A"} 
                                   for tn in tiep_nhan_list]
                        pd.DataFrame(tn_data).to_excel(writer, sheet_name='Tiếp nhận', index=False)
                
                print(f"✅ Đã xuất báo cáo tổng hợp: {filename}")
                
            except ImportError:
                # Fallback to CSV
                import csv
                csv_filename = filename.replace('.xlsx', '.csv')
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['Chỉ số', 'Giá trị'])
                    writer.writeheader()
                    writer.writerows(summary_data)
                print(f"✅ Đã xuất báo cáo tổng hợp: {csv_filename}")
                
        except Exception as e:
            print(f"❌ Lỗi khi xuất báo cáo: {e}")


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
                print("❌ Mã bác sĩ và họ tên không được để trống!")
                return
                
            self.controller.them_bac_si(ma_bs, ho_ten, chuyen_khoa, so_dt, email)
            print("💡 Gợi ý: Sau khi thêm bác sĩ, bạn có thể gán bác sĩ vào phòng khám bằng chức năng 'Gán bác sĩ vào phòng khám'")
        except Exception as e:
            print(f"❌ Lỗi khi thêm bác sĩ: {e}")

    def delete_bac_si(self):
        """Delete bac si"""
        try:
            ma_bs = input("Nhập mã bác sĩ cần xóa: ").strip()
            if not ma_bs:
                print("❌ Mã bác sĩ không được để trống!")
                return
            
            confirm = input(f"Bạn có chắc chắn muốn xóa bác sĩ {ma_bs}? (y/N): ").strip().lower()
            if confirm == 'y':
                self.controller.xoa_bac_si(ma_bs)
            else:
                print("❌ Đã hủy thao tác xóa.")
        except Exception as e:
            print(f"❌ Lỗi khi xóa bác sĩ: {e}")

    def assign_bac_si_to_phong_kham(self):
        """Assign bac si to phong kham"""
        try:
            print("📋 Danh sách bác sĩ hiện tại:")
            self.controller.hien_thi_ds_bac_si()
            print("\n📋 Danh sách phòng khám:")
            self.controller.hien_thi_ds_phong_kham()
            
            ma_bs = input("\nNhập mã bác sĩ: ").strip()
            ma_phong = input("Nhập mã phòng khám (để trống để hủy gán): ").strip()
            
            if not ma_bs:
                print("❌ Mã bác sĩ không được để trống!")
                return
                
            self.controller.gan_bac_si_phong_kham(ma_bs, ma_phong)
        except Exception as e:
            print(f"❌ Lỗi khi gán bác sĩ vào phòng khám: {e}")

    def list_bac_si_by_phong_kham(self):
        """List bac si by phong kham"""
        try:
            print("📋 Danh sách phòng khám:")
            phong_kham_list = self.controller.model.list_phong_kham()
            for i, pk in enumerate(phong_kham_list, 1):
                print(f"{i}. {pk}")
            
            if not phong_kham_list:
                print("❌ Không có phòng khám nào!")
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
                    print("❌ Số thứ tự không hợp lệ!")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi khi liệt kê bác sĩ theo phòng khám: {e}")

    def migration_menu(self):
        """Migration dữ liệu tỉnh bệnh nhân theo NQ 202/2025/QH15"""
        try:
            from migration_hanh_chinh import run_full_migration
            from admin_migration_menu import check_migration_status
            
            print("\n" + "="*60)
            print("🏛️  MIGRATION DỮ LIỆU TỈNH BỆNH NHÂN (NQ 202/2025/QH15)")
            print("="*60)
            print("📋 Chức năng này sẽ:")
            print("   • Tạo các bảng hành chính mới theo NQ 202/2025/QH15")
            print("   • Mapping dữ liệu từ 63 tỉnh cũ sang 34 đơn vị mới")
            print("   • Cập nhật thông tin tỉnh của tất cả bệnh nhân")
            print("   • Bảo toàn dữ liệu gốc trong cột 'Tinh' và thêm cột 'TinhMoi'")
            print("="*60)
            
            # Kiểm tra tình trạng migration hiện tại
            print("🔍 KIỂM TRA TÌNH TRẠNG HIỆN TẠI:")
            check_migration_status()
            
            print("\n" + "⚠️ " + "="*58)
            print("  CẢNH BÁO: Thao tác này sẽ thay đổi cấu trúc database!")
            print("  Nên backup database trước khi thực hiện migration!")
            print("="*60)
            
            confirm = input("Bạn có chắc chắn muốn thực hiện migration? (y/N): ").strip().lower()
            
            if confirm == 'y':
                print("\n🚀 Bắt đầu migration...")
                success = run_full_migration()
                if success:
                    print("\n✅ Migration hoàn thành thành công!")
                    print("💡 Từ giờ hệ thống sẽ sử dụng cấu trúc hành chính mới")
                else:
                    print("\n❌ Migration gặp lỗi!")
            else:
                print("❌ Đã hủy thao tác migration.")
                
        except ImportError as e:
            print(f"❌ Không thể import module migration: {e}")
        except Exception as e:
            print(f"❌ Lỗi khi thực hiện migration: {e}")


def main():
    init_db(seed=True)

    view = View()
    model = Model()
    controller = Controller(view, model)
    user_repo = UserRepo()

    print("=" * 60)
    print("     HỆ THỐNG QUẢN LÝ KHÁM BỆNH - ĐĂNG NHẬP")
    print("=" * 60)
    username = input("👤 Username: ").strip()
    password = input("🔒 Password: ").strip()
    print(username, password)
    user = user_repo.auth(username, password)

    if not user:
        print("❌ Sai tài khoản hoặc mật khẩu!")
        return

    print(f"✅ Xin chào {username}! Quyền: {user._role}")
    
    # Initialize menu manager and start
    menu_manager = MenuManager(controller, user._user_id, user._role, username)
    menu_manager.main_menu()


if __name__ == "__main__":
    main()
