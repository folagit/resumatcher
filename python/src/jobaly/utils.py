
def loadArrayFromFile(fileName): 
        result = []         
        with open(fileName, 'r') as the_file:
            for line in the_file: 
                word = line.strip()
                if not len(word)==0:
                   result.append(word)     
        return result
        
def transferListToDict(_list):
    _dict = {}
    for key in _list:
        _dict[key] = True
    return _dict
    
def writeDict( the_dict, fileName ): 
    with open(fileName, 'w') as the_file:
        for key in sorted(the_dict.iterkeys()):
            jstr = "%s: %s \n" % (key, the_dict[key])
            try:            
                the_file.write(jstr)  
            except Exception as e:
                print e

