BASE_PATH = 'http://data.fixer.io/api/latest?access_key='
API_KEY = '1efae8c05a77a3bafc8754fbd12e43f2'

url = BASE_PATH + API_KEY

EMAIL_RECEIVER = "hosein@inprobes.com"

# rules = {
#     'archive': True,
#     'send_mail': True,
#     # preferred default is None
#     # 'preferred': None
#     'preferred': ['BTC', 'IRR', "IQD", "USD", "CAD", "AED"],
#     'notification': True
# }

rules = {
    'archive': True,
    'email': {
        'receiver': 'hosein@inprobes.com',
        'enable': False,
        'preferred': ['BTC', 'IRR', "IQD", "USD", "CAD", "AED"],
    },
    'notification': {
        'enable': True,
        'receiver': '',
        'preferred': {
            'BTC': {'min': 0.000101, 'max': 0.000110},
            'IRR': {'min': 45000, 'max': 50000},
        }
    }
}
