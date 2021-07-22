

def getName(name):

    final = None
    for i in range(0,len(name)):
        
        if i == 0:
            final = name[i].upper()
            continue
            
        if name[i].isupper():
            final = final + ' ' + name[i]
            
        else:
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
            final = final + name[i]
            
    return final
