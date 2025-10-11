from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from MSSQLServer import BenhNhanRepo, PhongKhamRepo, DichVuRepo, TiepNhanRepo, BacSiRepo
from utils.qr_utils import parse_qr_code, display_benh_nhan_info, generate_username_from_qr, generate_password_from_qr, QRbenh_nhanInfo

# ===== Abstracts =====
class TruuTuong(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def print_obj(self) -> None:
        print(str(self))
# ===== MVC Components =====

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

    # Thông tin danh sách bệnh nhân, phòng khám, dịch vụ, tiếp nhận, bác sĩ
    def ds_benh_nhan(self) -> List[AbcBenhNhan]:
        return self.bn_repo.list_all()

    def ds_phong_kham(self) -> List[AbcPhongKham]:
        return self.pk_repo.list_all()

    def ds_dich_vu(self) -> List[AbcDichVu]:
        return self.dv_repo.list_all()

    def ds_tiep_nhan(self) -> List[AbcTiepNhan]:
        return self.tn_repo.list_all()

    def ds_tiep_nhan_theo_user(self, username: str) -> List[AbcTiepNhan]:
        return self.tn_repo.list_by_user(username)

    def ds_bac_si(self) -> List[AbcBacSi]:
        return self.bs_repo.list_all()

# ===== Nghiệp vụ =====
class AbcUser(TruuTuong):
    def __init__(self, user_id: str, username: str, role: str):
        self._user_id = user_id
        self._username = username
        self._role = role

    def __str__(self) -> str:
        return f"[User: id={self._user_id}, username={self._username}, role={self._role}]"

    @property
    def user_id(self) -> str: return self._user_id


class AbcPhongKham(TruuTuong):
    def __init__(self, pk_id: str, ma_phong: str, ten_phong: str, bac_si: Optional['AbcBacSi'] = None):
        self._pk_id = pk_id
        self._ma_phong = ma_phong
        self._ten_phong = ten_phong
        self._bac_si = bac_si
        self.ten_bac_si = None
    def __str__(self) -> str:
        if self._bac_si:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong} - BS: {self._bac_si.ho_ten}]"
        elif hasattr(self, 'ten_bac_si') and self.ten_bac_si:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong} - BS: {self.ten_bac_si}]"
        else:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong}]"

    @property
    def pk_id(self) -> str: return self._pk_id
    @property
    def ma_phong(self) -> str: return self._ma_phong
    @property
    def ten_phong(self) -> str: return self._ten_phong
    @property
    def bac_si(self) -> Optional['AbcBacSi']: return self._bac_si


class AbcDichVu(TruuTuong):
    def __init__(self, dv_id: str, ma_dv: str, ten_dv: str, gia: int):
        self._dv_id = dv_id
        self._ma_dv = ma_dv
        self._ten_dv = ten_dv
        self._gia = gia

    def __str__(self) -> str:
        return f"[DichVu: {self._ma_dv} - {self._ten_dv} : {self._gia:,}đ]"

    @property
    def dv_id(self) -> str: return self._dv_id
    @property
    def ma_dv(self) -> str: return self._ma_dv
    @property
    def ten_dv(self) -> str: return self._ten_dv
    @property
    def gia(self) -> int: return self._gia


class AbcBacSi(TruuTuong):
    def __init__(self, bs_id: str, ma_bs: str, ho_ten: str, chuyen_khoa: str = "", so_dt: str = "", email: str = ""):
        self._bs_id = bs_id
        self._ma_bs = ma_bs
        self._ho_ten = ho_ten
        self._chuyen_khoa = chuyen_khoa
        self._so_dt = so_dt
        self._email = email

    def __str__(self) -> str:
        return f"[BacSi: {self._ma_bs} - {self._ho_ten} - {self._chuyen_khoa}]"

    @property
    def bs_id(self) -> str: return self._bs_id
    @property
    def ma_bs(self) -> str: return self._ma_bs
    @property
    def ho_ten(self) -> str: return self._ho_ten
    @property
    def chuyen_khoa(self) -> str: return self._chuyen_khoa
    @property
    def so_dt(self) -> str: return self._so_dt
    @property
    def email(self) -> str: return self._email


class AbcBenhNhan(TruuTuong):
    def __init__(self, bn_id: str, ma_bn: str, pid: str, ho_ten: str, gioi_tinh: str, nam_sinh: int, so_cccd: str):
        self._bn_id = bn_id
        self._ma_bn = ma_bn
        self._pid = pid
        self._ho_ten = ho_ten
        self._gioi_tinh = gioi_tinh
        self._nam_sinh = nam_sinh
        self._so_cccd = so_cccd

    def __str__(self) -> str:
        return f"[BenhNhan: {self._ma_bn} - PID:{self._pid} - {self._ho_ten} - {self._gioi_tinh} - {self._nam_sinh} - CCCD:{self._so_cccd}]"

    @property
    def bn_id(self) -> str: return self._bn_id
    @property
    def ma_bn(self) -> str: return self._ma_bn
    @property
    def pid(self) -> str: return self._pid
    @property
    def so_cccd(self) -> str: return self._so_cccd
    @property
    def nam_sinh(self) -> int: return self._nam_sinh
    @property
    def ho_ten(self) -> str: return self._ho_ten
    @property
    def gioi_tinh(self) -> str: return self._gioi_tinh
    
    @staticmethod
    def lay_nam_sinh(ngay_sinh_str: str) -> int:
        """lấy năm sinh từ chuỗi ngày sinh với các định dạng khác nhau.
        Hỗ trợ các định dạng:"""
        try:
            if not ngay_sinh_str:
                return 0
            
            ngay_sinh_clean = ngay_sinh_str.strip()
            
            # Format 1: DDMMYYYY (8 ký tự, không dấu phân cách)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 8:
                return int(ngay_sinh_clean[4:8])
            
            # Format 2: DD/MM/YYYY (dấu phân cách '/')
            if '/' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('/')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 3: DD-MM-YYYY (dấu phân cách '-')
            if '-' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('-')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 4: YYYY only (4 ký tự)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 4:
                return int(ngay_sinh_clean)
            
            # Tìm 4 ký tự liên tiếp bắt đầu bằng 19xx hoặc 20xx trong chuỗi
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', ngay_sinh_clean)
            if year_match:
                return int(year_match.group())
            
            return 0
            
        except (ValueError, IndexError, AttributeError):
            return 0


class AbcTiepNhan(TruuTuong):
    def __init__(self, tn_id: str, ma_tn: str, bn: AbcBenhNhan, ly_do: str, dv: AbcDichVu, pk: AbcPhongKham, bs: Optional[AbcBacSi] = None, created_at: str = ""):
        self._tn_id = tn_id
        self._ma_tn = ma_tn
        self._bn = bn
        self._ly_do = ly_do
        self._dv = dv
        self._pk = pk
        self._bs = bs
        self._created_at = created_at

    def __str__(self) -> str:
        bs_info = f" | BS: {self._bs.ma_bs}-{self._bs.ho_ten} ({self._bs.chuyen_khoa})" if self._bs else " | BS: Chưa chọn"
        dv_info = f"{self._dv._ma_dv}-{self._dv._ten_dv} ({self._dv._gia:,}đ)" if self._dv else "Chưa chọn dịch vụ"
        pk_info = f"{self._pk._ma_phong}-{self._pk._ten_phong}" if self._pk else "Chưa chọn phòng khám"
        date_info = f" | Ngày: {self._created_at[:10]}" if self._created_at else ""
        return (f"[TiepNhan: {self._ma_tn} | BN: {self._bn.ma_bn}-{self._bn._ho_ten} ({self._bn._gioi_tinh}, {self._bn._nam_sinh}) | "
                f"DV: {dv_info} | PK: {pk_info}{bs_info} | Lý do: {self._ly_do}{date_info}]")

    @property
    def tn_id(self) -> str: return self._tn_id
    @property  
    def ma_tn(self) -> str: return self._ma_tn
    @property
    def bac_si(self) -> Optional[AbcBacSi]: return self._bs
    @property
    def created_at(self) -> str: return self._created_at

# ===== Domain service =====
class ChiPhiKham:
    """Tính chi phí dựa trên dịch vụ."""
    @staticmethod
    def tinh_chi_phi(dv: AbcDichVu, pk: AbcPhongKham) -> int:
        # Chỉ tính chi phí dịch vụ, không có phụ phí
        return dv.gia

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

    def them_benh_nhan(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str, 
        so_cccd: str
    ) -> None:
        from utils.qr_utils import phantich_cccd, lay_thongtin_tinhmoi_tu_tinhcu
        
        tinh_cu, gioitinh_cccd, nam_sinh_cccd, tinh_moi = phantich_cccd(so_cccd)
        
        try:
            input_year = int(ngay_sinh_ddmmyyyy.split('/')[-1])
        except:
            input_year = None
        
        nam_sinh_hieuluc = nam_sinh_cccd if nam_sinh_cccd else input_year
        
        tinh_hientai = tinh_moi if tinh_moi else tinh_cu
        
        if nam_sinh_cccd and nam_sinh_cccd != input_year:
            self.view.print_message(f"Tự động cập nhật năm sinh từ CCCD: {nam_sinh_cccd} (thay vì {input_year})")
        
        if tinh_hientai:
            self.view.print_message(f"Tự động xác định tỉnh từ CCCD: {tinh_hientai}")
        
        if gioitinh_cccd and gioitinh_cccd != gioi_tinh:
            self.view.print_message(f"Lưu ý: Giới tính nhập ({gioi_tinh}) khác với CCCD ({gioitinh_cccd})")
        
        bn_id = self.model.bn_repo.create_enhanced(
            ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd, 
            nam_sinh_hieuluc, tinh_hientai
        )
        self.view.print_message(f"Đã thêm bệnh nhân id={bn_id} và tạo tài khoản USER role (username = CCCD).")
        
    def them_benh_nhan_daydu(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,
        so_cccd: str,
        phuong_xa: str = "",
        tinh: str = ""
    ) -> None:
        from utils.qr_utils import phantich_cccd, lay_thongtin_tinhmoi_tu_tinhcu
        
        tinh_cu, gioitinh_cccd, nam_sinh_cccd, tinh_moi = phantich_cccd(so_cccd)
        
        try:
            input_year = int(ngay_sinh_ddmmyyyy.split('/')[-1])
        except:
            input_year = None
        
        nam_sinh_hieuluc = nam_sinh_cccd if nam_sinh_cccd else input_year
        
        tinh_hientai = tinh if tinh else (tinh_moi if tinh_moi else tinh_cu)
        
        if nam_sinh_cccd and nam_sinh_cccd != input_year:
            self.view.print_message(f"Tự động cập nhật năm sinh từ CCCD: {nam_sinh_cccd} (thay vì {input_year})")
        
        if not tinh and tinh_hientai:
            self.view.print_message(f"Tự động xác định tỉnh từ CCCD: {tinh_hientai}")
        
        if gioitinh_cccd and gioitinh_cccd != gioi_tinh:
            self.view.print_message(f"Lưu ý: Giới tính nhập ({gioi_tinh}) khác với CCCD ({gioitinh_cccd})")
        
        bn_id = self.model.bn_repo.create_with_address(
            ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd, 
            phuong_xa, tinh_hientai, nam_sinh_hieuluc
        )
        self.view.print_message(f"Đã thêm bệnh nhân id={bn_id} và tạo tài khoản USER role (username = CCCD).")

    def tiep_nhan(self, so_cccd: str, ma_dv: str, ma_pk: str, ly_do: str, ma_bs: str = "") -> None:
        tiep_nhan, chi_phi = self.them_tiep_nhan(so_cccd, ma_dv, ma_pk, ly_do, ma_bs)
        
        if tiep_nhan and chi_phi is not None:
            bs_info = f" - Bác sĩ: {ma_bs}" if ma_bs else ""
            self.view.print_message(f"Đăng ký thành công (id={tiep_nhan.ma_tn}). Chi phí tạm tính: {chi_phi:,}đ{bs_info}")
            
            self.in_thong_tin_tiep_nhan(tiep_nhan, chi_phi)

    def in_thong_tin_tiep_nhan(self, tiep_nhan: 'AbcTiepNhan', chi_phi: int) -> None:
        self.view.print_message("\n" + "="*60)
        self.view.print_message("📋 THÔNG TIN TIẾP NHẬN")
        self.view.print_message("="*60)
        self.view.print_message(f"🆔 ID Tiếp nhận    : {tiep_nhan.ma_tn}")
        self.view.print_message(f"📄 CCCD            : {tiep_nhan._bn.so_cccd}")
        self.view.print_message(f"👤 Họ tên          : {tiep_nhan._bn._ho_ten}")
        self.view.print_message(f"📝 Lý do khám      : {tiep_nhan._ly_do}")
        self.view.print_message(f"🏥 Dịch vụ đăng ký : {tiep_nhan._dv._ma_dv} - {tiep_nhan._dv._ten_dv}")
        self.view.print_message(f"🏠 Phòng khám      : {tiep_nhan._pk._ma_phong} - {tiep_nhan._pk._ten_phong}")
        if tiep_nhan._bs:
            self.view.print_message(f"👨‍⚕️ Bác sĩ          : {tiep_nhan._bs.ma_bs} - {tiep_nhan._bs.ho_ten} ({tiep_nhan._bs.chuyen_khoa})")
        else:
            self.view.print_message(f"👨‍⚕️ Bác sĩ          : Chưa chọn")
        self.view.print_message(f"💰 Chi phí tạm tính: {chi_phi:,}đ")
        self.view.print_message("="*60)

    def tiep_nhan_cho_user(self, username: str, ma_dv: str, ma_pk: str, ly_do: str, ma_bs: str = "") -> None:
        tiep_nhan, chi_phi = self.them_tiep_nhan(username, ma_dv, ma_pk, ly_do, ma_bs)
        
        if tiep_nhan and chi_phi is not None:
            bs_info = f" - Bác sĩ: {ma_bs}" if ma_bs else ""
            self.view.print_message(f"Đăng ký thành công (id={tiep_nhan.ma_tn}). Chi phí tạm tính: {chi_phi:,}đ{bs_info}")
            
            self.in_thong_tin_tiep_nhan(tiep_nhan, chi_phi)

    def them_tiep_nhan(self, so_cccd: str, ma_dv: str, ma_pk: str, ly_do: str, ma_bs: str = "") -> tuple:
        bn = self.model.bn_repo.get_by_cccd(so_cccd)
        if not bn:
            self.view.print_message("Không tìm thấy bệnh nhân với CCCD đã nhập.")
            return None, None
        
        dv = self.model.dv_repo.get_by_ma(ma_dv)
        pk = self.model.pk_repo.get_by_ma(ma_pk)
        if not dv or not pk:
            self.view.print_message("Không tìm thấy dịch vụ hoặc phòng khám.")
            return None, None
        
        bs = None
        bs_id = ""
        if ma_bs:
            bs = self.model.bs_repo.get_by_ma(ma_bs)
            if not bs:
                self.view.print_message("Không tìm thấy bác sĩ với mã đã nhập.")
                return None, None
            bs_id = bs.bs_id
        
        ma_tn = self.model.tn_repo.create(bn.bn_id, ly_do, dv.dv_id, pk.pk_id, bs_id)
        chi_phi = ChiPhiKham.tinh_chi_phi(dv, pk)
        
        tiep_nhan = self.model.tn_repo.get_by_ma(ma_tn)
        
        return tiep_nhan, chi_phi

    def hien_thi_ds_benh_nhan(self):
        self.view.print_list(self.model.ds_benh_nhan())

    def hien_thi_ds_phong_kham(self):
        self.view.print_list(self.model.ds_phong_kham())

    def hien_thi_ds_dich_vu(self):
        self.view.print_list(self.model.ds_dich_vu())
    
    def hien_thi_danh_sach_dich_vu_cho_user(self):
        dich_vu_list = self.model.ds_dich_vu()
        if not dich_vu_list:
            self.view.print_message("📋 Không có dịch vụ nào!")
            return
        
        self.view.print_message("\n🩺 DANH SÁCH DỊCH VỤ KHÁM")
        self.view.print_message("="*60)
        self.view.print_message(f"{'STT':<4} {'Mã DV':<8} {'Tên dịch vụ':<30} {'Giá tiền':<15}")
        self.view.print_message("-"*60)
        
        for i, dv in enumerate(dich_vu_list, 1):
            self.view.print_message(f"{i:<4} {dv._ma_dv:<8} {dv._ten_dv:<30} {dv._gia:,}đ")
        
        self.view.print_message("="*60)

    def hien_thi_danh_sach_phong_kham_cho_user(self):
        phong_kham_list = self.model.ds_phong_kham()
        if not phong_kham_list:
            self.view.print_message("📋 Không có phòng khám nào!")
            return
        
        self.view.print_message("\n🏥 DANH SÁCH PHÒNG KHÁM")
        self.view.print_message("="*80)
        self.view.print_message(f"{'STT':<4} {'Mã PK':<8} {'Tên phòng khám':<25} {'Bác sĩ phụ trách':<35}")
        self.view.print_message("-"*80)
        
        for i, pk in enumerate(phong_kham_list, 1):
            bs_info = pk.ten_bac_si if hasattr(pk, 'ten_bac_si') and pk.ten_bac_si else "Chưa gán"
            if pk._bac_si:
                bs_info = pk._bac_si.ho_ten
            self.view.print_message(f"{i:<4} {pk._ma_phong:<8} {pk._ten_phong:<25} {bs_info:<35}")
        
        self.view.print_message("="*80)

    def hien_thi_danh_sach_bac_si_cho_user(self):
        bac_si_list = self.model.ds_bac_si()
        if not bac_si_list:
            self.view.print_message("📋 Không có bác sĩ nào!")
            return
        
        self.view.print_message("\n👨‍⚕️ DANH SÁCH BÁC SĨ")
        self.view.print_message("="*70)
        self.view.print_message(f"{'STT':<4} {'Mã BS':<8} {'Họ tên':<25} {'Chuyên khoa':<25}")
        self.view.print_message("-"*70)
        
        for i, bs in enumerate(bac_si_list, 1):
            self.view.print_message(f"{i:<4} {bs.ma_bs:<8} {bs.ho_ten:<25} {bs.chuyen_khoa:<25}")
        
        self.view.print_message("="*70)

    def hien_thi_ds_tiep_nhan(self):
        self.view.print_list(self.model.ds_tiep_nhan())
    
    def hien_thi_lich_su_kham_cua_user(self, username: str):
        lich_su = self.model.ds_tiep_nhan_theo_user(username)
        if not lich_su:
            self.view.print_message(f"📋 Không tìm thấy lịch sử khám cho tài khoản: {username}")
            return
        
        benh_nhan_info = None
        if lich_su:
            benh_nhan_info = lich_su[0]._bn
        
        self.view.print_message(f"\n📋 LỊCH SỬ KHÁM BỆNH")
        if benh_nhan_info:
            self.view.print_message(f"👤 Bệnh nhân: {benh_nhan_info._ho_ten} ({benh_nhan_info._gioi_tinh}, {benh_nhan_info._nam_sinh})")
            self.view.print_message(f"🆔 CCCD: {benh_nhan_info.so_cccd}")
        self.view.print_message("="*125)
        self.view.print_message(f"{'STT':<4} {'Mã TN':<12} {'Ngày khám':<12} {'Dịch vụ':<30} {'Phòng khám':<20} {'Bác sĩ':<40} {'Chi phí':<12}")
        self.view.print_message("-"*125)
        
        for i, tn in enumerate(lich_su, 1):
            dv_info = f"{tn._dv.ten_dv}" if tn._dv else "Chưa có"
            # cộng chuỗi thông tin dịch vụ nếu quá dài
            if len(dv_info) > 28:
                dv_info = dv_info[:25] + "..."
            
            pk_info = f"{tn._pk.ten_phong}" if tn._pk else "Chưa có"
            # cộng chuỗi thông tin phòng khám nếu quá dài
            if len(pk_info) > 18:
                pk_info = pk_info[:15] + "..."
                
            bs_info = f"{tn._bs.ho_ten}" if tn._bs else "Chưa có"
            # cộng chuỗi thông tin bác sĩ nếu quá dài
            if len(bs_info) > 40:
                bs_info = bs_info[:40] + "..."
                
            chi_phi = f"{tn._dv.gia:,}đ" if tn._dv else "0đ"
            

            ngay_kham = "Chưa rõ"
            if hasattr(tn, '_created_at') and tn._created_at:
                try:
                    ngay_kham = tn._created_at[:10] if len(tn._created_at) >= 10 else tn._created_at
                except:
                    ngay_kham = "Chưa rõ"
            
            self.view.print_message(f"{i:<4} {tn._ma_tn:<12} {ngay_kham:<12} {dv_info:<30} {pk_info:<20} {bs_info:<40} {chi_phi:<12}")
        
        self.view.print_message("="*125)
        self.view.print_message(f"📊 Tổng số lần khám: {len(lich_su)}")
        
        # Tính chi phí khám
        total_cost = sum(tn._dv.gia for tn in lich_su if tn._dv)
        self.view.print_message(f"💰 Tổng chi phí đã khám: {total_cost:,}đ")
        
        # Chọn STT xem chi tiết
        if lich_su:
            self.view.print_message("\n🔍 Nhập số STT để xem chi tiết (hoặc Enter để quay lại):")
            try:
                choice = input().strip()
                if choice and choice.isdigit():
                    stt = int(choice)
                    if 1 <= stt <= len(lich_su):
                        self._hien_thi_chi_tiet_tiep_nhan(lich_su[stt-1])
                    else:
                        self.view.print_message("❌ Số STT không hợp lệ!")
            except:
                pass
    
    def _hien_thi_chi_tiet_tiep_nhan(self, tn: 'AbcTiepNhan'):
        """Hiển thị chi tiết một lần tiếp nhận"""
        self.view.print_message(f"\n🔍 CHI TIẾT LỊCH SỬ KHÁM")
        self.view.print_message("="*60)
        self.view.print_message(f"📋 Mã tiếp nhận: {tn._ma_tn}")
        
        # Thông tin bệnh nhân
        self.view.print_message(f"👤 Bệnh nhân: {tn._bn._ho_ten}")
        self.view.print_message(f"   - Giới tính: {tn._bn._gioi_tinh}")
        self.view.print_message(f"   - Năm sinh: {tn._bn._nam_sinh}")
        self.view.print_message(f"   - CCCD: {tn._bn.so_cccd}")
        
        # thông tin dich vụ đăng ký
        if tn._dv:
            self.view.print_message(f"🩺 Dịch vụ: {tn._dv.ten_dv}")
            self.view.print_message(f"   - Mã dịch vụ: {tn._dv.ma_dv}")
            self.view.print_message(f"   - Giá: {tn._dv.gia:,}đ")
        
        # thông tin phòng khám đăng ký
        if tn._pk:
            self.view.print_message(f"🏥 Phòng khám: {tn._pk.ten_phong}")
            self.view.print_message(f"   - Mã phòng: {tn._pk.ma_phong}")
        
        # thông tin bác sĩ
        if tn._bs:
            self.view.print_message(f"👨‍⚕️ Bác sĩ: {tn._bs.ho_ten}")
            self.view.print_message(f"   - Mã bác sĩ: {tn._bs.ma_bs}")
            self.view.print_message(f"   - Chuyên khoa: {tn._bs.chuyen_khoa}")
        
        # lý do khám
        self.view.print_message(f"📝 Lý do khám: {tn._ly_do}")
        
        # ngày khám
        if hasattr(tn, '_created_at') and tn._created_at:
            self.view.print_message(f"📅 Ngày khám: {tn._created_at}")
        
        self.view.print_message("="*60)
        input("\n📥 Nhấn Enter để tiếp tục...")
        
    def hien_thi_lich_su_kham_cua_user_chi_tiet(self, username: str):
        lich_su = self.model.ds_tiep_nhan_theo_user(username)
        if not lich_su:
            self.view.print_message(f"📋 Không tìm thấy lịch sử khám cho tài khoản: {username}")
            return
            
        benh_nhan_info = lich_su[0]._bn if lich_su else None
        
        while True:
            self.view.print_message(f"\n📋 LỊCH SỬ KHÁM CHI TIẾT")
            if benh_nhan_info:
                self.view.print_message(f"👤 {benh_nhan_info._ho_ten} ({benh_nhan_info.so_cccd})")
            
            self.view.print_message("\n🔧 Tùy chọn:")
            self.view.print_message("1. 📋 Xem tất cả lịch sử")  
            self.view.print_message("2. 🔍 Tìm theo mã tiếp nhận")
            self.view.print_message("0. ⬅️  Quay lại")
            
            try:
                choice = int(input("Chọn: ").strip())
                match choice:
                    case 1: 
                        self.hien_thi_lich_su_kham_cua_user(username)
                        break
                    case 2:
                        ma_tn = input("Nhập mã tiếp nhận: ").strip()
                        found = False
                        for tn in lich_su:
                            if tn._ma_tn.upper() == ma_tn.upper():
                                self._hien_thi_chi_tiet_tiep_nhan(tn)
                                found = True
                                break
                        if not found:
                            self.view.print_message("❌ Không tìm thấy mã tiếp nhận!")
                    case 0: 
                        break
                    case _: 
                        self.view.print_message("❌ Lựa chọn không hợp lệ!")
            except ValueError:
                self.view.print_message("❌ Vui lòng nhập số hợp lệ!")

    def hien_thi_ds_bac_si(self):
        self.view.print_list(self.model.ds_bac_si())

    def hien_thi_danh_sach_benh_nhan_cho_admin(self):
        benh_nhan_list = self.model.ds_benh_nhan()
        if not benh_nhan_list:
            self.view.print_message("📋 Không có bệnh nhân nào!")
            return
        
        self.view.print_message("\n👳 DANH SÁCH BỆNH NHÂN")
        self.view.print_message("="*90)
        self.view.print_message(f"{'STT':<4} {'Mã BN':<12} {'PID':<12} {'Họ tên':<20} {'Giới tính':<8} {'Năm sinh':<8} {'CCCD':<15}")
        self.view.print_message("-"*90)
        
        for i, bn in enumerate(benh_nhan_list, 1):
            self.view.print_message(f"{i:<4} {bn.ma_bn:<12} {bn.pid:<12} {bn._ho_ten:<20} {bn._gioi_tinh:<8} {bn.nam_sinh:<8} {bn.so_cccd:<15}")
        
        self.view.print_message("="*90)
        self.view.print_message(f"📊 Tổng cộng: {len(benh_nhan_list)} bệnh nhân")

    def hien_thi_danh_sach_tiep_nhan_cho_admin(self):
        tiep_nhan_list = self.model.ds_tiep_nhan()
        if not tiep_nhan_list:
            self.view.print_message("📋 Không có tiếp nhận nào!")
            return
        
        self.view.print_message("\n📋 DANH SÁCH TIẾP NHẬN")
        self.view.print_message("="*120)
        self.view.print_message(f"{'STT':<4} {'Mã TN':<12} {'Tên BN':<25} {'CCCD':<13} {'Dịch vụ':<30} {'Phòng khám':<25} {'Bác sĩ':<30} {'Lý do':<30}")
        self.view.print_message("-"*120)
        
        for i, tn in enumerate(tiep_nhan_list, 1):
            dv_name = tn._dv._ten_dv[:30] + "..." if len(tn._dv._ten_dv) > 30 else tn._dv._ten_dv if tn._dv else "N/A"
            pk_name = tn._pk._ten_phong[:30] + "..." if len(tn._pk._ten_phong) > 30 else tn._pk._ten_phong if tn._pk else "N/A"
            bs_name = tn._bs.ho_ten[:30] + "..." if tn._bs and len(tn._bs.ho_ten) > 30 else (tn._bs.ho_ten if tn._bs else "Chưa gán")
            ly_do = tn._ly_do[:30] + "..." if len(tn._ly_do) > 30 else tn._ly_do

            self.view.print_message(f"{i:<4} {tn._ma_tn:<12} {tn._bn._ho_ten:<25} {tn._bn.so_cccd:<13} {dv_name:<30} {pk_name:<25} {bs_name:<30} {ly_do:<30}")

        self.view.print_message("="*120)
        self.view.print_message(f"📊 Tổng cộng: {len(tiep_nhan_list)} tiếp nhận")

    def huy_tiep_nhan(self, ma_tn: str):
        n = self.model.tn_repo.delete_by_ma(ma_tn)
        self.view.print_message(f"Đã hủy {n} hồ sơ tiếp nhận.")

    def them_bac_si(self, ma_bs: str, ho_ten: str, chuyen_khoa: str, so_dt: str, email: str):
        bs_id = self.model.bs_repo.create(ma_bs, ho_ten, chuyen_khoa, so_dt, email)
        self.view.print_message(f"Đã thêm bác sĩ thành công (ID: {bs_id})")

    def xoa_bac_si(self, ma_bs: str):
        n = self.model.bs_repo.delete_by_ma(ma_bs)
        self.view.print_message(f"Đã xóa {n} bác sĩ.")

    def gan_bac_si_phong_kham(self, ma_bs: str, ma_phong: str):
        if not ma_phong:
            self.view.print_message("Mã phòng khám không được để trống.")
            return
            
        pk = self.model.pk_repo.get_by_ma(ma_phong)
        if not pk:
            self.view.print_message("Không tìm thấy phòng khám với mã đã nhập.")
            return
        
        bs = self.model.bs_repo.get_by_ma(ma_bs)
        if not bs:
            self.view.print_message("Không tìm thấy bác sĩ với mã đã nhập.")
            return
        
        success = self.model.bs_repo.assign_to_phong_kham(ma_bs, ma_phong)
        if success:
            self.view.print_message(f"Đã gán bác sĩ {bs.ho_ten} ({ma_bs}) vào phòng khám {pk._ten_phong} ({ma_phong})")
        else:
            self.view.print_message("Có lỗi xảy ra khi gán bác sĩ vào phòng khám.")

    def process_qr_scan(self, qr_string: str) -> Optional[AbcBenhNhan]:
        qr_info = parse_qr_code(qr_string)
        if not qr_info:
            self.view.print_message("❌ QR code không hợp lệ!")
            return None
        
        display_benh_nhan_info(qr_info)
        
        # kiểm tra bệnh nhân đã tồn tại
        existing_benh_nhan = self.model.bn_repo.get_by_cccd(qr_info.cccd)
        if existing_benh_nhan:
            print(f"\n⚠️  Bệnh nhân đã tồn tại trong hệ thống:")
            print(f"   Mã BN: {existing_benh_nhan.ma_bn}")
            print(f"   Họ tên: {existing_benh_nhan._ho_ten}")
            xac_nhan = input("\nBạn có muốn sử dụng bệnh nhân này? (y/n): ").strip().lower()
            if xac_nhan == 'y':
                return existing_benh_nhan
            else:
                return None
        
        # xác nhận tạo bệnh nhân mới
        print(f"\n📝 Thông tin tài khoản sẽ được tạo:")
        print(f"   👤 Username: {qr_info.cccd}")
        print(f"   🔒 Password: {qr_info.ngay_sinh}")
        
        xac_nhan = input("\n✅ Xác nhận tạo bệnh nhân mới? (y/n): ").strip().lower()
        if xac_nhan != 'y':
            self.view.print_message("❌ Đã hủy tạo bệnh nhân.")
            return None
        
        # tạo bệnh nhân mới từ chuỗi QR
        try:
            formatted_date = qr_info.get_formatted_date()  # Convert sang dd/mm/yyyy
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
                
                # trả thông tin bệnh nhân mới tạo
                return self.model.bn_repo.get_by_cccd(qr_info.cccd)
            else:
                self.view.print_message("❌ Có lỗi khi tạo bệnh nhân!")
                return None
        except Exception as e:
            self.view.print_message(f"❌ Lỗi: {e}")
            return None
