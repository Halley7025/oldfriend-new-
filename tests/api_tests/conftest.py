import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    # 模拟后端测试环境地址
    return "http://localhost:8080/api/v1"

@pytest.fixture(scope="session")
def auth_token(base_url):
    """获取测试用户的鉴权Token"""
    # 实际项目中这里会调用登录接口，这里做Mock处理
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

@pytest.fixture
def api_client(auth_token):
    """封装携带Token的Requests Session"""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    })
    return session
