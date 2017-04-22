import data
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('example_custom_categories.htm')

if __name__ == "__main__":
    app.run()
