#!/usr/bin/env python3
from flask import Flask, render_template, request, url_for
from recommender.controller import Controller
app = Flask(__name__)


@app.route("/", methods=['GET'])
def blank_page():
    print("Blank page")
    return render_template("index/index.html", users=[],
                           searcher_text="")


def return_home():
    print("Trying to return!")
    return url_for('blank_page')


@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    text = request.form['text']
    input = Controller()
    ideal = input.get_recommendations(text)
    print("submitted text is: {}".format(text))
    return render_template("index/recommended.html", users=ideal,
                           searcher_text="{} Your recommended partners are:".format(text))
