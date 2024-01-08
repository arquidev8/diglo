
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import TimeoutException



driver = webdriver.Chrome()
driver.set_page_load_timeout(20)

try:
    driver.get("https://digloservicer.com/venta-y-alquiler-activos/cualquiera")
except TimeoutException:
    print("The page took too long to load!")


# Inicializa una variable para el scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Este conjunto almacenará los enlaces únicos
unique_links = set()

# Este DataFrame almacenará los enlaces para guardarlos en Excel
df = pd.DataFrame(columns=['Links'])

while True:
    # Desplázate hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera a que se cargue la página
    time.sleep(80)

    # Calcula la nueva altura del scroll y compárala con la última altura
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    # Encuentra todos los elementos con el xpath dado y extrae los href
    # Asegúrate de que el xpath sea correcto para localizar los enlaces. Esta parte del código puede requerir ajuste en base a la estructura de la página
    elements = driver.find_elements(By.XPATH, '//*[@id="enlaceimagen"]')
    for element in elements:
        href = element.get_attribute("href")
        if href not in unique_links:
            print(href)
            unique_links.add(href)
            df = df._append({'Links': href}, ignore_index=True)

            # Si hemos encontrado 20 propiedades nuevas, guardamos los enlaces en un archivo Excel y vaciamos el DataFrame
            if df.shape[0] % 20 == 0:
                df.to_excel('links.xlsx', index=False)

# Guarda todos los enlaces únicos en el archivo Excel después de completar el scraping
df.to_excel('links.xlsx', index=False)

# Cierra el driver
driver.quit()


time.sleep(20)


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
    time.sleep(80)

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
        descripcion_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='block-gavias-lozin-content']/div/article/div[1]/div[1]/div[1]/div[5]/div[2]")))
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



    images_sources_list = []

    # imagen 1
    try:
        photo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[1]/img")))
        images_sources_list.append(photo_element.get_attribute("src"))
    except:
        images_sources_list.append('N/A')

    # imagen 2
    try:
        photo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[2]/img")))
        images_sources_list.append(photo_element.get_attribute("src"))
    except:
        images_sources_list.append('N/A')

    # imagen 3
    try:
        photo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[3]/img")))
        images_sources_list.append(photo_element.get_attribute("src"))
    except:
        images_sources_list.append('N/A')

    # imagen 4
    try:
        photo_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='sync2']/div[1]/div/div[4]/img")))
        images_sources_list.append(photo_element.get_attribute("src"))
    except:
        images_sources_list.append('N/A')

    # Convertir la lista de fuentes de imágenes a formato JSON
    images_sources_json = json.dumps({"src": images_sources_list})

    # # Lista de XPATHs de las imágenes
    # img_xpath_list = ["//*[@id='sync2']/div[1]/div/div[1]/img",
    #                   "//*[@id='sync2']/div[1]/div/div[2]/img",
    #                   "//*[@id='sync2']/div[1]/div/div[3]/img",
    #                   "//*[@id='sync2']/div[1]/div/div[4]/img"]
    #
    # # Lista para almacenar los URLs de las imágenes
    # img_urls_list = []
    #
    # # Revisamos cada XPATH y añadimos la URL específica al diccionario de la imagen correspondiente
    # for xpath in img_xpath_list:
    #     try:
    #         photo_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #         img_urls_list.append({"src": photo_element.get_attribute("src")})
    #     except:
    #         img_urls_list.append({"src": "N/A"})
    #
    # # Convertimos la lista de resultados en formato JSON
    # images_sources_json = json.dumps(img_urls_list)



    # Imprime todos los valores por consola
    try:
        print(f'ciudad: {desired_word}, referencia: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text},  price: {price_text},img: {image_source}, img2: {images_sources_json}, provincia: {desired_word_3}')
    except BrokenPipeError:
        print("Error al escribir en el pipe")

    # Almacena los datos en la lista
    # data.append({
    #     "Provincia": desired_word_3,
    #     "Ciudad": desired_word,
    #     "Referencia": referencia_text,
    #     "Title": title_text,
    #     "Descripcion": descripcion_text,
    #     "Direccion": direccion_text,
    #     "MetrosCuadrados": metros_text,
    #     "Habitaciones": "N/A",
    #     "Banos": "N/A",
    #     "Price": price_text,
    #     "MainPhoto": image_source,
    #     "ImagesSources": images_sources_json
    # })

    # Verificar si la referencia está vacía o es "N/A"
    if referencia_text and referencia_text != "N/A":
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
    else:
        print(f"Referencia vacía o 'N/A' en la URL: {url}. Omitiendo esta propiedad.")
        continue  # Salta a la próxima iteración del bucle



    # Convierte la lista de datos en un DataFrame
    df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Provincia', 'Direccion', 'MetrosCuadrados', 'Habitaciones',  'Banos', 'Price', 'MainPhoto', 'ImageSources', 'Ciudad'])

    # Guarda los datos en un archivo Excel
    df.to_excel(f"properties_data.xlsx", index=False, engine="openpyxl")

    if counter % 20 == 0:
        file_counter = counter // 20
        df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")

    counter += 1

# Guardar los datos en un archivo xlsx al finalizar
df_final = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Provincia', 'Direccion', 'MetrosCuadrados', 'Habitaciones', 'Banos', 'Price', 'MainPhoto', 'ImagesSources', 'Ciudad'])
df_final.to_excel("diglo_data_final.xlsx", index=False, engine="openpyxl")

driver.quit()


time.sleep(20)


# INSERTAR DATOS EN BD
import pandas as pd
from sqlalchemy import create_engine

# Nombre del archivo Excel
archivo_excel = 'diglo_data_final.xlsx'

# Nombre de la tabla en la base de datos
nombre_tabla = 'diglo_properties'

# Conexión a la base de datos
usuario = 'lrdlmrgw_user_baes_hector'
contrasena = 'hannanpiper'
host = '50.31.177.50'
nombre_bd = 'lrdlmrgw_baes'
conexion_bd = f'mysql://{usuario}:{contrasena}@{host}/{nombre_bd}'
engine = create_engine(conexion_bd)

# Leer el archivo Excel y almacenarlo en un DataFrame
df = pd.read_excel(archivo_excel)

# Insertar los datos en la tabla en la base de datos
# df.to_sql(nombre_tabla, engine, if_exists='append', index=False)
df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)