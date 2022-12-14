from QLSach import client, keys
from twilio.base.exceptions import TwilioRestException

def SMS(name):
# try:
    mess = client.messages.create(
            body=name + " đã thanh toán thành công!!",
            from_=keys.twilio_number,
            to=keys.my_phone_number
        )
#     verify=client.verify.v2.services(keys.account_sid)
#     verify.verifications.create(to='+84987135520',channel='sms')


#
# except TwilioRestException as err:
#     print(err)