from flask import Flask, request, jsonify

#  api - application programming interface

app = Flask(__name__)  # Initialize server


@app.route("/", methods = ["POST"])  #get input x
def app_():
    var = request.form["hello"]
    return jsonify({"hello": var})


@app.route("/hello")
def hello_():
    return "hi"


app.run(host = "0.0.0.0")
