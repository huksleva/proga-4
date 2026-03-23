from flask import Flask


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    return ("<HTML><body>"
            "<p>Hello world</p>"
            "<form>"
            '<input type="text">'
            '<input type="submit">'
            "</form>"
           "</body></HTML>")


@app.route("/a", methods=["POST"])
def request():

    pass







if __name__ == "__main__":
    app.run(debug=True)