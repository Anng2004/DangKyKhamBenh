from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
from MSSQLServer import MSSQLConnection
from utils.qr_utils import parse_qr_code, display_benh_nhan_info, generate_username_from_qr, generate_password_from_qr, QRbenh_nhanInfo
# ===== Abstracts =====
class TruuTuong(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def print_obj(self) -> None:
        print(str(self))
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
#====== Repositories =====
class UserRepo:
    def get_by_username(self, username: str) -> Optional[AbcUser]:
        conn = MSSQLConnection(database="DangKyKhamBenh");
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, role FROM [user] WHERE username=?", (username,))
        r = cur.fetchone(); conn.close()
        if r:
            return AbcUser(str(r.user_id), r.username, r.role)
        return None

    def auth(self, username: str, password: str) -> Optional[AbcUser]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT user_id, username, role FROM [user] WHERE username=?", (username))
        r = cur.fetchone(); conn.close()
        if r:
            return AbcUser(str(r.user_id), r.username, r.role)
        return None


class PhongKhamRepo:
    def list_all(self) -> List[AbcPhongKham]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT pk.PK_ID, pk.MaPhong, pk.TenPhong, 
                   bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM PhongKham pk 
            LEFT JOIN BacSi bs ON pk.BS_ID = bs.BS_ID 
            ORDER BY pk.MaPhong
        """)
        rows = cur.fetchall(); conn.close()
        result = []
        for r in rows:
            bac_si = None
            if r.BS_ID:
                bac_si = AbcBacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", r.SoDienThoai or "", r.Email or "")
            pk = AbcPhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong, bac_si)
            result.append(pk)
        return result

    def get_by_ma(self, ma_phong: str) -> Optional[AbcPhongKham]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT pk.PK_ID, pk.MaPhong, pk.TenPhong, 
                   bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM PhongKham pk 
            LEFT JOIN BacSi bs ON pk.BS_ID = bs.BS_ID 
            WHERE pk.MaPhong=?
        """, (ma_phong,))
        r = cur.fetchone(); conn.close()
        if r: 
            bac_si = None
            if r.BS_ID:
                bac_si = AbcBacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", r.SoDienThoai or "", r.Email or "")
            return AbcPhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong, bac_si)
        return None

    # --- CRUD tối thiểu cho Admin demo ---
    def create(self, ma_phong: str, ten_phong: str, user_created: str) -> str:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("INSERT INTO PhongKham(MaPhong, TenPhong, user_created) VALUES (?, ?, ?)", (ma_phong, ten_phong, user_created))
        conn.commit()
        # Get the newly created ID
        cur.execute("SELECT PK_ID FROM PhongKham WHERE MaPhong = ?", (ma_phong,))
        row = cur.fetchone()
        conn.close()
        return str(row.PK_ID) if row else ""

    def delete_by_ma(self, ma_phong: str) -> int:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("DELETE FROM PhongKham WHERE MaPhong=?", (ma_phong,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n


class DichVuRepo:
    def list_all(self) -> List[AbcDichVu]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT dv_id, MaDichVu, TenDichVu, GiaDichVu FROM DM_DichVuKyThuat ORDER BY MaDichVu")
        rows = cur.fetchall(); conn.close()
        return [AbcDichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) for r in rows]

    def get_by_ma(self, ma_dv: str) -> Optional[AbcDichVu]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT dv_id, MaDichVu, TenDichVu, GiaDichVu FROM DM_DichVuKyThuat WHERE MaDichVu=?", (ma_dv,))
        r = cur.fetchone(); conn.close()
        if r: return AbcDichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu)
        return None

    # --- CRUD tối thiểu cho Admin demo ---
    def create(self, ma_dv: str, ten_dv: str, gia: int, user_created: str) -> str:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("INSERT INTO DM_DichVuKyThuat(MaDichVu, TenDichVu, GiaDichVu, user_created) VALUES (?, ?, ?, ?)", (ma_dv, ten_dv, gia, user_created))
        conn.commit()
        # Get the newly created ID
        cur.execute("SELECT dv_id FROM DM_DichVuKyThuat WHERE MaDichVu = ?", (ma_dv,))
        row = cur.fetchone()
        conn.close()
        return str(row.dv_id) if row else ""

    def delete_by_ma(self, ma_dv: str) -> int:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("DELETE FROM DM_DichVuKyThuat WHERE MaDichVu=?", (ma_dv,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n


class BenhNhanRepo:
    @staticmethod
    def _mk_pass_from_cccd_and_dob(so_cccd: str, ngay_sinh_ddmmyyyy: str) -> str:
        # ngay_sinh_ddmmyyyy: "dd/mm/yyyy" hoặc "d/m/yyyy"
        parts = [p.zfill(2) for p in ngay_sinh_ddmmyyyy.strip().split("/")]
        if len(parts) != 3:
            raise ValueError("Ngày sinh phải có định dạng dd/mm/yyyy")
        dd, mm, yyyy = parts[0], parts[1], parts[2]
        yy = yyyy[-2:]
        last4 = so_cccd[-4:]
        return f"{last4}{dd}{mm}{yy}"

    @staticmethod
    def _generate_pid() -> str:
        """Generate 8-digit PID: 2 digits for current year + 6 digits ordinal number"""
        import datetime
        conn = MSSQLConnection(); cur = conn.cursor()
        
        current_year = datetime.datetime.now().year
        year_suffix = str(current_year)[-2:]  # Last 2 digits of year
        
        # số thứ tự trong năm
        cur.execute("""
            SELECT COUNT(*) as count 
            FROM BenhNhan 
            WHERE PID LIKE ? AND PID IS NOT NULL
        """, (f"{year_suffix}%",))
        
        row = cur.fetchone()
        count = row.count if row else 0
        ordinal = count + 1
        
        # định dạng PID: YY + 6 số thứ tự (ví dụ: 240001)
        pid = f"{year_suffix}{ordinal:06d}"
        conn.close()
        return pid

    def create(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,   # <-- THÊM
        so_cccd: str
    ) -> str:
        conn = MSSQLConnection(); cur = conn.cursor()

        # tạo PID
        pid = self._generate_pid()

        # 1) Thêm bệnh nhân (dùng CONVERT kiểu 103 = dd/mm/yyyy)
        cur.execute("""
            INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, SoCCCD, user_created)
            VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd))

        # Lấy BN_ID (pyodbc không luôn hỗ trợ lastrowid)
        cur.execute("SELECT BN_ID FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        row = cur.fetchone()
        bn_id = str(row.BN_ID) if row else ""

        # 2) tự động đăng ký user nếu chưa tồn tại
        init_pass = self._mk_pass_from_cccd_and_dob(so_cccd, ngay_sinh_ddmmyyyy)
        cur.execute("SELECT 1 FROM [user] WHERE username = ?", (so_cccd,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute("""
                INSERT INTO [user](username, role, pass)
                VALUES (?, 'USER', ?)
            """, (so_cccd, init_pass))

        conn.commit()
        conn.close()
        return bn_id
    
    def create_enhanced(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,
        so_cccd: str,
        nam_sinh: int = None,
        tinh: str = None
    ) -> str:
        """Tạo thông tin bệnh nhân từ chuỗi CCCD với các thông tin bổ sung như năm sinh và tỉnh"""
        conn = MSSQLConnection(); cur = conn.cursor()

        # Tạo PID
        pid = self._generate_pid()

        # lấy phường xã từ tỉnh nếu có
        phuong_xa = ""
        if tinh:
            
            phuong_xa = ""

        # 1) 
        if tinh and nam_sinh:
            cur.execute("""
                INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, SoCCCD, PhuongXa, Tinh, user_created)
                VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
            """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd, phuong_xa, tinh))
        elif tinh:
            cur.execute("""
                INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, SoCCCD, Tinh, user_created)
                VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
            """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd, tinh))
        else:
            cur.execute("""
                INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, SoCCCD, user_created)
                VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
            """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd))

        # Lấy BN_ID
        cur.execute("SELECT BN_ID FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        row = cur.fetchone()
        bn_id = str(row.BN_ID) if row else ""

        # 2) 
        init_pass = self._mk_pass_from_cccd_and_dob(so_cccd, ngay_sinh_ddmmyyyy)
        cur.execute("SELECT 1 FROM [user] WHERE username = ?", (so_cccd,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute("""
                INSERT INTO [user](username, role, pass)
                VALUES (?, 'USER', ?)
            """, (so_cccd, init_pass))

        conn.commit()
        conn.close()
        return bn_id
    
    def create_with_address(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,
        so_cccd: str,
        phuong_xa: str = "",
        tinh: str = "",
        nam_sinh: int = None
    ) -> str:
        """Create benh_nhan with full address information"""
        conn = MSSQLConnection(); cur = conn.cursor()

        # Tạo PID
        pid = self._generate_pid()
        # 1) 
        cur.execute("""
            INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, NamSinh, SoCCCD, PhuongXa, Tinh, user_created)
            VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, nam_sinh, so_cccd, phuong_xa, tinh))

        # Lấy BN_ID
        cur.execute("SELECT BN_ID FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        row = cur.fetchone()
        bn_id = str(row.BN_ID) if row else ""

        # 2) 
        init_pass = self._mk_pass_from_cccd_and_dob(so_cccd, ngay_sinh_ddmmyyyy)
        cur.execute("SELECT 1 FROM [user] WHERE username = ?", (so_cccd,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute("""
                INSERT INTO [user](username, role, pass)
                VALUES (?, 'USER', ?)
            """, (so_cccd, init_pass))

        conn.commit()
        conn.close()
        return bn_id

    def create_from_qr(
        self,
        ho_ten: str,
        gioi_tinh: str,
        ngay_sinh_ddmmyyyy: str,
        so_cccd: str,
        so_cmnd: str,
        dia_chi: str
    ) -> str:
        """Create benh_nhan from QR code data with full address"""
        conn = MSSQLConnection(); cur = conn.cursor()

        # Tạo PID
        pid = self._generate_pid()

        # Tách phường xã và tỉnh từ địa chỉ đầy đủ
        address_parts = dia_chi.split(', ')
        if len(address_parts) >= 2:
            phuong_xa = ', '.join(address_parts[:-1])  # Everything except last part
            tinh = address_parts[-1]  # Last part is province
        else:
            phuong_xa = dia_chi
            tinh = ""

        # 1) 
        cur.execute("""
            INSERT INTO BenhNhan(PID, HoTen, GioiTinh, NgaySinh, SoCCCD, SoCMND, PhuongXa, Tinh, user_created)
            VALUES (?, ?, ?, CONVERT(date, ?, 103), ?, ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (pid, ho_ten, gioi_tinh, ngay_sinh_ddmmyyyy, so_cccd, so_cmnd, phuong_xa, tinh))

        # Lấy BN_ID (pyodbc không luôn hỗ trợ lastrowid)
        cur.execute("SELECT BN_ID FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        row = cur.fetchone()
        bn_id = str(row.BN_ID) if row else ""

        # 2) 
        init_pass = self._mk_pass_from_cccd_and_dob(so_cccd, ngay_sinh_ddmmyyyy)
        cur.execute("SELECT 1 FROM [user] WHERE username = ?", (so_cccd,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute("""
                INSERT INTO [user](username, role, pass)
                VALUES (?, 'USER', ?)
            """, (so_cccd, init_pass))

        conn.commit()
        conn.close()
        return bn_id

    def get_by_cccd(self, so_cccd: str) -> Optional[AbcBenhNhan]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT BN_ID, PID, HoTen, GioiTinh, YEAR(NgaySinh) as NamSinh, SoCCCD FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        r = cur.fetchone(); conn.close()
        if r:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            return AbcBenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
        return None

    def exists_by_cccd(self, so_cccd: str) -> bool:
        """Check if benh_nhan with given CCCD already exists"""
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        r = cur.fetchone(); conn.close()
        return r.count > 0 if r else False

    def list_all(self) -> List[AbcBenhNhan]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("SELECT BN_ID, PID, HoTen, GioiTinh, YEAR(NgaySinh) as NamSinh, SoCCCD FROM BenhNhan ORDER BY HoTen")
        rows = cur.fetchall(); conn.close()
        result = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            result.append(AbcBenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD))
        return result

class TiepNhanRepo:
    @staticmethod
    def _generate_ma_tn() -> str:
        """Generate ma_tn: TN + YYMMDD + 4-digit sequential number (e.g., TN2409240001)"""
        import datetime
        conn = MSSQLConnection(); cur = conn.cursor()
        
        now = datetime.datetime.now()
        date_prefix = now.strftime("%y%m%d")  # YYMMDD format
        
        # Get the next sequential number for today
        cur.execute("""
            SELECT COUNT(*) as count 
            FROM TiepNhan 
            WHERE MaTiepNhan LIKE ? AND MaTiepNhan IS NOT NULL
        """, (f"TN{date_prefix}%",))
        
        row = cur.fetchone()
        count = row.count if row else 0
        ordinal = count + 1
        
        # Format as TN + YYMMDD + 4-digit ordinal (pad with zeros)
        ma_tn = f"TN{date_prefix}{ordinal:04d}"
        conn.close()
        return ma_tn

    def create(self, bn_id: str, ly_do: str, dv_id: str, pk_id: str, bs_id: str = "") -> str:
        # Auto-generate ma_tn
        ma_tn = self._generate_ma_tn()
        
        # Auto-assign doctor from clinic if not specified
        if not bs_id:
            conn = MSSQLConnection(); cur = conn.cursor()
            cur.execute("SELECT BS_ID FROM PhongKham WHERE PK_ID = ?", (pk_id,))
            row = cur.fetchone()
            if row and row.BS_ID:
                bs_id = str(row.BS_ID)
            conn.close()
        
        bs_id_param = bs_id if bs_id else None
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO TiepNhan(MaTiepNhan, BN_ID, LyDoKham, Dv_ID, PK_ID, BS_ID, user_created)
            VALUES (?, ?, ?, ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (ma_tn, bn_id, ly_do, dv_id, pk_id, bs_id_param))
        conn.commit()
        conn.close()
        return ma_tn  # Return the ma_tn code instead of TiepNhan_ID

    def list_all(self) -> List[AbcTiepNhan]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT tn.TiepNhan_ID, tn.MaTiepNhan, tn.LyDoKham,
                   bn.BN_ID, bn.PID, bn.HoTen, bn.GioiTinh, YEAR(bn.NgaySinh) as NamSinh, bn.SoCCCD,
                   dv.dv_id, dv.MaDichVu, dv.TenDichVu, dv.GiaDichVu,
                   pk.PK_ID, pk.MaPhong, pk.TenPhong,
                   bs.BS_ID, bs.MaBacSi, bs.HoTen as BSHoTen, bs.ChuyenKhoa,
                   tn.created_at
            FROM TiepNhan tn
            JOIN BenhNhan bn ON bn.BN_ID = tn.BN_ID
            LEFT JOIN DM_DichVuKyThuat dv ON dv.dv_id = tn.Dv_ID
            LEFT JOIN PhongKham pk ON pk.PK_ID = tn.PK_ID
            LEFT JOIN BacSi bs ON bs.BS_ID = tn.BS_ID
            ORDER BY tn.created_at DESC
        """)
        rows = cur.fetchall(); conn.close()

        result: List[AbcTiepNhan] = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            bn = AbcBenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
            dv = AbcDichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) if r.dv_id else None
            pk = AbcPhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong) if r.PK_ID else None
            bs = AbcBacSi(str(r.BS_ID), r.MaBacSi, r.BSHoTen, r.ChuyenKhoa or "", "", "") if r.BS_ID else None
            result.append(AbcTiepNhan(str(r.TiepNhan_ID), r.MaTiepNhan, bn, r.LyDoKham, dv, pk, bs, str(r.created_at) if r.created_at else ""))
        return result

    def list_by_user(self, username: str) -> List[AbcTiepNhan]:
        """Lấy lịch sử tiếp nhận của một user cụ thể dựa trên username == CCCD bệnh nhân"""
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT tn.TiepNhan_ID, tn.MaTiepNhan, tn.LyDoKham,
                   bn.BN_ID, bn.PID, bn.HoTen, bn.GioiTinh, YEAR(bn.NgaySinh) as NamSinh, bn.SoCCCD,
                   dv.dv_id, dv.MaDichVu, dv.TenDichVu, dv.GiaDichVu,
                   pk.PK_ID, pk.MaPhong, pk.TenPhong,
                   bs.BS_ID, bs.MaBacSi, bs.HoTen as BSHoTen, bs.ChuyenKhoa,
                   tn.created_at
            FROM TiepNhan tn
            JOIN BenhNhan bn ON bn.BN_ID = tn.BN_ID
            LEFT JOIN DM_DichVuKyThuat dv ON dv.dv_id = tn.Dv_ID
            LEFT JOIN PhongKham pk ON pk.PK_ID = tn.PK_ID
            LEFT JOIN BacSi bs ON bs.BS_ID = tn.BS_ID
            WHERE bn.SoCCCD = ?
            ORDER BY tn.created_at DESC
        """, (username,))
        rows = cur.fetchall(); conn.close()

        result: List[AbcTiepNhan] = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            bn = AbcBenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
            dv = AbcDichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) if r.dv_id else None
            pk = AbcPhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong) if r.PK_ID else None
            bs = AbcBacSi(str(r.BS_ID), r.MaBacSi, r.BSHoTen, r.ChuyenKhoa or "", "", "") if r.BS_ID else None
            result.append(AbcTiepNhan(str(r.TiepNhan_ID), r.MaTiepNhan, bn, r.LyDoKham, dv, pk, bs, str(r.created_at) if r.created_at else ""))
        return result

    def get_by_ma(self, ma_tn: str) -> Optional[AbcTiepNhan]:
        """Lấy thông tin tiếp nhận theo mã tiếp nhận"""
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT tn.TiepNhan_ID, tn.MaTiepNhan, tn.LyDoKham,
                   bn.BN_ID, bn.PID, bn.HoTen, bn.GioiTinh, YEAR(bn.NgaySinh) as NamSinh, bn.SoCCCD,
                   dv.dv_id, dv.MaDichVu, dv.TenDichVu, dv.GiaDichVu,
                   pk.PK_ID, pk.MaPhong, pk.TenPhong,
                   bs.BS_ID, bs.MaBacSi, bs.HoTen as BSHoTen, bs.ChuyenKhoa
            FROM TiepNhan tn
            JOIN BenhNhan bn ON bn.BN_ID = tn.BN_ID
            LEFT JOIN DM_DichVuKyThuat dv ON dv.dv_id = tn.Dv_ID
            LEFT JOIN PhongKham pk ON pk.PK_ID = tn.PK_ID
            LEFT JOIN BacSi bs ON bs.BS_ID = tn.BS_ID
            WHERE tn.MaTiepNhan = ?
        """, (ma_tn,))
        row = cur.fetchone(); conn.close()
        
        if not row: return None
        
        ma_bn = f"BN{str(row.BN_ID)[:8]}"  
        pid = row.PID if row.PID else "00000000"  # PID mặc định nếu null
        bn = AbcBenhNhan(str(row.BN_ID), ma_bn, pid, row.HoTen, row.GioiTinh, row.NamSinh, row.SoCCCD)
        dv = AbcDichVu(str(row.dv_id), row.MaDichVu, row.TenDichVu, row.GiaDichVu) if row.dv_id else None
        pk = AbcPhongKham(str(row.PK_ID), row.MaPhong, row.TenPhong) if row.PK_ID else None
        bs = AbcBacSi(str(row.BS_ID), row.MaBacSi, row.BSHoTen, row.ChuyenKhoa or "", "", "") if row.BS_ID else None
        return AbcTiepNhan(str(row.TiepNhan_ID), row.MaTiepNhan, bn, row.LyDoKham, dv, pk, bs)

    def delete_by_ma(self, ma_tn: str) -> int:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("DELETE FROM TiepNhan WHERE MaTiepNhan=?", (ma_tn,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n


class BacSiRepo:
    def create(self, ma_bs: str, ho_ten: str, chuyen_khoa: str, so_dt: str, email: str) -> str:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO BacSi(MaBacSi, HoTen, ChuyenKhoa, SoDienThoai, Email, user_created)
            VALUES (?, ?, ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (ma_bs, ho_ten, chuyen_khoa, so_dt, email))
        conn.commit()
        # lấy BS_ID mới tạo
        cur.execute("SELECT BS_ID FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
        row = cur.fetchone()
        conn.close()
        return str(row.BS_ID) if row else ""

    def list_all(self) -> List[AbcBacSi]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            ORDER BY bs.HoTen
        """)
        rows = cur.fetchall(); conn.close()

        result: List[AbcBacSi] = []
        for r in rows:
            result.append(AbcBacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", 
                               r.SoDienThoai or "", r.Email or ""))
        return result

    def get_by_ma(self, ma_bs: str) -> Optional[AbcBacSi]:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            WHERE bs.MaBacSi = ?
        """, (ma_bs,))
        row = cur.fetchone(); conn.close()
        
        if not row: return None
        return AbcBacSi(str(row.BS_ID), row.MaBacSi, row.HoTen, row.ChuyenKhoa or "",
                    row.SoDienThoai or "", row.Email or "")

    def get_by_phong_kham(self, ma_phong: str) -> List[AbcBacSi]:
        """Lấy bác sĩ của phòng khám"""
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            INNER JOIN PhongKham pk ON pk.BS_ID = bs.BS_ID
            WHERE pk.MaPhong = ?
            ORDER BY bs.HoTen
        """, (ma_phong,))
        rows = cur.fetchall(); conn.close()

        result: List[AbcBacSi] = []
        for r in rows:
            result.append(AbcBacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "",
                               r.SoDienThoai or "", r.Email or ""))
        return result

    def delete_by_ma(self, ma_bs: str) -> int:
        conn = MSSQLConnection(); cur = conn.cursor()
        cur.execute("DELETE FROM BacSi WHERE MaBacSi=?", (ma_bs,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n

    def assign_to_phong_kham(self, ma_bs: str, ma_phong: str) -> bool:
        """Gán bác sĩ vào phòng khám (cập nhật PhongKham.BS_ID)"""
        conn = MSSQLConnection(); cur = conn.cursor()
        
        # lấy BS_ID từ ma_bs
        cur.execute("SELECT BS_ID FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
        bs_row = cur.fetchone()
        if not bs_row:
            conn.close()
            return False
        
        bs_id = str(bs_row.BS_ID)
        
        # Update Phòng khám
        cur.execute("UPDATE PhongKham SET BS_ID = ? WHERE MaPhong = ?", (bs_id, ma_phong))
        success = cur.rowcount > 0
        conn.commit(); conn.close()
        return success          
        conn.commit(); success = cur.rowcount > 0; conn.close()
        return success

