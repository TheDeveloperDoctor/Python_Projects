from flask import Flask
app = Flask(__name__)
@app.route("/")
def helloworld():
    return "<p> Hello World </p>"

app.run(debug=True)