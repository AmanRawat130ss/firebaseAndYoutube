from firebase import *
import pafy

pafy.set_api_key('AIzaSyCk9A6Wzst_2PpKh9JP-QoVuden9FX3yNU')
collectionNames = {'artists':1,'allUnit':1}


batch = db.batch()


for key, value in collectionNames.items():
        print(key, value)


        if value == 0:
            print(f"=======================> {key} <==============================")
            getDoc = db.collection(key).stream()
            count = 1

            for doc in getDoc:

                id = doc.id
        
                dic = doc.to_dict()

                videoUrl = dic['ytUrl']
        
                url = videoUrl

                result = pafy.new(url)

                best_quality_audio = result.getbestaudio().url_https
                # print(f"{count} =======> {best_quality_audio}")
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

                    id = doc.id
                    print("\n \n",id)
                    
        
                    dic = doc.to_dict()

                    videoUrl = dic['ytUrl']
        
                    url = videoUrl
                    print(url)
                    

                    # print("\n phase ==>", count)
                    # print(f' \n id ==> {id} \n \n dic ==> {dic} \n \nvideourl ==> {videoUrl} \n \n url ==> {url}  ')

                    result = pafy.new(url,basic=False, gdata=False,  size=False, callback=None)
                    print("pafy run " ,result, '\n', url)
                    # print('',)

                    bestAudio = result.getbestaudio()
                    print("this is for bestAudio")
                    best_quality_audio = bestAudio.url
                    # print(best_quality_audio)
                    
                    # print(f"{count} document complteed=======> ")
                    count+=1

                    sf_ref = db.collection(key).document(docs).collection('songs').document(id)
                    batch.update(sf_ref, {'url':best_quality_audio})

                run = run+1
                

                batch.commit()  





