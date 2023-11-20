from src.models import MachineLearning, db
from datetime import datetime


class MachineLearningService:
    @staticmethod
    def bulk_create_entry(data_list):
        for json_data in data_list:
            new_entry = MachineLearning(**json_data)
            new_entry.timestamp = datetime.now()
            db.session.add(new_entry)
            db.session.commit()

    @staticmethod
    def create_entry(data):
        new_entry = MachineLearning(**data)
        new_entry.timestamp = datetime.now()
        db.session.add(new_entry)
        db.session.commit()

    def get_storage(params):
        variable = db.session.query(MachineLearning).all()
        return variable
