from flask import Flask
from playwright_script import run_login_if_authorized
import os

app = Flask(__name__)

@app.route('/BankOfGuam/<username>')
def login_bank(username):
    if username == "hello.world@gmail.com":
        return run_login_if_authorized(username)
    else:
        return "Unauthorized username", 403

#Required block to run properly on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
