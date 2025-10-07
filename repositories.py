# repositories.py
from typing import List, Optional
import pyodbc  # hoặc bỏ nếu bạn vẫn đang dùng sqlite3
from db import get_conn
from models import User, PhongKham, DichVu, BenhNhan, TiepNhan, BacSi

class UserRepo:
    def get_by_username(self, username: str) -> Optional[User]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT user_id, username, role, pass FROM [user] WHERE username = ?", (username,))
        r = cur.fetchone(); conn.close()
        print(r)
        if r:
            return User(str(r.user_id), r.username, r.role)
        return None

    def auth(self, username: str, password: str) -> Optional[User]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT user_id, username, role FROM [user] WHERE username=?", (username))
        r = cur.fetchone(); conn.close()
        if r:
            return User(str(r.user_id), r.username, r.role)
        return None


class PhongKhamRepo:
    def list_all(self) -> List[PhongKham]:
        conn = get_conn(); cur = conn.cursor()
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
                bac_si = BacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", r.SoDienThoai or "", r.Email or "")
            pk = PhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong, bac_si)
            result.append(pk)
        return result

    def get_by_ma(self, ma_phong: str) -> Optional[PhongKham]:
        conn = get_conn(); cur = conn.cursor()
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
                bac_si = BacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", r.SoDienThoai or "", r.Email or "")
            return PhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong, bac_si)
        return None

    # --- CRUD tối thiểu cho Admin demo ---
    def create(self, ma_phong: str, ten_phong: str, user_created: str) -> str:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO PhongKham(MaPhong, TenPhong, user_created) VALUES (?, ?, ?)", (ma_phong, ten_phong, user_created))
        conn.commit()
        # Get the newly created ID
        cur.execute("SELECT PK_ID FROM PhongKham WHERE MaPhong = ?", (ma_phong,))
        row = cur.fetchone()
        conn.close()
        return str(row.PK_ID) if row else ""

    def delete_by_ma(self, ma_phong: str) -> int:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("DELETE FROM PhongKham WHERE MaPhong=?", (ma_phong,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n


class DichVuRepo:
    def list_all(self) -> List[DichVu]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT dv_id, MaDichVu, TenDichVu, GiaDichVu FROM DM_DichVuKyThuat ORDER BY MaDichVu")
        rows = cur.fetchall(); conn.close()
        return [DichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) for r in rows]

    def get_by_ma(self, ma_dv: str) -> Optional[DichVu]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT dv_id, MaDichVu, TenDichVu, GiaDichVu FROM DM_DichVuKyThuat WHERE MaDichVu=?", (ma_dv,))
        r = cur.fetchone(); conn.close()
        if r: return DichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu)
        return None

    # --- CRUD tối thiểu cho Admin demo ---
    def create(self, ma_dv: str, ten_dv: str, gia: int, user_created: str) -> str:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO DM_DichVuKyThuat(MaDichVu, TenDichVu, GiaDichVu, user_created) VALUES (?, ?, ?, ?)", (ma_dv, ten_dv, gia, user_created))
        conn.commit()
        # Get the newly created ID
        cur.execute("SELECT dv_id FROM DM_DichVuKyThuat WHERE MaDichVu = ?", (ma_dv,))
        row = cur.fetchone()
        conn.close()
        return str(row.dv_id) if row else ""

    def delete_by_ma(self, ma_dv: str) -> int:
        conn = get_conn(); cur = conn.cursor()
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
        conn = get_conn(); cur = conn.cursor()
        
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
        conn = get_conn(); cur = conn.cursor()

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
        conn = get_conn(); cur = conn.cursor()

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
        conn = get_conn(); cur = conn.cursor()

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
        conn = get_conn(); cur = conn.cursor()

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

    def get_by_cccd(self, so_cccd: str) -> Optional[BenhNhan]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT BN_ID, PID, HoTen, GioiTinh, YEAR(NgaySinh) as NamSinh, SoCCCD FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        r = cur.fetchone(); conn.close()
        if r:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            return BenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
        return None

    def exists_by_cccd(self, so_cccd: str) -> bool:
        """Check if benh_nhan with given CCCD already exists"""
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM BenhNhan WHERE SoCCCD = ?", (so_cccd,))
        r = cur.fetchone(); conn.close()
        return r.count > 0 if r else False

    def list_all(self) -> List[BenhNhan]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT BN_ID, PID, HoTen, GioiTinh, YEAR(NgaySinh) as NamSinh, SoCCCD FROM BenhNhan ORDER BY HoTen")
        rows = cur.fetchall(); conn.close()
        result = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            result.append(BenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD))
        return result

class TiepNhanRepo:
    @staticmethod
    def _generate_ma_tn() -> str:
        """Generate ma_tn: TN + YYMMDD + 4-digit sequential number (e.g., TN2409240001)"""
        import datetime
        conn = get_conn(); cur = conn.cursor()
        
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
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT BS_ID FROM PhongKham WHERE PK_ID = ?", (pk_id,))
            row = cur.fetchone()
            if row and row.BS_ID:
                bs_id = str(row.BS_ID)
            conn.close()
        
        bs_id_param = bs_id if bs_id else None
        conn = get_conn(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO TiepNhan(MaTiepNhan, BN_ID, LyDoKham, Dv_ID, PK_ID, BS_ID, user_created)
            VALUES (?, ?, ?, ?, ?, ?, (SELECT TOP 1 user_id FROM [user] WHERE role='ADMIN'))
        """, (ma_tn, bn_id, ly_do, dv_id, pk_id, bs_id_param))
        conn.commit()
        conn.close()
        return ma_tn  # Return the ma_tn code instead of TiepNhan_ID

    def list_all(self) -> List[TiepNhan]:
        conn = get_conn(); cur = conn.cursor()
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

        result: List[TiepNhan] = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            bn = BenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
            dv = DichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) if r.dv_id else None
            pk = PhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong) if r.PK_ID else None
            bs = BacSi(str(r.BS_ID), r.MaBacSi, r.BSHoTen, r.ChuyenKhoa or "", "", "") if r.BS_ID else None
            result.append(TiepNhan(str(r.TiepNhan_ID), r.MaTiepNhan, bn, r.LyDoKham, dv, pk, bs, str(r.created_at) if r.created_at else ""))
        return result

    def list_by_user(self, username: str) -> List[TiepNhan]:
        """Lấy lịch sử tiếp nhận của một user cụ thể dựa trên username == CCCD bệnh nhân"""
        conn = get_conn(); cur = conn.cursor()
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

        result: List[TiepNhan] = []
        for r in rows:
            ma_bn = f"BN{str(r.BN_ID)[:8]}"  # Use first 8 chars of UUID for ma_bn
            pid = r.PID if r.PID else "00000000"  # Default PID if null
            bn = BenhNhan(str(r.BN_ID), ma_bn, pid, r.HoTen, r.GioiTinh, r.NamSinh, r.SoCCCD)
            dv = DichVu(str(r.dv_id), r.MaDichVu, r.TenDichVu, r.GiaDichVu) if r.dv_id else None
            pk = PhongKham(str(r.PK_ID), r.MaPhong, r.TenPhong) if r.PK_ID else None
            bs = BacSi(str(r.BS_ID), r.MaBacSi, r.BSHoTen, r.ChuyenKhoa or "", "", "") if r.BS_ID else None
            result.append(TiepNhan(str(r.TiepNhan_ID), r.MaTiepNhan, bn, r.LyDoKham, dv, pk, bs, str(r.created_at) if r.created_at else ""))
        return result

    def get_by_ma(self, ma_tn: str) -> Optional[TiepNhan]:
        """Lấy thông tin tiếp nhận theo mã tiếp nhận"""
        conn = get_conn(); cur = conn.cursor()
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
        bn = BenhNhan(str(row.BN_ID), ma_bn, pid, row.HoTen, row.GioiTinh, row.NamSinh, row.SoCCCD)
        dv = DichVu(str(row.dv_id), row.MaDichVu, row.TenDichVu, row.GiaDichVu) if row.dv_id else None
        pk = PhongKham(str(row.PK_ID), row.MaPhong, row.TenPhong) if row.PK_ID else None
        bs = BacSi(str(row.BS_ID), row.MaBacSi, row.BSHoTen, row.ChuyenKhoa or "", "", "") if row.BS_ID else None
        return TiepNhan(str(row.TiepNhan_ID), row.MaTiepNhan, bn, row.LyDoKham, dv, pk, bs)

    def delete_by_ma(self, ma_tn: str) -> int:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("DELETE FROM TiepNhan WHERE MaTiepNhan=?", (ma_tn,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n


class BacSiRepo:
    def create(self, ma_bs: str, ho_ten: str, chuyen_khoa: str, so_dt: str, email: str) -> str:
        conn = get_conn(); cur = conn.cursor()
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

    def list_all(self) -> List[BacSi]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            ORDER BY bs.HoTen
        """)
        rows = cur.fetchall(); conn.close()

        result: List[BacSi] = []
        for r in rows:
            result.append(BacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "", 
                               r.SoDienThoai or "", r.Email or ""))
        return result

    def get_by_ma(self, ma_bs: str) -> Optional[BacSi]:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            WHERE bs.MaBacSi = ?
        """, (ma_bs,))
        row = cur.fetchone(); conn.close()
        
        if not row: return None
        return BacSi(str(row.BS_ID), row.MaBacSi, row.HoTen, row.ChuyenKhoa or "",
                    row.SoDienThoai or "", row.Email or "")

    def get_by_phong_kham(self, ma_phong: str) -> List[BacSi]:
        """Lấy bác sĩ của phòng khám"""
        conn = get_conn(); cur = conn.cursor()
        cur.execute("""
            SELECT bs.BS_ID, bs.MaBacSi, bs.HoTen, bs.ChuyenKhoa, bs.SoDienThoai, bs.Email
            FROM BacSi bs
            INNER JOIN PhongKham pk ON pk.BS_ID = bs.BS_ID
            WHERE pk.MaPhong = ?
            ORDER BY bs.HoTen
        """, (ma_phong,))
        rows = cur.fetchall(); conn.close()

        result: List[BacSi] = []
        for r in rows:
            result.append(BacSi(str(r.BS_ID), r.MaBacSi, r.HoTen, r.ChuyenKhoa or "",
                               r.SoDienThoai or "", r.Email or ""))
        return result

    def delete_by_ma(self, ma_bs: str) -> int:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("DELETE FROM BacSi WHERE MaBacSi=?", (ma_bs,))
        conn.commit(); n = cur.rowcount; conn.close()
        return n

    def assign_to_phong_kham(self, ma_bs: str, ma_phong: str) -> bool:
        """Gán bác sĩ vào phòng khám (cập nhật PhongKham.BS_ID)"""
        conn = get_conn(); cur = conn.cursor()
        
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
