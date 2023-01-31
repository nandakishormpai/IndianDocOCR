from flask import Flask, jsonify, request, render_template, flash, session, url_for
import base64
from flask_cors import CORS
from ocr import ocr_image
import numpy as np
import validators
import urllib
import cv2
import os
import io
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "JUSTFORDEMO"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def ocr_web_app():
    if request.method == 'POST':
        if (request.form.get('imgurl') != ""):
            filepath = request.form.get('imgurl')
            if validators.url(filepath):
                url_response = urllib.request.urlopen(filepath)
                arr = np.asarray(
                    bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)
            else:
                flash('Invalid URL' + filepath, category='error')
        elif request.files['imgfile'].filename != '':
            file = request.files['imgfile']
            # basepath = os.path.dirname(__file__)
            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            img = cv2.imread(filepath)
            filepath = url_for('static', filename='uploads/' +
                               secure_filename(file.filename))

        else:
            flash('No Input', category='error')
            return render_template("base.html")
        words = ocr_image(img)
        return render_template("base.html", words=words, filepath=filepath)
    return render_template("base.html")


@app.route('/api')
def ocr_api():
    reqDict = request.get_json()
    image = reqDict["image"]
    img = base64.b64decode(image)
    img = Image.open(io.BytesIO(img))
    words = ocr_image(img)
    return jsonify({"result": words})


if __name__ == "__main__":
    app.run(debug=True)
