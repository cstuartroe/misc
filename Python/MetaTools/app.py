from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('test.html')


@app.route('/token', methods=['POST'])
def token():
    with open("token.json", "w") as fh:
        json.dump(request.get_json(), fh, indent=2)
    return "Done."
