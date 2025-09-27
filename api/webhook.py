from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# ========== 你需要配置的部分 ==========

# 在 eBay 控制台里填的 Verification Token
VERIFICATION_TOKEN = "asYD78V7a5ZSLWl5u1G4f_b1VAqguH7dUxFE6iIdfdjwY12wj2MyqtPBoVQ-hUhE"

# 在 eBay 控制台里填的 Endpoint URL，一定要和这里保持完全一致
# 包括 https:// 开头，域名，路径（如果有）和末尾的 “/” 等
ENDPOINT_URL = "https://ebay-webhook-82evwjjy2-yj6666s-projects.vercel.app/"  

# ========== 下面是处理逻辑，不要轻易改动 ==========

@app.route("/", methods=["GET", "POST"])
def handle_account_deletion():
    # 验证阶段：eBay 会发 GET 请求带 challenge_code 参数
    challenge_code = request.args.get("challenge_code")
    if challenge_code is not None:
        # 拼接字符串：challenge_code + verificationToken + endpointURL
        concat_str = f"{challenge_code}{VERIFICATION_TOKEN}{ENDPOINT_URL}"
        # 计算 SHA-256 哈希（hex 格式）
        hash_obj = hashlib.sha256(concat_str.encode("utf-8"))
        hash_hex = hash_obj.hexdigest()
        # 返回 JSON 响应。Flask 的 jsonify 会自动设置 Content-Type: application/json
        return jsonify({"challengeResponse": hash_hex}), 200

    # 通知阶段：eBay 发 POST 请求发送账号删除通知
    if request.method == "POST":
        try:
            notification = request.get_json()
        except Exception as e:
            # 如果请求体解析失败，也返回 200（让 eBay 不重试？取决你对失败的策略）
            notification = None

        # 你可以在这里把通知写入日志或数据库，做你自己的业务处理
        app.logger.info("Received marketplace account deletion notification: %s", notification)

        # 必须返回 HTTP 200，否则 eBay 会认为失败
        return "OK", 200

    # 对于其他类型请求，可以返回一个简单信息或 200
    return "Webhook is running", 200


if __name__ == "__main__":
    # 仅用于本地开发时运行
    app.run(host="0.0.0.0", port=5000, debug=True)
