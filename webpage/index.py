import math
import pandas as pd

OGC_DEGREE_TO_METERS = 6378137.0 * 2.0 * math.pi / 360
EPSILON = 0.000001

if __name__ == '__main__':
    # 10KM grid
    def gethcode(lon, lat, r=0.1):
        pi = int(math.floor((lon + 180) / r + EPSILON))
        pj = int(math.floor((90 - lat) / r + EPSILON))
        if (pi < 0):
            pi = 0
        if (pj < 0):
            pj = 0
        return str(pi)+"_"+str(pj)

    # 10KM grid
    # converts a distance in kilometers into an equivalent distance in degrees of longitude and latitude
    # creates a grid of cells that cover the area around the hurricane. 
    # Each cell is assigned a unique 'hcode' value based on its position in the grid
    # the function returns a list of all the 'hcode' values corresponding to the cells 
    # that intersect with the hurricane's area
    def gethcode2(lon, lat, r0, r=0.1):
        r0 = r0 * 1000 / OGC_DEGREE_TO_METERS
        xmin = lon - r0
        xmax = lon + r0
        ymin = lat - r0
        ymax = lat + r0
        #calculates the column index pi of the leftmost cell that intersects with the hurricane
        pi = int(math.floor((xmin + 180) / r + EPSILON))
        #calculates the row index pj of the topmost cell that intersects with the hurricane, 
        #by subtracting the hurricane's latitude from 90 (to account for the fact that latitude ranges from -90 to 90
        pj = int(math.floor((90 - ymax) / r + EPSILON))
        if (pi < 0):
            pi = 0
        if (pj < 0):
            pj = 0

        # This calculates the column index pi2 of the rightmost cell that intersects with the hurricane
        pi2 = int(math.floor((xmax + 180) / r + EPSILON))
        #This calculates the row index pj2 of the bottommost cell that intersects with the hurricane
        pj2 = int(math.floor((90 - ymin) / r + EPSILON))

        pnts = []
        for i in range(pi, pi2 + 1):
            for j in range(pj, pj2 + 1):
                pnts.append(str(i)+"_"+str(j))
        return pnts

    def add_hcodecol(row):
        return gethcode(row["LON"], row["LAT"])

    # takes a row of the hurricanedf DataFrame and returns a set of 'hcodeset' values 
    #based on the longitude, latitude, and radius of the hurricane described in the row
    def add_hcodesetcol(row):
        return gethcode2(row["LON"], row["LAT"], row["RADIUS_KM"])

    housedf = pd.read_csv('data/house.csv')
    housedf = housedf[["LON", "LAT"]]
    housedf.loc[:, "hcode"] = housedf.apply(add_hcodecol, axis=1)
    housedf.to_parquet("house.index")

    hurricanedf = pd.read_csv('data/hurricane.csv')
    hurricanedf = hurricanedf[["RADIUS_KM", "YEAR", "MONTH", "LON", "LAT", "USA_STATUS", "NATURE"]]
    hurricanedf = hurricanedf[(hurricanedf['USA_STATUS'].isin(['HU', 'HR'])) & (hurricanedf['NATURE'] == 'TS')]
    hurricanedf = hurricanedf.dropna(axis=0, how='any')
    hurricanedf.drop(["USA_STATUS", "NATURE"], axis=1, inplace=True)


    #creates a new column called 'hcodeset'
    hurricanedf.loc[:, "hcodeset"] = hurricanedf.apply(add_hcodesetcol, axis=1)
    hurricanedf.to_parquet("hurricane.index")
