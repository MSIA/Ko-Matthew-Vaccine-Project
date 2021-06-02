import logging.config

from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.config.from_pyfile('config/flaskconfig.py')

logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])

# @app.route("/")
# def main():
#     return "Hello world"

@app.route("/")
def show_temp():
    try:
        logger.info("main page returned")
        return render_template('index.html')
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
