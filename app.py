#!/usr/bin/python3

#import dependencies
import datetime as dt
import numpy as np
import pandas as pd 

#import sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask
from flask import Flask, jsonify

#access sqlite file to query
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)

#creating variables for classes
measurement = Base.classes.measurement
station = Base.classes.station

#session link
session = Session(engine)

#flask app
app = Flask(__name__)

#Welcome route
@app.route("/")
def welcome():
	return(
        '''Welcome to the Climate Analysis API!<br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/temp/start/end<br/>'''
	)

#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation = session.query(measurement.date, measurement.prcp).\
		filter(measurement.date >= prev_year).all()
        precip = {date: prcp for date, prcp in precipitation}
        return jsonify(precip)

#station route
@app.route("/api/v1.0/stations")
def stations():
        results = session.query(station.station).all()
        stations = list(np.ravel(results))
        return jsonify(stations)

#temp route
@app.route("/api/v1.0/tobs")
def temp_monthly():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        results = session.query(measurement.tobs).\
                filter(measurement.station == 'USC00519281').\
                filter(measurement.date >= prev_year).all()
        temps = list(np.ravel(results))        
        return jsonify(temps)

#start/end date route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
        sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
        if not end:
                results = session.query(*sel).\
                        filter(measurement.date >= start).\
                        filter(measurement.date <= end).all()
                temps = list(np.ravel(results))
                return jsonify(temps)
        results = session.query(*sel).\
                filter(measurement.date >= start).\
                filter(measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

#run flask app
if __name__=='__main__':
        app.run()