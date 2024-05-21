import dearpygui.dearpygui as dpg
import pickle
import os.path
from entidades.presidente import Presidente
from entidades.archivo import Archivo

class ControlPresidentes():
    def __init__(self):
        self.folder_archivos = "archivos/"
        self.presidentes =  []
        self.archivoRespaldo = 'data.pickle'

    def restaurarInfo(self):
        #restaura la informacion del programa cuando inicia
        if os.path.isfile(self.archivoRespaldo):
            with open(self.archivoRespaldo, 'rb') as file:
                self.presidentes
                self.presidentes = pickle.load(file)

    def guardarInfo(self):
        #guarda la informacion del programa cuando se cierra el programa
        with open(self.archivoRespaldo, 'wb') as file:
            pickle.dump(self.presidentes, file)
    
    def agregarPresidente(self,nomPresidente,nomCarpeta):
        #agrega un nuevo Presidente a la lista de presidentes  
        if nomPresidente!='' and  nomCarpeta!='':
          aux_presidente = Presidente(nomPresidente,nomCarpeta)
          if nomPresidente in [p.nombre for p in self.presidentes] or  nomCarpeta in [p.dir for p in self.presidentes]:
            dpg.set_value("letrero_Agregar_presidente","Nombre o carpeta ya registrado!!!")
          else:
            self.presidentes.append(aux_presidente)
            dpg.set_value("letrero_Agregar_presidente","Presidente registrado exitosamente!!!")
        else:
          dpg.set_value("letrero_Agregar_presidente","Llena los campos!!!")
    
    def obtenerListaNomPresidentes(self):
        #regresa un arreglo con los nombres de cada presidente
        noms_presidentes = []
        for presidente in self.presidentes:
            noms_presidentes.append(presidente.nombre)
        return (noms_presidentes)

    def obtenerListaNomArchivosPresidente(self,nomPresidente):
        #regresa un arreglo con los nombres de los archivos de un presidente
        nomsArchivos = []
        for presidente in self.presidentes:
            if presidente.nombre == nomPresidente:
                for archivo in presidente.archivos:
                    nomsArchivos.append(archivo.nombre)
                break
        return (nomsArchivos)

    def obtenerDirPresidente(self,nomPresidente):
        #regresa el nombre del directorio de un presidente en base se nombre
        presidente_encontrado = None
        for presidente in self.presidentes:
            if presidente.nombre == nomPresidente:
                presidente_encontrado = presidente
                break
        return (presidente_encontrado.dir+"/")

    def obtenerArchivoPresidente(self,nomPresidente,nomArchivo):
        # Se obtiene un objeto Archivo en base al nombre del archivo 
        # y el nombre del presidente al que pertenece
        archivo_encontrado = None
        for presidente in self.presidentes:
            if presidente.nombre == nomPresidente:
                archivo_encontrado = presidente.obtenerArchivo(nomArchivo)
                break
        return (archivo_encontrado)

    def borrarArchivoDePresidente(self,nomPresidente,nomArchivo):
        # Se borra el objeto Archivo en base al nombre del archivo 
        # y el nombre del presidente al que pertenece
        print(nomPresidente,nomArchivo)
        presidente_encontrado = None
        for presidente in self.presidentes:
            if presidente.nombre == nomPresidente:
                presidente_encontrado = presidente
                break
        if presidente_encontrado:
            presidente_encontrado.borrarArchivo(nomArchivo)

    def agregarArchivoDePresidente(self,sender, app_data, user_data):
        # Este es un callback en el cual user_data es un arreglo de la forma:
        # ["nombre presidente",año del archivo (int)]
        # app_data es un diccionario que devuelve el explorador de archivos
        # cuando se confirma la seleccion
        print(user_data)
        # se toman los archivos seleccionados del app_data
        archivosSeleccionados = [direcciones for direcciones in app_data['selections']]
        # se busca el directorio del presidente seleccionado
        directorio_presidente = self.obtenerDirPresidente(user_data[0])
        print(directorio_presidente)

        for dirs in archivosSeleccionados:
            dpg.set_value("cargandoArchivo", "Cargando archivo...")
            dpg.configure_item("cargandoArchivo", show=False)
            dpg.configure_item("archivo_cargado", show=False)
            dpg.configure_item("archivo_existe", show=False)
            
            # obtenemos el path del pdf y el path donde se guardara el archivo txt extraido
            dirPDF = app_data['current_path']+"/"+dirs
            nombre_base_archivo_pdf = os.path.basename(dirPDF)
            nom_archivo_sin_extension = os.path.splitext(nombre_base_archivo_pdf)[0]
            dirTXT = self.folder_archivos+directorio_presidente+nom_archivo_sin_extension+".txt"
            
            # Si el folder del presidente no existe lo crea
            if not os.path.exists(self.folder_archivos+directorio_presidente):
                os.makedirs(self.folder_archivos+directorio_presidente)
                
            print(dirTXT)

            # se busca el presidente 
            presidente_encontrado = None
            for presidente in self.presidentes:
                if presidente.nombre == user_data[0]:
                    presidente_encontrado = presidente
                    break
            if presidente_encontrado:
                # si existe el archivo pdf y el archivo txt no existe se 
                # realiza la agregacion del archivo
                if os.path.isfile(dirPDF) and not os.path.exists(dirTXT):
                    nuevoArchivo = Archivo(nom_archivo_sin_extension,dirTXT,dirPDF,user_data[1])
                    presidente_encontrado.agregarArchivo(nuevoArchivo)
                else:
                    # de lo contrario se muestra el texto de archivo ya existente
                    dpg.configure_item("archivo_existe", show=True)
                    print("already "+dirTXT)