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
def account_deletion():
    challenge_code = request.args.get("challenge_code")
    if challenge_code:
        print("Received challenge_code:", challenge_code)
        print("Using VERIFICATION_TOKEN:", VERIFICATION_TOKEN)
        print("Using ENDPOINT_URL:", ENDPOINT_URL)

        # 拼接字符串
        concat_str = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        print("Concat string for hashing:", concat_str)

        # 生成 SHA‑256 哈希
        hash_obj = hashlib.sha256(concat_str.encode("utf-8"))
        hash_hex = hash_obj.hexdigest()

        print("Generated hash:", hash_hex)
        return jsonify({"challengeResponse": hash_hex}), 200

    if request.method == "POST":
        notification = request.get_json()
        print("Received account deletion notification:", notification)
        return "OK", 200

    return "Webhook is running", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)