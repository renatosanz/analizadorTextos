import dearpygui.dearpygui as dpg

class PantallaAgregarPresidente():
    def __init__(self,cntrlPresidentes):
        self.cntrlPresidentes = cntrlPresidentes 

        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        window_width1 = 500
        window_height1 = 300
        x_pos1 = (viewport_width - window_width1) // 2
        y_pos1 = (viewport_height - window_height1) // 2

        with dpg.window(label="Agregar Presidentes", id = 'agregarPresidentes' ,modal=True,show=False,width=window_width1,height=window_height1,pos=[x_pos1, y_pos1],no_move=True):
            dpg.add_text("Ingresa el nombre del presidente: ")
            dpg.add_input_text(tag="input_nombre_presidente")
            dpg.add_text("Ingresa el nombre de la carpeta para archivos del presidente:")
            dpg.add_input_text(tag="input_carpeta_presidente")
            dpg.add_button(label="Agregar Presidente",tag="boton_agregar_presidente",callback=self.realizarAgregado)
            dpg.add_text("",tag="letrero_Agregar_presidente")
        
    def realizarAgregado(self):
        self.cntrlPresidentes.agregarPresidente(dpg.get_value("input_nombre_presidente"),dpg.get_value("input_carpeta_presidente"))
        #si no hay presidentes registrados no se muestran las demas opciones
        #solo se muestra la opcion de Agregar Presidente
        # de lo contrario mostramos todas las opciones
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

