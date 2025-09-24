#!/usr/bin/env python3
"""Update database schema to move relationship from BacSi->PhongKham to PhongKham->BacSi"""

from db import init_db, get_conn

def update_schema():
    """Update database schema for new relationship"""
    print("="*60)
    print("      CẬP NHẬT DATABASE SCHEMA")
    print("="*60)
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        print("🔄 Đang cập nhật schema...")
        
        # Remove PK_ID column from BacSi if exists (old relationship)
        print("1️⃣ Xóa mối quan hệ cũ BacSi->PhongKham...")
        cur.execute("""
        IF COL_LENGTH('BacSi', 'PK_ID') IS NOT NULL
        BEGIN
            -- Drop foreign key constraint first
            DECLARE @constraint_name NVARCHAR(128)
            SELECT @constraint_name = name 
            FROM sys.foreign_keys 
            WHERE parent_object_id = OBJECT_ID('BacSi') 
            AND referenced_object_id = OBJECT_ID('PhongKham')
            
            IF @constraint_name IS NOT NULL
            BEGIN
                DECLARE @sql NVARCHAR(MAX) = 'ALTER TABLE BacSi DROP CONSTRAINT ' + @constraint_name
                EXEC sp_executesql @sql
            END
            
            -- Drop the column
            ALTER TABLE BacSi DROP COLUMN PK_ID
        END
        """)
        
        # Add BS_ID to PhongKham if not exists (new relationship)
        print("2️⃣ Tạo mối quan hệ mới PhongKham->BacSi...")
        cur.execute("""
        IF COL_LENGTH('PhongKham', 'BS_ID') IS NULL
            ALTER TABLE PhongKham ADD BS_ID UNIQUEIDENTIFIER 
            CONSTRAINT FK_PhongKham_BacSi FOREIGN KEY REFERENCES BacSi(BS_ID);
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Cập nhật schema thành công!")
        
        # Now assign doctors to clinics based on their specialty
        print("3️⃣ Gán bác sĩ vào phòng khám theo chuyên khoa...")
        assign_doctors_to_clinics()
        
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật schema: {e}")

def assign_doctors_to_clinics():
    """Assign doctors to clinics based on their specialty"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Mapping specialty to clinic code
        specialty_mapping = {
            'Nội tổng quát': 'PK001',
            'Nhi khoa': 'PK002', 
            'Sản phụ khoa': 'PK003',
            'Tai Mũi Họng': 'PK004',
            'Mắt': 'PK005',
            'Da liễu': 'PK006',
            'Tim mạch': 'PK007',
            'Thần kinh': 'PK008',
            'Cơ xương khớp': 'PK009',
            'Ung bướu': 'PK010',
            'Cấp cứu': 'PK011',
            'Chẩn đoán hình ảnh': 'PK012',  # X-Quang
            'Xét nghiệm': 'PK014',
            'Phục hồi chức năng': 'PK015'
        }
        
        # Update PhongKham with corresponding doctor
        for specialty, clinic_code in specialty_mapping.items():
            cur.execute("""
                UPDATE pk SET BS_ID = bs.BS_ID
                FROM PhongKham pk
                INNER JOIN BacSi bs ON bs.ChuyenKhoa = ?
                WHERE pk.MaPhong = ?
                AND pk.BS_ID IS NULL
            """, (specialty, clinic_code))
            
            # Check if update was successful
            if cur.rowcount > 0:
                cur.execute("SELECT bs.HoTen FROM BacSi bs INNER JOIN PhongKham pk ON pk.BS_ID = bs.BS_ID WHERE pk.MaPhong = ?", (clinic_code,))
                doctor = cur.fetchone()
                if doctor:
                    print(f"  ✅ {clinic_code}: {doctor.HoTen} ({specialty})")
        
        conn.commit()
        conn.close()
        
        print("✅ Gán bác sĩ vào phòng khám hoàn tất!")
        
    except Exception as e:
        print(f"❌ Lỗi khi gán bác sĩ: {e}")

if __name__ == "__main__":
    update_schema()
    print("\n🎉 Hoàn tất cập nhật!")