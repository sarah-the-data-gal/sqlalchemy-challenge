# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine= create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement= Base.classes.measurment 
Station= Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app= Flask(__name__)


#################################################
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation()
    session= Session(engine)
# Calculating the date from 1 year ago from the last data point
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
    year_ago = latest_date - dt.timedelta(days=365)
  # Query for the last 12 months of precipitation data
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    session.close()

#Dictionary 
precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
# Converting to a list 
stations = [result[0] for result in results]
    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
# Find the most active station
most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]

# Calculate the date 1 year ago from the last data point in the database
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
year_ago = latest_date - dt.timedelta(days=365)

#  Last 12 months of temperature observations of the most active station
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= year_ago).all()
    session.close()

# Convert to a list
temperature_observations = [{date: tobs} for date, tobs in results]
    return jsonify(temperature_observations)

@app.route("/api/v1.0/<start>")
def calc_temps_sd(start):
    session = Session(engine)
    # Query for min, avg, and max temperatures for the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    # Convert the query results to a dictionary
    temps = {
        "Min_Temp": results[0][0],
        "Avg_Temp": results[0][1],
        "Max_Temp": results[0][2]
    }

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)


#################################################

