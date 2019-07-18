from tests.db.models import QNetDwDimGame
from tests.db.repositories.base_repository import BaseRepository


class QNetDwDimGameRepository(BaseRepository):
    def __init__(self):
        super(QNetDwDimGameRepository, self).__init__()
        self.model = QNetDwDimGame
    
    def get_by_id(self, id, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.GameID == id,
                                                         self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result

    def get_by_name(self, name):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.GameName == name)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result

    def get_by_merchant_id(self, merchant_id, limit=10):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.MerchantID == merchant_id)\
                .order_by(self.model.GameID.desc()).limit(limit)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result