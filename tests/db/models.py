from sqlalchemy import Column, DateTime, Integer, String
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
    MerchantID = Column(Integer)
    Name = Column(String(100))
    Surname = Column(String(100))
    Address = Column(String(200))
    ZipCode = Column(String(25))
    City = Column(String(50))
    CountryCode = Column(String(2))
    Email = Column(String(2))
    DateOfBirth = Column(String(50))
    PhoneNumber = Column(String(50))
    ExternalCustomerID = Column(String(50))

    def to_dict(self):
        return super(QNetCustomer, self).to_dict()

