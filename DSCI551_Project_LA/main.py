from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import sys
import json
import requests
import plotly as py
# import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as plt

# import plotly.graph_objs as go

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search", methods=['GET', 'POST'])
def search():

    out = dict()

    query = f'https://neighborhood-score-la.firebaseio.com/NeighborhoodData.json'
    json_query = requests.get(query)
    dict_query = json.loads(json_query.text)

    neigh_list = list(dict_query.keys())
    out["neighboorhood"] = dict_query.keys()
    return render_template("search.html", result = neigh_list)

@app.route("/searchByParams", methods=['GET', 'POST'])
def search_post():
    request_data = request.data
    decoded_bytedata = request_data.decode('utf-8')  # Decode using the utf-8 encoding
    json_obj = json.loads(decoded_bytedata)
    print(json_obj)

    pd_crime, pd_housing, pd_act = {}, {}, {}

    if json_obj["crime"] and len(json_obj["crime"]) != 0:
        pd_crime = search_neighborhoods_features(json_obj["crime"], ["CrimeCount", 'CrimeScore']).to_dict()
    if json_obj["housing"] and len(json_obj["housing"]) != 0:
        pd_housing = search_neighborhoods_features(json_obj["housing"], ["HousingScore"]).to_dict()
    if json_obj["act"] and len(json_obj["act"]) != 0:
        pd_act = search_neighborhoods_features(json_obj["act"], ["AvgACT", "AvgScrEng","AvgScrMath"]).to_dict()

    out = {"crime": pd_crime,"housing": pd_housing, "act": pd_act}
    return render_template("search_result.html", result=out)

@app.route('/showBarChart', methods=['GET', 'POST'])
def line():
    request_data = request.data
    decoded_bytedata = request_data.decode('utf-8')  # Decode using the utf-8 encoding
    json_obj = json.loads(decoded_bytedata)
    print(json_obj)

    pd_crime, pd_housing, pd_act = {}, {}, {}

    if json_obj["crime"] and len(json_obj["crime"]) != 0:
        pd_crime = search_neighborhoods_features(json_obj["crime"], ["CrimeCount", 'CrimeScore']).to_dict()
    if json_obj["housing"] and len(json_obj["housing"]) != 0:
        pd_housing = search_neighborhoods_features(json_obj["housing"], ["HousingScore"]).to_dict()
    if json_obj["act"] and len(json_obj["act"]) != 0:
        pd_act = search_neighborhoods_features(json_obj["act"], ["AvgACT", "AvgScrEng", "AvgScrMath"]).to_dict()

    print(pd_crime)
    # out = {"crime": pd_crime, "housing": pd_housing, "act": pd_act}
    fig1 = createLayout(pd_act, "ACT Score", "Region", "ACT score per region")
    fig2 = createLayout(pd_housing, "Housing Score", "Region", "Housing score per region")
    fig3 = createLayout({"CrimeCount": pd_crime['CrimeCount']}, "Crime Count", "Region", "Crime count per region")
    fig4 = createLayout({"CrimeScore": pd_crime['CrimeScore']}, "Crime Score", "Region", "Crime score per region", [0,1])

    fig_json = json.dumps([fig1,fig2,fig3,fig4], cls=py.utils.PlotlyJSONEncoder)
    return render_template('chart_bar.html', graphJSON=fig_json)

def search_neighborhoods_features(NEIGHBORHOODS, FEATURES):
    query_output_dict = {}

    # First populate the query_output_dict
    for feat in FEATURES:
        for neig in NEIGHBORHOODS:
            query_output_dict[neig] = {feat: None}

    # Then query
    for feat in FEATURES:
        for neig in NEIGHBORHOODS:
            query = f'https://neighborhood-score-la.firebaseio.com/{feat}/{neig}.json'
            json_query = requests.get(query)
            dict_query = json.loads(json_query.text)
            query_output_dict[neig][feat] = dict_query

    df_output = pd.DataFrame.from_dict(query_output_dict).T

    return df_output

def createLayout(data, title, xaxis, yaxis, range = None):
    traces, idx = [], 0

    for k, v in data.items():
        list_neigh, list_values = [], []
        for k1, v1 in v.items():
            list_neigh.append(k1)
            if v1 is None: v1 = 0
            list_values.append(v1)

        traces.append(go.Bar(name=k, x=list_neigh, y=list_values, offsetgroup=idx))
        idx += 1

    if range is not None:
        layout = go.Layout(title=title, xaxis=dict(title=xaxis), yaxis=dict(title=yaxis, range=range))
    else:
        layout = go.Layout(title=title, xaxis=dict(title=xaxis), yaxis=dict(title=yaxis))
    data = traces
    fig = go.Figure(data=data, layout=layout)

    return fig

if __name__ == "__main__":
    app.run(debug=True)
