#!/usr/bin/env python3
from db import get_conn

def check_migration_status():
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        # Thống kê bệnh nhân
        cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN Tinh IS NOT NULL AND Tinh != '' THEN 1 ELSE 0 END) as has_province
        FROM BenhNhan
        """)
        
        stats = cur.fetchone()
        total = stats.total
        has_province = stats.has_province
        
        print(f"\n👳 Thống kê bệnh nhân:")
        print(f"   - Tổng số: {total}")
        print(f"   - Có thông tin tỉnh: {has_province}")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        conn.close()