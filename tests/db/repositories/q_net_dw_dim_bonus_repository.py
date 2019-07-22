from tests.db.models import QNetDWDimBonus
from tests.db.repositories.base_repository import BaseRepository


class QNetDwDimBonusRepository(BaseRepository):
    def __init__(self):
        super(QNetDwDimBonusRepository, self).__init__()
        self.model = QNetDWDimBonus

    def get_by_merchant_name_and_vertical_id(self, merchant, name, vertical_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.MerchantID == merchant,
                                                         self.model.Name == name,
                                                         self.model.VerticalID == vertical_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
