import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set up the Database, give us access to HawaiiSQLite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the Database into our classes
Base = automap_base()
# Reflect tables, we can save our references to each table
Base.prepare(engine, reflect=True)

# Varibales for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database 
session = Session(engine)

# Set up Flask
app = Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the Date One Year Ago to begin Analysis
    # This function allows us to trace back a certain number of days 
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   # Get Precipitation Scores
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()

    # Create Dictionary 
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations Route 
@app.route("/api/v1.0/stations")
def stations():
    #Get Number of Stations
    results= session.query(Station.station).all()
    # unravel results into an array
    stations= list(np.ravel(results))
    return jsonify(stations=stations)

# Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # query primary station for all temperature scores from previous year 
    prev_year=dt.date(2017,8,23) - dt.timedelta(365)
    
    results= session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()

    # unravel results into an array
    temps= list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics Route 

# Start and end dates are not defined. Need to inpout them into link 
# Ex. /api/v1.0/temp/2017-06-01/2017-06-30
@app.route("/api/v1.0/temp/start/end")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# @app.route("/api/v1.0/temp/start/end")
# def stats(start=None, end=None):
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

#     if not end:
#         results= session.query(*sel).filter(Measurement.date >= start).all()
#         temps=list(np.ravel(results))
#         return jsonify(temps=temps)
    
#     results=session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
#     temps=list(np.ravel(results))
#     return jsonify(temps=temps)

