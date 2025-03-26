import requests

url = "http://127.0.0.1:8000/api/utilisateur/login/"
param = {"mail":"canard@gmail.com", "password":"canard"}
reponse = requests.post(url,data=param)

data = reponse.json()
csrftoken = data["csrftoken"]
sessionid = data["sessionid"]

url = f"http://127.0.0.1:8000/api/utilisateur/getUser/?geojson=1"
header = {"csrftoken":csrftoken,"sessionid":sessionid}
header["colonne"] = ["mail"]
header["filtre"] = ["laurepeyramayou@yahoo.fr"]
header["mode"] = ["=="]

#reponse = requests.get(url,params=header)


url = f"http://127.0.0.1:8000/api/import/updateWeLogin"
header = {"csrftoken":csrftoken,"sessionid":sessionid}
reponse = requests.post(url,params=header)
print(reponse.json())