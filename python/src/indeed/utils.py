
def loadArrayFromFile(fileName): 
        result = []         
        with open(fileName, 'r') as the_file:
            for line in the_file: 
                word = line.strip()
                if not len(word)==0:
                   result.append(word)     
        return result
