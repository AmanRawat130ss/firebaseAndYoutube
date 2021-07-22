from firebase import *

def autoUpdateWithMainScrap(sub_col):
    getDoc = sub_col.stream()
            

    for doc in getDoc:

                id = doc.id
                print("id ==>",id)
        
                dic = doc.to_dict()

                videoUrl = dic['ytUrl']
                print(videoUrl,"videourl")