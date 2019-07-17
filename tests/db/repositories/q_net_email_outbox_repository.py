from tests.db.models import EmailOutbox
from tests.db.repositories.base_repository import BaseRepository


class EmailOutboxRepository(BaseRepository):
    def __init__(self):
        super(EmailOutboxRepository, self).__init__()
        self.model = EmailOutbox

    def get_by_recipient(self, recipient):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.Recipients == recipient).all()
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
        return result
