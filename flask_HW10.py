#%%
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#%%
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
#%%
M = Base.classes.measurement
S = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        f"/start<br/>"
        f"/start/end<br/>"        
    )

@app.route("/precipitation")
def precipitation():
    results = session.query(M.date,M.prcp).all()
    all_names = dict(results)
    return jsonify(all_names)

@app.route("/stations")
def stations():
    results = session.query(M.station, S.name).\
        group_by(M.station).filter(M.station==S.station).all()
    all_names = dict(results)
    return jsonify(all_names)

@app.route("/tobs")
def tobs():
    results = session.query(M.date, M.tobs).\
        filter(M.date>'2016-08-23').order_by(M.date.desc()).all()
    all_names = dict(results)
    return jsonify(all_names)

@app.route("/<start>")
def calc_temps1(start):  
    results= session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)
    
@app.route("/<start>/<end>")
def calc_temps2(start,end):
    results= session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).filter(M.date<=end).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True).order_by(M.date.desc())