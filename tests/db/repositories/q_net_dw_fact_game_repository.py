from tests.db.models import QNetDwFactGame
from tests.db.repositories.base_repository import BaseRepository


class QNetDwFactGameRepository(BaseRepository):
    def __init__(self):
        super(QNetDwFactGameRepository, self).__init__()
        self.model = QNetDwFactGame

    def get_by_customer_id_and_merchant_id(self, customer_id, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == customer_id,
                                                         self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result

    def get_by_customer_id(self, customer_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == customer_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
