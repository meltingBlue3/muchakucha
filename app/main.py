from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api import auth, users, groups, events, tasks, notes

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="家庭共享日历和任务管理系统 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 中间件配置（根据需要调整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(events.router)
app.include_router(tasks.router)
app.include_router(notes.router)


@app.on_event("startup")
def on_startup():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/", tags=["Root"])
def root():
    """根路径"""
    return {
        "message": "Welcome to Family Calendar API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """健康检查"""
    return {"status": "ok"}

