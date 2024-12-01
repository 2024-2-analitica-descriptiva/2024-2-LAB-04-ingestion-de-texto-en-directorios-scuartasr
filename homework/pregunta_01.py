# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import zipfile
import os
import pandas as pd

def descomprimir_zip(archivo_zip):
    """
    Descomprime un archivo .zip y aloja los archivos descomprimidos en una carpeta
    ubicada en el directorio padre del archivo .zip.

    :param archivo_zip: Ruta completa del archivo .zip
    """
    # Verifica que el archivo sea un .zip
    if not archivo_zip.endswith('.zip'):
        raise ValueError("El archivo proporcionado no es un .zip")

    # Obtiene el directorio padre del archivo .zip
    directorio_actual = os.path.dirname(archivo_zip)
    directorio_padre = os.path.dirname(directorio_actual)

    # Obtiene el nombre base del archivo .zip (sin extensión)
    nombre_base = os.path.splitext(os.path.basename(archivo_zip))[0]

    # Crea la ruta de la carpeta de salida directamente en el directorio padre
    carpeta_salida = os.path.join(directorio_padre, nombre_base)

    # Crea la carpeta de salida si no existe
    os.makedirs(carpeta_salida, exist_ok=True)

    # Extrae los archivos del .zip en la carpeta de salida
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_salida)

# ========================================================================
# ========================================================================

def lectura_textos(carpeta: str) -> pd.DataFrame:
    """
    Esta función recorre todos los archivos .txt que existen dentro de una carpeta
    y adiciona el texto de un marco de datos
    """
    nombre_carpeta = os.path.basename(os.path.normpath(carpeta))

    datos = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith('.txt'):
            ruta_archivo = os.path.join(carpeta, archivo)
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Agrega el contenido a la lista
            datos.append({'phrase': contenido, 'target': nombre_carpeta})

    # Crea un DataFrame con el contenido
    df = pd.DataFrame(datos)
    return df

# ========================================================================
# ========================================================================

def union_carpetas_txt(directorio_principal, ruta_salida):
    """
    Recorre todas las subcarpetas dentro de un directorio principal, aplica la función
    procesar_txt_en_carpeta en cada subcarpeta y combina los resultados en un único DataFrame.

    :param directorio_principal: Ruta del directorio que contiene las subcarpetas.
    :return: DataFrame combinado con columnas 'phrase' y 'target'.
    """
    dataframes = []

    # Recorre todas las subcarpetas en el directorio principal
    for subcarpeta in os.listdir(directorio_principal):
        ruta_subcarpeta = os.path.join(directorio_principal, subcarpeta)
        
        # Verifica que sea un directorio
        if os.path.isdir(ruta_subcarpeta):
            # Llama a la función procesar_txt_en_carpeta para la subcarpeta
            df_subcarpeta = lectura_textos(ruta_subcarpeta)
            dataframes.append(df_subcarpeta)

    # Combina todos los DataFrames en uno solo
    df_combinado = pd.concat(dataframes, ignore_index=True)

    # Asegura que la carpeta de salida exista
    carpeta_destino = os.path.dirname(ruta_salida)
    if not os.path.exists(carpeta_destino):
        try:
            os.makedirs(carpeta_destino)
            print(f"Carpeta creada: {carpeta_destino}")
        except Exception as e:
            print(f"Error al crear la carpeta: {e}")
            return  # Si no se puede crear la carpeta, detiene el proceso.

    # Depuración: Verifica la ruta de salida antes de intentar guardar el archivo
    print(f"Guardando el archivo CSV en: {ruta_salida}")

    try:
        # Guarda el DataFrame combinado como un archivo .csv
        df_combinado.to_csv(ruta_salida, index=False)
        print(f"Archivo CSV guardado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")

# ========================================================================
# ========================================================================

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """

    # Descompersión
    comprimido = './files/input.zip'
    descomprimir_zip(comprimido)

    testeo = './input/input/test'
    testeo_rta = './files/output/test_dataset.csv'

    entrenamiento = './input/input/train'
    entrenamiento_rta = './files/output/train_dataset.csv'
    
    union_carpetas_txt(testeo, testeo_rta)
    union_carpetas_txt(entrenamiento, entrenamiento_rta)

    df = pd.read_csv(testeo_rta, header=0)