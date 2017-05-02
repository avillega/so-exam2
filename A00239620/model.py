from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_time = db.Column(db.Integer, nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    free_ram = db.Column(db.Integer, nullable=False)
    free_disk = db.Column(db.Integer, nullable=False)
