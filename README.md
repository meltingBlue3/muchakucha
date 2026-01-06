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

4. **共享任务**
   - 创建/查看/更新/删除任务
   - 任务状态管理（pending / in_progress / completed）
   - 任务优先级（low / medium / high）
   - 任务分配

5. **共享笔记**
   - 创建/查看/更新/删除笔记
   - 简单的标题和内容结构

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
│   │   └── note.py
│   │
│   ├── schemas/                # Pydantic 数据模式
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── event.py
│   │   ├── task.py
│   │   └── note.py
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── event.py
│   │   ├── task.py
│   │   └── note.py
│   │
│   ├── api/                    # REST API 路由
│   │   ├── deps.py             # 依赖注入
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── groups.py
│   │   ├── events.py
│   │   ├── tasks.py
│   │   └── notes.py
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

复制环境变量模板并修改配置：

```bash
# Windows PowerShell
Copy-Item env.example .env
# 编辑 .env 文件，至少修改 SECRET_KEY 和数据库密码
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

创建 `.env` 文件（参考 `env.example`）：

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

本项目提供了完整的 Docker 支持。详细部署指南请查看 [DOCKER.md](./DOCKER.md)。

### 核心文件

### 文件说明

| 文件 | 用途 |
|------|------|
| `Dockerfile` | 生产环境镜像（多阶段构建，优化体积） |
| `Dockerfile.dev` | 开发环境镜像（支持热重载） |
| `docker-compose.yml` | 编排配置（MySQL + 后端） |
| `.dockerignore` | 排除不必要的文件 |
| `env.example` | 环境变量模板 |

### Dockerfile 特性

**生产 Dockerfile（`Dockerfile`）：**
- 多阶段构建减小镜像体积
- 使用非 root 用户运行（安全最佳实践）
- 内置健康检查
- 支持多 worker 进程（默认 4 个）
- 优化层缓存

**开发 Dockerfile（`Dockerfile.dev`）：**
- 支持代码热重载
- 包含开发工具
- 更快的构建速度

### Docker Compose 服务

**db（MySQL 8.0）：**
- 自动初始化数据库和用户
- 数据持久化到 volume
- 健康检查
- 暴露端口 3306（可配置）

**backend（FastAPI）：**
- 依赖 db 服务健康检查
- 环境变量注入
- 暴露端口 8000（可配置）
- 开发模式支持代码挂载

### 快速启动方式

项目提供了多种便捷的启动方式，任选其一：

#### 方式 1：使用 Makefile（推荐 - Linux/Mac）

```bash
# 查看所有可用命令
make help

# 初始化环境
make init

# 启动服务
make up

# 查看日志
make logs

# 查看状态
make status

# 停止服务
make down

# 更多命令请运行 make help 查看
```

#### 方式 2：使用启动脚本

为了简化操作，项目提供了便捷的启动脚本：

**Windows PowerShell：**
```powershell
# 初始化环境（首次使用）
.\docker-start.ps1 init

# 启动服务
.\docker-start.ps1 up

# 查看日志
.\docker-start.ps1 logs

# 查看服务状态
.\docker-start.ps1 status

# 重启服务
.\docker-start.ps1 restart

# 停止服务
.\docker-start.ps1 down

# 重新构建
.\docker-start.ps1 build

# 清理所有数据（谨慎使用）
.\docker-start.ps1 clean

# 启动生产模式
.\docker-start.ps1 up prod
```

**Linux/Mac：**
```bash
# 添加执行权限（首次使用）
chmod +x docker-start.sh

# 初始化环境
./docker-start.sh init

# 启动服务
./docker-start.sh up

# 查看日志
./docker-start.sh logs

# 其他命令同上...
```

### 常用 Docker Compose 命令

```bash
# 启动所有服务
docker-compose up -d

# 仅启动数据库
docker-compose up -d db

# 重新构建并启动
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f db

# 进入容器 shell
docker-compose exec backend bash
docker-compose exec db mysql -u root -p

# 停止服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷
docker-compose down -v
```

### 环境变量

所有环境变量都在 `.env` 文件中配置，关键配置项：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | JWT 签名密钥（必须修改） | - |
| `DB_NAME` | 数据库名 | `family_calendar` |
| `DB_USER` | 数据库用户 | `family_user` |
| `DB_PASSWORD` | 数据库密码（必须修改） | - |
| `DB_ROOT_PASSWORD` | 数据库 root 密码（必须修改） | - |
| `BACKEND_PORT` | 后端服务端口 | `8000` |
| `DEBUG` | 调试模式 | `False` |

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
| GET | `/api/groups/{group_id}/events` | 获取事件列表 |
| GET | `/api/groups/{group_id}/events/{event_id}` | 获取事件详情 |
| PUT | `/api/groups/{group_id}/events/{event_id}` | 更新事件 |
| DELETE | `/api/groups/{group_id}/events/{event_id}` | 删除事件 |

### 任务 `/api/groups/{group_id}/tasks`

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/groups/{group_id}/tasks` | 创建任务 |
| GET | `/api/groups/{group_id}/tasks` | 获取任务列表 |
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

**使用生产 Dockerfile：**

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

生产环境需要修改 `docker-compose.yml`：

1. 移除后端服务的 volumes 挂载（避免代码热重载）
2. 将 command 改为生产模式（移除 `--reload`）
3. 配置资源限制（CPU、内存）
4. 使用 secrets 管理敏感信息
5. 配置健康检查和重启策略

#### 其他建议

6. 配置数据库连接池（已在代码中配置）
7. 添加日志系统和监控
8. 配置反向代理（Nginx）处理 SSL 和负载均衡
9. 定期备份数据库
10. 使用容器编排工具（Kubernetes / Docker Swarm）用于多实例部署

## License

MIT

