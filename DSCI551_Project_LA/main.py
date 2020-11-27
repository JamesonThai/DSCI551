from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import sys
import json
import requests
import plotly as py
# import plotly.plotly as py
import plotly.graph_objs as go
# plotly.graph_objs.Choropleth
import plotly.offline as plt
import plotly.express as px

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
    # print(json_obj)

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
        pd_act = search_neighborhoods_features(json_obj["act"], ["AvgACT", "AvgScrEng", "AvgScrMath", "AvgScrRead","AvgScrSci"]).to_dict()

    # print(pd_crime)
    # out = {"crime": pd_crime, "housing": pd_housing, "act": pd_act}
    fig1 = createLayout(pd_act, "ACT Score", "Region", "ACT score per region")
    fig2 = createLayout(pd_housing, "Housing Score", "Region", "Housing score per region")
    fig3 = createLayout({"CrimeCount": (pd_crime['CrimeCount'] if 'CrimeCount' in pd_crime else {})}, "Crime Count", "Region", "Crime count per region")
    fig4 = createLayout({"CrimeScore": (pd_crime['CrimeScore'] if 'CrimeScore' in pd_crime else {})}, "Crime Score", "Region", "Crime score per region", [0,0.3])

    # Mapping of GeoJSON
    # output1 = map_geojson(pd_act, "ACT_Scores")
    output1 = map_geojson(json_obj)
    # print(output1)

    fig_json = json.dumps([fig1,fig2,fig3,fig4, output1], cls=py.utils.PlotlyJSONEncoder)
    return render_template('chart_bar.html', graphJSON=fig_json)

# def map_geojson(df_input, obj_type):
def map_geojson(json_obj):
    print("Obtaining GeoJSON")
    with open("Los Angeles Neighborhood Map.geojson") as infile:
        geo_jsons = json.load(infile)
    infile.close()

    # Get list of neighborhoods
    score_neighborhooods = {}
    t1 = pd.read_excel("LA City Neighborhoods.xlsx").iloc[:,0]
    references = t1.values.tolist()
    
    # print(data_f)
    # Data is form of dict(list(dict))
    # default_map = {}

    # features = geo_jsons["features"]
    # for item in features:
    #     neighborhood_name = item['properties']['name']
    #     geo = item['geometry']
    #     lat = item['properties']['latitude']
    #     lon = item['properties']['longitude']

    #     default_map[neighborhood_name] = {"geo" : geo, "coordinates" : (lat, lon), "visibility" : 0}
    #     if neighborhood_name in references: score_neighborhooods[neighborhood_name] = {"geo": geo, "coordinates" : (lat, lon), "visibility" : 1}

        # break

    # print(df_input.head())
    # known_values = {}
    # for k,v in df_input.items():
    #     for k1,v2 in v.items():
    #         adder = v2
    #         if v2 is None: adder = 0
    #         if k1 in known_values.keys(): known_values[k1].append(adder)
    #         else: known_values[k1] = [adder]
    # list_neighbors, list_values = [],[]
    # for k,v in known_values.items():
    #     list_values.append(sum(v) / len(v))
    #     list_neighbors.append(k)

    # for i in range(len(list_neighbors)):
        # print(list_neighbors[i], list_values[i])
    x = set()
    for k,v in json_obj.items():
        x.update(v)

    queried_n = list(x)
    list_neighbors, list_values = [],[]
    for neighborhood in references: 
        outer_val = 0
        if neighborhood in queried_n: outer_val = 1
        list_neighbors.append(neighborhood)
        list_values.append(outer_val)


    data = {"name" : list_neighbors, "Queried" : list_values}
    out_data = pd.DataFrame.from_dict(data)

    #141 vs 77
    # print(len(references), len(score_neighborhooods.keys()))
    holder = t1.to_frame()
    # holder['randNumCol'] = np.random.randint(1, 6, holder.shape[0])
    holder['randNumCol'] = 0
    # print(holder)
    # mapper = px.choropleth_mapbox(holder, geojson = geo_jsons, locations = 'name', color="randNumCol", mapbox_style="carto-positron", center = {"lat": 34.0522,"lon" : -118.2437}, featureidkey="properties.name", zoom = 9)
    mapper = px.choropleth_mapbox(out_data, geojson = geo_jsons, locations = 'name', color="Queried", mapbox_style="carto-positron", center = {"lat": 34.0522,"lon" : -118.2437}, featureidkey="properties.name", zoom = 9)
    fig = go.Figure(data = mapper, layout = go.Layout(title = "LA Neighborhood Map"))
    fig.update_layout(coloraxis_showscale=False)
    return fig

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

    list_neigh, list_values = [], []
    for k, v in data.items():
        list_neigh, list_values = [], []
        for k1, v1 in v.items():
            list_neigh.append(k1)
            if v1 is None: v1 = 0
            list_values.append(round(v1,2))
        # print(list_neigh)
        # print(list_values)
        traces.append(go.Bar(name=k, x=list_neigh, y=list_values, offsetgroup=idx, text=list_values, textposition='outside'))
        idx += 1

    res_min, res_max = 0, 1
    if list_values:
        res_min = min(float(sub) for sub in list_values)
        res_max = max(float(sub) for sub in list_values)

    if range is not None:
        layout = go.Layout(title=title, xaxis=dict(title=xaxis), yaxis=dict(title=yaxis, range=range))
    else:
        layout = go.Layout(title=title, xaxis=dict(title=xaxis), yaxis=dict(title=yaxis, range=[res_min, res_max + res_max/6]))
    data = traces

    # total_labels = [{"x": x, "y": total} for x, total in zip(list_values, list_neigh)]

    fig = go.Figure(data=data, layout=layout)
    # Add averages here
    if title == "ACT Score":
        # print("act_scores")
        output = dict(color='maroon', width = 1)
        fig.add_shape(type='line', y0 = 20.02, y1 = 20.02, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
        # fig.add_shape(type='line', y0 = 19.96, y1 = 19.96, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
        # fig.add_shape(type='line', y0 = 20.44, y1 = 20.44, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
        # fig.add_shape(type='line', y0 = 19.786, y1 = 19.786, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
    elif title == "Housing Score":
        # print("Housing Scores")
        output = dict(color='maroon', width = 1)
        fig.add_shape(type='line', y0 = 829172, y1 = 829172, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
        # fig.add_hline(y=829172, row='all', col='all')
    elif title == "Crime Count":
        # print("CRIME COUNTS")
        output = dict(color='maroon', width = 1)
        fig.add_shape(type='line', y0 = 2377, y1 = 2377, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)
    else:
        output = dict(color='maroon', width = 1)
        fig.add_shape(type='line', y0 = 0.161093, y1 = 0.161093, yref = 'y', x0 = 0, x1 = 1, xref = 'paper', line = output)

    # fig = fig.update_layout(annotations=total_labels)
    return fig

if __name__ == "__main__":
    app.run(debug=True)
