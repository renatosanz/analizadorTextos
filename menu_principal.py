import tkinter as tk
import dearpygui.dearpygui as dpg

from control.control_presidentes import ControlPresidentes

#importamos las clases de interface
from interfaces.pantalla_cargar_archivo import  PantallaCargarArchivos
from interfaces.pantalla_eliminar_archivo import  PantallaEliminarArchivo
from interfaces.pantalla_seleccionar_archvos import  PantallaSeleccionarArchivos
from interfaces.pantalla_agregar_presidente import  PantallaAgregarPresidente

#importamos las clases de procesamiento
from control.operador_de_texto import OperadorDeTexto

def prueba(sender):
    print(sender)

class MenuPrincipal():
    def __init__(self):

        # calcula la mitad de la pantalla para ahi mostrar el programa
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        viewport_width = 600
        viewport_height = 400
        x_poss = (screen_width - viewport_width) // 2
        y_poss = (screen_height - viewport_height) // 2

        #creamos las clases de control
        self.cntrlPresidentes = ControlPresidentes()
        self.op = OperadorDeTexto()

        #restauramos la informacion del programa
        self.cntrlPresidentes.restaurarInfo()
        
        dpg.create_context()
        dpg.create_viewport(title='Analizador de textos',width=800,height=600,x_pos=x_poss,y_pos=y_poss, disable_close=True)

        #seleccion de fuente
        with dpg.font_registry():
            self.default_font = dpg.add_font("font.ttf", 16)

        #creamos las interfaces
        self.pca = PantallaCargarArchivos(self.cntrlPresidentes)
        self.pea = PantallaEliminarArchivo(self.cntrlPresidentes)
        self.psa = PantallaSeleccionarArchivos(self.cntrlPresidentes)
        self.pap = PantallaAgregarPresidente(self.cntrlPresidentes)


        #definimos opciones del menu principal        
        self.opciones = [["main_cargar_archivo","Cargar Archivo",lambda: dpg.show_item('cargarArchivos')],
            ["main_eliminar_archivo","Eliminar Archivo",lambda: dpg.show_item('eliminarArchivos')],
            ["main_gen_estadisiticas","Generar Estadisticas",lambda: self.psa.asignarAccion(self.op.GenerarEstadisticasGenerales)],
            ["main_disp_lexica","Generar Grafica de \nDispersion Lexica",lambda: self.psa.asignarAccion(self.op.GenerarDispLexica)],
            ["main_wordcloud","Generar WordCloud",lambda: self.psa.asignarAccion(self.op.GenerarWordClouds)],
            # ["main_serie_tiempos","Generar Modelo de \nSerie de Tiempos",self.catchCallback],
            ["main_serie_tiempos","Generar Modelo de \nSerie de Tiempos",lambda: self.psa.asignarAccion(self.op.GenererSerieDeTiempos, True)],
            #["main_tendencias","Generar Grafica de \nTendencias",self.catchCallback],
            ["main_tendencias","Generar Grafica de \nTendencias",lambda: self.psa.asignarAccion(self.op.GenererTendencias)],
            ["main_agregar_presidente","Agregar Presidente",lambda: dpg.show_item('agregarPresidentes')],
            ["main_salir","Salir",self.salir]]


        with dpg.window(label="Menu Pricipal",id='MAIN_MENU',width=800,height=600,no_resize=True):
            dpg.add_text("Buen dia, Maria Ramos.")
            with dpg.group():
                for op in self.opciones:
                    dpg.add_button(label=op[1],tag=op[0],callback=op[2])
                dpg.add_text("Favor de ingresar un presidente!!!",tag="sin_presidentes",show=False)

        #si no hay presidentes registrados no se muestran las demas opciones
        #solo se muestra la opcion de Agregar Presidente
        if self.cntrlPresidentes.presidentes.__len__()==0:
            dpg.configure_item("main_cargar_archivo",show = False)
            dpg.configure_item("main_eliminar_archivo",show = False)
            dpg.configure_item("main_gen_estadisiticas",show = False)
            dpg.configure_item("main_disp_lexica",show = False)
            dpg.configure_item("main_wordcloud",show = False)
            dpg.configure_item("main_serie_tiempos",show = False)
            dpg.configure_item("main_tendencias",show = False)
            dpg.configure_item("sin_presidentes",show = True)
        else:
            dpg.configure_item("main_cargar_archivo",show = True)
            dpg.configure_item("main_eliminar_archivo",show = True)
            dpg.configure_item("main_gen_estadisiticas",show = True)
            dpg.configure_item("main_disp_lexica",show = True)
            dpg.configure_item("main_wordcloud",show = True)
            dpg.configure_item("main_serie_tiempos",show = True)
            dpg.configure_item("main_tendencias",show = True)
            dpg.configure_item("sin_presidentes",show = False)

            

        dpg.bind_font(self.default_font)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MAIN_MENU",True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def catchCallback(sender, app_data):
     print(f"sender is: {sender}")
     print(f"app_data is: {app_data}")

    def salir(self):
        self.cntrlPresidentes.guardarInfo()
        dpg.stop_dearpygui()

