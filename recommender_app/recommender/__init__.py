#!/usr/bin/env python3
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from recommender.controller import Controller
from recommender.model.model import Model
from recommender.model.config_flask import MyConfig

# Create app

app = Flask(__name__)
# Add bootstrap to app
