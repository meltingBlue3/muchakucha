"""
数据库初始化脚本
运行此脚本将重新创建所有数据库表
警告：这将删除现有的所有数据！
"""
from app.database import engine, Base
from app.models import user, group, event, task, note

def init_database():
    """初始化数据库，创建所有表"""
    print("开始初始化数据库...")
    
    # 删除所有现有表
    print("删除现有表...")
    Base.metadata.drop_all(bind=engine)
    
    # 创建所有表
    print("创建新表...")
    Base.metadata.create_all(bind=engine)
    
    print("✓ 数据库初始化完成！")
    print("\n创建的表:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ 数据库初始化失败: {e}")
        print("\n请检查：")
        print("  1. .env 文件中的 DATABASE_URL 配置是否正确")
        print("  2. 数据库服务是否已启动")
        print("  3. 数据库用户是否有足够的权限")





