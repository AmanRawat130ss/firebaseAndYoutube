from firebase import *

from nameWrites import getDocumentName , getName
from playlistsNamesAndLinks import deatils

from linkUpdaterWithAutoScrap import *



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


def to_the_firebase(dic,artistName):
    artistName = artistName
    print(artistName," in function")
    print(translator.translate(artistName,lang_tgt='hi'), "translate")
    aai = 1
         

    for i in dic: 
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









for i in deatils:

    if i[1] == 1:

        print("\n  sub collection")

        collectionName = i[0]

        for j in i[2]:

            documentName = getDocumentName(j[0])  
            print("documenttt name ", documentName)                             #artist name etc
            plId = j[1]

            #for nested collection and sub-collections

            artistName = getName(documentName)
            print("artisst Name", artistName)

            doc_ref = db.collection(collectionName).document(documentName)
            sub_coll = doc_ref.collection('songs')
            
            

            # print(f" collection name = {collectionName} document name = {documentName} \n artist name = {artistName}  ")
            # print(f" doc ref = {doc_ref}  sub_collection = {sub_coll} ")

            

            dataObj = fetch_all_youtube_videos(plId)

            dic = dataObj['items']
            print("data object and dic complter")

            
            to_the_firebase(dic,artistName)
            print("compaleet sub collection")


    else : 
        print("\n non sub collection")

        collectionName = i[0]
        artistName = ''


        plId = i[2]

        sub_coll = db.collection(collectionName)

        print(f" collection name => {collectionName}  ")

        

        dataObj = fetch_all_youtube_videos(plId)
        dic = dataObj['items']
        print("data object and dict complete")
              
        to_the_firebase(dic,artistName)
        print("compaleet non sub collection")



        



