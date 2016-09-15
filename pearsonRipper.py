import argparse
import urllib
import urllib.request
import os
from bs4 import BeautifulSoup

baseISBNUrl = 'http://www.iberlibro.com/servlet/SearchResults?isbn='
basePearsonUrl = 'https://biblionlinereader.pearson.com.mx/{0}/files/page/{1}.{2}'


def usage():
    print('Uso: pearsonRipper.py -isbn <codigo_isbn>')

def getBookTitle(isbninput):
    urlBook = baseISBNUrl+ str(isbninput)+'&n=100121501&sortby=17&x=74&y=7'
    try:

        with urllib.request.urlopen(urlBook) as url:
            s = url.read()
        print(urlBook)
        soup = BeautifulSoup(s,"html.parser")
        titulo = soup.find("div", {"id": "book-1"})
        tituloreal = titulo.find("a",{'itemprop': 'url'})
        print('Libro : '+tituloreal['title'])
    except(Exception):
        print('No se encontro el nombre del libro.')

def downloadBook(isbninput, paginas):

    getBookTitle(isbninput)
    attempts = 3
    for page in range(1,int(paginas)+1):

        while attempts:
            try:
                extension = 'swf'
                if (attempts==1):
                    extension = 'jpg'

                print('Descargando  '+basePearsonUrl.format(isbninput,page, extension))
                urllib.request.urlretrieve(basePearsonUrl.format(isbninput,page, extension), str(page)+'.'+extension)

                if(extension!='jpg'):
                    os.system("swfrender {0}.swf -o {1}.png -X {2}".format(page, page, 2000))
                break
            except:
                print('Error en la descarga.  '+str(attempts) + ' intento.')
                attempts -= 1
                if(attempts==0):
                    print('Error descargando pagina '+str(page))
                    continue
        attempts=3


__author__ = 'hexc0der'

parser = argparse.ArgumentParser(description='Script para "ripear" libros de Pearson. by hexc0der.')
parser.add_argument('-isbn', '--isbn', help='Codigo ISBN', required=True)
parser.add_argument('-paginas','--paginas', help='Numero de Paginas', required=True)
args = parser.parse_args()

downloadBook(args.isbn, args.paginas)
