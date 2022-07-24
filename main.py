from urllib import response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import FastAPI, HTTPException
import requests
from typing import List
from creds import SENDER_EMAIL, SENDGRID_API_KEY
app = FastAPI()


def get_current_btc_to_uah_exchange_rate():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=uah"
    response = requests.get(url)
    data = response.json()
    return data[0]['current_price']


def get_list_of_emails() -> List[str]:
    with open('emails.txt', 'r') as f:
        return f.read().splitlines()


@app.get("/rate", status_code=200)
def get_rate() -> int:
    return get_current_btc_to_uah_exchange_rate() 


@app.post("/subscribe")
def post_subscribe(email: str):
    try:
        if email not in get_list_of_emails():
            with open('emails.txt', 'a') as f:
                f.write(email + '\n')
            return {"message": "E-mail додано до списку підписки"}
        else :
            raise HTTPException(status_code=409, detail="E-mail вже є в списку підписки")
    except FileNotFoundError:
        with open('emails.txt', 'w') as f:
            f.write(email + '\n')
        return {"message": "E-mail додано до списку підписки"}



@app.post("/sendEmails", status_code=200)
def send_emails_to_subscribed_users():
    emails = get_list_of_emails()
    mails = Mail(
        from_email=SENDER_EMAIL,
        to_emails=emails,
        subject="Current BTC/UAH exchange rate report",
        plain_text_content=f"Current exchange rate for BTC/UAH is {get_current_btc_to_uah_exchange_rate()}.\n\nSended by test-case app for Genesis school"
        )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(mails)
    return {"message": "Листи надіслано підписникам відправлено"}