import re
import sys
import pickle
import os

def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def process(folder, indexer):
    collectionpath = "./" + folder
    directory = os.fsencode(collectionpath)#
    docid = 1 #Inicio del puntero docid
    docs = {} #Diccionario key
    palabras = {} #Diccionario con posting lists de las noticias
    tits= {} #Diccionario con posting lists de los títulos
    dates = {} #Diccionario con posting lists de las fechas indexadas
    cats = {} #Diccionario con posting lists de las categorías
    lnoticias = [] #Lista con todas las noticias indexadas
    totaldocs = len(os.listdir(directory)) 
    for f in os.listdir(directory):
        idnoticia = 1
        idtitulo = 1
        idfecha = 1
        idcategoria = 1
        fichero = collectionpath + "/" + os.fsdecode(f)
        with open(fichero , 'r' ) as origin:
            texto = origin.read()            
            docs[docid] = fichero
            titulos = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(texto)
            noticias = re.compile('<text>(.*?)</text>', re.DOTALL |  re.IGNORECASE).findall(texto)
            categorias = re.compile('<category>(.*?)</category>', re.DOTALL |  re.IGNORECASE).findall(texto)
            for noticia in noticias:
                notid = (docid,idnoticia)
                posicion = 0
                lnoticias.append(notid)
                noticiaprocesada= [x.lower() for x in re.sub(r'\n'," ", re.sub(r'[¡!(),-.:;¿?«»/"]'," ", noticia)).split()]
                for palabra in noticiaprocesada:
                    aux = palabras.get(palabra, [])
                    if aux:
                        if (aux[-1][0] != notid):
                            aux.append([notid,[posicion]])
                        else:
                            aux[-1][1].append(posicion)
                    else:
                        aux.append([notid, [posicion]])
                    palabras[palabra] = aux
                    posicion+=1
                idnoticia+=1
            for tit in titulos:
                titid = (docid,idtitulo)
                posicion = 0
                titprocesado= [x.lower() for x in re.sub(r'\n'," ", re.sub(r'[¡!(),-.:;¿?«»/"]'," ", tit)).split()]
                for palabra in titprocesado:
                    aux = tits.get(palabra, [])
                    if aux:
                        if (aux[-1][0] != titid):
                            aux.append([titid,[posicion]])
                        else:
                            aux[-1][1].append(posicion)
                    else:
                        aux.append([titid,[posicion]])
                    tits[palabra] = aux
                    posicion+=1
                idtitulo+=1
            for categoria in categorias:
                catid = (docid,idcategoria)
                catprocesado= [x.lower() for x in re.sub(r'\n'," ", re.sub(r'[¡!(),-.:;¿?«»/"]'," ", categoria)).split()]
                for palabra in catprocesado:
                    aux = cats.get(palabra, [])
                    if aux:
                        if (aux[-1] != catid):
                            aux.append(catid)
                    else:
                        aux.append(catid)
                    cats[palabra] = aux
                idcategoria+=1
        print("Finished indexing", docid,"/", totaldocs, "documents")
        dates[os.fsdecode(f)[:os.fsdecode(f).index(".")]] = docid
        docid+=1
    print("Storing index")
    save_object([docs,palabras,lnoticias,tits,cats,dates], indexer)
    
def syntax():
    print ("\n%s folder indexer\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        syntax()
    folder = sys.argv[1]
    indexer = sys.argv[2]
process(folder, indexer)