import time
import requests
import glob
import ssl, smtplib
import sys
import json

smtp_secret = "6O59tS3xb2kE4SVw"
smtp_account = "elias@keller-re.de"
smtp_server = "mail.your-server.de"
#  smtp_receiver = "eliaszobler@gmail.com"
smtp_receiver = smtp_account

client_id = "5Y4TlLLw5QsAVKsIvqxJr7rvT1WaAOG4"
client_secret = "bfjDCUXQVrAOg0xG"

def print_json(j):
    print(json.dumps(j, indent=2))

def send_sceneid (sceneid):
    port = 465
    message = f"""To: Elias <{smtp_account}>
From: Scany Box <{smtp_account}>
Subject: PhotoScene erstellt

PhotosceneID: {sceneid}

python3 upload.py {sceneid}
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(smtp_account, smtp_secret)
        server.sendmail(smtp_account, smtp_receiver, message)

def token ():
    payload = {}
    payload["client_id"] = client_id
    payload["client_secret"] = client_secret
    payload["grant_type"] = "client_credentials"
    payload["scope"] = "data:read data:write"
    url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
    r = requests.post(url, data = payload)
    token = r.json()['access_token']
    return (token)

def create_scene (token):
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {}
    payload['scenename'] = "testscene"
    payload['format'] = 'rcm,ortho'
    payload['metadata_name[0]'] = 'orthogsd'
    payload['metadata_value[0]'] = '0.1'
    payload['metadata_name[1]'] = 'targetcs'
    payload['metadata_value[1]'] = 'UTM84-32N'
    r = requests.post(url, headers=headers, data=payload)
    id = r.json()['Photoscene']['photosceneid']
    return (id)

def add_photo (token, sceneid, filename):
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/file"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {}
    payload['photosceneid'] = sceneid
    payload['type'] = "image"
    files = {'file[0]' : open(filename, 'rb') }
    r = requests.post(url, headers=headers, data=payload, files=files)
    return (r.json())

def start_process (token, sceneid):
    url = f"https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{sceneid}"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.post(url, headers=headers)

def progress (token, sceneid):
    url = f"https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{sceneid}/progress"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    return(r.json()['Photoscene'])

def get_obj (token, sceneid):
    url = f"https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/{sceneid}?format=obj"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    return (r.json())

def upload_and_send (folder):
    tkn = token ()
    scene = create_scene (tkn)
    print(f"Create scene {scene}")
    for photo in glob.glob(f'{folder}/*.jpg'):
        print (f"Upload {photo}")
        add_photo(tkn, scene, photo)
    start_process(tkn, scene)
    print (f"Send mail")
    send_sceneid(scene)
    return(scene)

def wait_and_download (scene):
    tkn = token ()
    prog = progress(tkn, scene)
    percent = prog['progress']
    while float(percent) < 100:
        print(f"Progress: {percent}", end="\r")
        time.sleep(10)
        prog = progress(tkn, scene)
        percent = prog['progress']
    print ("Processing finished.")
    print_json(prog)
    obj = get_obj(tkn, scene)
    print_json(obj)

def main():
    if len(sys.argv) < 2:
        print("Sceneid angeben!")
    else:
        wait_and_download(sys.argv[1])

if __name__ == "__main__":
    main()
