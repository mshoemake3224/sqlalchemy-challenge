import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

session = Session(engine)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()


    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    # Return a JSON list of stations from the dataset.
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)   
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    active_station = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()


    return jsonify(active_station)

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(results)
    
if __name__ == '__main__':
    app.run(debug=True)
