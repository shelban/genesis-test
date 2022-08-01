import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import FastAPI, HTTPException
import requests
from typing import List
from dotenv import load_dotenv

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

app = FastAPI()
sg = SendGridAPIClient(SENDGRID_API_KEY)

load_dotenv()


def get_list_of_emails() -> List[str]:
    with open('emails.txt', 'r') as f:
        return f.read().splitlines()


def get_current_btc_to_uah_exchange_rate():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=uah"
    response = requests.get(url)
    data = response.json()
    return data[0]['current_price']


@app.get("/rate", status_code=200)
def get_rate() -> int:
    return get_current_btc_to_uah_exchange_rate()


@app.post("/subscribe", status_code=200)
def post_subscribe(email: str) -> dict:
    try:
        if email not in get_list_of_emails():
            with open('emails.txt', 'a') as f:
                f.write(email + '\n')
            return {"description":"E-mail додано"}
        else:
            raise HTTPException(status_code=409,
                                detail="E-mail вже є в списку підписки")
    except FileNotFoundError:
        with open('emails.txt', 'w') as f:
            f.write(email + '\n')
        return {"description":"E-mail додано до списку підписки"}


@app.post("/sendEmails", status_code=200)
def send_emails_to_subscribed_users():
    subscribed_emails = get_list_of_emails()
    current_rate = get_current_btc_to_uah_exchange_rate()
    mails = Mail(
        from_email=SENDER_EMAIL,
        to_emails=subscribed_emails,
        subject="Current BTC/UAH exchange rate report",
        plain_text_content=f"Current exchange rate for BTC/UAH is {current_rate}.\n\nSended by test-case app for Genesis school"
    )
    sg.send(mails)
    return {"description":"E-mailʼи відправлено"}
