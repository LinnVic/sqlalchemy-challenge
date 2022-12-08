from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#  reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

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
        f"/api/v1.0/&ltstart&gt<br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt<br/>"
        f"Replace &ltstart&gt and &ltend&gt with a date in yyyy-mm-dd<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    date_and_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
    session.close()

    return jsonify({x:y for x,y in date_and_precip})


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations = session.query(Station.name, Station.longitude, Station.latitude, Station.elevation).all()
    session.close()

    data = []
    for a,b,c,d in stations:
        data.append({'name':a, 'longitude':b, 'lattitude':c, 'elevation':d})
    return jsonify(data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    tobs = session.query(Station.id, Measurement.tobs).filter(Measurement.date >= '2016-08-23').where(Station.id == 7).all()
    session.close()

    return jsonify([y for x,y in tobs])


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()
    
    data = []
    for a,b,c,d in query:
        data.append({'date':a, 'min':b, 'avg':c, 'max':d})
    return jsonify(data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).group_by(Measurement.date).all()
    session.close()
    
    data = []
    for a,b,c,d in query:
        data.append({'date':a, 'min':b, 'avg':c, 'max':d})
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
