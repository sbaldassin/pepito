from tests.db.models import QNetCustomer
from tests.db.repositories.base_repository import BaseRepository


class QNetCustomerRepository(BaseRepository):
    def __init__(self):
        super(QNetCustomerRepository, self).__init__()
        self.model = QNetCustomer

    def get_first(self):
        with self.dao.create_session() as session:
            instance = session.query(self.model).first()
            session.expunge_all()
            return instance.to_dict()

    def get_by_external_customer_id(self, external_customer_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == external_customer_id).all()
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
        return result

    def get_by_name_and_merchant_id(self, name, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.Name == name, self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
        return result
