from sqlalchemy import Column, DateTime, Integer, String, Boolean
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
    State = Column(String(50))
    CountryCode = Column(String(2))
    Email = Column(String(2))
    DateOfBirth = Column(String(50))
    PhoneNumber = Column(String(50))
    ExternalCustomerID = Column(String(50))
    CustomInt1 = Column(Integer)
    CustomInt2 = Column(Integer)
    CustomInt3 = Column(Integer)
    CustomInt4 = Column(Integer)
    CustomString1 = Column(String(50))
    CustomString2 = Column(String(50))
    CustomString3 = Column(String(50))
    CustomString4 = Column(String(50))
    LastKnownTimezone = Column(String(50))
    LastKnownLanguage = Column(String(50))
    #PromoCode = Column(String(50))
    BTag = Column(String(50))
    OptOutEmail = Column(Boolean)
    OptOutSms = Column(Boolean)
    OptOutPush = Column(Boolean)
    #OptOutMobilePush = Column(Boolean)

    def to_dict(self):
        return super(QNetCustomer, self).to_dict()


class QNetDwFactSignup(Base):
    __tablename__ = 'Q_net_dw_fact_signup'

    SignUpID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    ExternalCustomerID = Column(String(50))
    SignUpDate = Column(String(50))
    TimeID = Column(Integer)
    ChannelID = Column(Integer)

    def to_dict(self):
        return super(QNetDwFactSignup, self).to_dict()


class QNetDwFactSignIn(Base):
    __tablename__ = 'Q_net_dw_fact_signin'

    SignInID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    ExternalCustomerID = Column(String(50))
    TimeID = Column(Integer)
    GeoLocation = Column(Integer)
    DateCreated = Column(String(50))
    ActivityID = Column(String(50))
    ChannelID = Column(Integer)

    def to_dict(self):
        return super(QNetDwFactSignIn, self).to_dict()


class QNetDWFactWithdrawal(Base):
    __tablename__ = 'q_net_dw_fact_withdrawal'

    FactWithdrawalID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    TimeID = Column(Integer)
    Amount = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalCustomerID = Column(Integer)
    SignInID = Column(Integer)
    ActivityDate = Column(DateTime)

    def to_dict(self):
        return super(QNetDWFactWithdrawal, self).to_dict()