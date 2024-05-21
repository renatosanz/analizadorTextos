import dearpygui.dearpygui as dpg
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

class Archivo():
    def __init__(self,nombre,dirTXT,dirPDF,año):
        self.nombre = nombre
        self.dirTXT = dirTXT
        self.dirPDF = dirPDF
        self.año = año
        # realiza la extraccion y creacion del archivo txt
        # cuando se crea el objeto Archivo
        self.extraerPDFaTXT(nombre,dirTXT,dirPDF)

    def extraerPDFaTXT(self,nombre,dirTXT,dirPDF):
                # esta funcion realiza el escaneo de cada pagina del 
                # pdf al que se hacer referencia
                dpg.configure_item("cargandoArchivo", show=True)
                dpg.set_value("cargandoArchivo", "Cargando archivo "+nombre+".pdf")
                dpg.configure_item("examinar",show = False)

                reader = PdfReader(dirPDF)
                number_of_pages = len(reader.pages)
                contenido = " "
                for n in range(number_of_pages):    
                    page = reader.pages[n]
                    contenido = contenido + self.limpiarTexto(page.extract_text())
                    print("extracting page: "+str(n))
                    # se muestra en pantalla la pagina en la 
                    # cual se encuentra extrayendo el programa
                    dpg.set_value("extrayendo","Extrayendo pagina: "+str(n+1)+"/"+str(number_of_pages))

                with open(dirTXT,"w") as txt:
                    txt.write(contenido)

                # se muestra un aviso de archivo cargado exitosamente
                dpg.configure_item("archivo_cargado", show=True)
                dpg.configure_item("examinar",show = False)

    def getAño(self):
        return self.año 
    
    def setAño(self, newAño):
        self.año = newAño

    def limpiarTexto(self,contenidoTXT):
        # aqui se realiza la limpieza del texto (eliminado de stopwords, 
        # y cadenas de menos de 4 letras)
        palabras_tokenizadas = word_tokenize(contenidoTXT)  
        # tokenizar el texto por palabras
        # extraer las palabras vacias de español
        palabras_vacias = set(stopwords.words("spanish"))
        palabras_filtradas = [word.lower() for word in palabras_tokenizadas if word.lower(
        ) not in palabras_vacias and str(word).__len__()>4]  # filtrado
        # unir todas las palabras en el arreglo como una sola cadena
        texto_filtrado = " ".join(palabras_filtradas)
        return texto_filtrado
    
    def borrar(self):
        # se borra archivo txt que referencia este objeto
        print(self.dirTXT)
        os.remove(self.dirTXT)

    
