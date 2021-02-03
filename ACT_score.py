import pandas as pd
import googlemaps

pd_sat2019 = pd.read_csv('sat19_LA.csv')
pd_act2019 = pd.read_csv('act19_LA.csv')
pd_neighborhood = pd.read_csv('neighborhood_score.csv')
apiKey = 'Enter Your API'

gmaps = googlemaps.Client(key=apiKey)
neighborList = pd_neighborhood['RegionName'].tolist()
out = list()
count = 0
for index, row in pd_act2019.iterrows():
    school, AvgScrRead, AvgScrEng, AvgScrMath, AvgScrSci = row['SName'], row['AvgScrRead'], row['AvgScrEng'], row['AvgScrMath'], row['AvgScrSci']

    schoolInfo = list()
    if school is None or pd.isna(school): continue

    geocode_result = gmaps.geocode(school + ',LA')

    if len(geocode_result) == 0:
        print(school + ' location is not found.')
        continue

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    addr1 = geocode_result[0]["address_components"][1]["long_name"]
    addr2 = geocode_result[0]["address_components"][2]["long_name"]
    addr3 = geocode_result[0]["address_components"][3]["long_name"]
    # state = geocode_result[0]["address_components"][5]["long_name"]

    schoolNeigh = None
    for add in geocode_result[0]["address_components"]:
        name = add["long_name"]
        if name in neighborList:
            schoolNeigh = name

    if schoolNeigh is None:
        #print(geocode_result[0]["address_components"][2]["long_name"])
        schoolNeigh = geocode_result[0]["address_components"][2]["long_name"]
        count += 1

    schoolInfo.append(school)
    schoolInfo.append(AvgScrRead)
    schoolInfo.append(AvgScrEng)
    schoolInfo.append(AvgScrMath)
    schoolInfo.append(AvgScrSci)
    schoolInfo.append((AvgScrRead + AvgScrEng + AvgScrMath + AvgScrSci)/4)
    schoolInfo.append(schoolNeigh)
    schoolInfo.append(lat)
    schoolInfo.append(lon)
    schoolInfo.append(addr1)
    schoolInfo.append(addr2)
    schoolInfo.append(addr3)



    ## iterate address_component and set "" if list is empty ( maximum number = 4 )
    ## check county
    ## get average sat score

    out.append(schoolInfo)

# df = pd.DataFrame(out, columns=['schoolName', 'Lan', 'Lon', 'City', 'District', 'State'])
df = pd.DataFrame(out, columns=['schoolName', 'AvgScrRead', 'AvgScrEng', 'AvgScrMath', 'AvgScrSci', 'AVERAGE', 'RegionName', 'Lan', 'Lon',  'Add1', 'Add2', 'Add3'])
gf = df.groupby('RegionName').agg({'AvgScrRead': "mean", 'AvgScrEng': "mean",'AvgScrMath': 'mean', 'AvgScrSci': 'mean', 'AVERAGE':'mean'})


df.to_csv('ACT19_LA_School.csv')
