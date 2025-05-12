import psycopg2
from psycopg2 import OperationalError
import os
from datetime import date
from config import settings

def check_db_connection():
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.USER_DB_NAME,
            password=settings.DB_PASS
        )
        conn.close()
        print("✅ Database connected successfully")
        return True
    except OperationalError as e:
        print("❌ Database connection failed:", e)
        return False

def is_subscribed_pg(user_id: str) -> bool:
    conn = check_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM users_all WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
    conn.close()
    return result is not None

def new_user_pg(user_id: str):
    conn = check_db_connection()
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO users_all (user_id, status, update_dtm)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    status = EXCLUDED.status,
                    update_dtm = EXCLUDED.update_dtm
            """, (user_id, "active", date.today()))
            conn.commit()
            print("✅ บันทึกหรืออัปเดต user_id:", user_id)
        except Exception as e:
            print("❌ เกิดข้อผิดพลาด:", e)
    conn.close()

def terminate_user_pg(user_id: str):
    conn = check_db_connection()
    with conn.cursor() as cur:
        try:
            cur.execute("""
                UPDATE users_all
                SET status = %s,
                    update_dtm = CURRENT_DATE
                WHERE user_id = %s
            """, ("Terminated", user_id))
            conn.commit()
            print(f"✅ ยกเลิกสมาชิก user_id: {user_id}")
        except Exception as e:
            print(f"❌ ERROR: {e}")
    conn.close()
