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
        payload = {}
        url =  f"https://{mgmt_ip}/api/v2/GetDeviceGroupsTree"
        r = requests.post(url, headers=headers, json=payload, verify=False, cookies=response_auth.cookies)
        cookies = response_auth.cookies
        # ПОЛУЧАЕМ ID глобальной группы
        global_gr_id = get_id_groupe(r.json()['groups'][0])

    else:
        print("auth fail")
        exit()


def get_id_groupe(groups):
    # Проверка текущей группы
    if groups.get("name") == groupe_name:
        return groups.get("id")
    # Проверка вложенных групп, если они существуют
    if "subgroups" in groups:
        for subgroup in groups["subgroups"]:  # Проходим по списку подгрупп
            result = get_id_groupe(subgroup)
            if result:  # Если id найдено, возвращаем его
                return result
    return None  # Возвращаем None, если ничего не найдено

def get_rules():
    # -----------   GET LIST RULES -------------------
    url = f"https://{mgmt_ip}:443/api/v2/ListSecurityRules"
    payload = {
        "limit": 100000,
        "deviceGroupId": global_gr_id,
        "precedence": "pre"
    }
    response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
    id_rules = []
    if response.status_code == 200:
        data = response.json()
        if delete_all:
            id_rules = [obj["id"] for obj in data["items"]]
        else:
            for i in data["items"]:
                if "Random_Rule" in i.get('name'):
                    id_rules.append(i.get('id'))

        return id_rules
    else:
        print(f"Error: {response.status_code} - {response.text}")



def main():
    auth()
    id_rules = get_rules()
    id_rules = id_rules[::-1]
    count = 0
    for i in id_rules:
        count += 1
        url = f"https://{mgmt_ip}:443/api/v2/DeleteSecurityRule"
        payload = {
            "id": i
        }
        response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
        if response.status_code == 200:
             print(f"{count}: remove id {i}")
        else:
            print(f"Error: {response.status_code} - {response.text} - ID RULE: {i}")




mgmt_ip = "192.168.212.101"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"
groupe_name = "Global"
delete_all = 0                # Если False удалит SecurityRules в названии которых есть "Random_Rule".  
                              # Если True  удалить все  SecurityRules. 

main()
