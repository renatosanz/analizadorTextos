import dearpygui.dearpygui as dpg
import os

class PantallaEliminarArchivo():
    def __init__(self,ctrlPresidentes):
        self.ctrlPresidentes = ctrlPresidentes

        #atributos de eliminar archivos
        self.list_presidente_seleccionado = []
        self.dir_presidente_seleccionado = ""
        self.archivo_seleccionado = ""
        self.presidente_seleccionado = ""

        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        window_width1 = 500
        window_height1 = 300
        window_width2 = 200
        window_height2 = 150
        x_pos1 = (viewport_width - window_width1) // 2
        y_pos1 = (viewport_height - window_height1) // 2

        x_pos2 = (viewport_width - window_width2) // 2
        y_pos2 = (viewport_height - window_height2) // 2

        with dpg.window(label="Eliminar Archivo", id = 'eliminarArchivos' ,modal=True, show=False,width=window_width1,height=window_height1,pos=[x_pos1, y_pos1],no_move=True):
            dpg.add_text("Selecciona una presidente y un archivo (.txt) a eliminar")
            dpg.add_listbox(self.ctrlPresidentes.obtenerListaNomPresidentes(),callback=self.eligePresidente, num_items=5)
            dpg.add_listbox([],id="list_archivos_presidente",show=False,callback=self.eligeArchivo)
            dpg.add_button(label="Eliminar",id="eliminar_btn",show=False,callback = self.mostrar_win_confirmar)

        with dpg.window(label="Confirmar", id = 'confirmarBorrado' ,show=False,width=window_width2,height=window_height2,pos=[x_pos2, y_pos2],no_move=True, no_title_bar=True):
            dpg.add_text("¿Borrar archivo?")
            dpg.add_text("Borrado Exitoso!!!",tag="borrado_exitoso",show=False)
            dpg.add_text("Archivo Borrado!",id="txt_archivoBorrado",show=False)
            dpg.add_button(label="Confirmar",id="confirmar_btn",callback= self.realizarBorrado)
            dpg.add_button(label="Volver",callback=self.ocultar_win_confirmar)

    def mostrar_win_confirmar(self):
        # muestra la ventana de confirmacion de borrado del archivo
        dpg.configure_item("confirmarBorrado",show=True) 
        dpg.configure_item("confirmar_btn",show=True)

    def ocultar_win_confirmar(self):
        # oculta la ventana de confirmacion de borrado del archivo
        dpg.configure_item("confirmarBorrado",show=False) 
        dpg.configure_item("list_archivos_presidente", show = False)
        dpg.configure_item("eliminar_btn", show = False)
        dpg.configure_item("confirmarBorrado", show = False)
        dpg.configure_item("txt_archivoBorrado", show = False)

    #funciones de eliminar archivo
    def eligePresidente(self,sender):
        dpg.configure_item("list_archivos_presidente", show = False)
        dpg.configure_item("eliminar_btn", show = False)
        dpg.configure_item("confirmarBorrado", show = False)
        dpg.configure_item("txt_archivoBorrado", show = False)
        self.presidente_seleccionado =  dpg.get_value(sender)
        self.dir_presidente_seleccionado = self.ctrlPresidentes.obtenerDirPresidente(self.presidente_seleccionado)
        if os.path.exists(self.ctrlPresidentes.folder_archivos+self.dir_presidente_seleccionado) and  os.listdir(self.ctrlPresidentes.folder_archivos+self.dir_presidente_seleccionado).__len__()>0:
            self.list_presidente_seleccionado = self.ctrlPresidentes.obtenerListaNomArchivosPresidente(self.presidente_seleccionado)
            dpg.configure_item("list_archivos_presidente",show=True, items=self.list_presidente_seleccionado) 
        else:
            dpg.configure_item("list_archivos_presidente",show=False, items=[]) 
            dpg.configure_item("eliminar_btn", show = False)

    def eligeArchivo(self,sender):
        self.archivo_seleccionado = dpg.get_value(sender)
        dpg.configure_item("eliminar_btn", show = True)

    def realizarBorrado(self):
        self.ctrlPresidentes.borrarArchivoDePresidente(self.presidente_seleccionado,self.archivo_seleccionado)
        dpg.configure_item("borrado_exitoso",show=True)
        dpg.configure_item("confirmar_btn",show=False)