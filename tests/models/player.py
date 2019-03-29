
class Player:

    def __init__(self, player_id, email, name, surname, country_code, city, zip_code, state, mobile_phone,
                 signup_date, date_of_bith, custom_int_1, custom_int_2, custom_int_3, custom_int_4, custom_string,
                 custom_string_2, custom_string_3, custom_string_4, time_zone, language_code, btag, promo_code,
                 tracking_code, optout_email, optout_sms, optout_push, optout_mobile_push):
        self.player_id = player_id
        self.email = email
        self.name = name
        self.surname = surname
        self.country_code = country_code
        self.city = city
        self.zip_code = zip_code
        self.state = state
        self.mobile_phone = mobile_phone
        self.signup_date = signup_date
        self.date_of_birth = date_of_bith
        self.custom_int_1 = custom_int_1
        self.custom_int_2 = custom_int_2
        self.custom_int_3 = custom_int_3
        self.custom_int_4 = custom_int_4
        self.custom_string = custom_string
        self.custom_string_2 = custom_string_2
        self.custom_string_3 = custom_string_3
        self.custom_string_4 = custom_string_4
        self.time_zone = time_zone
        self.language_code = language_code
        self.btag = btag
        self.promo_code = promo_code
        self.tracking_code = tracking_code
        self.optout_email = optout_email
        self.optout_sms = optout_sms
        self.optout_push = optout_push
        self.optout_mobile_push = optout_mobile_push
