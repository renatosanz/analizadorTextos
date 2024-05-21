# Analizador de Texto 📊📚

## Descripción
Este proyecto es un analizador de texto completo que proporciona diversas funcionalidades de análisis de texto, incluyendo la generación de estadísticas generales, gráficos de dispersión léxica, nubes de palabras, gráficos de tendencias y gráficos de series temporales. El proyecto está implementado en Python 3.8.10.

## Funcionalidades
- **Estadísticas Generales**: Proporciona análisis estadísticos básicos del texto.
- **Dispersión Léxica**: Visualiza la distribución de palabras a lo largo del texto.
- **Nubes de Palabras**: Genera nubes de palabras para mostrar la frecuencia de palabras de forma visual.
- **Gráficos de Tendencias**: Muestra tendencias del uso de palabras a lo largo del tiempo.
- **Gráficos de Series Temporales**: Muestra datos de series temporales del uso de palabras.

## Requisitos
Para ejecutar este proyecto, asegúrate de tener Python 3.8.10 instalado. Las librerías necesarias se pueden instalar utilizando los siguientes comandos:

### Librerías de Análisis de Texto
```bash
pip3 install --user -U nltk
pip3 install -U textblob
```

### Librerías de Matemáticas y Estadísticas
```bash
pip3 install numpy
pip3 install matplotlib
```

### Librería para Extracción de Texto de PDF
```bash
pip3 install PyPDF2
```

### Librería para Generación de Gráficas
```bash
pip3 install wordcloud
# Si surgen problemas, usa el siguiente comando:
pip3 install pillow==9.5-0
```

### Librería de Interfaces
```bash
pip3 install dearpygui
```

### Almacenamiento y Restauración de Datos
No se requiere instalación adicional para `pickle`, ya que viene incluido con Python.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/renatosanz/analizador Textos.git
   cd analizadorTextos
   ```

2. Instala las librerías necesarias como se mencionó anteriormente.

## Uso
Para ejecutar el proyecto, utiliza el siguiente comando:
```bash
python3 main.py
```
Nota: El comando de instalación y ejecución puede diferir ligeramente en Windows. Asegúrate de leer la documentación relevante si encuentras algún problema.

## Notas Importantes 📝
- **Lectura de Archivos en Windows**: La lectura de archivos usando la función `open` en Windows puede diferir de Linux. Consulta [esta página de Stack Overflow](https://stackoverflow.com/questions/491921/unicode-utf-8-reading-and-writing-to-files-in-python) si tienes problemas.
- **Instalación de Dependencias**: Asegúrate de que todas las dependencias estén instaladas antes de ejecutar el código.

## Contribuyendo
Siéntete libre de contribuir a este proyecto enviando una solicitud de extracción o abriendo un issue en el repositorio de GitHub.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.

---

Este archivo readme proporciona una descripción general, instrucciones de instalación, notas de uso y enlaces a recursos adicionales, asegurando que los usuarios puedan configurar y ejecutar el analizador de texto de manera efectiva.