"""
API 快速测试脚本
用于验证系统是否正常运行

运行前请确保：
1. 已启动 FastAPI 应用（python run.py）
2. 数据库已初始化（python init_db.py）

运行: python test_api.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """打印分节标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response):
    """打印响应结果"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_health():
    """测试健康检查"""
    print_section("1. 健康检查")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    return response.status_code == 200

def test_register():
    """测试用户注册"""
    print_section("2. 用户注册")
    
    # 注册第一个用户
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": "test1@example.com",
            "password": "password123",
            "nickname": "测试用户1"
        }
    )
    print("注册用户1:")
    print_response(response)
    
    # 注册第二个用户
    response2 = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": "test2@example.com",
            "password": "password123",
            "nickname": "测试用户2"
        }
    )
    print("\n注册用户2:")
    print_response(response2)
    
    return response.status_code in [200, 201]

def test_login():
    """测试用户登录"""
    print_section("3. 用户登录")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "test1@example.com",
            "password": "password123"
        }
    )
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"\n✓ Token 获取成功: {token[:50]}...")
        return token
    return None

def test_get_me(token):
    """测试获取当前用户信息"""
    print_section("4. 获取当前用户信息")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print_response(response)
    return response.status_code == 200

def test_create_group(token):
    """测试创建群组"""
    print_section("5. 创建群组")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/groups",
        json={
            "name": "测试家庭群组",
            "description": "这是一个测试群组"
        },
        headers=headers
    )
    print_response(response)
    
    if response.status_code in [200, 201]:
        group_id = response.json()["id"]
        print(f"\n✓ 群组创建成功，ID: {group_id}")
        return group_id
    return None

def test_add_member(token, group_id):
    """测试添加群组成员"""
    print_section("6. 添加群组成员")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/members",
        json={
            "email": "test2@example.com",
            "role": "member"
        },
        headers=headers
    )
    print_response(response)
    return response.status_code in [200, 201]

def test_get_members(token, group_id):
    """测试获取群组成员列表"""
    print_section("7. 获取群组成员列表")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/groups/{group_id}/members",
        headers=headers
    )
    print_response(response)
    return response.status_code == 200

def test_create_event(token, group_id):
    """测试创建事件"""
    print_section("8. 创建日历事件")
    headers = {"Authorization": f"Bearer {token}"}
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    
    response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/events",
        json={
            "title": "家庭聚餐",
            "description": "周末聚餐活动",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "all_day": False,
            "location": "某某餐厅"
        },
        headers=headers
    )
    print_response(response)
    
    if response.status_code in [200, 201]:
        event_id = response.json()["id"]
        print(f"\n✓ 事件创建成功，ID: {event_id}")
        return event_id
    return None

def test_get_events(token, group_id):
    """测试获取事件列表"""
    print_section("9. 获取事件列表")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/groups/{group_id}/events",
        headers=headers
    )
    print_response(response)
    return response.status_code == 200

def test_create_task(token, group_id):
    """测试创建任务"""
    print_section("10. 创建任务")
    headers = {"Authorization": f"Bearer {token}"}
    
    due_date = (datetime.now() + timedelta(days=7)).date().isoformat()
    
    response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/tasks",
        json={
            "title": "购买食材",
            "description": "准备周末聚餐的食材",
            "due_date": due_date,
            "status": "pending",
            "priority": "high"
        },
        headers=headers
    )
    print_response(response)
    
    if response.status_code in [200, 201]:
        task_id = response.json()["id"]
        print(f"\n✓ 任务创建成功，ID: {task_id}")
        return task_id
    return None

def test_get_tasks(token, group_id):
    """测试获取任务列表"""
    print_section("11. 获取任务列表")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/groups/{group_id}/tasks",
        headers=headers
    )
    print_response(response)
    return response.status_code == 200

def test_create_note(token, group_id):
    """测试创建笔记"""
    print_section("12. 创建笔记")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/groups/{group_id}/notes",
        json={
            "title": "家庭会议纪要",
            "content": "本次会议讨论了以下内容：\n1. 周末聚餐安排\n2. 下周任务分配"
        },
        headers=headers
    )
    print_response(response)
    
    if response.status_code in [200, 201]:
        note_id = response.json()["id"]
        print(f"\n✓ 笔记创建成功，ID: {note_id}")
        return note_id
    return None

def test_get_notes(token, group_id):
    """测试获取笔记列表"""
    print_section("13. 获取笔记列表")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/groups/{group_id}/notes",
        headers=headers
    )
    print_response(response)
    return response.status_code == 200

def main():
    """主测试流程"""
    print("\n" + "🚀 " * 20)
    print("  家庭共享日历与任务管理系统 - API 测试")
    print("🚀 " * 20)
    
    results = []
    
    # 1. 健康检查
    results.append(("健康检查", test_health()))
    
    # 2. 用户注册
    results.append(("用户注册", test_register()))
    
    # 3. 用户登录
    token = test_login()
    results.append(("用户登录", token is not None))
    
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 4. 获取当前用户信息
    results.append(("获取用户信息", test_get_me(token)))
    
    # 5. 创建群组
    group_id = test_create_group(token)
    results.append(("创建群组", group_id is not None))
    
    if not group_id:
        print("\n❌ 群组创建失败，无法继续测试")
        return
    
    # 6. 添加成员
    results.append(("添加成员", test_add_member(token, group_id)))
    
    # 7. 获取成员列表
    results.append(("获取成员列表", test_get_members(token, group_id)))
    
    # 8. 创建事件
    event_id = test_create_event(token, group_id)
    results.append(("创建事件", event_id is not None))
    
    # 9. 获取事件列表
    results.append(("获取事件列表", test_get_events(token, group_id)))
    
    # 10. 创建任务
    task_id = test_create_task(token, group_id)
    results.append(("创建任务", task_id is not None))
    
    # 11. 获取任务列表
    results.append(("获取任务列表", test_get_tasks(token, group_id)))
    
    # 12. 创建笔记
    note_id = test_create_note(token, group_id)
    results.append(("创建笔记", note_id is not None))
    
    # 13. 获取笔记列表
    results.append(("获取笔记列表", test_get_notes(token, group_id)))
    
    # 打印测试结果
    print_section("测试结果汇总")
    print("\n")
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status:8} | {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print("\n" + "-"*60)
    print(f"总计: {passed}/{total} 测试通过")
    print("-"*60)
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查系统配置。")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器，请确保：")
        print("   1. FastAPI 应用已启动（python run.py）")
        print("   2. 服务运行在 http://localhost:8000")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")

