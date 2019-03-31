# import dependencies
from flask import Flask, jsonify

import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Because I could not connect to SQLite on my MAC I used MYSQL
engine = create_engine("mysql://root:games4fun@localhost/hawaii")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#--------------------------------------------------#

app = Flask(__name__)

@app.route("/")
def index():
    return (
        # List all routes that are available
        "Available routes:<br/>"
        "<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        "<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        "<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        "<a href='/api/v1.0/<start>'>/api/v1.0/start</a><br/>"
        "<a href='/api/v1.0/<start>/<end>'>/api/v1.0/start/end</a>"
            )

@app.route("/api/v1.0/precipitation")
def about():
        # Perform a query to retrieve the data and precipitation scores
        precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date.desc()).all()

        # Convert the query results to a Dictionary using date as the key and prcp as the value
        dict = []
        for x in precip:
                precip_dict = {}
                precip_dict["date"] = x[0]
                precip_dict["precipitation"] = x[1]
                dict.append(precip_dict)

        return jsonify(dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset after writing the query
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the dates and temperature observations from a year from the last data point
        tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date <= '2017-08-18').\
        filter(Measurement.date >= '2016-08-18').\
        order_by(Measurement.date.desc()).all()

        # Adding the results to a dictionary
        dict_tobs = []
        for x in tobs:
                t_dict = {}
                t_dict["date"] = x.date
                t_dict["tobs"] = x.tobs
                dict_tobs.append(t_dict)

        # Return a JSON list of Temperature Observations (tobs) for the previous year
        return jsonify(dict_tobs)

@app.route("/api/v1.0/<start>")
def sdate(start):
        # # Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
        # for a given end date
        s_date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

        # adding the results to a dictionary
        start_tobs = []
        for x in s_date:
                s_dict = {}
                s_dict["min temp"] = x[0]
                s_dict["avg temp"] = x[2]
                s_dict["max temp"] = x[1]
                start_tobs.append(s_dict)

        return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def edate(start, end):
        # Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
        # for a given start date
        e_date = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

        # adding the results to a dictionary
        end_tobs = []
        for x in e_date:
                e_dict = {}
                e_dict["min temp"] = x[0]
                e_dict["avg temp"] = x[2]
                e_dict["max temp"] = x[1]
                end_tobs.append(e_dict)

        return jsonify(end_tobs)

if __name__ == "__main__":
    app.run(debug=True)