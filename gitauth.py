from flask import Flask, request, jsonify
import time

# 正经参数：
# api 是 chat 的入口，对应 CAPI；
# proxy 是代码补全接口，对应 proxy，这两个都需要 https
# 其他参数随便配置
ENDPOINTS = {"api": "https://60.204.219.177:8181/v1", "proxy": "https://60.204.219.177:8181"}
USER_CODE="MYCODE"
DEVICE_CODE = "0OMfCV7prArF6nT1H49nnv32sOo16yza"
ACCESS_TOKEN = "0OMfCV7prArF6nT1H49nnv32sOo16yza"
USER_NAME = "my_copilot_user"
COPILOT_TOKEN = "6d43a523cea5c062e0f339bfa7885d4"

# 设备认证参考文档：https://docs.github.com/zh/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
# 大概可以认为是：申请：/login/device/code，批准：/login/device，拿到 token：/login/oauth/access_token
app = Flask(__name__)

@app.route('/login/device/code', methods=['POST'])
def handle_dev_code():
    return jsonify({
            "expires_in": 900,
            "interval": 5,
            "user_code": USER_CODE,
            "device_code": DEVICE_CODE,
            "verification_uri":f"{request.url_root}login/device"
            })

@app.route('/login/device', methods=['GET'])
def handle_login_device():
    return "<html><body><h1>Hello, enjoy copilot. <br>you can close this page now.</h1></body</html>"

@app.route('/login/oauth/access_token', methods=['POST'])
def handle_oauth_access_token():
    return jsonify({
            "access_token": ACCESS_TOKEN,
            "scope": "user:email",
            "token_type": "bearer"
            })

# 这个是 copilot 相关信息的接口
@app.route('/copilot_internal/v2/token', methods=['GET'])
def handle_copilot_internal_v2_token():
    return jsonify({
            "endpoints": ENDPOINTS,
            "token": COPILOT_TOKEN,
            "expires_at": int(time.time() + 3600),
            "annotations_enabled": False,
            "chat_enabled": True,
            "chat_jetbrains_enabled": True,
            "code_quote_enabled": True,
            "codesearch":False,
            "copilot_ide_agent_chat_gpt4_small_prompt": False,
            "copilotignore_enabled":False,
            "individual":True,
            "nes_enabled":False,
            "prompt_8k":True,
            "public_suggestions": "disabled",
            "refresh_in":1500,
            "sku":"copilot_for_business_seat",
            "snippy_load_test_enabled":False,
            "telemetry":"disabled",
            "tracking_id":"d7e3cf63-303e-4975-9c45-b5d9c1cc0c0b",
            "intellij_editor_fetcher":False,
            "vsc_electron_fetcher":False,
            "vs_editor_fetcher":False,
            "vsc_panel_v2":False
            })

# 以下接口似乎关系不大，还缺了几个接口
@app.route('/api/v3/user', methods=['GET'])
def handle_v3_user():
    return jsonify({'login': USER_NAME})

@app.route('/user', methods=['GET'])
def handle_user():
    return jsonify({'login': USER_NAME})

@app.route('/api/v3/meta', methods=['GET'])
def handle_v3_meta():
    return jsonify({})

@app.route('/telemetry', methods=['POST'])
def handle_telmetry():
    return jsonify({"itemsReceived":0,"itemsAccepted":0,"appId":"null","errors":[]})

if __name__ == '__main__':
    app.run(debug=False)
