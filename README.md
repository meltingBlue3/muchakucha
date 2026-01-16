# 家庭共享日历与任务管理系统 Backend

一个基于 FastAPI + SQLAlchemy 2.x + MySQL 的家庭共享日历和任务管理系统后端。

## 技术栈

- **Python**: 3.10+
- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **Database**: MySQL 8.0
- **Validation**: Pydantic v2
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

## 核心功能

### MVP 功能列表

1. **用户认证**
   - 用户注册
   - 用户登录（JWT Token）
   - 获取当前用户信息

2. **群组管理**
   - 创建/查看/更新/删除群组
   - 添加/移除群组成员
   - 成员角色管理（owner / admin / member）

3. **共享日历事件**
   - 创建/查看/更新/删除事件
   - 支持日期范围过滤
   - 全天事件支持
   - 支持标签分类和过滤

4. **共享任务**
   - 创建/查看/更新/删除任务
   - 任务状态管理（pending / in_progress / completed）
   - 任务优先级（low / medium / high）
   - 任务分配
   - 支持标签分类和过滤

5. **共享笔记**
   - 创建/查看/更新/删除笔记
   - 简单的标题和内容结构

6. **标签管理**
   - 创建/查看/更新/删除标签
   - 标签统计信息（关联的任务和事件数量）
   - 支持任务和事件使用标签分类

## 项目结构

```
muchakucha/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 环境配置
│   ├── database.py             # 数据库连接
│   │
│   ├── models/                 # SQLAlchemy ORM 模型
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── event.py
│   │   ├── task.py
│   │   ├── note.py
│   │   └── label.py
│   │
│   ├── schemas/                # Pydantic 数据模式
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── event.py
│   │   ├── task.py
│   │   ├── note.py
│   │   └── label.py
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── event.py
│   │   ├── task.py
│   │   ├── note.py
│   │   └── label.py
│   │
│   ├── api/                    # REST API 路由
│   │   ├── deps.py             # 依赖注入
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── groups.py
│   │   ├── events.py
│   │   ├── tasks.py
│   │   ├── notes.py
│   │   └── labels.py
│   │
│   └── core/                   # 核心工具
│       ├── security.py         # JWT 和密码哈希
│       └── exceptions.py       # 自定义异常
│
├── requirements.txt
├── .env.example
└── README.md
```

## 快速开始

### 方式一：使用 Docker Compose（推荐）

这是最简单的启动方式，会自动配置 MySQL 数据库和后端服务。

#### 1. 配置环境变量

创建 `.env` 文件并配置以下变量：

```bash
# Windows PowerShell
New-Item -ItemType File -Path .env
# 编辑 .env 文件，至少配置 SECRET_KEY 和 DATABASE_URL
```

#### 2. 生成安全密钥

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

将生成的密钥填入 `.env` 文件的 `SECRET_KEY` 字段。

#### 3. 启动服务

```bash
# 构建并启动所有服务（MySQL + 后端）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止服务并删除数据卷（谨慎使用）
docker-compose down -v
```

#### 4. 访问应用

- API 地址: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 方式二：本地开发环境

#### 1. 环境要求

- Python 3.10+
- MySQL 8.0+

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

创建 `.env` 文件：

```env
# Application
APP_NAME=Family Calendar API
DEBUG=True

# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/family_calendar

# Security
SECRET_KEY=your-secret-key-here-please-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**注意**：`SECRET_KEY` 和 `DATABASE_URL` 为必填项。如果使用 TiDB Cloud 或其他云数据库，请配置相应的连接字符串。

#### 4. 创建数据库

```sql
CREATE DATABASE family_calendar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 5. 运行应用

```bash
# 使用 uvicorn 直接启动
uvicorn app.main:app --reload

# 或使用快速启动脚本
python run.py
```

应用将在 `http://localhost:8000` 启动。

#### 6. 访问 API 文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker 配置说明

本项目提供了完整的 Docker 支持。

### 文件说明

| 文件 | 用途 |
|------|------|
| `Dockerfile` | 生产环境镜像（使用非 root 用户运行） |
| `docker-compose.yml` | 容器编排配置 |
| `.dockerignore` | 排除不必要的文件 |
| `run.py` | 本地开发启动脚本 |

### Dockerfile 特性

**Dockerfile：**
- 基于 Python 3.11-slim-bookworm
- 使用非 root 用户运行（安全最佳实践）
- 安装 MariaDB 客户端库支持 MySQL 连接
- 优化层缓存

**注意**：当前配置使用 TiDB Cloud（兼容 MySQL 协议的云数据库）。如需使用本地 MySQL，请修改 `docker-compose.yml` 中的 `DATABASE_URL` 配置。

### Docker Compose 命令

**当前配置说明：**
- `docker-compose.yml` 仅包含后端服务
- 数据库连接通过 `DATABASE_URL` 环境变量配置
- 支持 TiDB Cloud 或任何 MySQL 兼容数据库

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 进入容器 shell
docker-compose exec backend bash

# 停止服务
docker-compose stop

# 停止并删除容器
docker-compose down
```

### 环境变量

所有环境变量都在 `.env` 文件中配置，关键配置项：

| 变量 | 说明 | 是否必需 |
|------|------|---------|
| `SECRET_KEY` | JWT 签名密钥 | 是 |
| `DATABASE_URL` | 数据库连接字符串 | 是 |
| `APP_NAME` | 应用名称 | 否（默认: "Family Calendar API"） |
| `DEBUG` | 调试模式 | 否（默认: False） |
| `ALGORITHM` | JWT 算法 | 否（默认: HS256） |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 过期时间（分钟） | 否（默认: 10080，7天） |

**DATABASE_URL 格式示例：**
- 本地 MySQL: `mysql+pymysql://root:password@localhost:3306/family_calendar`
- TiDB Cloud: `mysql+pymysql://user:password@host:port/database?ssl_ca=/path/to/ca.pem&ssl_verify_cert=true`

## API 端点概览

### 认证 `/api/auth`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 用户 `/api/users`

| Method | Endpoint | 说明 |
|--------|----------|------|
| PUT | `/api/users/me` | 更新当前用户信息 |

### 群组 `/api/groups`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups` | 创建群组 |
| GET | `/api/groups` | 获取当前用户的所有群组 |
| GET | `/api/groups/{group_id}` | 获取群组详情 |
| PUT | `/api/groups/{group_id}` | 更新群组信息 |
| DELETE | `/api/groups/{group_id}` | 删除群组 |
| POST | `/api/groups/{group_id}/members` | 添加成员 |
| GET | `/api/groups/{group_id}/members` | 获取群组成员列表 |
| PUT | `/api/groups/{group_id}/members/{user_id}` | 更新成员角色 |
| DELETE | `/api/groups/{group_id}/members/{user_id}` | 移除成员 |

### 事件 `/api/groups/{group_id}/events`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups/{group_id}/events` | 创建事件 |
| GET | `/api/groups/{group_id}/events` | 获取事件列表（支持 `start_date`、`end_date`、`label_ids` 查询参数） |
| GET | `/api/groups/{group_id}/events/{event_id}` | 获取事件详情 |
| PUT | `/api/groups/{group_id}/events/{event_id}` | 更新事件 |
| DELETE | `/api/groups/{group_id}/events/{event_id}` | 删除事件 |

### 任务 `/api/groups/{group_id}/tasks`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups/{group_id}/tasks` | 创建任务 |
| GET | `/api/groups/{group_id}/tasks` | 获取任务列表（支持 `status`、`priority`、`label_ids` 查询参数） |
| GET | `/api/groups/{group_id}/tasks/{task_id}` | 获取任务详情 |
| PUT | `/api/groups/{group_id}/tasks/{task_id}` | 更新任务 |
| DELETE | `/api/groups/{group_id}/tasks/{task_id}` | 删除任务 |

### 笔记 `/api/groups/{group_id}/notes`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups/{group_id}/notes` | 创建笔记 |
| GET | `/api/groups/{group_id}/notes` | 获取笔记列表 |
| GET | `/api/groups/{group_id}/notes/{note_id}` | 获取笔记详情 |
| PUT | `/api/groups/{group_id}/notes/{note_id}` | 更新笔记 |
| DELETE | `/api/groups/{group_id}/notes/{note_id}` | 删除笔记 |

### 标签 `/api/groups/{group_id}/labels`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups/{group_id}/labels` | 创建标签 |
| GET | `/api/groups/{group_id}/labels` | 获取标签列表 |
| GET | `/api/groups/{group_id}/labels/stats` | 获取带统计信息的标签列表 |
| GET | `/api/groups/{group_id}/labels/{label_id}` | 获取标签详情 |
| PUT | `/api/groups/{group_id}/labels/{label_id}` | 更新标签 |
| DELETE | `/api/groups/{group_id}/labels/{label_id}` | 删除标签 |

## 使用示例

### 1. 注册用户

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "nickname": "张三"
  }'
```

### 2. 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 3. 创建群组

```bash
curl -X POST "http://localhost:8000/api/groups" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "我的家庭",
    "description": "家庭成员共享日历和任务"
  }'
```

### 4. 创建事件

```bash
curl -X POST "http://localhost:8000/api/groups/1/events" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "家庭聚餐",
    "description": "周末全家聚餐",
    "start_time": "2026-01-10T18:00:00",
    "end_time": "2026-01-10T21:00:00",
    "all_day": false,
    "location": "xx餐厅"
  }'
```

## 数据库设计

### 表结构

- **users**: 用户基础信息
- **groups**: 群组（家庭/团队）
- **group_members**: 用户-群组关联（多对多）
- **events**: 日历事件
- **tasks**: 任务
- **notes**: 共享笔记
- **labels**: 标签
- **task_labels**: 任务-标签关联（多对多）
- **event_labels**: 事件-标签关联（多对多）

### 设计原则

- 不使用数据库级外键约束，在应用层保证数据一致性
- 使用 UTC 时间存储所有时间字段
- 简单的权限模型：owner / admin / member
- 所有业务数据按群组隔离

## 架构设计

### 三层架构

1. **API Layer** (`app/api/`)
   - REST API 路由定义
   - 请求/响应处理
   - 依赖注入

2. **Service Layer** (`app/services/`)
   - 业务逻辑封装
   - 权限校验
   - 数据处理

3. **Data Layer** (`app/models/`)
   - SQLAlchemy ORM 模型
   - 数据库交互

### 核心模块

- **Core** (`app/core/`)
  - `security.py`: JWT 生成/验证、密码哈希
  - `exceptions.py`: 自定义业务异常

- **Schemas** (`app/schemas/`)
  - Pydantic 数据验证模式
  - 请求/响应数据结构

## 开发建议

### 扩展功能

后续可以考虑添加以下功能：

- [ ] 事件和任务的提醒通知
- [ ] 周期性事件支持
- [ ] 更细粒度的权限控制
- [ ] 文件附件上传
- [ ] 活动日志记录
- [ ] 数据导出功能
- [ ] WebSocket 实时更新

### 生产部署建议

#### 环境配置

1. 修改 `SECRET_KEY` 为强随机字符串
2. 设置 `DEBUG=False`
3. 配置 CORS 允许的具体域名（修改 `app/main.py`）
4. 使用强密码保护数据库
5. 使用 HTTPS

#### Docker 生产部署

**使用 Dockerfile 构建：**

```bash
# 构建生产镜像
docker build -t muchakucha-backend:latest .

# 运行生产容器
docker run -d \
  --name muchakucha-backend \
  -p 8000:8000 \
  --env-file .env \
  muchakucha-backend:latest
```

**使用 Docker Compose：**

当前 `docker-compose.yml` 已配置为生产模式（无热重载）。如需进一步优化：

1. 配置资源限制（CPU、内存）
2. 使用 secrets 管理敏感信息
3. 配置健康检查和重启策略
4. 添加反向代理（Nginx）处理 SSL 终止

#### 其他建议

6. 配置数据库连接池（已在代码中配置）
7. 添加日志系统和监控
8. 配置反向代理（Nginx）处理 SSL 和负载均衡
9. 定期备份数据库
10. 使用容器编排工具（Kubernetes / Docker Swarm）用于多实例部署

## License

MIT

