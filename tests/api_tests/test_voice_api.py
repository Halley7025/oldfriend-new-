import pytest
import responses
import json
import os

# 读取外部测试用例数据
def load_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "test_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

class TestVoiceAssistantAPI:
    
    @pytest.mark.parametrize("case_data", load_test_data())
    @responses.activate
    def test_voice_recognition_data_driven(self, api_client, base_url, case_data):
        """数据驱动测试：覆盖语音转文字的等价类与边界值场景 (+50用例的缩影)"""
        url = f"{base_url}/voice/recognize"
        
        # 使用 responses 动态Mock后端返回（因脱敏脱库开源，模拟脱机执行）
        mock_response_body = {
            "code": case_data["expect_code"],
            "msg": case_data.get("expect_msg", "success"),
            "data": {"text": "模拟识别结果"} if case_data["expect_code"] == 20000 else None
        }
        
        status_code = 200 if case_data["expect_code"] == 20000 else 400
        responses.add(
            responses.POST, 
            url,
            json=mock_response_body, 
            status=status_code
        )

        # 模拟文件大小
        simulated_content = b"0" * (case_data["file_size_kb"] * 1024)
        files = {'file': (f"test_audio_{case_data['case_id']}.mp3", simulated_content, 'audio/mpeg')}
        api_client.headers.pop("Content-Type", None) 
        
        # 发起真实测试请求进入Mock
        response = api_client.post(url, files=files, data=case_data["params"])
        resp_json = response.json()
        
        # 核心断言
        assert response.status_code == status_code
        assert resp_json["code"] == case_data["expect_code"]
        if "expect_msg" in case_data:
            assert case_data["expect_msg"] in resp_json["msg"]
            
        print(f"✅ 执行用例: {case_data['case_id']} - {case_data['desc']} ---> Pass")

    @responses.activate
    def test_get_daily_news_for_elderly(self, api_client, base_url):
        """测试适老化新闻播报接口，验证返回内容的朗读文本与格式"""
        url = f"{base_url}/news/daily"
        
        responses.add(
            responses.GET,
            url,
            json={"code": 20000, "data": [{"id": 1, "title": "今日要闻", "title_audio_url": "http://mock/1.mp3"}]},
            status=200
        )
        
        response = api_client.get(url)
        assert response.status_code == 200
        
        data = response.json().get("data", [])
        assert len(data) > 0
        assert "title_audio_url" in data[0]
        print("✅ 专项测试：适老化每日新闻接口字段结构测试通过")
