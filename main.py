import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    print(f"facts = {facts}")

    return facts[0].getText()

def get_piglatin(fact):

    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    data = {"input_text": fact}
    response = requests.post(url, data, allow_redirects=False)

    soup = BeautifulSoup(response.content, "html.parser")
    redirect_link = soup.a.get('href')

    return url.replace('/piglatinize/', redirect_link)

@app.route('/')
def home():
    fact = get_fact().strip()

    print(f"fact = {fact}")

    result = get_piglatin(fact)

    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

