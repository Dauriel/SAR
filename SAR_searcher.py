import re
import sys
import pickle
import os

def generatesnippet(text, word, check = False):
    splitted = [x.lower() for x in text.split()]
    if(check):
        r = Math.floor(Math.random()* len(splitted))
        position = splitted.index(r)
    else:
        position = splitted.index(word)
    if position <=1:
        positionf = position+4
    else:
        positionm = position-2

    if len(splitted)-position <=1:
        positionm = position-4
    else:
        positionf = position+4  
    print(" ".join(splitted[positionm:positionf]))
        
#queries con posición
def andconposting(query1):
    query = query1.split()
    aux2 = []
    lista1 = palabras[query[0]]
    for i in range(0,len(query)-1):
        aux = []
        p1 = 0
        p2 = 0
        lista2 = palabras[query[i+1]]
        while(p1 < len(lista1)and p2<len(lista2)):
            if(lista1[p1][0] == lista2[p2][0]):
                test = [(lista1[p1][0]),[]]
                listaux1 = lista1[p1][1]
                listaux2 = lista2[p2][1]
                pp1 = 0
                pp2 = 0
                while(pp1 < len(listaux1)and pp2 < len(listaux2)):
                    if(listaux1[pp1] < listaux2[pp2]):
                        if(listaux2[pp2] - listaux1[pp1] == 1):
                            test[1].append(listaux2[pp2])
                            pp1+=1
                            pp2+=1
                        else:
                            pp1+=1
                    else:
                        pp2+=1
                if test[1]:
                    aux.append(test)
                p1+=1
                p2+=1
            elif(lista1[p1][0]> lista2[p2][0]):
                p2+=1
            else:
                p1+=1
        lista1 = aux
                
    if lista1:
        for i in lista1:
            aux2.append(i[0])
    return aux2
        
#or entre dos listas    
def orlistas(lista1, lista2):
    res = []
    p1 = 0
    p2 = 0
    while(p1 < len(lista1)and p2<len(lista2)):
        if(lista1[p1] == lista2[p2]):
            res.append(lista1[p1])
            p1+=1
            p2+=1
        elif(lista1[p1] < lista2[p2]):
            res.append(lista1[p1])
            p1+=1
        else:
            res.append(lista2[p2])
            p2+=1
    while(p1<len(lista1)):
        res.append(lista1[p1])
        p1+=1
    while(p2<len(lista2)):
        res.append(lista2[p2])
        p2+=1
    return res
   
#and etrne dos listas    
def andlistas(lista1, lista2):
    res = []
    p1 = 0
    p2 = 0
    while(p1 < len(lista1)and p2<len(lista2)):
        if(lista1[p1] == lista2[p2]):
            res.append(lista1[p1])
            p1+=1
            p2+=1
        elif(lista1[p1] < lista2[p2]):
            p1+=1
        else:
            p2+=1
    return res

#not entre dos listas
def notlistas(lista1):
    res = []
    p1 = 0
    p2 = 0
    while(p1 < len(lista1)and p2<len(lnoticias)):
        if(lista1[p1] == lnoticias[p2]):
            p1+=1
            p2+=1
        elif(lista1[p1] < lnoticias[p2]):
            p1+=1
        else:
            res.append(lnoticias[p2])
            p2+=1
    while(p2<len(lnoticias)):
        res.append(lnoticias[p2])
        p2+=1
    return res
#print según número de ocurrencias
def printnoticias(lista):
    if(len(lista) <= 2):
        noticia(lista)
    elif(len(lista)> 5):
        titles(lista)
    else:
        snippet(lista)

def snippet(lista):
     for (x,y) in lista:
        archivo = docs[x]
        test = False
        with open(archivo , 'r' ) as origin:
            contenido = origin.read()
            titulo = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(contenido)
            noticia = re.compile('<text>(.*?)</text>', re.DOTALL |  re.IGNORECASE).findall(contenido)
            print("-----------------------------------------------------")
            print(titulo[y-1])
            for w in queryinput:
                if(w in contenido):
                    generatesnippet(contenido, w)
                    test = True
            if not test:
                generatesnippet(contenido, w, True)
        
#print de los 10 primeros títulos
def titles(lista):
    i = 0
    for (x,y) in lista:
        if(i == 10):
            break
        else:
            archivo = docs[x]
            with open(archivo , 'r' ) as origin:
                contenido = origin.read()
                titulo = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(contenido)
                print("-----------------------------------------------------")
                print(titulo[y-1])
        i+=1
#convierte string a lista               
def stringtolist(string):
    tuplas = re.findall(r'\((.*?)\)',string)
    aux = []
    for tupla in tuplas:
        tupla1 = tupla.split(",")
        aux.append((int(tupla1[0]), int(tupla1[1])))
    return aux

#used to process queries, recursive
def logicadefrases(query):
    count = 0
    first = -1
    last = -1
    for item in query:
        if (item != "NOT" and item != "AND" and item != "OR"):
            count+=1
            if(first == last):
                first = query.index(item)
            elif(last != -1):
                first = last
                last = query.index(item)
            else:
                last = query.index(item)
    if(count == 1):
        if(query[0][0] == "["):
            posting = stringtolist(query[0])
        else:
            wordtq = query[-1]
            posting = returnposting(wordtq)
        if(len(query)> 1):
            posting = notlistas(posting)
        return posting
    else:
        pointer = last-1
        if(query[last][0][0] == "["):
            posting = stringtolist(query[last])
        else:
            posting = returnposting(query[last])
        shortquery = query[:first+1]
        if(pointer == first):
            return andlistas(logicadefrases(shortquery),posting)
        else:
            while(pointer != first):
                if(query[pointer] == "NOT"):
                    posting = notlistas(posting)
                    if(pointer-1 == first):
                        return andlistas(logicadefrases(shortquery), post)
                elif(query[pointer] == "AND"):
                    return andlistas(logicadefrases(shortquery),posting)
                else:
                    return orlistas(logicadefrases(shortquery),posting)
                pointer -= 1

#returns postinglist associated with term
def returnposting(term):
    if ":" in term:
        auxterm = term[term.index(":")+1:]
        queryinput.append(auxterm)
        if "headline:" in term:
            aux = []
            for t in tits[auxterm]:
                aux.append(t[0])
            return aux         
        elif "category" in term:
            return cats[auxterm]
        elif "date" in term:
            aux = []
            for key in docs.keys():
                doc = docs[key].split("/")
                termino = doc[-1]
                if(termino[:len(termino)-5] == auxterm):
                    for (x,y) in lnoticias:
                        if(x == key):
                            aux.append((x,y))
            return aux
        else:
            aux = []
            for t in palabras[auxterm]:
                aux.append(t[0])            
            return aux
    else:
        queryinput.append(term)
        aux = []
        for t in palabras[term]:
            aux.append(t[0])            
        return aux 
    
def noticia(lista):
    for(x,y) in lista:
        archivo = docs[x]
        with open(archivo , 'r' ) as origin:
            contenido = origin.read()
            titulo = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(contenido)
            noticia = re.compile('<text>(.*?)</text>', re.DOTALL |  re.IGNORECASE).findall(contenido)
            print("---------------------------------------------")
            print(titulo[y-1])
            print(noticia[y-1])
            
def wildcard(word):
    aux = []
    aux2 = []
    pos = word.find("*")
    split = word.split("*")
    if(pos == 0):
        for term in palabras.keys():
            aux2 = []
            if(term.endswith(split[1])):
                posting = returnposting(term)
                aux2 = orlistas(aux,posting)
                aux = aux2
    elif(pos == len(word)-1):
        for term in palabras.keys():
            aux2 = []
            if(term.startswith(split[0])):
                posting = returnposting(term)
                aux2 = orlistas(aux,posting)
                aux = aux2
    else:
        for term in palabras.keys():
            aux2 = []
            if(term.endswith(split[1]) and term.startswith(split[0])):
                posting = returnposting(term)
                aux2 = orlistas(aux,posting)
                aux = aux2
    new = "".join(str(aux).split())
    return new
        
    
def process(indexer):
    objeto = load_object(indexer)
    global docs #diccionario global id-doc
    docs= objeto[0] 
    global palabras #diccionario global palabra-[noticia,[posiciones]]
    palabras = objeto[1]
    global lnoticias #lista global [noticias]
    lnoticias = objeto[2]
    global tits #diccionario global palabra-[noticia,[posiciones]]
    tits = objeto[3] 
    global queryinput #initial query
    global cats
    cats = objeto[4]
    global dates
    dates = objeto[5]
    response = input("Please type in your query: ")
    while(response):
        queryinput = []
        seguidos = re.findall(r'"(.*?)"', response)
        if seguidos:
            for seguido in seguidos:
                lista = andconposting(seguido)
                listastring = "".join(str(lista).split())
                string = '"'+seguido+'"'
                response = response.replace(string, listastring)
        quer = response.split()
        aux = []
        for word in quer:
            if (word == "NOT" or word == "AND" or word == "OR"):
                aux.append(word)
            elif "*" in word:
                wild = wildcard(word)
                aux.append(wild)
            elif (word[0] != "["):                
                aux.append(word.lower())
            else:
                aux.append(word)
        query = " ".join(aux)
        try:
            splitted = query.split()
            listaresultado = logicadefrases(splitted)
            queryinput = aux            
            printnoticias(listaresultado)
            print("Number of elements found:",len(listaresultado))
        except KeyError:
            print("Word %s not found in current list of documents" % response.lower())
        response = input("Please type in your query: ")
    
def load_object(file_name):
    with open(file_name, 'rb')as fh:
        obj = pickle.load(fh)
    return obj

def syntax():
    print ("\n%s indexer\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        syntax()
    indexer = sys.argv[1]
    process(indexer)