import sqlite3
import os

def check_database():
    db_path = 'trading_system.db'

    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("数据库中的表:")
        for table in tables:
            print(f"  - {table[0]}")

        # 检查trade_records表
        if ('trade_records',) in tables:
            cursor.execute("SELECT COUNT(*) FROM trade_records")
            count = cursor.fetchone()[0]
            print(f"\ntrade_records表记录数: {count}")

            if count > 0:
                cursor.execute("SELECT * FROM trade_records LIMIT 3")
                records = cursor.fetchall()
                print("\n前3条记录:")
                for record in records:
                    print(f"  {record}")
        else:
            print("\ntrade_records表不存在")

        # 检查表结构
        if ('trade_records',) in tables:
            cursor.execute("PRAGMA table_info(trade_records)")
            columns = cursor.fetchall()
            print("\ntrade_records表结构:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")

        conn.close()

    except Exception as e:
        print(f"检查数据库时出错: {e}")

if __name__ == "__main__":
    check_database()
