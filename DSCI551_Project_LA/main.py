from flask import Flask, request, render_template
import pandas as pd
import sys
import json
import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    app.run(debug=True)
