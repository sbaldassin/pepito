from tests.db.models import QNetDwDimGameParimutuel
from tests.db.repositories.base_repository import BaseRepository


class QNetDwDimGameParimutuelRepository(BaseRepository):
    def __init__(self):
        super(QNetDwDimGameParimutuelRepository, self).__init__()
        self.model = QNetDwDimGameParimutuel
    
    def get_by_event_id(self, event_id, merchant_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.ExternalEventID == event_id,
                                                         self.model.MerchantID == merchant_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result
