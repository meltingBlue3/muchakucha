# Docker 快速启动脚本 (Windows PowerShell)
# 用途：简化 Docker Compose 常用操作

param(
    [Parameter(Position=0)]
    [ValidateSet('up', 'down', 'restart', 'logs', 'status', 'build', 'clean', 'init')]
    [string]$Action = 'up',
    
    [Parameter(Position=1)]
    [ValidateSet('dev', 'prod')]
    [string]$Mode = 'dev'
)

$ComposeFile = if ($Mode -eq 'prod') { 'docker-compose.prod.yml' } else { 'docker-compose.yml' }

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host " Muchakucha Docker 管理脚本" -ForegroundColor Cyan
Write-Host " 模式: $Mode" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

switch ($Action) {
    'up' {
        Write-Host "启动服务..." -ForegroundColor Green
        docker-compose -f $ComposeFile up -d
        Write-Host ""
        Write-Host "服务已启动!" -ForegroundColor Green
        Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Yellow
        Write-Host "查看日志: .\docker-start.ps1 logs" -ForegroundColor Yellow
    }
    
    'down' {
        Write-Host "停止服务..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile down
        Write-Host "服务已停止!" -ForegroundColor Green
    }
    
    'restart' {
        Write-Host "重启服务..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile restart
        Write-Host "服务已重启!" -ForegroundColor Green
    }
    
    'logs' {
        Write-Host "查看日志 (Ctrl+C 退出)..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile logs -f
    }
    
    'status' {
        Write-Host "服务状态:" -ForegroundColor Yellow
        docker-compose -f $ComposeFile ps
    }
    
    'build' {
        Write-Host "重新构建镜像..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile build
        Write-Host "构建完成!" -ForegroundColor Green
    }
    
    'clean' {
        Write-Host "警告: 这将删除所有容器和数据卷!" -ForegroundColor Red
        $confirm = Read-Host "确认删除? (yes/no)"
        if ($confirm -eq 'yes') {
            docker-compose -f $ComposeFile down -v
            Write-Host "清理完成!" -ForegroundColor Green
        } else {
            Write-Host "操作已取消" -ForegroundColor Yellow
        }
    }
    
    'init' {
        Write-Host "初始化环境..." -ForegroundColor Green
        
        # 检查 .env 文件
        if (-not (Test-Path ".env")) {
            Write-Host "创建 .env 文件..." -ForegroundColor Yellow
            if (Test-Path "env.example") {
                Copy-Item "env.example" ".env"
                Write-Host "已从 env.example 创建 .env 文件" -ForegroundColor Green
                Write-Host "请编辑 .env 文件，填写必要的配置!" -ForegroundColor Yellow
            } else {
                Write-Host "错误: env.example 文件不存在!" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host ".env 文件已存在，跳过创建" -ForegroundColor Yellow
        }
        
        # 生成 SECRET_KEY
        Write-Host ""
        Write-Host "生成安全密钥:" -ForegroundColor Yellow
        $secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
        Write-Host $secretKey -ForegroundColor Green
        Write-Host "请将此密钥填入 .env 文件的 SECRET_KEY 字段" -ForegroundColor Yellow
        
        Write-Host ""
        Write-Host "初始化完成! 下一步:" -ForegroundColor Green
        Write-Host "1. 编辑 .env 文件，填写配置" -ForegroundColor White
        Write-Host "2. 运行: .\docker-start.ps1 up" -ForegroundColor White
    }
    
    default {
        Write-Host "未知操作: $Action" -ForegroundColor Red
        Write-Host "可用操作: up, down, restart, logs, status, build, clean, init" -ForegroundColor Yellow
    }
}

Write-Host ""

