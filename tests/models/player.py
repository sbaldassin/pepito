
class Player:

    def __init__(self, player_id, email, name, surname, country_code, city, zip_code, state, mobile_phone,
                 signup_date, date_of_bith, custom_int_1, custom_int_2, custom_int_3, custom_int_4, custom_string,
                 custom_string_2, custom_string_3, custom_string_4, time_zone, language_code, btag, promo_code,
                 tracking_code, optout_email, optout_sms, optout_push, optout_mobile_push):
        self.PlayerID = player_id
        self.Email = email
        self.Name = name
        self.Surname = surname
        self.CountryCode = country_code
        self.City = city
        self.ZipCode = zip_code
        self.State = state
        self.MobilePhone = mobile_phone
        self.SignUpDate = signup_date
        self.DateOfBirth = date_of_bith
        self.CustomInt1 = custom_int_1
        self.CustomInt2 = custom_int_2
        self.CustomInt3 = custom_int_3
        self.CustomInt4 = custom_int_4
        self.CustomString1 = custom_string
        self.CustomString2 = custom_string_2
        self.CustomString3 = custom_string_3
        self.CustomString4 = custom_string_4
        self.TimeZone = time_zone
        self.LanguageCode = language_code
        self.Btag = btag
        self.PromoCode = promo_code
        self.TrackingCode = tracking_code
        self.OptOutEmail = optout_email
        self.OptOutSms = optout_sms
        self.OptOutPush = optout_push
        self.OptOutMobilePush = optout_mobile_push

    def to_csv(self):
        return [self.PlayerID, self.Name, self.Surname, self.ZipCode,self.State, self.City, self.CountryCode,
                self.Email, self.DateOfBirth, self.MobilePhone,self.SignUpDate, self.LanguageCode, self.TimeZone,
                self.CustomInt1, self.CustomInt2, self.CustomInt3, self.CustomInt4, self.CustomString1,
                self.CustomString2, self.CustomString3, self.CustomString4, self.Btag, self.OptOutEmail,
                self.OptOutSms, self.OptOutPush]
