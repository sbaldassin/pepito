from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def to_dict(self):
        model_dict = {}
        for column in self.__table__.columns:
            attribute = getattr(self, column.name)
            model_dict[column.name] = attribute
        return model_dict


Base = declarative_base(cls=Base)


class QNetCustomer(Base):
    __tablename__ = 'Q_Net_Customer'

    CustomerID = Column(Integer, primary_key=True)
    MechantID = Column(Integer)
    Name = Column(String(100))

    def to_dict(self):
        return super(QNetCustomer, self).to_dict()

