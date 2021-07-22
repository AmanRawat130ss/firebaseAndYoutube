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
batch = db.batch()


#Youtube Api
api_key = 'AIzaSyCk9A6Wzst_2PpKh9JP-QoVuden9FX3yNU'
youtube = build('youtube', 'v3' , developerKey = api_key)
print("hello")

