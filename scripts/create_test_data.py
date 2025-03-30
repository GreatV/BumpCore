import os
import sys
import sqlite3
from datetime import datetime
from passlib.context import CryptContext

# 获取项目根目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(root_dir, 'bumpbuddy.db')

# 密码加密设置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables(conn):
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        username TEXT UNIQUE,
        hashed_password TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at DATETIME,
        full_name TEXT,
        phone_number TEXT
    )
    ''')
    
    # 创建健康文章表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        category TEXT,
        tags TEXT,
        author TEXT,
        created_at TEXT
    )
    ''')
    
    conn.commit()

def insert_test_data(conn):
    cursor = conn.cursor()
    
    # 插入测试用户
    test_users = [
        {
            "email": "alice@example.com",
            "username": "alice",
            "password": "password123",
            "full_name": "Alice Johnson",
            "phone_number": "1234567890"
        },
        {
            "email": "bob@example.com",
            "username": "bob",
            "password": "password123",
            "full_name": "Bob Smith",
            "phone_number": "0987654321"
        },
        {
            "email": "carol@example.com",
            "username": "carol",
            "password": "password123",
            "full_name": "Carol Wang",
            "phone_number": "1357924680"
        },
        {
            "email": "david@example.com",
            "username": "david",
            "password": "password123",
            "full_name": "David Li",
            "phone_number": "2468013579"
        },
        {
            "email": "emma@example.com",
            "username": "emma",
            "password": "password123",
            "full_name": "Emma Liu",
            "phone_number": "1592638470"
        }
    ]
    
    for user in test_users:
        cursor.execute('''
        INSERT OR REPLACE INTO users 
        (email, username, hashed_password, is_active, created_at, full_name, phone_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user["email"],
            user["username"],
            pwd_context.hash(user["password"]),
            True,
            datetime.utcnow().isoformat(),
            user["full_name"],
            user["phone_number"]
        ))
    
    # 插入测试文章
    test_articles = [
        {
            "title": "孕期营养指南",
            "content": """
            孕期营养对母婴健康至关重要。以下是一些关键建议：

            1. 均衡饮食
            - 每天摄入充足的蛋白质
            - 补充叶酸和铁质
            - 适量摄入钙质

            2. 注意事项
            - 避免生食
            - 限制咖啡因摄入
            - 保持充足的水分摄入

            3. 推荐食物
            - 全谷物
            - 新鲜蔬果
            - 优质蛋白
            """,
            "category": "营养",
            "tags": "孕期,饮食,营养",
            "author": "营养师 王医生",
            "created_at": "2024-01-15T10:00:00"
        },
        {
            "title": "孕期运动指南",
            "content": """
            适度运动对孕期健康大有裨益。以下是一些安全的运动建议：

            1. 推荐运动
            - 散步
            - 孕期瑜伽
            - 游泳

            2. 运动原则
            - 循序渐进
            - 注意强度
            - 听从身体感受

            3. 注意事项
            - 避免剧烈运动
            - 保持适度
            - 及时补充水分
            """,
            "category": "运动",
            "tags": "运动,瑜伽,散步",
            "author": "健身教练 李教练",
            "created_at": "2024-01-16T14:30:00"
        },
        {
            "title": "孕期心理调适",
            "content": """
            孕期心理健康同样重要。以下是一些心理调适建议：

            1. 情绪管理
            - 学会放松
            - 保持乐观
            - 与家人沟通

            2. 压力缓解
            - 适度运动
            - 冥想放松
            - 听轻音乐

            3. 社交建议
            - 参加孕妇课程
            - 结识同期孕妈
            - 保持工作生活平衡
            """,
            "category": "心理",
            "tags": "心理,情绪,压力",
            "author": "心理咨询师 张医生",
            "created_at": "2024-01-17T09:15:00"
        },
        {
            "title": "孕期常见不适及应对",
            "content": """
            孕期可能会遇到各种不适症状，以下是应对建议：

            1. 孕吐
            - 少食多餐
            - 避免刺激性食物
            - 起床前先吃些干粮

            2. 腰背痛
            - 保持正确姿势
            - 适当运动
            - 使用孕妇支撑枕

            3. 腿抽筋
            - 补充钙质
            - 睡前拉伸腿部肌肉
            - 保持足部温暖
            """,
            "category": "健康",
            "tags": "不适,孕吐,腰痛",
            "author": "妇产科 陈医生",
            "created_at": "2024-01-18T11:20:00"
        },
        {
            "title": "产前检查时间表",
            "content": """
            规律的产检对保障母婴健康至关重要：

            1. 第一阶段 (1-12周)
            - 首次产检：确认怀孕及基本评估
            - 超声检查：确定孕周
            - 血液检查：血常规、血型等

            2. 第二阶段 (13-27周)
            - 常规产检：每4周一次
            - 唐氏筛查：16-20周
            - 大型超声：20-24周，检查胎儿发育

            3. 第三阶段 (28周至分娩)
            - 28-36周：每2周一次
            - 36周后：每周一次
            - 胎心监护：评估胎儿健康状况
            """,
            "category": "检查",
            "tags": "产检,超声,时间表",
            "author": "妇产科 林医生",
            "created_at": "2024-01-19T15:45:00"
        },
        {
            "title": "分娩准备与待产包",
            "content": """
            为即将到来的分娩做好准备：

            1. 分娩前准备
            - 制定分娩计划
            - 了解产兆
            - 掌握呼吸法

            2. 待产包必备物品
            - 孕妇用品：月子服、产后内裤、防溢乳垫
            - 婴儿用品：衣物、尿布、毛巾
            - 证件用品：身份证、医保卡、准生证

            3. 分娩后注意事项
            - 产后恢复
            - 母乳喂养
            - 新生儿护理
            """,
            "category": "分娩",
            "tags": "待产,分娩,产后",
            "author": "助产士 赵老师",
            "created_at": "2024-01-20T13:10:00"
        },
        {
            "title": "孕期皮肤护理指南",
            "content": """
            孕期荷尔蒙变化会影响皮肤状态，以下是护理建议：

            1. 妊娠纹预防
            - 保持适当体重增长
            - 使用孕妇专用妊娠纹霜
            - 保持皮肤水分充足

            2. 色素沉着问题
            - 避免阳光直射
            - 使用防晒产品
            - 选择温和保养品

            3. 敏感肌肤护理
            - 避免使用刺激性产品
            - 选择低敏配方
            - 保持充分睡眠
            """,
            "category": "护理",
            "tags": "皮肤,妊娠纹,护理",
            "author": "皮肤科 杨医生",
            "created_at": "2024-01-21T08:30:00"
        },
        {
            "title": "孕期饮食禁忌与安全指南",
            "content": """
            孕期饮食安全至关重要，以下是需要注意的事项：

            1. 食物禁忌
            - 未经巴氏消毒的奶制品
            - 生肉和半熟肉类
            - 高汞鱼类：金枪鱼、鲨鱼等

            2. 烹饪安全
            - 彻底清洗水果蔬菜
            - 食物需煮熟吃
            - 避免交叉污染

            3. 健康饮食建议
            - 多样化食物搭配
            - 控制糖分和精制碳水化合物
            - 增加膳食纤维摄入
            """,
            "category": "营养",
            "tags": "食品安全,禁忌,饮食",
            "author": "营养师 周老师",
            "created_at": "2024-01-22T16:20:00"
        },
        {
            "title": "孕期旅行须知",
            "content": """
            孕期旅行需要特别注意，以下是一些建议：

            1. 旅行时机
            - 第二孕期(14-28周)最适合旅行
            - 避免孕早期和临产前旅行
            - 出行前咨询医生意见

            2. 交通方式选择
            - 飞机：孕32周前较安全，准备医生证明
            - 汽车：每2小时休息一次，系好安全带
            - 火车：选择方便上下和靠近洗手间的座位

            3. 旅行准备
            - 携带产检记录
            - 准备孕期常用药品
            - 了解目的地医疗条件
            """,
            "category": "生活",
            "tags": "旅行,安全,准备",
            "author": "旅行顾问 黄老师",
            "created_at": "2024-01-23T10:40:00"
        },
        {
            "title": "胎教方法与益处",
            "content": """
            科学的胎教有助于促进胎儿发育：

            1. 音乐胎教
            - 选择舒缓的古典音乐
            - 保持适中音量
            - 每天1-2次，每次15-20分钟

            2. 抚触胎教
            - 轻柔抚摸腹部
            - 与胎儿互动交流
            - 感受胎动并回应

            3. 阅读胎教
            - 大声朗读儿童故事
            - 保持愉快心情
            - 培养语言环境敏感度
            """,
            "category": "胎教",
            "tags": "胎教,音乐,互动",
            "author": "儿童发展专家 郑教授",
            "created_at": "2024-01-24T14:15:00"
        }
    ]
    
    for article in test_articles:
        cursor.execute('''
        INSERT OR REPLACE INTO health_articles 
        (title, content, category, tags, author, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            article["title"],
            article["content"],
            article["category"],
            article["tags"],
            article["author"],
            article["created_at"]
        ))
    
    conn.commit()

def main():
    try:
        # 连接到数据库
        conn = sqlite3.connect(db_path)
        
        # 创建表
        create_tables(conn)
        
        # 插入测试数据
        insert_test_data(conn)
        
        print("测试数据已成功添加到数据库中！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
