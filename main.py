import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

def load_page(address):
    url = "http://etherscan.io/txsPending?a={}".format(address)
    # zenrows proxy
    proxy = ""
    proxies = {"http": proxy}

    response = requests.get(url, proxies=proxies)
    try:
        response = requests.get(url, proxies=proxies, verify=False)
        response.raise_for_status()
        with open("response.html", "w") as file:
            file.write(response.text)
        print('Write file success')
    except requests.RequestException as e:
        print(f"Request failed: {str(e)}")

def read_html():
    with open('response.html', 'r') as file:
        html_data = file.read()
    soup = BeautifulSoup(html_data, 'html.parser')
    target_element = soup.select_one('div#ContentPlaceHolder1_divTopPage span.text-dark')

    if target_element:
        text_with_number = target_element.text.strip()
        number = int(''.join(filter(str.isdigit, text_with_number)))
        data = {'number': number, 'timestamp': datetime.now().isoformat()}
        return data
    else:
        return {'number': 0, 'timestamp': datetime.now().isoformat()}

@app.get("/txn-pending")
async def root(address:str):
    load_page(address)
    return read_html()

@app.post("/set-mode")
async def set_mode(user:str,password:str,isMaintenance:bool):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    if user == config['user'] and password == config['password']:
        with open('maintenance.json', 'r') as file:
            data = json.load(file)
        data['isMaintenance'] = isMaintenance
        data['timestamp'] = datetime.now().isoformat()
        with open('maintenance.json', 'w') as file:
            json.dump(data, file)

@app.get('/get-mode')
async def get_mode():
    with open('maintenance.json', 'r') as file:
        data = json.load(file)
    return data
