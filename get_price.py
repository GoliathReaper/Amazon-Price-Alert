from bs4 import BeautifulSoup
import lxml
import requests
import json


def amazon_price(link):
    response = requests.get(link,
                            headers={
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'GET',
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Max-Age': '3600',
                                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
                            })

    soup = BeautifulSoup(response.text, features='lxml')
    price = soup.find(class_="a-offscreen").getText()
    # Remove commas and rupees symbol
    cleaned_amount = price.replace(',', '').replace('₹', '')
    # Remove trailing ".00"
    cleaned_amount = cleaned_amount.replace('.00', '')
    product_name = soup.find(id="productTitle").getText().strip()
    img_url = soup.findAll("img")
    images = soup.find("div", {"id": "imgTagWrapperId"}).find("img")
    data = json.loads(images["data-a-dynamic-image"])
    all_img = list(data.keys())

    return int(cleaned_amount), product_name, all_img[0]
