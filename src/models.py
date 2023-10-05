from src import db


class MachineLearning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.String)
    response_text = db.Column(db.String)
    timestamp = db.Column(db.db.String)
    model_version = db.Column(db.db.String(64))

    def to_dict(self):
        return {
            'id': self.id,
            'prompt_text': self.prompt_text,
            'response_text': self.response_text,
            'timestamp': self.timestamp,
            'model_version': self.model_version
        }
