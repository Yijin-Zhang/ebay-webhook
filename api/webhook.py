from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "asYD78V7a5ZSLWl5u1G4f_b1VAqguH7dUxFE6iIdfdjwY12wj2MyqtPBoVQ-hUhE"

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if challenge_code:
            return jsonify({"challengeResponse": challenge_code + VERIFICATION_TOKEN}), 200
    elif request.method == "POST":
        print("Received notification:", request.json)
        return jsonify({"status": "received"}), 200

    return "Webhook is running", 200
