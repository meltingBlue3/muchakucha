#!/bin/bash
# Docker 快速启动脚本 (Linux/Mac)
# 用途：简化 Docker Compose 常用操作

ACTION=${1:-up}
MODE=${2:-dev}

COMPOSE_FILE="docker-compose.yml"
if [ "$MODE" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
fi

echo "====================================="
echo " Muchakucha Docker 管理脚本"
echo " 模式: $MODE"
echo "====================================="
echo ""

case $ACTION in
    up)
        echo "启动服务..."
        docker-compose -f $COMPOSE_FILE up -d
        echo ""
        echo "服务已启动!"
        echo "API 文档: http://localhost:8000/docs"
        echo "查看日志: ./docker-start.sh logs"
        ;;
    
    down)
        echo "停止服务..."
        docker-compose -f $COMPOSE_FILE down
        echo "服务已停止!"
        ;;
    
    restart)
        echo "重启服务..."
        docker-compose -f $COMPOSE_FILE restart
        echo "服务已重启!"
        ;;
    
    logs)
        echo "查看日志 (Ctrl+C 退出)..."
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
    
    status)
        echo "服务状态:"
        docker-compose -f $COMPOSE_FILE ps
        ;;
    
    build)
        echo "重新构建镜像..."
        docker-compose -f $COMPOSE_FILE build
        echo "构建完成!"
        ;;
    
    clean)
        echo "警告: 这将删除所有容器和数据卷!"
        read -p "确认删除? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            docker-compose -f $COMPOSE_FILE down -v
            echo "清理完成!"
        else
            echo "操作已取消"
        fi
        ;;
    
    init)
        echo "初始化环境..."
        
        # 检查 .env 文件
        if [ ! -f ".env" ]; then
            echo "创建 .env 文件..."
            if [ -f "env.example" ]; then
                cp env.example .env
                echo "已从 env.example 创建 .env 文件"
                echo "请编辑 .env 文件，填写必要的配置!"
            else
                echo "错误: env.example 文件不存在!"
                exit 1
            fi
        else
            echo ".env 文件已存在，跳过创建"
        fi
        
        # 生成 SECRET_KEY
        echo ""
        echo "生成安全密钥:"
        python3 -c "import secrets; print(secrets.token_urlsafe(32))"
        echo "请将此密钥填入 .env 文件的 SECRET_KEY 字段"
        
        echo ""
        echo "初始化完成! 下一步:"
        echo "1. 编辑 .env 文件，填写配置"
        echo "2. 运行: ./docker-start.sh up"
        ;;
    
    *)
        echo "未知操作: $ACTION"
        echo "可用操作: up, down, restart, logs, status, build, clean, init"
        echo ""
        echo "使用方法:"
        echo "  ./docker-start.sh [action] [mode]"
        echo ""
        echo "示例:"
        echo "  ./docker-start.sh up dev    # 启动开发环境"
        echo "  ./docker-start.sh up prod   # 启动生产环境"
        echo "  ./docker-start.sh logs      # 查看日志"
        echo "  ./docker-start.sh init      # 初始化环境"
        exit 1
        ;;
esac

echo ""

