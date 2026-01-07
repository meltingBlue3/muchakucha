# 多阶段构建 - 第一阶段：构建阶段
FROM python:3.11-slim-bookworm AS builder

# 设置工作目录
WORKDIR /app

RUN rm -f /etc/apt/sources.list.d/debian.sources \
 && printf "deb https://mirrors.aliyun.com/debian bookworm main contrib non-free non-free-firmware\n\
deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware\n\
deb https://mirrors.aliyun.com/debian bookworm-updates main contrib non-free non-free-firmware\n" \
 > /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖到临时目录
RUN pip install --no-cache-dir --user -r requirements.txt

# 第二阶段：运行阶段
FROM python:3.11-slim-bookworm

# 设置工作目录
WORKDIR /app

RUN rm -f /etc/apt/sources.list.d/debian.sources \
 && printf "deb https://mirrors.aliyun.com/debian bookworm main contrib non-free non-free-firmware\n\
deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware\n\
deb https://mirrors.aliyun.com/debian bookworm-updates main contrib non-free non-free-firmware\n" \
 > /etc/apt/sources.list

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制已安装的依赖
COPY --from=builder /root/.local /root/.local

# 确保 Python 可以找到用户安装的包
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建非 root 用户（生产环境最佳实践）
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 启动命令（生产环境配置）
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

