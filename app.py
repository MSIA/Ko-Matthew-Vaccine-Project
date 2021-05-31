from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")


# @app.route("/")
# def main():
#     return "Hello world"

@app.route("/")
def show_temp():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
