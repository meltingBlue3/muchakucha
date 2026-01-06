# Docker 部署完整指南

本文档提供 Muchakucha 后端服务的详细 Docker 部署说明。

## 📋 目录

- [快速开始](#快速开始)
- [文件说明](#文件说明)
- [配置详解](#配置详解)
- [开发环境](#开发环境)
- [生产环境](#生产环境)
- [常见问题](#常见问题)
- [进阶配置](#进阶配置)

## 🚀 快速开始

### 第一次使用

```bash
# 1. 克隆项目
git clone <your-repo>
cd muchakucha

# 2. 初始化环境（根据操作系统选择）
# Windows PowerShell:
.\docker-start.ps1 init

# Linux/Mac (使用 Makefile):
make init

# Linux/Mac (使用脚本):
chmod +x docker-start.sh
./docker-start.sh init

# 3. 编辑 .env 文件，填写必要配置
# 至少修改以下字段：
#   - SECRET_KEY
#   - DB_PASSWORD
#   - DB_ROOT_PASSWORD

# 4. 启动服务
# Windows:
.\docker-start.ps1 up

# Linux/Mac:
make up
# 或
./docker-start.sh up

# 5. 访问服务
# API 文档: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
# 健康检查: http://localhost:8000/health
```

## 📁 文件说明

### Docker 配置文件

| 文件 | 说明 | 用途 |
|------|------|------|
| `Dockerfile` | 生产环境镜像 | 多阶段构建，优化体积，包含安全配置 |
| `Dockerfile.dev` | 开发环境镜像 | 支持热重载，包含开发工具 |
| `docker-compose.yml` | 开发环境编排 | MySQL + 后端，代码挂载，热重载 |
| `docker-compose.prod.yml` | 生产环境编排 | 资源限制，健康检查，多 worker |
| `docker-compose.override.yml.example` | 本地配置覆盖模板 | 自定义端口、环境变量等 |
| `.dockerignore` | Docker 构建忽略文件 | 减小镜像体积 |

### 管理工具

| 文件 | 说明 | 适用系统 |
|------|------|----------|
| `Makefile` | Make 命令集合 | Linux/Mac |
| `docker-start.sh` | Bash 启动脚本 | Linux/Mac |
| `docker-start.ps1` | PowerShell 启动脚本 | Windows |
| `healthcheck.py` | 健康检查脚本 | 跨平台 |

### 其他配置

| 文件 | 说明 |
|------|------|
| `env.example` | 环境变量模板 |
| `nginx/nginx.conf.example` | Nginx 反向代理配置示例 |
| `.github/workflows/docker-build.yml` | GitHub Actions CI/CD 配置 |

## ⚙️ 配置详解

### 环境变量说明

在 `.env` 文件中配置：

```env
# 应用配置
APP_NAME=Family Calendar API          # 应用名称
DEBUG=False                            # 调试模式（生产环境必须为 False）

# 数据库配置
DB_NAME=family_calendar                # 数据库名
DB_USER=family_user                    # 数据库用户
DB_PASSWORD=your_secure_password       # 数据库密码（必须修改）
DB_ROOT_PASSWORD=your_root_password    # 数据库 root 密码（必须修改）
DB_PORT=3306                           # 数据库端口

# 数据库连接 URL
# 本地开发：
DATABASE_URL=mysql+pymysql://family_user:password@localhost:3306/family_calendar
# Docker 环境会自动使用容器间通信

# 安全配置
SECRET_KEY=your_secret_key_here        # JWT 签名密钥（必须修改，32+ 字符）
ALGORITHM=HS256                        # JWT 算法
ACCESS_TOKEN_EXPIRE_MINUTES=10080      # Token 过期时间（分钟）

# 服务端口
BACKEND_PORT=8000                      # 后端服务端口
```

### 生成安全密钥

```bash
# Python 方式
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL 方式
openssl rand -base64 32

# PowerShell 方式
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

## 💻 开发环境

### 使用 docker-compose.yml

开发环境配置特点：
- 代码热重载
- 数据库端口暴露到宿主机（3306）
- 详细日志输出
- 代码卷挂载（实时同步修改）

### 启动开发环境

```bash
# 方式 1: Makefile
make up

# 方式 2: 脚本
./docker-start.sh up        # Linux/Mac
.\docker-start.ps1 up       # Windows

# 方式 3: Docker Compose
docker-compose up -d
```

### 查看日志

```bash
# 所有服务日志
make logs
docker-compose logs -f

# 仅后端日志
make logs-backend
docker-compose logs -f backend

# 仅数据库日志
make logs-db
docker-compose logs -f db
```

### 进入容器

```bash
# 进入后端容器
make shell
docker-compose exec backend bash

# 进入数据库容器
make db-shell
docker-compose exec db mysql -u root -p
```

### 本地自定义配置

复制 `docker-compose.override.yml.example` 为 `docker-compose.override.yml`：

```bash
cp docker-compose.override.yml.example docker-compose.override.yml
```

编辑 `docker-compose.override.yml` 来自定义本地配置，例如：

```yaml
version: '3.8'

services:
  backend:
    ports:
      - "8001:8000"  # 使用不同端口
    environment:
      DEBUG: "True"
```

## 🏭 生产环境

### 使用 docker-compose.prod.yml

生产环境配置特点：
- 无代码卷挂载（使用镜像内代码）
- 多 worker 进程（4 个）
- 资源限制（CPU、内存）
- 健康检查
- 自动重启策略
- 数据库端口不对外暴露

### 部署步骤

#### 1. 准备配置

```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env，确保以下配置：
# - DEBUG=False
# - 使用强密码
# - SECRET_KEY 使用随机生成的密钥
```

#### 2. 构建镜像

```bash
# 构建生产镜像
docker build -t muchakucha-backend:latest .

# 或使用 docker-compose 构建
docker-compose -f docker-compose.prod.yml build
```

#### 3. 启动服务

```bash
# 使用脚本
.\docker-start.ps1 up prod          # Windows
./docker-start.sh up prod           # Linux/Mac
make up-prod                         # Linux/Mac

# 或直接使用 docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

#### 4. 验证部署

```bash
# 检查服务状态
docker-compose -f docker-compose.prod.yml ps

# 检查健康状态
curl http://localhost:8000/health

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend
```

### 配置 Nginx 反向代理

生产环境建议使用 Nginx 处理 SSL 和负载均衡。

#### 1. 复制配置模板

```bash
cp nginx/nginx.conf.example nginx/nginx.conf
```

#### 2. 修改配置

编辑 `nginx/nginx.conf`，替换 `your-domain.com` 为实际域名。

#### 3. 放置 SSL 证书

将 SSL 证书放到 `nginx/ssl/` 目录：

```
nginx/ssl/
  ├── fullchain.pem
  └── privkey.pem
```

#### 4. 启用 Nginx 服务

取消 `docker-compose.prod.yml` 中 nginx 服务的注释并启动：

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## ❓ 常见问题

### 1. 端口被占用

**问题**: `Error: bind: address already in use`

**解决方案**:
- 方式 1: 修改 `.env` 文件中的 `BACKEND_PORT` 或 `DB_PORT`
- 方式 2: 创建 `docker-compose.override.yml` 修改端口映射

### 2. 数据库连接失败

**问题**: `Can't connect to MySQL server`

**解决方案**:
```bash
# 1. 检查数据库容器状态
docker-compose ps

# 2. 查看数据库日志
docker-compose logs db

# 3. 确认 .env 中的数据库配置正确

# 4. 等待数据库初始化完成（首次启动需要时间）
docker-compose logs -f db
```

### 3. 代码修改不生效

**问题**: 修改代码后没有自动重载

**解决方案**:
```bash
# 开发环境：确保使用 docker-compose.yml（不是 prod）
docker-compose restart backend

# 或重新启动
docker-compose down
docker-compose up -d
```

### 4. 数据持久化

**问题**: 删除容器后数据丢失

**解决方案**:
```bash
# 停止容器但保留数据卷
docker-compose down

# 查看数据卷
docker volume ls

# 只有使用 -v 标志才会删除数据卷
# docker-compose down -v  # 谨慎使用！
```

### 5. 镜像体积过大

**问题**: Docker 镜像过大

**解决方案**:
```bash
# 使用多阶段构建的生产 Dockerfile
docker build -f Dockerfile -t muchakucha-backend:latest .

# 清理未使用的镜像
docker image prune -a

# 查看镜像大小
docker images muchakucha-backend
```

## 🔧 进阶配置

### 水平扩展（多实例）

修改 `docker-compose.prod.yml`：

```yaml
services:
  backend:
    deploy:
      replicas: 3  # 运行 3 个实例
```

或使用 `docker-compose scale`：

```bash
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### 资源限制

在 `docker-compose.prod.yml` 中已配置：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'      # 最多使用 2 个 CPU
          memory: 2G     # 最多使用 2GB 内存
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 数据库备份

```bash
# 手动备份
make backup-db

# 或使用 docker-compose
mkdir -p backups
docker-compose exec db mysqldump -u root -p family_calendar > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker-compose exec -T db mysql -u root -p family_calendar < backups/backup_20260106_120000.sql
```

### 日志管理

配置日志驱动：

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 环境分离

使用不同的 `.env` 文件：

```bash
# 开发环境
docker-compose --env-file .env.dev up -d

# 测试环境
docker-compose --env-file .env.test up -d

# 生产环境
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 🔐 安全最佳实践

1. **不要提交敏感信息**
   - `.env` 文件已在 `.gitignore` 中
   - 使用环境变量或 secrets 管理敏感数据

2. **使用强密码**
   - 数据库密码至少 16 字符
   - JWT SECRET_KEY 至少 32 字符

3. **最小权限原则**
   - Dockerfile 使用非 root 用户
   - 数据库不要使用 root 用户连接

4. **定期更新**
   - 定期更新基础镜像
   - 定期更新依赖包

5. **生产环境配置**
   - 设置 `DEBUG=False`
   - 配置具体的 CORS 允许域名
   - 使用 HTTPS
   - 不要暴露不必要的端口

## 📚 相关资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [FastAPI 部署文档](https://fastapi.tiangolo.com/deployment/)
- [MySQL Docker Hub](https://hub.docker.com/_/mysql)

## 🤝 贡献

如果发现问题或有改进建议，请提交 Issue 或 Pull Request。

---

**注意**: 本指南持续更新中，最新版本请查看项目仓库。

