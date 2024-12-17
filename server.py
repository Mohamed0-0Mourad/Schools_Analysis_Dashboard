from flask import Flask, jsonify, render_template
import pandas as pd 
from sqlalchemy import create_engine

# Data Proccessing Code-------------------------------------------
# def most_achieve():




# Flask Code-------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/data_most_achieve")
def get_most_achieve_data():
    data = [

    ]
    return jsonify(data)