import dearpygui.dearpygui as dpg

class PantallaCargarArchivos():
    def __init__(self,cntrlPresidentes):
        self.cntrlPresidentes = cntrlPresidentes

        #atributos de cargar archivo
        self.presidente_seleccionado = ''
        self.fecha = 0

        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        window_width = 800
        window_height = 600
        x_pos = (viewport_width - window_width) // 2
        y_pos = (viewport_height - window_height) // 2
        
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.realizarCarga, id="explorador", width=500,height=300):
            dpg.add_file_extension(".pdf")

        with dpg.window(label="Explorar Archivo", id = 'cargarArchivos' ,show=False,width=window_width,height=window_height,pos=[x_pos, y_pos],no_move=True):
            dpg.add_text("Selecciona una presidente y un archivo (.pdf) a cargar",show=True,tag = 'extrayendo')
            dpg.add_listbox(cntrlPresidentes.obtenerListaNomPresidentes(),callback=self.asignarPresidente,num_items=8)
            dpg.add_text("Ingresa el año del Archivo: ",show=True)
            dpg.add_input_int(tag="fecha_Archivo",default_value=2000,max_value=3000,min_value=0,min_clamped=True,max_clamped=True)
            dpg.add_button(label="Examinar",show=False,tag = "examinar",callback = self.examinarArchivos)
            dpg.add_text("Cargando archivo...",show=False,id = 'cargandoArchivo')
            dpg.add_text("Archivo Cargado Exitosamente!!!",show=False,id = 'archivo_cargado')
            dpg.add_text("Archivo Ya Existente!!!",show=False,id = 'archivo_existe')

    def asignarPresidente(self,sender):
        # se guarda el nombre del presidente seleccionado
        self.presidente_seleccionado =  dpg.get_value(sender)
        dpg.configure_item("examinar", show=True)

    def examinarArchivos(self):
        # se muestra el explorador de archivos
        self.fecha = dpg.get_value("fecha_Archivo")
        # se asigna a user_data los valores del nombre 
        # presidente seleccionado y la fecha (año del archivi)
        dpg.configure_item("explorador",user_data=[self.presidente_seleccionado,self.fecha])
        dpg.show_item("explorador")
    
    def realizarCarga(self,sender, app_data, user_data):
        self.cntrlPresidentes.agregarArchivoDePresidente(sender, app_data, user_data)