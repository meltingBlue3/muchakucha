.PHONY: help init up down restart logs status build clean test shell db-shell

# 默认目标
.DEFAULT_GOAL := help

# 颜色输出
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# 配置
COMPOSE_FILE := docker-compose.yml
COMPOSE_FILE_PROD := docker-compose.prod.yml

help: ## 显示帮助信息
	@echo "$(BLUE)=====================================$(NC)"
	@echo "$(BLUE) Muchakucha Docker 管理命令$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

init: ## 初始化开发环境
	@echo "$(YELLOW)初始化环境...$(NC)"
	@if [ ! -f .env ]; then \
		if [ -f env.example ]; then \
			cp env.example .env; \
			echo "$(GREEN)已创建 .env 文件$(NC)"; \
			echo "$(YELLOW)请编辑 .env 文件并填写必要的配置！$(NC)"; \
		else \
			echo "$(RED)错误: env.example 文件不存在$(NC)"; \
			exit 1; \
		fi \
	else \
		echo "$(YELLOW).env 文件已存在，跳过创建$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)生成安全密钥：$(NC)"
	@python3 -c "import secrets; print(secrets.token_urlsafe(32))"
	@echo "$(YELLOW)请将上述密钥填入 .env 文件的 SECRET_KEY 字段$(NC)"
	@echo ""
	@echo "$(GREEN)初始化完成！下一步运行: make up$(NC)"

up: ## 启动所有服务（开发模式）
	@echo "$(GREEN)启动开发环境...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo ""
	@echo "$(GREEN)服务已启动！$(NC)"
	@echo "$(YELLOW)API 文档: http://localhost:8000/docs$(NC)"
	@echo "$(YELLOW)查看日志: make logs$(NC)"

up-prod: ## 启动所有服务（生产模式）
	@echo "$(GREEN)启动生产环境...$(NC)"
	docker-compose -f $(COMPOSE_FILE_PROD) up -d
	@echo "$(GREEN)服务已启动！$(NC)"

down: ## 停止所有服务
	@echo "$(YELLOW)停止服务...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down
	@echo "$(GREEN)服务已停止！$(NC)"

restart: ## 重启所有服务
	@echo "$(YELLOW)重启服务...$(NC)"
	docker-compose -f $(COMPOSE_FILE) restart
	@echo "$(GREEN)服务已重启！$(NC)"

logs: ## 查看服务日志
	@echo "$(YELLOW)查看日志（Ctrl+C 退出）...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## 查看后端服务日志
	@echo "$(YELLOW)查看后端日志（Ctrl+C 退出）...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-db: ## 查看数据库日志
	@echo "$(YELLOW)查看数据库日志（Ctrl+C 退出）...$(NC)"
	docker-compose -f $(COMPOSE_FILE) logs -f db

status: ## 查看服务状态
	@echo "$(YELLOW)服务状态：$(NC)"
	docker-compose -f $(COMPOSE_FILE) ps

build: ## 重新构建镜像
	@echo "$(YELLOW)重新构建镜像...$(NC)"
	docker-compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)构建完成！$(NC)"

build-no-cache: ## 无缓存重新构建镜像
	@echo "$(YELLOW)无缓存重新构建镜像...$(NC)"
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	@echo "$(GREEN)构建完成！$(NC)"

clean: ## 清理所有容器和数据卷（谨慎使用）
	@echo "$(RED)警告: 这将删除所有容器和数据卷！$(NC)"
	@read -p "确认删除? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose -f $(COMPOSE_FILE) down -v; \
		echo "$(GREEN)清理完成！$(NC)"; \
	else \
		echo "$(YELLOW)操作已取消$(NC)"; \
	fi

shell: ## 进入后端容器 shell
	@echo "$(YELLOW)进入后端容器...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend bash

db-shell: ## 进入数据库容器
	@echo "$(YELLOW)进入数据库容器...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec db mysql -u root -p

test: ## 运行测试
	@echo "$(YELLOW)运行测试...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend pytest

format: ## 格式化代码
	@echo "$(YELLOW)格式化代码...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend black app/
	docker-compose -f $(COMPOSE_FILE) exec backend isort app/

lint: ## 代码检查
	@echo "$(YELLOW)运行代码检查...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend ruff check app/

migrate: ## 数据库迁移（如果需要）
	@echo "$(YELLOW)运行数据库迁移...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend python -m app.database

backup-db: ## 备份数据库
	@echo "$(YELLOW)备份数据库...$(NC)"
	@mkdir -p backups
	docker-compose -f $(COMPOSE_FILE) exec db mysqldump -u root -p family_calendar > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)备份完成！$(NC)"

