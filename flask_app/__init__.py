from flask import Flask
from flask import render_template, redirect, request, session
app = Flask(__name__)
app.secret_key = "shhhhhhhh"