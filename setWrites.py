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




def getName(name):

    final = None
    for i in range(0,len(name)):
        
        if i == 0:
            final = name[i].upper()
           
            continue
            
        if name[i].isupper():
            final = final + ' ' + name[i]
            
        else:
            print(name[i])
            final = final + name[i]
            

    return final



def getDocumentName(name):

    final = None

    for i in range(0,len(name)):
        
        if i == 0:
            final = name[i].lower()
           
            continue
            
        if name[i] == " ":
            final = final.replace(" ","")
            


        else:
            print(name[i])
            final = final + name[i]
            
    
    return final



collectionName = 'artists'
documentName = getDocumentName('Gajendra Rana') 
print("documenttt name ", documentName)                             #artist name etc
plId = 'PLTmuNW3SpiF_K9wiGjRzUk7KqVeFGluSJ'

#for nested collection and sub-collections

artistName = getName(documentName)
print("artisst Name", artistName)
doc_ref = db.collection(collectionName).document(documentName)
sub_coll = doc_ref.collection('songs')

# for single collection and document

# sub_coll = db.collection(collectionName)






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
    songCounter = 0
    
    documentUpdater = 0
    
    collect = []
        

    for i in dic:      
               
        if songCounter == 7:
           
           songCounter = 0


           finalData = {'songs':collect}           

           
           docName = 'set'+str(documentUpdater)
           print(f"\n \n <============= docNAme {docName} ==================>")
        
            #to database

           sub_coll.document(docName).set(finalData,merge=True)
           print("succesfull \n \n \n")

           documentUpdater = documentUpdater + 1
           

           collect = []
        

       
        getData =  {
            'id': i["contentDetails"]["videoId"] , 
                'url':'https://www.youtube.com/watch?v='+i["contentDetails"]["videoId"] ,
                        'title' : i["snippet"]['title'],
                                'artist': artistName,
                                'artistNameHindi': translator.translate(artistName,lang_tgt='hi'),
                                    'date': i["contentDetails"]["videoPublishedAt"],
                                    'artwork' : i["snippet"]["thumbnails"]["high"]["url"], 
                                    'bgImg': " ",
                                        'hindiTitle' : translator.translate(i["snippet"]['title'],lang_tgt='hi'),
                                        'hindiArtist': ''
                                        } 

                                        

        collect.append(getData)
        songCounter = songCounter+1
        print(f"song counter +1 ==== {songCounter} \n")
        
      
    finalData = {'songs':collect}
    print("\n \n out of the loop ======>>>")           

           # neww 
    docName = 'set'+str(documentUpdater)
    print(f"\n \n <============= docNAme {docName}  ==================>")
        
    sub_coll.document(docName).set(finalData,merge=True)
    print("succesfull")

    documentUpdater = documentUpdater + 1
    

    collect = []  





dataObj = fetch_all_youtube_videos(plId)
dic = dataObj['items']
# print(dic)

 
to_the_firebase(dic)
print("compaleet")