import requests
import urllib3
from requests.auth import HTTPBasicAuth
import json
from tqdm import tqdm


#cluster variables
PC = "<PC-IP>"
pc_user = "admin"
pc_password = "xxxxxxxxx"
sourceimage = "CentOS.qcow2"
filepath = "/Users/bmp/Documents/test.qcow2"


#disable cert warnings 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Set headers
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

#Get image UUID from name
paylod = {"length":200}
r = requests.post("https://" +PC+ ":9440/api/nutanix/v3/images/list", auth = HTTPBasicAuth(pc_user, pc_password), data=json.dumps(paylod), headers=headers, verify=False)
image_json = json.loads(r.content)
for image in image_json['entities']:
    if image['status']['name'] == sourceimage:
        imageuuid = image['metadata']['uuid']
        imagesize = image ['status']['resources']['size_bytes']


#Set download url
downloadpath = "https://" +PC+ ":9440/api/nutanix/v3/images/" +imageuuid+ "/file"
print(downloadpath)
print(imagesize)


#Start download
r = requests.get(downloadpath, auth = HTTPBasicAuth(pc_user, pc_password), headers=headers, verify=False, stream=True)
print("Starting Download")
block_size = 1024 
progress_bar = tqdm(total=imagesize, unit='iB', unit_scale=True)
with open(filepath, 'wb') as file:
    for data in r.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if imagesize != 0 and progress_bar.n != imagesize:
    print("ERROR, something went wrong")

#Print completed
print(r.status_code)
print("Download Complete")
