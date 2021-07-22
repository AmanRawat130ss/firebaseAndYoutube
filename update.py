from googleapiclient.discovery import build
from collections import ChainMap
from google_trans_new import google_translator  
translator = google_translator()

#firebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("fireBaseSDK.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Youtube Api
api_key = 'AIzaSyCk9A6Wzst_2PpKh9JP-QoVuden9FX3yNU'
youtube = build('youtube', 'v3' , developerKey = api_key)



docs = db.collection('allUnit').document('kumaoni').collection('songs').stream()

for doc in docs:
    # print(f'    {doc.id} => {doc.to_dict()}   \n \n')
    id = doc.id
    add = {'artist' : ''}

    # db.collection('trendingSongs').document(id).set(add, merge = True)

    db.collection('allUnit').document('kumaoni').collection('songs').document(id).set(add, merge = True)
    

