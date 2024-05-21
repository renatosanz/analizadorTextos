import dearpygui.dearpygui as dpg
import os


class PantallaSeleccionarArchivos():
    def __init__(self,cntrlPresidentes):
        self.cntrlPresidentes = cntrlPresidentes

        #atributos de seleccionar archivos
        self.nom_presidente_seleccionado = ""
        self.archivos_seleccionados = []
        self.accion = None
        
    
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        window_width1 = 600
        window_height1 = 500
        x_pos1 = (viewport_width - window_width1) // 2
        y_pos1 = (viewport_height - window_height1) // 2

        with dpg.window(label="Seleccion de Archivos", id = 'seleccion_achivos' ,modal=True,show=False,width=window_width1,height=window_height1,pos=[x_pos1, y_pos1],no_move=True):
            with dpg.group(horizontal=True):
                with dpg.group(width=250):
                    dpg.add_text("Selecciona los archivos a evaluar: ",wrap=200)
                    dpg.add_listbox(cntrlPresidentes.obtenerListaNomPresidentes(),callback = self.seleccionarPresidentes, num_items=6)
                    dpg.add_listbox([],id="list_archivos_presidentes",show=False,callback = self.seleccionarArchivos,num_items=6)
                with dpg.group(width=300):
                    dpg.add_text("Archivos Seleccionados: ")    
                    dpg.add_text(str(self.archivos_seleccionados)+"", id='selecciones')

            dpg.add_text("Maximo de palabras: ", id="max_num_palabras_label")  
            dpg.add_input_int(default_value=10, id="max_num_palabras", tag="max_num_palabras",max_value=20,min_value=1,max_clamped=True,min_clamped=True)    
            
            # Filtro Busqueda Para Diagrama Serie de Tiempos
            dpg.add_text("Palabras Busqueda (Separadas por Espacio)", id="Palabras_Busqueda_Serie_Tiempos_label", show=False)
            dpg.add_input_text(default_value="",id="Palabras_Busqueda_Serie_Tiempos", tag="palabras_modeloSerieTiempo", show=False)

            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_button(label="Avanzar",id="avanzar_btn",show=False,callback = self.ejecutarAccion)
                with dpg.group():
                    dpg.add_button(label="Limpiar Seleccion",id="limpia_select_btn",show=False,callback = self.limpiarSeleccion)

    def showPalabrasBuscarSerieTiempo(self):
      dpg.show_item("Palabras_Busqueda_Serie_Tiempos_label")
      dpg.show_item("Palabras_Busqueda_Serie_Tiempos")
      dpg.hide_item("max_num_palabras_label")
      dpg.hide_item("max_num_palabras")

    def hidePalabrasBuscarSerieTiempo(self):
      dpg.hide_item("Palabras_Busqueda_Serie_Tiempos_label")
      dpg.hide_item("Palabras_Busqueda_Serie_Tiempos")
      dpg.show_item("max_num_palabras_label")
      dpg.show_item("max_num_palabras")

    def asignarAccion(self,act, opcionPalabrasFiltro=None):
        # esta funcion se usa para asignar una operacion a realizar 
        # cuando se termine la seleccion de archivos, por ejemplo:
        # generar grafica de dispersion lexica,
        # generar grafica de wordcloud, o generar estadisticas generales
        self.list_presidente_seleccionado = []
        self.dir_presidente_seleccionado = ""
        self.nom_presidente_seleccionado = ""
        # la seleccion se guarda en esta estructura de datos:
        # [nombre: "nombre presidente", archivos: [ arreglo de objetos Archivo]]
        self.archivos_seleccionados = [{'nombre':p.nombre,'archivos':[]} for p in self.cntrlPresidentes.presidentes]
        self.accion = act
        # limpiamos la ventana de cualquier seleccion
        dpg.show_item('seleccion_achivos')
        dpg.configure_item("list_archivos_presidentes", show = False)
        dpg.configure_item("avanzar_btn", show = False)
        dpg.configure_item("selecciones", show = False)

        self.hidePalabrasBuscarSerieTiempo()
        if opcionPalabrasFiltro == True:
          self.showPalabrasBuscarSerieTiempo()

    def seleccionarPresidentes(self,sender):
        # dado el nombre del presidente seleccionado se 
        # muestran sus archivos posibles a seleccionar
        dpg.configure_item("list_archivos_presidentes", show = False)
        dpg.configure_item("avanzar_btn", show = False)        
        self.nom_presidente_seleccionado =  dpg.get_value(sender)
        self.dir_presidente_seleccionado = self.cntrlPresidentes.obtenerDirPresidente(self.nom_presidente_seleccionado)
        if os.path.exists(self.cntrlPresidentes.folder_archivos+self.dir_presidente_seleccionado) and  os.listdir(self.cntrlPresidentes.folder_archivos+self.dir_presidente_seleccionado).__len__()>0:
            self.list_presidente_seleccionado = self.cntrlPresidentes.obtenerListaNomArchivosPresidente(self.nom_presidente_seleccionado)
            dpg.configure_item("list_archivos_presidentes",show=True, items=self.list_presidente_seleccionado) 
        else:
          dpg.configure_item("list_archivos_presidentes",show=False, items=[]) 
          dpg.configure_item("limpia_select_btn", show = False)
          dpg.configure_item("avanzar_btn", show = False)            
          dpg.configure_item("avanzar_btn", show = False)
          dpg.configure_item("limpia_select_btn", show = False)

    def seleccionarArchivos(self,sender):
      # cuando se selecciona un archivo se agrega al 
      # arreglo de archivos al presidente correspondiente
      # en la estructura de datos antes mecionada
      nom_archivo = dpg.get_value(sender)
      archivo = self.cntrlPresidentes.obtenerArchivoPresidente(self.nom_presidente_seleccionado,nom_archivo)

      for pres in self.archivos_seleccionados:
        #si ya se encuentra seleccionado el archivos, no se agrega de nuevo
        if pres["nombre"] == self.nom_presidente_seleccionado and not archivo in pres["archivos"]:
          pres["archivos"].append(archivo)
          break

      dpg.configure_item("avanzar_btn", show = True)
      dpg.configure_item("limpia_select_btn", show = True)
      dpg.configure_item("selecciones", show = True)
      self.actualizarSeleccion()


    def ejecutarAccion(self):
      # cuando se pulsa el boton avanzar se ejecuta la funcion accion con los parametros:
      # [un arreglo con los presidentes que tienen mas de 0 archivos seleccionados]  
      self.accion([pres for pres in self.archivos_seleccionados if pres['archivos'].__len__()!=0])

    def actualizarSeleccion(self):
      # actualizamos el letrero que muestra los archivos seleccionados hasta el momento
      text = ""
      for pres in self.archivos_seleccionados:
        if pres["archivos"].__len__()!=0:
          text=text+"*"+pres['nombre']+"\n"
          for arch in pres['archivos']:
            text=text+"  -->"+str(arch.año)+" : "+arch.nombre+"\n"
      dpg.set_value('selecciones',text)

    def limpiarSeleccion(self):
      # en caso que el usuario quiera limpiar las selecciones que ha hecho 
      # esta funcion resetea las variables para volver a realizar la seleccion  
      self.list_presidente_seleccionado = []
      self.dir_presidente_seleccionado = ""
      self.nom_presidente_seleccionado = ""
      self.archivos_seleccionados = [{'nombre':p.nombre,'archivos':[]} for p in self.cntrlPresidentes.presidentes]
      self.actualizarSeleccion()
      dpg.configure_item("list_archivos_presidentes",show=False, items=[]) 
      dpg.configure_item("limpia_select_btn", show = False)
      dpg.configure_item("avanzar_btn", show = False)