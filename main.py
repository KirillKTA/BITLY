import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(link, token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        "long_url": link
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(link, token):
    parsed_url = urlparse(link)
    url_without_scheme = f"{parsed_url.netloc}/{parsed_url.path}"

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_without_scheme}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(link, token):
    parsed_url = urlparse(link)
    url_without_scheme = f"{parsed_url.netloc}/{parsed_url.path}"

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_without_scheme}'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(
        description='сокращаят ссылки и считает клики'
    )
    parser.add_argument('link', help='ваша ссылка')
    args = parser.parse_args()
    user_url = args.link
    try:
        if is_bitlink(user_url, token):
            clicks_count = count_clicks(user_url, token)
            print(clicks_count)
        else:
            bitlink = shorten_link(user_url, token)
            print(bitlink)
    except requests.exceptions.HTTPError:
        print("ошибка неверная ссылка")