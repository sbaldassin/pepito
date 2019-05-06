from tests.db.models import QNetTaskApx
from tests.db.repositories.base_repository import BaseRepository


class QNetTaskApxRepository(BaseRepository):
    def __init__(self):
        super(QNetTaskApxRepository, self).__init__()
        self.model = QNetTaskApx

    def get_by_task_id(self, task_id):
        with self.dao.create_session() as session:
            instances = session.query(self.model).filter(self.model.TaskID == task_id)
            session.expunge_all()
            result = []
            for instance in instances:
                result.append(instance.to_dict())
            return result