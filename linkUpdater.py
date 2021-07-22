from firebase import *

import pafy

# 
collectionNames ={'devotional':0,'evergreen':0,'newRelease':0,'trendingSongs':0,'trendingSongs':0,'artists':1}


batch = db.batch()



def fun():
    
    
    for key, value in collectionNames.items():
        print(key, value)


        if value == 0:
            print(f"=======================> {key} <==============================")
            getDoc = db.collection(key).stream()
            count = 1

            for doc in getDoc:

                id = doc.id
                print("id ==>",id)
        
                dic = doc.to_dict()

                videoUrl = dic['ytUrl']
                print(videoUrl,"videourl")
        
                url = videoUrl

                result = pafy.new(url,basic=False, gdata=False,  size=False, callback=None)

                best_quality_audio = result.getbestaudio().url
                # print(f"{count} =======> {best_quality_audio}")
                # a = result.audiostreams[-1]
                # best_quality_audio = a.url
                count+=1

                sf_ref = db.collection(key).document(id)
                batch.update(sf_ref, {'url':best_quality_audio})
            
            batch.commit()  
            print("complete non subcollection")
                
        else:
            getInfo = db.collection(key).document('info').get()
            # getCollections = db.collection(key).stream()
            run = 1

            for docs in getInfo.to_dict():
                
                print(run)

                print(f'key ==> {key} docs ==> {docs}')

                getDoc = db.collection(key).document(docs).collection('songs').stream()
                # print(getDoc,"get doc")
                
                count = 1

                for doc in getDoc:
                    print('started')

                    id = doc.id
                    print(f"id= {id}")
                    
        
                    dic = doc.to_dict()

                    videoUrl = dic['ytUrl']
        
                    url = videoUrl
                    

                    # print("\n phase ==>", count)
                    # print(f' \n id ==> {id} \n \n dic ==> {dic} \n \nvideourl ==> {videoUrl} \n \n url ==> {url}  ')

                    result = pafy.new(url,basic=False, gdata=False,  size=False, callback=None)
                    # print(result, '\n', url,"\n \n")

                    best_quality_audio = result.getbestaudio().url
                    # print(f"{count} document complteed=======> ")
                    # a = result.audiostreams[-1]
                    # best_quality_audio = a.url

                    count+=1

                    sf_ref = db.collection(key).document(docs).collection('songs').document(id)
                    batch.update(sf_ref, {'url':best_quality_audio})

                run = run+1
                

                batch.commit()  
                
    return ('its complete')

fun()