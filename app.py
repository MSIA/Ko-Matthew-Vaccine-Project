import logging.config

import numpy as np
from flask import Flask
from flask import render_template, request, redirect, url_for
from src.train import get_model, predict_ind

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.config.from_pyfile('config/flaskconfig.py')

logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])

model_path = app.config["MODEL_PATH"]
encoder_path = app.config["ENCODER_PATH"]

# @app.route("/")
# def main():
#     return "Hello world"

@app.route("/", methods=['GET', 'POST'])
def show_temp():
    if request.method == "GET":
        try:
            logger.info("main page returned")
            return render_template('index.html')
        except Exception as e:
            logger.error(e)

    if request.method == "POST":
        model, enc = get_model(model_path, encoder_path)
        gender = int(request.form["gender"])
        race = int(request.form["race"])
        educ = int(request.form["education"])
        marital = int(request.form["ms"])
        work = int(request.form["work"])
        region = int(request.form["region"])
        cat_vars = [gender, race, educ, marital, work, region]
        year = int(request.form["year"])
        prediction = predict_ind(model, enc, cat_vars, year)
        top3 = np.argsort(prediction)[::-1]
        top3 = top3[:3]
        top3_probs = [prediction[i] for i in top3]
        url_for_post = url_for('response_page', class1=top3[0], class2=top3[1],
                               class3=top3[2], prob1=top3_probs[0],
                               prob2=top3_probs[1], prob3=top3_probs[2])

        return redirect(url_for_post)


@app.route("/response/<class1>/<class2>/<class3>/<prob1>/<prob2>/<prob3>",
           methods=['GET', 'POST'])
def response_page(class1, class2, class3, prob1, prob2, prob3):
    if request.method == "GET":

        return str(class1 + " " + class2 + " " + class3 + " " + prob1 + " " + prob2 + " " + prob3)

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
