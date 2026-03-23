from flask import Flask, request, render_template, send_from_directory
import os, uuid
from PIL import Image
import json


app = Flask(__name__)


@app.route("/", method=["GET"])
def main_page():
    return "Hello world"


@app.route("/a", method=["POST"])
def request():

    pass







if __name__ == "__main__":
    app.run(debug=True)