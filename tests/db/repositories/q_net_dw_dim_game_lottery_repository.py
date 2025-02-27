from tests.db.models import QNetDwDimGameLottery
from tests.db.repositories.base_repository import BaseRepository


class QNetDwDimGameLotteryRepository(BaseRepository):
    def __init__(self):
        super(QNetDwDimGameLotteryRepository, self).__init__()
        self.model = QNetDwDimGameLottery
    
    def get_by_name_category(self, name, category, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.Name == name,
                                                         self.model.Category == category,
                                                         self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
