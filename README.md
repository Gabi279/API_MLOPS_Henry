Proyecto individual N°1

Descripción:
Este proyecto se realiza para hacer análisis de los datos presentados a través de los archivos movies y credits, con los cuales se busca crear un sistema de recomendación de películas y además detectar otro tipode relaciónes que puedan  servir para los usuarios de distintas plataformas.

Datasets:
Los archivos de base con los que se trabajo están en formato CSV y se encuentran dentro de la carpeta de Data. Los mismos fueron transformados a DataFrames para poder trabajar en formato columnar.

Procesamiento de datos:
Se realizó una limpieza de datos, borrando valores nulos, reemplazando cuando era necesario para alguna función que lo requiriera, crearión de nuevas columnas unificadas y desanidamiento de diccionarios dentro de los DataSets.
Este proceso se encuentra dentro del archivo PI1, dentro de la carpeta de Notebooks.

EDA:
Una vez hecha la limpieza de datos, se hace un análisis para detectar relaciones entre las variables o las columnas, para poder mostrar estas relaciones y poder trabajar en un futuro con ellas.

Desarrollo de API:
Se crean las funciones para desarrollar la API con FastAPI y deployar con Render.
Además se crea la función para hacer el sistema de recomencaiones.

