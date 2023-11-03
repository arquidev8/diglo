# #
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pandas as pd
# from selenium.common.exceptions import TimeoutException
#
#
#
# driver = webdriver.Chrome()
# driver.set_page_load_timeout(10)
#
# try:
#     driver.get("https://digloservicer.com/venta-y-alquiler-activos/cualquiera")
# except TimeoutException:
#     print("The page took too long to load!")
#
#
# # Inicializa una variable para el scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
#
# # Este conjunto almacenará los enlaces únicos
# unique_links = set()
#
# # Este DataFrame almacenará los enlaces para guardarlos en Excel
# df = pd.DataFrame(columns=['Links'])
#
# while True:
#     # Desplázate hasta el final de la página
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Espera a que se cargue la página
#     time.sleep(40)
#
#     # Calcula la nueva altura del scroll y compárala con la última altura
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#
#     # Encuentra todos los elementos con el xpath dado y extrae los href
#     # Asegúrate de que el xpath sea correcto para localizar los enlaces. Esta parte del código puede requerir ajuste en base a la estructura de la página
#     elements = driver.find_elements(By.XPATH, '//*[@id="enlaceimagen"]')
#     for element in elements:
#         href = element.get_attribute("href")
#         if href not in unique_links:
#             print(href)
#             unique_links.add(href)
#             df = df._append({'Links': href}, ignore_index=True)
#
#             # Si hemos encontrado 20 propiedades nuevas, guardamos los enlaces en un archivo Excel y vaciamos el DataFrame
#             if df.shape[0] % 20 == 0:
#                 df.to_excel('links.xlsx', index=False)
#
# # Guarda todos los enlaces únicos en el archivo Excel
# if not df.empty:
#     df.to_excel('links.xlsx', index=False)
#
# # Cierra el driver
# driver.quit()


#
#
# import mysql.connector
# import json
# import xml.etree.ElementTree as ET
# from selenium import webdriver
# from selenium.common import NoSuchElementException, TimeoutException
# from selenium.webdriver.common.by import By
# import pandas as pd
# from datetime import date
# import time
# import re
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
#
#
# # Establecer la conexión a la base de datos SQL
# try:
#     conn = mysql.connector.connect(
#         host="50.31.177.50",
#         user="lrdlmrgw_user_baes",
#         password="hannanpiper",
#         database="lrdlmrgw_baes"
#     )
#     print('Conexión exitosa a la base de datos')
# except:
#     print('Error al conectarse a la base de datos')
#
# # Crear una tabla en la base de datos
# cur = conn.cursor()
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS diglo_properties (
#         Referencia TEXT,
#         Title TEXT,
#         Descripcion TEXT,
#         Provincia TEXT,
#         Direccion TEXT,
#         MetrosCuadrados TEXT,
#         Habitaciones TEXT,
#         Banos TEXT,
#         Price TEXT,
#         MainPhoto TEXT,
#         ImageSources JSON,
#         Ciudad TEXT
#     )
#     """)
# conn.commit()
#
# # Eliminar todos los registros de la tabla
# cur.execute("""
#     TRUNCATE TABLE solvia_properties;
# """)
# conn.commit()
#
#
# # Inicializar el navegador
# driver = webdriver.Chrome()
#
# # Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
# df = pd.read_excel('links.xlsx', sheet_name='Sheet1', usecols=['Links'])
#
# # Convierte los URLs en una lista
# url_list = df['Links'].tolist()
#
#
#
#
# data = []
# counter = 0
# for url in url_list:
#
#     driver.get(url)
#     time.sleep(15)
#
#
#     accept_cookies_button = driver.find_elements(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
#     if accept_cookies_button:
#         accept_cookies_button[0].click()
#
#     # Esperar a que el elemento esté presente en la página antes de extraer el texto
#     wait = WebDriverWait(driver, 40)
#
#     try:
#         title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='property-title']//span")))
#         title_text = title.text
#     except TimeoutException:
#         title_text = 'N/A'
#
#
#     # provincia
#     try:
#         provincia = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='listing-location-taxonomy bb']")))
#         provincia_text = provincia.text
#         words = provincia_text.split(',')
#         if len(words) > 0:
#             desired_word_3 = words[0].strip()  # split by space and take the first word
#         else:
#             desired_word_3 = 'N/A'
#     except TimeoutException:
#         desired_word_3 = 'N/A'
#
#
#     # Ciudad
#     try:
#         ciudad = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='listing-location-taxonomy bb']")))
#         ciudad_text = ciudad.text
#         words = ciudad_text.split(',')
#         if len(words) > 1:
#             desired_word = words[1].strip()  # strip() se usa para eliminar espacios en blanco al principio y al final
#             desired_word = desired_word.split('/')[
#                 0].strip()  # divide la cadena de texto por '/' y toma el primer elemento
#         else:
#             desired_word = 'N/A'
#     except TimeoutException:
#         desired_word = 'N/A'
#
#     # Metros cuadrados
#     try:
#         metros_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sidebar-detail']/div[1]/div[3]/div[2]/div/span")))
#         metros_text = metros_element.text.replace("m2", "")
#     except TimeoutException:
#         metros_text = 'N/A'
#
#
#     # Referencia
#     try:
#         referencia = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='property-ref']")))
#         referencia_text = referencia.text.replace("Ref:", "")
#     except TimeoutException:
#         referencia_text = 'N/A'
#
#     # Direccion
#     try:
#         direccion_element = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='listing-location']/div[2]/div[1]")))
#         direccion_text = direccion_element.text
#     except TimeoutException:
#         direccion_text = 'N/A'
#
#
#     # Descripción
#     try:
#         descripcion_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='block-gavias-lozin-content']/div/article/div[1]/div[2]/div[1]/div[5]/div[2]")))
#         descripcion_text = descripcion_element.text.replace("Descripción", "")
#     except:
#         descripcion_text = 'N/A'
#
#     # Precio
#     try:
#         price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='property-price mt-3 mb-2 dscto-line-height-1']")))
#         price_text = price_element.text.split(' ')[0]  # divide la cadena de texto por espacios y toma el primer elemento
#     except:
#         price_text = 'N/A'
#
#     # Imagen principal
#     try:
#         main_photo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sync1']/div[1]/div/div[1]/div/div/img")))
#         image_source = main_photo_element.get_attribute("src")
#     except:
#         image_source = 'N/A'
#
#     #imagen 2
#     try:
#         photo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[1]/img")))
#         images_sources = photo_element.get_attribute("src")
#     except:
#         images_sources = 'N/A'
#
#     images_sources_json = json.dumps({"src": images_sources})
#
#
#     #imprimir todos los valores por consola
#     try:
#         print(f'ciudad: {desired_word}, referencia: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text},  price: {price_text},img: {image_source}, img2: {images_sources}, provincia: {desired_word_3}')
#     except BrokenPipeError:
#         print("Error al escribir en el pipe")
#
#     # Almacenar los datos en la lista
#     data.append({
#         "Provincia": desired_word_3,
#         "Ciudad": desired_word,
#         "Referencia": referencia_text,
#         "Title": title_text,
#         "Descripcion": descripcion_text,
#         "Direccion": direccion_text,
#         "MetrosCuadrados": metros_text,
#         "Habitaciones": "N/A",
#         "Banos": "N/A",
#         "Price": price_text,
#         "MainPhoto": image_source,
#         "ImagesSources": images_sources_json
#
#     })
#
#     # Convertir la lista de datos en un DataFrame
#     df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Provincia', 'Direccion', 'MetrosCuadrados', 'Habitaciones',  'Banos', 'Price', 'MainPhoto', 'ImageSources' 'Ciudad'])
#
#
#     # Insertar los datos extraídos en la tabla de la base de datos
#     cur.execute("""
#                 INSERT INTO diglo_properties (
#                     Referencia,
#                     Title,
#                     Descripcion,
#                     Provincia,
#                     Direccion,
#                     MetrosCuadrados,
#                     Habitaciones,
#                     Banos,
#                     Price,
#                     MainPhoto,
#                     ImageSources,
#                     Ciudad
#                 )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#             """, (
#         referencia_text,
#         title_text,
#         descripcion_text,
#         desired_word_3,
#         direccion_text,
#         metros_text,
#         "N/A",
#         "N/A",
#         price_text,
#         image_source,
#         images_sources_json,
#         desired_word
#     ))
#     conn.commit()
#
#     # Añade los datos a la lista
#     data.append(df)
#
#
#
#     if counter % 20 == 0:
#         file_counter = counter // 20
#         df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
#
# driver.quit()
#
# # Cerrar la conexión con la base de datos
# cur.close()
# conn.close()


import json
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializar el navegador
driver = webdriver.Chrome()

# Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
df = pd.read_excel('links.xlsx', sheet_name='Sheet1', usecols=['Links'])

# Convierte los URLs en una lista
url_list = df['Links'].tolist()

data = []
counter = 0
for url in url_list:

    driver.get(url)
    time.sleep(15)

    accept_cookies_button = driver.find_elements(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
    if accept_cookies_button:
        accept_cookies_button[0].click()

    # Esperar a que el elemento esté presente en la página antes de extraer el texto
    wait = WebDriverWait(driver, 40)

    try:
        title = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='property-title']//span")))
        title_text = title.text
    except TimeoutException:
        title_text = 'N/A'

    # provincia
    try:
        provincia = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='listing-location-taxonomy bb']")))
        provincia_text = provincia.text
        words = provincia_text.split(',')
        if len(words) > 0:
            desired_word_3 = words[0].strip()  # split by space and take the first word
        else:
            desired_word_3 = 'N/A'
    except TimeoutException:
        desired_word_3 = 'N/A'

    # Ciudad
    try:
        ciudad = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='listing-location-taxonomy bb']")))
        ciudad_text = ciudad.text
        words = ciudad_text.split(',')
        if len(words) > 1:
            desired_word = words[1].strip()  # strip() se usa para eliminar espacios en blanco al principio y al final
            desired_word = desired_word.split('/')[
                0].strip()  # divide la cadena de texto por '/' y toma el primer elemento
        else:
            desired_word = 'N/A'
    except TimeoutException:
        desired_word = 'N/A'

    # Metros cuadrados
    try:
        metros_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sidebar-detail']/div[1]/div[3]/div[2]/div/span")))
        metros_text = metros_element.text.replace("m2", "")
    except TimeoutException:
        metros_text = 'N/A'

    # Referencia
    try:
        referencia = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='property-ref']")))
        referencia_text = referencia.text.replace("Ref:", "")
    except TimeoutException:
        referencia_text = 'N/A'

    # Direccion
    try:
        direccion_element = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='listing-location']/div[2]/div[1]")))
        direccion_text = direccion_element.text
    except TimeoutException:
        direccion_text = 'N/A'

    # Descripción
    try:
        descripcion_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='block-gavias-lozin-content']/div/article/div[1]/div[2]/div[1]/div[5]/div[2]")))
        descripcion_text = descripcion_element.text.replace("Descripción", "")
    except:
        descripcion_text = 'N/A'

    # Precio
    try:
        price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='property-price mt-3 mb-2 dscto-line-height-1']")))
        price_text = price_element.text.split(' ')[0]  # divide la cadena de texto por espacios y toma el primer elemento
    except:
        price_text = 'N/A'

    # Imagen principal
    try:
        main_photo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='sync1']/div[1]/div/div[1]/div/div/img")))
        image_source = main_photo_element.get_attribute("src")
    except:
        image_source = 'N/A'

    # imagen 2
    try:
        photo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[1]/img")))
        images_sources = photo_element.get_attribute("src")
    except:
        images_sources = 'N/A'

    images_sources_json = json.dumps({"src": images_sources})

    # Imprime todos los valores por consola
    try:
        print(f'ciudad: {desired_word}, referencia: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text},  price: {price_text},img: {image_source}, img2: {images_sources}, provincia: {desired_word_3}')
    except BrokenPipeError:
        print("Error al escribir en el pipe")

    # Almacena los datos en la lista
    data.append({
        "Provincia": desired_word_3,
        "Ciudad": desired_word,
        "Referencia": referencia_text,
        "Title": title_text,
        "Descripcion": descripcion_text,
        "Direccion": direccion_text,
        "MetrosCuadrados": metros_text,
        "Habitaciones": "N/A",
        "Banos": "N/A",
        "Price": price_text,
        "MainPhoto": image_source,
        "ImagesSources": images_sources_json
    })

    # Convierte la lista de datos en un DataFrame
    df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Provincia', 'Direccion', 'MetrosCuadrados', 'Habitaciones',  'Banos', 'Price', 'MainPhoto', 'ImageSources', 'Ciudad'])

    # Guarda los datos en un archivo Excel
    df.to_excel(f"properties_data.xlsx", index=False, engine="openpyxl")

    if counter % 20 == 0:
        file_counter = counter // 20
        df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")

    counter += 1

driver.quit()