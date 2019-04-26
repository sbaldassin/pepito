from tests.db.models import QNetDWFactRevenue
from tests.db.repositories.base_repository import BaseRepository


class QNetDWFactRevenueRepository(BaseRepository):
    def __init__(self):
        super(QNetDWFactRevenueRepository, self).__init__()
        self.model = QNetDWFactRevenue

    def get_by_external_customer_id(self, external_customer_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalCustomerID == external_customer_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
