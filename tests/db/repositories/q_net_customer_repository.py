from tests.db.models import QNetCustomer
from tests.db.repositories.base_repository import BaseRepository


class QNetCustomerRepository(BaseRepository):
    def __init__(self):
        super(QNetCustomerRepository, self).__init__()
        self.model = QNetCustomer

    def get_by_customer_id(self):
        with self.dao.create_session() as session:
            instance = session.query(self.model).first()
            session.expunge_all()
            return instance.to_dict()
