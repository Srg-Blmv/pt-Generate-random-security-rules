import requests
import random
import ipaddress
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


global_gr_id = ""
cookies = ""
headers = {"Content-Type": "application/json"}

def auth():
    global global_gr_id, cookies
    url = f"https://{mgmt_ip}/api/v2/Login"
    payload = {
        "login": mgmt_login,
        "password": mgmt_pass
    }
    
    response_auth = requests.post(url, json=payload, headers=headers, verify=False)
    if response_auth.status_code == 200:
        print("auth ok")
        url =  f"https://{mgmt_ip}/api/v2/GetDeviceGroupsTree"
        r = requests.post(url, headers=headers, verify=False, cookies=response_auth.cookies)
        cookies = response_auth.cookies
        # ПОЛУЧАЕМ ID глобальной группы
        global_gr_id = r.json()['groups'][0]['id']
        # Пример 1 группы в глобальной:
        # global_gr_id = (r.json()['groups'][0].get("subgroups")[0].get('id'))
        # Или заберите нужное ID через web api интерфейс: https://IP_MGMT/apidoc/v2/ui/#tag/device-groups/POST/api/v2/GetDeviceGroupsTree

    else:
        print("auth fail")
        exit()


def get_rules():
    # -----------   GET LIST RULES -------------------
    url = f"https://{mgmt_ip}:443/api/v2/ListSecurityRules"
    payload = {
        "limit": 10000,
        "deviceGroupId": global_gr_id,
        "precedence": "pre"
    }
    response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
    id_rules = []
    if response.status_code == 200:
        data = response.json()

        #id_rules = [obj["id"] for obj in data["items"]] список всех правил для удаления.
        for i in data["items"]:
            if "Random_Rule" in i.get('name'):
                id_rules.append(i.get('id'))

        return id_rules
    else:
        print(f"Error: {response.status_code} - {response.text}")



def main():
    id_rules = get_rules()
    for i in id_rules:
        url = f"https://{mgmt_ip}:443/api/v2/DeleteSecurityRule"
        payload = {
            "id": i
        }
        response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
        if response.status_code == 200:
            print(f"del: {i}")
        else:
            print(f"Error: {response.status_code} - {response.text} - ID RULE: {i}")




mgmt_ip = "192.168.1.100"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"


auth()
main()