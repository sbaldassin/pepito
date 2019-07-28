from tests.db.models import QNetDwDimFreeSpin
from tests.db.repositories.base_repository import BaseRepository


class QNetDwDimFreeSpinRepository(BaseRepository):
    def __init__(self):
        super(QNetDwDimFreeSpinRepository, self).__init__()
        self.model = QNetDwDimFreeSpin

    def get_by_merchant_id_name_value(self, merchant_id, name, value):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.MerchantID == merchant_id,
                                                         self.model.Name == name,
                                                         self.model.Value == value)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result

