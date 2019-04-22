#!/usr/bin/env python3
from flask import render_template, request
from recommender.controller import Controller
from recommender import app

# Create app


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
