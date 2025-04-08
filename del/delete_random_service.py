import requests
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



def get_service():
    # -----------   GET LIST SERVICE -------------------
    url = f"https://{mgmt_ip}:443/api/v2/ListServices"

    payload = {
        "deviceGroupId": global_gr_id,
    
        "objectOriginKinds": ["OBJECT_ORIGIN_KIND_CUSTOM"],
        "offset": 0,
        "limit": 10000
    }

    id_dict_services = []
    response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)

    if response.status_code == 200:
        data = response.json()

        #id_dict_services = [obj["id"] for obj in data["services"] ]  - если  надо удалить все сервисы, но нижний цикл for надо закоментировать.

        for i in data["services"]:
            if "r_" in i.get('name'):
                id_dict_services.append(i.get('id'))
        return id_dict_services
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()


def remove_service():
    auth()
    # ---------------  DEL service r_ ----------------
    id_dict_services = get_service()
    for i in id_dict_services:
        url = f"https://{mgmt_ip}:443/api/v2/DeleteService"
        payload = {
            "id": i
        }
        response = requests.request("POST", url, json=payload,  headers=headers, cookies=cookies, verify=False)
        if response.status_code == 200:
            print(f"del: {i}")
        else:
            print(f"Error: {response.status_code} - {response.text} - ID RULE: {i}")


mgmt_ip = "192.168.212.10"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"
groupe_name = "Global"


remove_service()