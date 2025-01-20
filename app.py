from flask import Flask, jsonify, render_template, request
import pandas as pd 
import numpy as np
from sqlalchemy import create_engine

db_url = 'sqlite:///ca_school.db'
engine = create_engine(db_url, echo=True)
# Data Proccessing Code-------------------------------------------
def most_achieve(achievment:str):
    join_Q = "Achievements a JOIN School s ON a.[School Number]=s.[School Number]"
    df = pd.read_sql(f"select [School Name], [{achievment}], City, Enrolment from ({join_Q})", engine)
    df[achievment] = df[achievment].replace(['nan'], np.nan)
    df.dropna(inplace= True)
    df[achievment].astype(np.float16)
    df.sort_values(by=achievment, ascending=False, inplace=True)
    df.reset_index(inplace=True)
    df = df.loc[:10]
    df.sort_values(by=achievment, ascending=True, inplace=True, ignore_index=True)
    data = list((zip(df['School Name'], df[achievment], df["City"], df["Enrolment"])))
    data = [{'category': school, 'value': achievement, "City": p, "Enrolment":e} for school, achievement, p, e in data]
    return data
def dist_map(level):
    select_Q = "[School Name], Latitude, Longitude, Enrolment"
    df = pd.read_sql(f"select {select_Q} from School where [School Level] == '{level}'", engine)
    df['Latitude'] = df['Latitude'].replace(['.'], np.nan)
    df["Longitude"] = df["Longitude"].replace(['.'], np.nan)
    df["Enrolment"] = df["Enrolment"].replace(['nan', np.nan], '50')
    df.dropna(inplace= True, ignore_index=True)
    df["Latitude"] = df["Latitude"].astype(np.float16)
    df["Longitude"] = df["Longitude"].astype(np.float16)
    data = list((zip(df['School Name'], df['Latitude'], df["Longitude"], df["Enrolment"])))
    data = [{'category': school, 'latitude': lat, "longitude": long, "Enrolment":e} for school,lat, long, e in data]
    # lat_min, lat_max = df['Latitude'].min(), df['Latitude'].max()
    # long_min, long_max = df['Longitude'].min(), df['Longitude'].max()
    # lat_min, lat_max = float(lat_min), float(lat_max)
    # long_min, long_max = float(long_min), float(long_max)
    # print(f"Latitude range: {lat_min} - {lat_max}")
    # print(f"Longitude range: {long_min} - {long_max}")
    # print([ (long_max+long_min)/2, (lat_max+lat_min)/2 ])
    return data
# dist_map("Elementary")
# Flask Code-------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/data_most_achieve", methods=["GET", "POST"])
def get_most_achieve_data():
    if request.method == "POST":
        inp = request.json
        achievment = inp.get('achievement', 'gifted_perc')
        return jsonify(most_achieve(achievment))
    return jsonify({"error": "Invalid request method"}), 405

@app.route("/data_dist_map", methods=["GET", "POST"])
def get_dist_map_data():
    if request.method == "POST":
        inp = request.json
        level = inp.get('level', 'Elementary')
        return jsonify(dist_map(level))
    return jsonify({"error": "Invalid request method"}), 405
