from wordcloud import WordCloud
import matplotlib.pyplot as plt
import dearpygui.dearpygui as dpg
import copy
import random

# import nltk
# import matplotlib

from nltk.draw.dispersion import dispersion_plot
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from textblob import TextBlob

from collections import Counter

# nltk.download('stopwords')
# nltk.download('punkt')
# matplotlib.use('TkAgg')

class OperadorDeTexto:
  def __init__(self):
    pass

  def GenerarDispLexica(self, sender):
    # favor de hacer print(sender) para enteder lo que recibe la funcion
    for pres in sender:
      texto_total = []
      for archivo in pres["archivos"]:
        with open(archivo.dirTXT, "r") as archivo:
          contenidoTXT = archivo.read()  # leer el texto del archivo
          texto_total = texto_total + contenidoTXT.split()

      conteo = Counter(texto_total).most_common(dpg.get_value("max_num_palabras"))
      tags = []
      for tag in conteo:
        tags.append(tag[0])

      ax = dispersion_plot(texto_total, tags)
      ax.set_yticks(list(range(len(tags))), reversed(tags), color="C0")
      plt.title(pres["nombre"])
    plt.show()

#==========================================================================================#

  def GenerarWordClouds(self, sender):
    contPres = 0
    texto_totalMax = []  # Lista para almacenar el texto total para cada presidente
    nombres_presidentes = set()  # Lista para almacenar los nombres de los presidentes

    for pres in sender:
      texto_total = ""
      for archivo in pres["archivos"]:
          nombres_presidentes.add(pres["nombre"])
          with open(archivo.dirTXT, "r", encoding="utf-8") as archivo_txt:
              contenidoTXT = archivo_txt.read()  # Leer el texto del archivo
              texto_total += contenidoTXT
      # Agregar el texto total para este presidente a la lista
      texto_totalMax.append(texto_total)
      contPres += 1
    
      # Creamos un wordcloud para este presidente
      wordcloud = WordCloud(
          width=2160, height=1720, background_color="white", max_words=dpg.get_value("max_num_palabras")
      ).generate(texto_total)

      # Usamos matplotlib para mostrar el wordcloud
      plt.figure(figsize=(6, 5))
      plt.imshow(wordcloud, interpolation="bilinear")
      plt.axis("off")  # Elimina los ejes
      plt.title(pres["nombre"])
    
    if contPres > 1:  # Si hay más de un presidente seleccionado
        # Creamos un wordcloud combinando todos los textos de los presidentes con sus colores correspondientes
        texto_total_combinado = ' '.join(texto_totalMax)

        # Creamos un wordcloud combinando todos los textos de los presidentes con colores aleatorios
        wordcloud = WordCloud(
            width=2160, height=1720, background_color="white", colormap='viridis',
            max_words=dpg.get_value("max_num_palabras")*2
        ).generate(texto_total_combinado)

        # Usamos matplotlib para mostrar el wordcloud combinado
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")  # Elimina los ejes
        plt.title(", ".join(nombres_presidentes))  # Título con los nombres de los presidentes
        
    plt.show()

#==========================================================================================#

  def GenerarEstadisticasGenerales(self, sender):
    # favor de hacer print(sender) para enteder lo que recibe la funcion
    for pres in sender:
      texto_total = ""
      for archivo in pres["archivos"]:
        with open(archivo.dirTXT, "r") as archivoTXT:
          contenidoTXT = archivoTXT.read()  # leer el texto del archivo
          texto_total = texto_total + contenidoTXT
      texto_tokenizado = word_tokenize(texto_total)

      num_palabras = len(texto_total.split())
      finder = BigramCollocationFinder.from_words(texto_tokenizado)
      collocations = finder.nbest(BigramAssocMeasures.likelihood_ratio, dpg.get_value("max_num_palabras"))

      unique_words = set(texto_tokenizado)
      lexical_diversity = len(unique_words) / len(texto_tokenizado)

      blob = TextBlob(texto_total)
      sent = blob.sentences[0].sentiment_assessments

      word_freq = Counter(texto_tokenizado)
      top_words = word_freq.most_common(dpg.get_value("max_num_palabras"))

      paragraphs = texto_total.split("\n")
      avg_paragraph_length = sum(len(p) for p in paragraphs) / len(paragraphs)

      plt.figure(figsize=(6,5))
      plt.text(0, 0.9, "Estadisticas Generales", fontsize=14)
      plt.text(0, 0.8, str(num_palabras) + " Palabras", fontsize=10)
      plt.text(
        0,
        0.65,
        "Longitud Promedio\nde Parrafos: \n"
        + str(avg_paragraph_length)
        + " caracteres",
        fontsize=10,
      )
      plt.text(0.5, 0.8, "Oraciones más comunes", fontsize=10)
      i = 0.05
      for p in collocations:
        plt.text(0.5, 0.8 - i, "-> " + " ".join(p), fontsize=10)
        i = i + 0.05

      plt.text(0.5, 0.4, "Palabras más comunes", fontsize=10)
      plt.text(0.5, 0.35, "(veces : palabra)", fontsize=10)
      i = 0.05
      for p in top_words:
        plt.text(0.5, 0.35 - i, "-> " + str(p[1]) + " : " + p[0], fontsize=10)
        i = i + 0.05

      plt.text(0, 0.5, "Sentimiento Del Texto", fontsize=10)
      plt.text(
        0,
        0.45,
        "Riqueza léxica : " + str(round(lexical_diversity, 4)),
        fontsize=10,
      )
      plt.text(0, 0.4, "Polaridad : " + str(round(sent.polarity, 4)), fontsize=10)
      plt.text(
        0,
        0.35,
        "Subjetividad : " + str(round(sent.subjectivity, 4)),
        fontsize=10,
      )

      plt.axis("off")  # Elimina los ejes
      plt.title(pres["nombre"])

    plt.show()

#==========================================================================================#

  def GenererTendencias(self, sender):
    # implementar grafica de tendencias a lo largo del tiempo
    print(sender)
    #nombres_presidentes = set()  # Lista para almacenar los nombres de los presidentes

    for pres in sender:
      texto_total = ""
      for archivo in pres["archivos"]:
        #nombres_presidentes.add(pres["nombre"])
        with open(archivo.dirTXT, "r", encoding="utf-8") as archivo_txt:
          contenidoTXT = archivo_txt.read()  # leer el texto del archivo
          texto_total = texto_total + contenidoTXT

      palabras = texto_total.split()  

      # Cuenta la frecuencia de cada palabra
      contador_palabras = Counter(palabras)

      # Encuentra las 10 palabras más frecuentes
      palabras_mas_frecuentes = contador_palabras.most_common(dpg.get_value("max_num_palabras"))

      # Separa las palabras y sus frecuencias en listas separadas
      palabras, frecuencias = zip(*palabras_mas_frecuentes)

      # Colores aleatorios para cada barra
      colores_barras = [random.choice(['#'+str(hex(random.randint(0, 16777215)))[2:].zfill(6) for _ in range(len(palabras))]) for _ in range(len(palabras))]

      # Crea la gráfica de tendencia
      plt.figure(figsize=(10, 6))
      plt.bar(palabras, frecuencias, color=colores_barras)

      # Personaliza la gráfica
      plt.title(pres["nombre"])
      plt.xticks(rotation=45, ha='right')
      plt.tight_layout()

    # Muestra la gráfica
    plt.show()

#==========================================================================================#

  def GenererSerieDeTiempos(self, sender):
    # implementar grafica de serie de tiempos
    print(sender)

    # Lista de palabras vacías
    stop_words = set(stopwords.words("spanish"))

    # Ordenar Archivos por Año
    for pres in sender:
      frecuencia_palabras = {}
      frecuencia_palabras_por_anio = {}

      files = []
      for archivo in pres["archivos"]:
        year = archivo.getAño()
        if len(files) == 0:
          files.append(archivo)
        else:
          posicion = -1
          for indice, file in enumerate(files):
            if int(file.getAño()) > year:
              posicion = indice
              break
          if posicion == -1:
            files.append(archivo)
          else:
            files.insert(posicion, archivo)

      if len(files) == 1:
        file_aux = copy.deepcopy(files[0])
        file_aux.setAño(float(file_aux.getAño()) + 1)
        files.append(file_aux)

      for archivo in files:  # Recorrer Presidentes
        with open(archivo.dirTXT, "r") as archivo_txt:
          contenidoTXT = archivo_txt.read()  # leer el texto del archivo

          # Año
          year = archivo.getAño()

          tokens = word_tokenize(
            contenidoTXT.lower()
          )  # Tokenizacion y conversion a minusculas
          palabras = [
            word
            for word in tokens
            if word.isalpha() and word not in stop_words
          ]  # Eliminar Palabras Vacias
          if year not in frecuencia_palabras_por_anio:
            frecuencia_palabras_por_anio[year] = {}
          
          palabrasFiltro_ = dpg.get_value("Palabras_Busqueda_Serie_Tiempos").strip()
          palabrasFiltro = []
          if palabrasFiltro_ != "":
            palabrasFiltro = palabrasFiltro_.split(" ")
            newPalabrasFiltro = []
            for aux in palabrasFiltro:
              newPalabrasFiltro.append(aux.strip())
            palabrasFiltro = newPalabrasFiltro

          for palabra in palabras:
            if (palabra in frecuencia_palabras and palabrasFiltro == []) or (palabra in frecuencia_palabras and palabra in palabrasFiltro):
              frecuencia_palabras[palabra] += 1
            else:
              frecuencia_palabras[palabra] = 1
            if (palabra in frecuencia_palabras_por_anio[year] and palabrasFiltro == []) or (palabra in frecuencia_palabras_por_anio[year] and palabra in palabrasFiltro):
              frecuencia_palabras_por_anio[year][palabra] += 1
            else:
              frecuencia_palabras_por_anio[year][palabra] = 1

      # Ordenar las palabras por frecuencia
      palabras_mas_comunes = sorted(
        frecuencia_palabras.items(), key=lambda x: x[1], reverse=True
      )
      if palabrasFiltro == []:
        palabras_mas_comunes = palabras_mas_comunes[:10]

      # Crear la serie de tiempo para las palabras mas comunes
      serie_de_tiempo = {}
      for palabra, _ in palabras_mas_comunes:
        serie_de_tiempo[palabra] = []

      # Recorrer nuevamente los informes de gobierno para contar la frecuencia de las palabras seleccionadas
      for year, frecuencias_por_anio in frecuencia_palabras_por_anio.items():
        for palabra, _ in palabras_mas_comunes:
          if palabra in frecuencias_por_anio:
            serie_de_tiempo[palabra].append(frecuencias_por_anio[palabra])
          else:
            serie_de_tiempo[palabra].append(0)

      # Años
      years = list(frecuencia_palabras_por_anio.keys())

      # Visualizar Los Datos
      plt.figure(figsize=(6, 5))
      elementos = 0
      for palabra, frecuencias in serie_de_tiempo.items():
        elementos = elementos + 1
        print(palabra, frecuencias, years)
        
        vacio = True
        for frecuencia in frecuencias:
          if (palabrasFiltro == [] and frecuencia != 0) or (palabrasFiltro != [] and palabra in palabrasFiltro and frecuencia != 0):
            vacio = False
            break
        if not vacio:
          plt.plot(years, frecuencias, label=palabra)
        #if elementos == dpg.get_value("max_num_palabras"):  # Palabras limite a mostrar
        #  break
      plt.title(
        "Modelo Serie de Tiempo\n"+pres["nombre"]
      )
      plt.xlabel("Año")
      plt.ylabel("Frecuencia")
      plt.legend()
      plt.tight_layout()
      # return
    plt.show()
