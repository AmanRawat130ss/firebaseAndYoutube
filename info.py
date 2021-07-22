from googleapiclient.discovery import build
from collections import ChainMap
from google_trans_new import google_translator  
translator = google_translator()

from nameWrites import getDocumentName , getName

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

# lis =[]
lis = ['Anil Bisht','Gajendra Rana','Manglesh Dangwal','Narendra Singh Negi','Pritam Bhartwan',
'Meena Rana','Saurav Vedwal','Virender rajput','Hema Negi Karasi']

toFB = []

for i in lis:
    name = getDocumentName(i)
    info = { name:{'nameEnglish' : i, 'nameHindi': translator.translate(i,lang_tgt='hi'),
                'imgURL' : ''

    }

                }
    toFB.append(info)
    


doc_ref = db.collection('artists').document('info')
toDict = dict(ChainMap(*toFB))

doc_ref.set(toDict,merge=True)




