
from typing import List, Optional
from models import BenhNhan, PhongKham, DichVu, TiepNhan, BacSi, ChiPhiKham
from repositories import BenhNhanRepo, PhongKhamRepo, DichVuRepo, TiepNhanRepo, BacSiRepo
from qr_utils import parse_qr_code, display_patient_info, generate_username_from_qr, generate_password_from_qr, QRPatientInfo

class View:
    @classmethod
    def print_list(cls, items: List[object]) -> None:
        for it in items: print(it)

    @classmethod
    def print_message(cls, msg: str) -> None:
        print(msg)


class Model:
    def __init__(self):
        self.bn_repo = BenhNhanRepo()
        self.pk_repo = PhongKhamRepo()
        self.dv_repo = DichVuRepo()
        self.tn_repo = TiepNhanRepo()
        self.bs_repo = BacSiRepo()

    # Proxy to repos
    def list_benh_nhan(self) -> List[BenhNhan]:
        return self.bn_repo.list_all()

    def list_phong_kham(self) -> List[PhongKham]:
        return self.pk_repo.list_all()

    def list_dich_vu(self) -> List[DichVu]:
        return self.dv_repo.list_all()

    def list_tiep_nhan(self) -> List[TiepNhan]:
        return self.tn_repo.list_all()

    def list_bac_si(self) -> List[BacSi]:
        return self.bs_repo.list_all()


class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

    # 1. Đăng ký Bệnh nhân
    def them_benh_nhan(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,   # <-- THÊM
        so_cccd: str
    ) -> None:
        bn_id = self.model.bn_repo.create(
            ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd
        )
        self.view.print_message(f"Đã thêm bệnh nhân id={bn_id} và tạo tài khoản USER role (username = CCCD).")

    # 2. Tiếp nhận (đăng ký khám)
    def tiep_nhan(self, so_cccd: str, ma_dv: str, ma_pk: str, ly_do: str, ma_bs: str = "") -> None:
        bn = self.model.bn_repo.get_by_cccd(so_cccd)
        if not bn:
            self.view.print_message("Không tìm thấy bệnh nhân với CCCD đã nhập.")
            return
        dv = self.model.dv_repo.get_by_ma(ma_dv)
        pk = self.model.pk_repo.get_by_ma(ma_pk)
        if not dv or not pk:
            self.view.print_message("Không tìm thấy dịch vụ hoặc phòng khám.")
            return
        
        bs_id = ""
        if ma_bs:
            bs = self.model.bs_repo.get_by_ma(ma_bs)
            if not bs:
                self.view.print_message("Không tìm thấy bác sĩ với mã đã nhập.")
                return
            bs_id = bs.bs_id
        
        # ma_tn will be auto-generated in the repository
        tn_id = self.model.tn_repo.create(bn.bn_id, ly_do, dv.dv_id, pk.pk_id, bs_id)
        chi_phi = ChiPhiKham.tinh_chi_phi(dv, pk)
        bs_info = f" - Bác sĩ: {ma_bs}" if ma_bs else ""
        self.view.print_message(f"Đăng ký thành công (id={tn_id}). Chi phí tạm tính: {chi_phi:,}đ{bs_info}")

    # 3. Xem danh sách
    def hien_thi_ds_benh_nhan(self):
        self.view.print_list(self.model.list_benh_nhan())

    def hien_thi_ds_phong_kham(self):
        self.view.print_list(self.model.list_phong_kham())

    def hien_thi_ds_dich_vu(self):
        self.view.print_list(self.model.list_dich_vu())

    def hien_thi_ds_tiep_nhan(self):
        self.view.print_list(self.model.list_tiep_nhan())

    def hien_thi_ds_bac_si(self):
        self.view.print_list(self.model.list_bac_si())

    # 4. Hủy tiếp nhận
    def huy_tiep_nhan(self, ma_tn: str):
        n = self.model.tn_repo.delete_by_ma(ma_tn)
        self.view.print_message(f"Đã hủy {n} hồ sơ tiếp nhận.")

    # 5. Quản lý Bác sĩ
    def them_bac_si(self, ma_bs: str, ho_ten: str, chuyen_khoa: str, so_dt: str, email: str):
        bs_id = self.model.bs_repo.create(ma_bs, ho_ten, chuyen_khoa, so_dt, email)
        self.view.print_message(f"Đã thêm bác sĩ thành công (ID: {bs_id})")

    def xoa_bac_si(self, ma_bs: str):
        n = self.model.bs_repo.delete_by_ma(ma_bs)
        self.view.print_message(f"Đã xóa {n} bác sĩ.")

    def gan_bac_si_phong_kham(self, ma_bs: str, ma_phong: str):
        """Gán bác sĩ vào phòng khám (cập nhật PhongKham.BS_ID)"""
        if not ma_phong:
            self.view.print_message("Mã phòng khám không được để trống.")
            return
            
        # Check if clinic exists
        pk = self.model.pk_repo.get_by_ma(ma_phong)
        if not pk:
            self.view.print_message("Không tìm thấy phòng khám với mã đã nhập.")
            return
        
        # Check if doctor exists
        bs = self.model.bs_repo.get_by_ma(ma_bs)
        if not bs:
            self.view.print_message("Không tìm thấy bác sĩ với mã đã nhập.")
            return
        
        success = self.model.bs_repo.assign_to_phong_kham(ma_bs, ma_phong)
        if success:
            self.view.print_message(f"Đã gán bác sĩ {bs.ho_ten} ({ma_bs}) vào phòng khám {pk._ten_phong} ({ma_phong})")
        else:
            self.view.print_message("Có lỗi xảy ra khi gán bác sĩ vào phòng khám.")

    # 6. QR Code Processing
    def process_qr_scan(self, qr_string: str) -> Optional[BenhNhan]:
        """Process QR code scan for patient registration"""
        # Parse QR code
        qr_info = parse_qr_code(qr_string)
        if not qr_info:
            self.view.print_message("❌ QR code không hợp lệ!")
            return None
        
        # Display patient info
        display_patient_info(qr_info)
        
        # Check if patient already exists
        existing_patient = self.model.bn_repo.get_by_cccd(qr_info.cccd)
        if existing_patient:
            print(f"\n⚠️  Bệnh nhân đã tồn tại trong hệ thống:")
            print(f"   Mã BN: {existing_patient.ma_bn}")
            print(f"   Họ tên: {existing_patient._ho_ten}")
            confirm = input("\n🤔 Bạn có muốn sử dụng bệnh nhân này? (y/n): ").strip().lower()
            if confirm == 'y':
                return existing_patient
            else:
                return None
        
        # Confirm creation
        print(f"\n📝 Thông tin tài khoản sẽ được tạo:")
        print(f"   👤 Username: {qr_info.cccd}")
        print(f"   🔒 Password: {qr_info.ngay_sinh}")
        
        confirm = input("\n✅ Xác nhận tạo bệnh nhân mới? (y/n): ").strip().lower()
        if confirm != 'y':
            self.view.print_message("❌ Đã hủy tạo bệnh nhân.")
            return None
        
        # Create patient from QR
        try:
            formatted_date = qr_info.get_formatted_date()  # Convert to dd/mm/yyyy
            bn_id = self.model.bn_repo.create_from_qr(
                ho_ten=qr_info.ho_ten,
                gioi_tinh=qr_info.gioi_tinh,
                ngay_sinh_ddmmyyyy=formatted_date,
                so_cccd=qr_info.cccd,
                so_cmnd=qr_info.cmnd,
                dia_chi=qr_info.dia_chi
            )
            
            if bn_id:
                self.view.print_message("✅ Tạo bệnh nhân thành công!")
                self.view.print_message(f"   📋 ID: {bn_id}")
                self.view.print_message(f"   👤 Username: {qr_info.cccd}")
                self.view.print_message(f"   🔒 Password: {qr_info.ngay_sinh}")
                
                # Return the newly created patient
                return self.model.bn_repo.get_by_cccd(qr_info.cccd)
            else:
                self.view.print_message("❌ Có lỗi khi tạo bệnh nhân!")
                return None
        except Exception as e:
            self.view.print_message(f"❌ Lỗi: {e}")
            return None
