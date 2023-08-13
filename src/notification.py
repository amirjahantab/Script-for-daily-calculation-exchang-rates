from kavenegar import *

from config import rules
from local_config import KAVENEGAR_API_KEY


def send_sms(text):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'sender': '10004346',
            'receptor': rules['notification']['receiver'],
            'message': text
        }
        response = api.sms_send(params)
        print(str(response))
    except APIException as e:
            print(str(e))
    except HTTPException as e:
            print(str(e))
