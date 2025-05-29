from flask import Flask
from playwright_script import run_login_if_authorized

app = Flask(__name__)

@app.route('/BankOfGuam/<username>')
def login_bank(username):
    if username == "hello.world@gmail.com":
        return run_login_if_authorized(username)
    else:
        return "Unauthorized username", 403
