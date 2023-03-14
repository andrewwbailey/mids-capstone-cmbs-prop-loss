import math

import json
import geopandas as gpd
import pandas as pd
from flask import Flask
from flask import render_template
from flask import request


OGC_DEGREE_TO_METERS = 6378137.0 * 2.0 * math.pi / 360

app = Flask(__name__, template_folder='templates')

# ol map https://openlayers.org/en/v5.3.0/examples/geojson.html
# pip install hilbertcurve
# pip install parquet

@app.route('/')
def home():
    return render_template('flaskapp.html')

@app.route('/filter')
def filter():
    # Read in the HOUSE index into a Pandas DataFrame 
    housecsvdf = pd.read_parquet('house.index')

    #Creates a GeoDataFrame from the housecsvdf DataFrame
    housedf = gpd.GeoDataFrame(housecsvdf, geometry=gpd.points_from_xy(housecsvdf.LON, housecsvdf.LAT))

    #Get the unique values from the 'hcode' column
    # all the house code
    houseset = set(housedf['hcode'])

    hurricanecsvdf = pd.read_parquet('hurricane.index')
    hurricanedf = gpd.GeoDataFrame(hurricanecsvdf, geometry=gpd.points_from_xy(hurricanecsvdf.LON, hurricanecsvdf.LAT))

    # Time filters
    # Filter hurricane dataset
    year = request.args.get('year')
    if len(year) > 0:
        hurricanedf.query("YEAR=="+str(year), inplace=True)
    quarter = request.args.get('quarter')
    if len(quarter) > 0:
        quarter = int(quarter)
        if quarter==1:
            hurricanedf.query("MONTH>=1 & MONTH<=3", inplace=True)
        if quarter==2:
            hurricanedf.query("MONTH>=4 & MONTH<=6", inplace=True)
        if quarter==3:
            hurricanedf.query("MONTH>=7 & MONTH<=9", inplace=True)
        if quarter==4:
            hurricanedf.query("MONTH>=10 & MONTH<=12", inplace=True)
    
    # all the hurricane code
    hurricaneset = set()
    # Go over each hurricane rows
    for index, hurricane in hurricanedf.iterrows():
        #creates a new set containing the values from the 'hcodeset' column 
        # takes the union of this set with the existing hurricane code set
        hurricaneset = hurricaneset | set(hurricane['hcodeset'])

    # get the intersection of house and hurricane codes
    resultset = houseset & hurricaneset

    # house exposed hurricane
    hurricanelist = []

    # all hurricane circles
    yellowhurricane = []

    # Go over each hurricane row
    for index, hurricane in hurricanedf.iterrows():
        print('test1' + str(hurricane))
        # This applies the buffer() method to the geometry column of the hurricane GeoDataFrame, 
        # generating a circular buffer polygon around each point in the 'geometry' column. 
        # The argument to buffer() is the radius of the circle, in degrees of longitude/latitude.

        #ccc -> POLYGON
        ccc = hurricane["geometry"].buffer(hurricane["RADIUS_KM"] * 1000 / OGC_DEGREE_TO_METERS)
        print('test2' + str(ccc))

        yellowhurricane.append(ccc)

        #create a new set called rrr that contains the intersection of two other sets: 
        #resultset and set(hurricane['hcodeset'])
        rrr = resultset & set(hurricane['hcodeset'])
        print('test3' + str(rrr))
        if len(rrr) > 0:
            hurricanelist.append(ccc)

    redhouse = []
    redhouseaddr = []

    greenhouse = []
    greenhouseaddr = []

    for index, house in housedf.iterrows():
        print('house' + str(house))
        flag = False
        if house["hcode"] in resultset:
            pnt = house["geometry"]
            for ccc in hurricanelist:
                if ccc.contains(pnt):
                    print("redhouseobject" + str(house["geometry"]))
                    redhouse.append(house["geometry"])
                    redhouseaddr.append(house["Address"])
                    flag = True
                    break
            if flag == False:
                print("greenhouseobject" + str(house["geometry"]))

                greenhouse.append(house["geometry"])
                greenhouseaddr.append(house["Address"])
        else:

            greenhouse.append(house["geometry"])
            greenhouseaddr.append(house["Address"])

    print("redhouse " + str(redhouse))
    dic = {"geometry":redhouse,"Address":redhouseaddr}
    print("redhousedic " + str(dic))

    redhousedf = gpd.GeoDataFrame(dic, crs="EPSG:4326")
    print('11111111111')
    print(redhousedf)

    print("greenhouse " + str(greenhouse))
    dic = {"geometry": greenhouse,"Address":greenhouseaddr}
    greenhousedf = gpd.GeoDataFrame(dic, crs="EPSG:4326")
    print('22222222222')
    print(greenhousedf)

    print("yellowhurricane " + str(yellowhurricane))
    dic = {"geometry": yellowhurricane}
    print("yellowhurricanedic " + str(dic))

    yellowhurricanedf = gpd.GeoDataFrame(dic, crs="EPSG:4326")

    print('333333333333')
    print(yellowhurricanedf)


    result = {}
    result['greenhouse'] = greenhousedf.to_json()
    result['redhouse'] = redhousedf.to_json()
    result['yellowhurricane'] = yellowhurricanedf.to_json()

    return result

@app.route('/join')
def join():
    address = request.args.get('address')
    financialdf = pd.read_csv('data/financial.csv')
    # print(financialdf.count())
    financialdf.query("Address=='" + address + "'", inplace=True)
    # print(financialdf.count())
    street = ""
    city = ""
    state = ""
    xdata = []
    ydata = []
    for index, financial in financialdf.iterrows():
        if len(street) < 1:
            street = financial["Street Address"]
        if len(city) < 1:
            city = financial["City"]
        if len(state) < 1:
            state = financial["State"]
        if  math.isnan(financial["Effective Rent"]) :
            continue
        xdata.append(str(financial["Year"]) + "-" + str(financial["Quarter"]))
        ydata.append(financial["Effective Rent"])

    rst = {}
    rst['street'] = street
    rst['city'] = city
    rst['state'] = state
    rst['xdata'] = xdata
    rst['ydata'] = ydata
    return json.dumps(rst)

if __name__ == '__main__':
    app.run(debug=True)
