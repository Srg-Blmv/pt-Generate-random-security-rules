import requests
import random
import ipaddress
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import string



global_gr_id = ""
cookies = ""


def auth():
    global global_gr_id, cookies

    url = f"https://{mgmt_ip}/api/v2/Login"
    headers = {"Content-Type": "application/json"}
    
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
        # Или заберите нужное ID через web api интерфейс: https://IP_MGMT/apidoc/v2/ui/#tag/device-groups/POST/api/v2/GetDeviceGroupsTreeч

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

def random_ip():
  url_serv  = f"https://{mgmt_ip}/api/v2/CreateNetworkObject"

  ip_range_start = ipaddress.IPv4Address('1.0.0.0')
  ip_range_end = ipaddress.IPv4Address('9.255.255.255')
  rule_name_masks = ["Source", "Dest"]

  for rule_name_mask in rule_name_masks:
    for i in range(obj_num):
      random_ip = str(ipaddress.IPv4Address(random.randint(int(ip_range_start), int(ip_range_end))))

      payload_serv = {
          "name": f"{rule_name_mask}_ip_{random_ip.replace('.', '_')}",
          "deviceGroupId": global_gr_id,
          "description": "",
          "value": {
          "inet": {
              "inet": f"{random_ip}/32"
          }
      }
      }
      #print(payload_serv)
      headers = {"Content-Type": "application/json"}
      response_ser = requests.post(url_serv, json=payload_serv, headers=headers, verify=False, cookies=cookies)
      print(f"{random_ip}: {response_ser.json()}")


def random_network():
  url_serv  = f"https://{mgmt_ip}/api/v2/CreateNetworkObject"

  ip_range_start = ipaddress.IPv4Address('1.0.0.0')
  ip_range_end = ipaddress.IPv4Address('9.255.255.255')
  rule_name_masks = ["Source", "Dest"]
  prefix = ["30","29","28","27","26","25","24"]
  for rule_name_mask in rule_name_masks:
    for i in range(obj_num):
      random_ip = str(ipaddress.IPv4Address(random.randint(int(ip_range_start), int(ip_range_end))))
      random_prefix = random.choice(prefix)

      payload_serv = {
          "name": f"{rule_name_mask}_net_{random_ip.replace('.', '_')}",
          "deviceGroupId": global_gr_id,
          "description": "",
          "value": {
          "inet": {
              "inet": f"{random_ip}/{random_prefix}"
          }
      }
      }
      #print(payload_serv)
      headers = {"Content-Type": "application/json"}
      response_ser = requests.post(url_serv, json=payload_serv, headers=headers, verify=False, cookies=cookies)
      print(f"{random_ip}: {response_ser.json()}")


def random_range():
  url_serv  = f"https://{mgmt_ip}/api/v2/CreateNetworkObject"

  ip_range_start = ipaddress.IPv4Address('1.0.0.0')
  ip_range_end = ipaddress.IPv4Address('9.255.255.255')
  rule_name_masks = ["Source", "Dest"]
  for rule_name_mask in rule_name_masks:
    for i in range(obj_num):
      random_ip_from = str(ipaddress.IPv4Address(random.randint(int(ip_range_start), int(ip_range_end))))
      random_ip_to = str(ipaddress.IPv4Address(random.randint(int(ip_range_start), int(ip_range_end))))  

      if random_ip_from > random_ip_to:
         random_ip_from, random_ip_to = random_ip_to, random_ip_from

      payload_serv = {
          "name": f"{rule_name_mask}_range_{random_ip_from.replace('.', '_')}",
          "deviceGroupId": global_gr_id,
          "description": "",
          "value": {
          "ipRange": {
              "from": f"{random_ip_from}",
              "to": f"{random_ip_to}"
          }
      }
      }
      #print(payload_serv)
      headers = {"Content-Type": "application/json"}
      response_ser = requests.post(url_serv, json=payload_serv, headers=headers, verify=False, cookies=cookies)
      print(f"from: {random_ip_from} to: {random_ip_to}:  {response_ser.json()}")


def random_fqdn():
   url_serv  = f"https://{mgmt_ip}/api/v2/CreateNetworkObject"
   letters = string.ascii_lowercase + string.digits
   tlds = ['com', 'net', 'org']
   for i in range(obj_num):
    length = random.randint(5, 15)  # Длина имени домена от 5 до 15 символов
    domain_name = ''.join(random.choice(letters) for _ in range(length))
    tld = random.choice(tlds)
    random_fqdn =  f"{domain_name}.{tld}"
    payload_serv = {
        "name": f"fqdn_{random_fqdn}",
        "deviceGroupId": global_gr_id,
        "description": "",
        "value": {
        "fqdn": {
            "fqdn": f"{random_fqdn}",
        }
    }
    }
    #print(payload_serv)
    headers = {"Content-Type": "application/json"}
    response_ser = requests.post(url_serv, json=payload_serv, headers=headers, verify=False, cookies=cookies)
    print(f"{random_fqdn}:  {response_ser.json()}")


mgmt_ip = "192.168.212.10"
mgmt_login =  "admin"
mgmt_pass = "xxXX1234$"
groupe_name= "Global"
obj_num = 10


auth()
random_ip()
random_network()
random_range()
random_fqdn()