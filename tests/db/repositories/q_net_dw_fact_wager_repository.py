from tests.db.models import QNetDwFactWager
from tests.db.repositories.base_repository import BaseRepository


class QNetDwFactWagerRepository(BaseRepository):
    def __init__(self):
        super(QNetDwFactWagerRepository, self).__init__()
        self.model = QNetDwFactWager

    def get_by_external_customer_id(self, external_customer_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == external_customer_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
        
    def get_by_external_customer_id_and_merchant_id(self, external_customer_id, mechant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == external_customer_id,
                                                         self.model.MerchantID == mechant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
        
    def get_by_external_customer_id_and_wagercount(self, external_customer_id, wagercount, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == external_customer_id,
                                                         self.model.WagerCount == wagercount,
                                                         self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result

