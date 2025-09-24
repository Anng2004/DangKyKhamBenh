# import_data.py - Import dữ liệu mẫu cho hệ thống

import sys
from db import get_conn, init_db

def check_database_ready():
    """Kiểm tra database đã sẵn sàng chưa"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Kiểm tra bảng chính có tồn tại không
        cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('user', 'PhongKham', 'DM_DichVuKyThuat', 'BacSi')")
        table_count = cur.fetchone()[0]
        
        conn.close()
        return table_count >= 4
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return False

def import_phong_kham():
    """Import thêm dữ liệu phòng khám"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Dữ liệu phòng khám mẫu
    phong_kham_data = [
        ('PK002', 'Phòng Nhi khoa'),
        ('PK003', 'Phòng Sản phụ khoa'),
        ('PK004', 'Phòng Tai Mũi Họng'),
        ('PK005', 'Phòng Mắt'),
        ('PK006', 'Phòng Da liễu'),
        ('PK007', 'Phòng Tim mạch'),
        ('PK008', 'Phòng Thần kinh'),
        ('PK009', 'Phòng Cơ xương khớp'),
        ('PK010', 'Phòng Ung bướu'),
        ('PK011', 'Phòng Cấp cứu'),
        ('PK012', 'Phòng X-Quang'),
        ('PK013', 'Phòng Siêu âm'),
        ('PK014', 'Phòng Xét nghiệm'),
        ('PK015', 'Phòng Phục hồi chức năng'),
        ('PK02', 'Phòng cấp cứu')  # Phòng bổ sung
    ]
    
    print("🏥 Đang import dữ liệu Phòng khám...")
    for ma_phong, ten_phong in phong_kham_data:
        try:
            # Check if already exists
            cur.execute("SELECT COUNT(*) FROM PhongKham WHERE MaPhong = ?", (ma_phong,))
            exists = cur.fetchone()[0]
            
            if exists == 0:
                cur.execute("""
                    INSERT INTO PhongKham(PK_ID, MaPhong, TenPhong) 
                    VALUES (NEWID(), ?, ?)
                """, (ma_phong, ten_phong))
                print(f"  ✅ Đã thêm: {ma_phong} - {ten_phong}")
            else:
                print(f"  ⚠️  Đã tồn tại: {ma_phong} - {ten_phong}")
        except Exception as e:
            print(f"  ❌ Lỗi khi thêm {ma_phong}: {e}")
    
    conn.commit()
    conn.close()

def import_dich_vu():
    """Import thêm dữ liệu dịch vụ"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Dữ liệu dịch vụ mẫu
    dich_vu_data = [
        ('DV002', 'Khám chuyên khoa Nhi', 120000),
        ('DV003', 'Khám Sản phụ khoa', 150000),
        ('DV004', 'Khám Tai Mũi Họng', 100000),
        ('DV005', 'Khám Mắt', 80000),
        ('DV006', 'Khám Da liễu', 90000),
        ('DV007', 'Khám Tim mạch', 200000),
        ('DV008', 'Khám Thần kinh', 180000),
        ('DV009', 'Khám Cơ xương khớp', 130000),
        ('DV010', 'Khám Ung bướu', 250000),
        ('DV011', 'Cấp cứu', 300000),
        ('DV012', 'Chụp X-Quang', 150000),
        ('DV013', 'Siêu âm tổng quát', 200000),
        ('DV014', 'Siêu âm thai', 180000),
        ('DV015', 'Xét nghiệm máu tổng quát', 100000),
        ('DV016', 'Xét nghiệm sinh hóa', 150000),
        ('DV017', 'Xét nghiệm nước tiểu', 50000),
        ('DV018', 'Chụp CT Scanner', 500000),
        ('DV019', 'Chụp MRI', 800000),
        ('DV020', 'Nội soi dạ dày', 300000),
        ('DV021', 'Điện tim', 80000),
        ('DV022', 'Đo huyết áp 24h', 200000),
        ('DV023', 'Phục hồi chức năng', 150000),
        ('DV024', 'Vật lý trị liệu', 120000),
        ('DV025', 'Tư vấn dinh dưỡng', 100000)
    ]
    
    print("🩺 Đang import dữ liệu Dịch vụ...")
    for ma_dv, ten_dv, gia in dich_vu_data:
        try:
            # Check if already exists
            cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat WHERE MaDichVu = ?", (ma_dv,))
            exists = cur.fetchone()[0]
            
            if exists == 0:
                cur.execute("""
                    INSERT INTO DM_DichVuKyThuat(dv_id, MaDichVu, TenDichVu, GiaDichVu) 
                    VALUES (NEWID(), ?, ?, ?)
                """, (ma_dv, ten_dv, gia))
                print(f"  ✅ Đã thêm: {ma_dv} - {ten_dv} - {gia:,}đ")
            else:
                print(f"  ⚠️  Đã tồn tại: {ma_dv} - {ten_dv}")
        except Exception as e:
            print(f"  ❌ Lỗi khi thêm {ma_dv}: {e}")
    
    conn.commit()
    conn.close()

def import_bac_si():
    """Import dữ liệu bác sĩ"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Dữ liệu bác sĩ (không có PK_ID, sẽ assign sau)
    bac_si_data = [
        ('BS001', 'BS. Nguyễn Văn An', 'Nội tổng quát', '0901234567', 'bs.an@hospital.com'),
        ('BS002', 'TS.BS. Trần Thị Bình', 'Nhi khoa', '0907654321', 'bs.binh@hospital.com'),
        ('BS003', 'PGS.TS. Lê Văn Cường', 'Sản phụ khoa', '0912345678', 'bs.cuong@hospital.com'),
        ('BS004', 'BS. Phạm Thị Dung', 'Tai Mũi Họng', '0987654321', 'bs.dung@hospital.com'),
        ('BS005', 'BS. Hoàng Minh Tuan', 'Mắt', '0934567890', 'bs.tuan@hospital.com'),
        ('BS006', 'BS. Đinh Thị Hoa', 'Da liễu', '0923456789', 'bs.hoa@hospital.com'),
        ('BS007', 'GS.TS. Vũ Công Minh', 'Tim mạch', '0945678901', 'bs.minh@hospital.com'),
        ('BS008', 'PGS. Ngô Thị Linh', 'Thần kinh', '0956789012', 'bs.linh@hospital.com'),
        ('BS009', 'BS. Bùi Văn Khoa', 'Cơ xương khớp', '0967890123', 'bs.khoa@hospital.com'),
        ('BS010', 'TS.BS. Mai Thị Lan', 'Ung bướu', '0978901234', 'bs.lan@hospital.com'),
        ('BS011', 'BS. Trịnh Văn Nam', 'Cấp cứu', '0989012345', 'bs.nam@hospital.com'),
        ('BS012', 'BS. Lý Thị Oanh', 'Chẩn đoán hình ảnh', '0990123456', 'bs.oanh@hospital.com'),
        ('BS013', 'BS. Đỗ Minh Phú', 'Chẩn đoán hình ảnh', '0901234560', 'bs.phu@hospital.com'),
        ('BS014', 'BS. Cao Thị Quyên', 'Xét nghiệm', '0912345601', 'bs.quyen@hospital.com'),
        ('BS015', 'BS. Lương Văn Sơn', 'Phục hồi chức năng', '0923456012', 'bs.son@hospital.com'),
    ]
    
    print("👨‍⚕️ Đang import dữ liệu Bác sĩ...")
    for ma_bs, ho_ten, chuyen_khoa, sdt, email in bac_si_data:
        try:
            # Check if already exists
            cur.execute("SELECT COUNT(*) FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
            exists = cur.fetchone()[0]
            
            if exists == 0:
                cur.execute("""
                    INSERT INTO BacSi(MaBacSi, HoTen, ChuyenKhoa, SoDienThoai, Email) 
                    VALUES (?, ?, ?, ?, ?)
                """, (ma_bs, ho_ten, chuyen_khoa, sdt, email))
                print(f"  ✅ Đã thêm: {ma_bs} - {ho_ten} - {chuyen_khoa}")
            else:
                print(f"  ⚠️  Đã tồn tại: {ma_bs} - {ho_ten}")
        except Exception as e:
            print(f"  ❌ Lỗi khi thêm {ma_bs}: {e}")
    
    conn.commit()
    conn.close()

def assign_doctors_to_clinics():
    """Gán bác sĩ vào phòng khám"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Mapping bác sĩ - phòng khám
    assignments = [
        ('BS001', 'PK001'),  # BS. Nguyễn Văn An -> Phòng Nội tổng quát
        ('BS002', 'PK002'),  # TS.BS. Trần Thị Bình -> Phòng Nhi khoa
        ('BS003', 'PK003'),  # PGS.TS. Lê Văn Cường -> Phòng Sản phụ khoa
        ('BS004', 'PK004'),  # BS. Phạm Thị Dung -> Phòng Tai Mũi Họng
        ('BS005', 'PK005'),  # BS. Hoàng Minh Tuan -> Phòng Mắt
        ('BS006', 'PK006'),  # BS. Đinh Thị Hoa -> Phòng Da liễu
        ('BS007', 'PK007'),  # GS.TS. Vũ Công Minh -> Phòng Tim mạch
        ('BS008', 'PK008'),  # PGS. Ngô Thị Linh -> Phòng Thần kinh
        ('BS009', 'PK009'),  # BS. Bùi Văn Khoa -> Phòng Cơ xương khớp
        ('BS010', 'PK010'),  # TS.BS. Mai Thị Lan -> Phòng Ung bướu
        ('BS011', 'PK011'),  # BS. Trịnh Văn Nam -> Phòng Cấp cứu
        ('BS012', 'PK012'),  # BS. Lý Thị Oanh -> Phòng X-Quang
        ('BS013', 'PK012'),  # BS. Đỗ Minh Phú -> Phòng X-Quang (shared)
        ('BS014', 'PK014'),  # BS. Cao Thị Quyên -> Phòng Xét nghiệm
        ('BS015', 'PK015'),  # BS. Lương Văn Sơn -> Phòng Phục hồi chức năng
    ]
    
    print("🔄 Đang gán bác sĩ vào phòng khám...")
    for ma_bs, ma_pk in assignments:
        try:
            # Get BS_ID and PK_ID
            cur.execute("SELECT BS_ID FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
            bs_row = cur.fetchone()
            if not bs_row:
                print(f"  ❌ Không tìm thấy bác sĩ {ma_bs}")
                continue
            bs_id = bs_row.BS_ID
            
            cur.execute("SELECT PK_ID FROM PhongKham WHERE MaPhong = ?", (ma_pk,))
            pk_row = cur.fetchone()
            if not pk_row:
                print(f"  ❌ Không tìm thấy phòng khám {ma_pk}")
                continue
            pk_id = pk_row.PK_ID
            
            # Update PhongKham with BS_ID (one doctor per clinic for primary assignment)
            cur.execute("SELECT BS_ID FROM PhongKham WHERE PK_ID = ?", (pk_id,))
            current_bs = cur.fetchone()
            
            if not current_bs or current_bs.BS_ID is None:
                cur.execute("UPDATE PhongKham SET BS_ID = ? WHERE PK_ID = ?", (bs_id, pk_id))
                print(f"  ✅ Đã gán bác sĩ {ma_bs} vào phòng khám {ma_pk}")
            else:
                print(f"  ⚠️  Phòng khám {ma_pk} đã có bác sĩ chính")
                
        except Exception as e:
            print(f"  ❌ Lỗi khi gán {ma_bs}: {e}")
    
    conn.commit()
    conn.close()

def show_statistics():
    """Hiển thị thống kê sau khi import"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Đếm phòng khám
    cur.execute("SELECT COUNT(*) FROM PhongKham")
    pk_count = cur.fetchone()[0]
    
    # Đếm dịch vụ
    cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat")
    dv_count = cur.fetchone()[0]
    
    # Đếm bác sĩ
    cur.execute("SELECT COUNT(*) FROM BacSi")
    bs_count = cur.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*50)
    print("           📊 THỐNG KÊ SAU IMPORT")
    print("="*50)
    print(f"🏥 Tổng số Phòng khám: {pk_count}")
    print(f"🩺 Tổng số Dịch vụ: {dv_count}")
    print(f"👨‍⚕️ Tổng số Bác sĩ: {bs_count}")
    print("="*50)

def main():
    print("="*60)
    print("     🚀 IMPORT DỮ LIỆU MẪU - PHÒNG KHÁM, DỊCH VỤ & BÁC SĨ")
    print("="*60)
    
    try:
        # Import phòng khám
        import_phong_kham()
        print()
        
        # Import dịch vụ
        import_dich_vu()
        print()
        
        # Import bác sĩ
        import_bac_si()
        print()
        
        # Hiển thị thống kê
        show_statistics()
        
        print("\n🎉 Import hoàn tất!")
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình import: {e}")

def main():
    """Main function to import sample data"""
    print("🚀 Bắt đầu import dữ liệu mẫu...")
    print("=" * 60)
    
    try:
        # Check database connection first
        check_database_ready()
        
        # Import data in correct order
        import_phong_kham()
        print()
        
        import_dich_vu()
        print()
        
        import_bac_si()
        print()
        
        assign_doctors_to_clinics()
        print()
        
        print("=" * 60)
        print("✅ Hoàn thành import dữ liệu mẫu!")
        print("📊 Dữ liệu đã sẵn sàng để sử dụng")
        print()
        print("🔍 Kiểm tra dữ liệu đã import:")
        
        # Show summary
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM PhongKham")
        pk_count = cur.fetchone()[0]
        print(f"   • Phòng khám: {pk_count} records")
        
        cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat")
        dv_count = cur.fetchone()[0]
        print(f"   • Dịch vụ: {dv_count} records")
        
        cur.execute("SELECT COUNT(*) FROM BacSi")
        bs_count = cur.fetchone()[0]
        print(f"   • Bác sĩ: {bs_count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi import dữ liệu: {e}")
        print("💡 Vui lòng kiểm tra:")
        print("   1. Database server đã khởi động?")
        print("   2. Cấu hình kết nối trong db.py đã đúng?")
        print("   3. Đã chạy init_db() để tạo schema?")
        sys.exit(1)

if __name__ == "__main__":
    main()