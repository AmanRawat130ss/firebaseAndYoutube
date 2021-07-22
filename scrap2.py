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

doc_ref = db.collection('artists').document('Preetam Bhartwan')


#Youtube Api


api_key = 'AIzaSyCk9A6Wzst_2PpKh9JP-QoVuden9FX3yNU'
youtube = build('youtube', 'v3' , developerKey = api_key)


def subcollection(dic):
    pass




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
    collect = []

    for i in dic:

        getData = { i["contentDetails"]["videoId"] : {
            'id': i["contentDetails"]["videoId"] , 
                'url':'https://www.youtube.com/watch?v='+i["contentDetails"]["videoId"] ,
                        'title' : i["snippet"]['title'],
                                'artist': 'Pritam Bhartwan',
                                'artistNameHindi': translator.translate('Pritam Bhartwan',lang_tgt='hi'),
                                    'date': i["contentDetails"]["videoPublishedAt"],
                                    'artwork' : i["snippet"]["thumbnails"]["high"]["url"], 
                                    'bgImg': " ",
                                        'hindiTitle' : translator.translate(i["snippet"]['title'],lang_tgt='hi'),
                                        'hindiArtist': ''
                                        }

                                        }
        
        
        collect.append(getData)


    print(len(collect)," \n \n len of coll ====......")

    print(collect[0])

    toDict = dict(ChainMap(*collect))
    
    doc_ref.set(toDict)





dataObj = fetch_all_youtube_videos('PLTmuNW3SpiF-JGVoQV6LKD45HV8sWjFJF')
dic = dataObj['items']
# print(len(dic[0][0]))

# print(dataObj)
# 
to_the_firebase(dic)
print("compaleet")

