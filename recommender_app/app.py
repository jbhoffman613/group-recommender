#!/usr/bin/env python3
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from recommender.controller import Controller

# Create app
app = Flask(__name__)
# Add bootstrap to app


@app.route("/", methods=['GET'])
def blank_page():
    return render_template("index/index.html", users=[],
                           searcher_text="")


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    text = request.form['text']
    input = Controller()
    ideal = input.get_recommendations(text)
    return render_template("index/recommended.html", users=ideal,
                           searcher_text="{} Your recommended partners are:".format(text))
