from flask import Flask, request, render_template

app = Flask(__name__)

# ОТКЛЮЧАЕМ сортировку ключей по алфавиту
app.json.sort_keys = False



@app.route("/login")
def login():
    return {"author": "1153307"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/size2json", methods=['POST'])
def size_to_json():
    from PIL import Image

    img = request.files['image']
    image = Image.open(img)

    # Проверка на .png
    if image.format != "PNG":
        return {"result": "invalid filetype"}

    return {"width": image.size[0], "height": image.size[1]}




@app.route("/showPicture", methods=['POST'])
def show_picture():
    from PIL import Image

    img = request.files['image']
    image = Image.open(img)


    return {"lol": 4}





if __name__ == "__main__":
    app.run(debug=True)