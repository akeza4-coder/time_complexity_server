import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Analysis(db.Model):
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    algorithm_name = db.Column(db.String(100), nullable=True)
    theoretical_complexity = db.Column(db.String(50), nullable=True)
    n_max = db.Column(db.Integer, nullable=True)
    step = db.Column(db.Integer, nullable=True)
    local_snapshot_path = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "algorithm_name": self.algorithm_name,
            "theoretical_complexity": self.theoretical_complexity,
            "n_max": self.n_max,
            "step": self.step,
            "local_snapshot_path": self.local_snapshot_path,
            "timestamp": self.timestamp.isoformat(),
            "data": json.loads(self.data)
        }