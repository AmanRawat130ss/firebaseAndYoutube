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
batch = db.batch()


#Youtube Api
api_key = 'AIzaSyCk9A6Wzst_2PpKh9JP-QoVuden9FX3yNU'
youtube = build('youtube', 'v3' , developerKey = api_key)



collectionName = 'Kumauni'
# documentName = getDocumentName(' ') 
# print("documenttt name ", documentName)                             #artist name etc
plId = 'PLTmuNW3SpiF9iNbt5ftiuyq9weCaF6CkA'

#for nested collection and sub-collections

# artistName = getName(documentName)
# print("artisst Name", artistName)

# doc_ref = db.collection(collectionName).document(documentName)

# sub_coll = doc_ref.collection('songs')

# for single collection and document

artistName = ''
sub_coll = db.collection(collectionName)











def fetch_all_youtube_videos(playlistId):
    
    """
    Fetches a playlist of videos from youtube
    We splice the results together in no particular order

    Parameters:
        parm1 - (string) playlistId
    Returns:
        playListItem Dict
    """

    res = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId=playlistId,
    maxResults="50"
    ).execute()
    
   
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlistId,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res


def to_the_firebase(dic):
    aai = 1
         

    for i in dic: 
        print(i["contentDetails"]["videoId"], " video id")
        print(i["contentDetails"]["videoId"],"yturl")
        print(i["snippet"]['title'],"title")
        # print(dic)

         
        getData =  {
                'id': i["contentDetails"]["videoId"] ,
                'url': None, 
                    'ytUrl':'https://www.youtube.com/watch?v='+i["contentDetails"]["videoId"] ,
                            'title' : i["snippet"]['title'],
                                    'artist':artistName,
                                    'artistNameHindi': translator.translate(artistName,lang_tgt='hi'),
                                        'date': i["contentDetails"]["videoPublishedAt"],
                                        'artwork' : i["snippet"]["thumbnails"]["high"]["url"], 
                                        'bgImg': " ",
                                            'hindiTitle' : translator.translate(i["snippet"]['title'],lang_tgt='hi'),
                                            'hindiArtist': ''
                                            } 
        
                                        

        # sub_coll.document().set(getData)

        batch.set(sub_coll.document(), getData)
        print(f"succesfull {aai}")
        aai = aai+1

    batch.commit()
        

  





dataObj = fetch_all_youtube_videos(plId)
dic = dataObj['items']
# print(dic)

 
to_the_firebase(dic)
print("compaleet")


# data = dict(ChainMap(*data))