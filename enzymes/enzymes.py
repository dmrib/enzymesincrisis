import os
import data
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/premade_query/<string:query>")
def premade_query(query):
    session['dataset'] = data.create_d3_dataset(query)
    return render_template('visualization.html')

@app.route("/custom_query/", methods=['POST'])
def custom_query():
    query_result = data.create_d3_dataset(request.form['query'])
    if len(query_result) == 2:
        return render_template('emptysearch.html')
    else:
        session['dataset'] = query_result
        return render_template('visualization.html')

@app.route("/empty_search")
def empty_search():
    return render_template('emptysearch.html')


if __name__ == "__main__":
    app.run()
