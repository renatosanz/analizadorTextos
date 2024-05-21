class Presidente():
  def __init__(self,nombre,dir):
    self.nombre = nombre
    self.dir = dir
    self.archivos = []

  def borrarArchivo(self,nomArchivo):
    # en base al nombre del archivo, se busca el objeto y se elimina
    archivo_encontrado = None
    for archivo in self.archivos:
      if archivo.nombre == nomArchivo:
        archivo_encontrado = archivo
        archivo_encontrado.borrar()
        self.archivos.remove(archivo_encontrado)
        break

  def agregarArchivo(self,archivo):
    # se recibe un objeto Archivo y se agrega a la lista de archivos
    # para despues ordenarlos por el año 
    self.archivos.append(archivo)
    self.archivos = sorted(self.archivos,key=lambda x: x.año)

  def obtenerArchivo(self,nomArchivo):
    # buasca el objeto Archivo dentro del 
    # arreglo de archivos en base al nombre de este
    archivo_encontrado = None
    for archivo in self.archivos:
      if archivo.nombre == nomArchivo:
        archivo_encontrado = archivo
        return archivo_encontrado
        break