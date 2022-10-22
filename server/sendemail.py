import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

api_key = config['MAILGUN_API_KEY']
api_domain = config['MAILGUN_DOMAIN']


def send_message(recipient_email, file_name):
    status = requests.post(
		api_domain,
		auth=("api", api_key),
        files=[("attachment", open(file_name, 'rb'))],
		data={"from": f"mailgun@{api_domain.split('/')[-2]}",
			"to": [recipient_email],
			"subject": "OLX Sample Results",
			"text": "Here is a sample result for your last request through OLX API Scraper!!!"})
    return status
