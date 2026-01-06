#!/usr/bin/env python3
"""
健康检查脚本
用于 Docker 容器健康检查和服务监控
"""
import sys
import urllib.request
import urllib.error

def check_health(url: str = "http://localhost:8000/health", timeout: int = 5) -> bool:
    """
    检查服务健康状态
    
    Args:
        url: 健康检查端点 URL
        timeout: 超时时间（秒）
    
    Returns:
        bool: 服务是否健康
    """
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        
        if response.status == 200:
            return True
        else:
            print(f"Health check failed with status code: {response.status}", file=sys.stderr)
            return False
            
    except urllib.error.URLError as e:
        print(f"Health check failed: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Health check error: {str(e)}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # 可以通过命令行参数指定 URL
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/health"
    
    is_healthy = check_health(url)
    
    # 退出码：0 表示健康，1 表示不健康
    sys.exit(0 if is_healthy else 1)

