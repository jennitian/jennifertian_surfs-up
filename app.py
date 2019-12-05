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

@app.route("/")
def welcome():
	return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
	)
