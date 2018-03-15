"""Modulo principal."""
from flask import Flask
app = Flask(__name__)
from app.controllers import routes
app.config.from_pyfile('../config.py')
