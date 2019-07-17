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


class EmailOutbox(Base):
    __tablename__ = 'EmailOutbox'

    EmailID = Column(Integer, primary_key=True)
    From = Column(String(100))
    FromDisplay = Column(String(100))
    Recipients = Column(String(500))
    IsHtml = Column(Integer)
    Body = Column(String(5000))
    AttachmentsCount = Column(Integer)
    DateSent = Column(String(50))

    def to_dict(self):
        return super(EmailOutbox, self).to_dict()


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


class QNetDWFactRevenue(Base):
    __tablename__ = 'Q_net_dw_fact_revenue'

    FactRevenueID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    TimeID = Column(Integer)
    EuroAmount = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalCustomerID = Column(Integer)
    SignInID = Column(Integer)
    ChannelID = Column(Integer)
    PaymentMethodID = Column(Integer)
    ActivityDate = Column(DateTime)

    def to_dict(self):
        return super(QNetDWFactRevenue, self).to_dict()


class QNetDWFactBonus(Base):
    __tablename__ = 'q_net_dw_fact_bonus'

    FactBonusID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    TimeID = Column(Integer)
    BonusID = Column(Integer)
    BonusEuroValue = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalCustomerID = Column(Integer)
    SignInID = Column(Integer)
    ActivityDate = Column(DateTime)

    def to_dict(self):
        return super(QNetDWFactBonus, self).to_dict()

    
class QNetDwFactWager(Base):
    __tablename__ = 'Q_Net_Dw_Fact_Wager'

    WagerID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    ExternalCustomerID = Column(String(50))
    GameID = Column(Integer)
    SignInID = Column(Integer)
    EuroCentsValue = Column(Integer)
    WagerTimeID = Column(Integer)
    WagerDate = Column(DateTime)
    DateCreated = Column(DateTime)
    VerticalID = Column(Integer)
    ChannelID = Column(Integer)
    WagerCount = Column(Integer)
    
    def to_dict(self):
        return super(QNetDwFactWager, self).to_dict()


class QNetDwFactPayout(Base):
    __tablename__ = 'Q_Net_Dw_Fact_Payout'

    FactPayoutID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    ExternalCustomerID = Column(String(50))
    GameID = Column(Integer)
    SignInID = Column(Integer)
    Amount = Column(Integer)
    TimeID = Column(Integer)
    ActivityDate = Column(DateTime)
    DateCreated = Column(DateTime)
    VerticalID = Column(Integer)
    PayoutCount = Column(Integer)

    def to_dict(self):
        return super(QNetDwFactPayout, self).to_dict()


class QNetDwDimGameParimutuel(Base):
    __tablename__ = 'Q_Net_Dw_Dim_Game_Parimutuel'
    
    GameID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    Event = Column(String(250))
    Breed = Column(String(250))
    EventDate = Column(DateTime)
    TimeID = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalEventID = Column(String(50))
    
    def to_dict(self):
        return super(QNetDwDimGameParimutuel, self).to_dict()


class QNetDwDimGameLottery(Base):
    __tablename__ = 'Q_Net_Dw_Dim_Game_Lottery'

    GameID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    Name = Column(String(250))
    Category = Column(String(250))
    DateCreated = Column(DateTime)
    DrawDate = Column(DateTime)
    TimeID = Column(Integer)

    def to_dict(self):
        return super(QNetDwDimGameLottery, self).to_dict()


class QNetDwDimGameSports(Base):
    __tablename__ = 'Q_Net_Dw_Dim_Game_Sports'

    GameID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    Sport = Column(String(250))
    League = Column(String(250))
    Event = Column(String(250))
    Live = Column(Boolean)
    EventDate = Column(DateTime)
    TimeID = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalEventID = Column(String(50))

    def to_dict(self):
        return super(QNetDwDimGameSports, self).to_dict()


class QNetDwDimGame(Base):
    __tablename__ = 'Q_Net_Dw_Dim_Game'

    GameID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    GameName = Column(String(250))
    GameCategory = Column(String(250))
    DateCreated = Column(DateTime)

    def to_dict(self):
        return super(QNetDwDimGame, self).to_dict()


class QNetDwFactGame(Base):
    __tablename__ = 'Q_Net_Dw_Fact_Game'

    FactGameID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    TimeID = Column(Integer)
    GameID = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalCustomerID = Column(String(50))
    SignInID = Column(Integer)
    ChannelID = Column(Integer)
    ActivityDate = Column(DateTime)

    def to_dict(self):
        return super(QNetDwFactGame, self).to_dict()


class QNetDwFactFreeSpin(Base):
    __tablename__ = 'Q_Net_Dw_Fact_FreeSpin'

    FactFreeSpinID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    TimeID = Column(Integer)
    FreeSpinID = Column(Integer)
    DateCreated = Column(DateTime)
    ExternalCustomerID = Column(String(50))
    SignInID = Column(Integer)
    ActivityDate = Column(DateTime)

    def to_dict(self):
        return super(QNetDwFactFreeSpin, self).to_dict()


class QNetTaskApx(Base):
    __tablename__ = 'Q_Net_Task_Apx'
    
    TaskID = Column(Integer, primary_key=True)
    MerchantID = Column(Integer)
    Type = Column(Integer)
    State = Column(Integer)
    Attempts = Column(Integer)
    DateCreated = Column(DateTime)
    Data = Column(String(250))
    Error = Column(String(200))
    
    def to_dict(self):
        return super(QNetTaskApx, self).to_dict()
