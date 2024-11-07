from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint
import traceback  # Importamos traceback para obtener detalles completos del error


# Configuramos opciones para Chrome en modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializamos el controlador de Chrome con las opciones configuradas
driver = webdriver.Chrome(options=chrome_options)

# Función para realizar la búsqueda de un producto y obtener las URLs de los primeros 10 resultados
def obtener_urls_productos(busqueda, cantidad=10):
    # Construimos la URL de búsqueda con el término proporcionado
    url_busqueda = f"https://listado.mercadolibre.com.co/{busqueda}"
    driver.get(url_busqueda)
    try:
        # Esperamos hasta que los elementos de la lista de resultados estén presentes
        productos = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ui-search-layout__item a'))
        )

        # Obtenemos las URLs de los primeros 10 productos
        urls = [producto.get_attribute('href') for producto in productos[:cantidad]]
        return urls
    except Exception as e:
        print(f"Error al obtener las URLs de los productos: {e}")
        traceback.print_exc()  # Imprime el traceback completo del error
        return []

# Función para obtener los detalles de un producto
def obtener_detalles_producto(url_producto):
    data = {}
    try:
        driver.get(url_producto)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-pdp-title')))

        # Extraemos los detalles del producto usando bloques try-except
        try:
            data['Categoria'] = driver.find_element(By.CLASS_NAME, 'ui-pdp-breadcrumb').text.strip()
        except:
            data['Categoria'] = None

        try:
            data['Titulo'] = driver.find_element(By.CLASS_NAME, 'ui-pdp-title').text.strip()
        except:
            data['Titulo'] = None

        try:
            data['Precio'] = driver.find_element(By.CSS_SELECTOR, 'div.ui-pdp-price__second-line span.andes-money-amount__fraction').text.strip()
        except:
            data['Precio'] = None

        try:
            discount = driver.find_element(By.CSS_SELECTOR, 's[role="img"][aria-label^="Antes:"]')
            data['Descuento'] = True if discount else False
        except:
            data['Descuento'] = False

        try:
            seller_button = driver.find_element(By.CLASS_NAME, 'ui-pdp-seller__link-trigger-button')
            seller = seller_button.find_elements(By.TAG_NAME, 'span')[1].text.strip()
            data['Vendedor'] = seller
        except:
            data['Vendedor'] = None

        try:
            data['Calificacion promedio'] = driver.find_element(By.CSS_SELECTOR, 'span.ui-pdp-review__rating[aria-hidden="true"]').text.strip()
        except:
            data['Calificacion promedio'] = None

        try:
            data['Cantidad de Calificaciones'] = driver.find_element(By.CSS_SELECTOR, 'span.ui-pdp-review__amount[aria-hidden="true"]').text.strip()
        except:
            data['Cantidad de Calificaciones'] = None

        try:
            warranty = driver.find_element(By.XPATH, "//p[contains(., 'garantía de fábrica.')]")
            data['Garantia'] = warranty.text.strip() if 'garantía de fábrica.' in warranty.text.strip() else None
        except:
            data['Garantia'] = None

        try:
            data['Descripcion'] = driver.find_element(By.CLASS_NAME, 'ui-pdp-description__content').text.strip()
        except:
            data['Descripcion'] = None

        try:
            data['Stock'] = driver.find_element(By.CLASS_NAME, 'ui-pdp-stock-information__title').text.strip()
        except:
            data['Stock'] = None

        try:
            data['Cantidad de Opiniones'] = driver.find_element(By.CLASS_NAME, 'total-opinion').text.strip()
        except:
            data['Cantidad de Opiniones'] = None

        try:
            data['Numero de Publicacion'] = driver.find_element(By.CSS_SELECTOR, 'span.ui-pdp-color--BLACK.ui-pdp-family--SEMIBOLD').text.strip()
        except:
            data['Numero de Publicacion'] = None

        # Agregamos la URL del producto al diccionario
        data['URL del Producto'] = url_producto

    except Exception as e:
        print(f"Error al extraer los datos del producto: {e}")
    return data

# Realizamos la búsqueda y obtenemos los detalles de los primeros 10 productos
busqueda = 'portatil'
urls_productos = obtener_urls_productos(busqueda)

# Lista para almacenar los detalles de cada producto
detalles_productos = []

# Iteramos sobre cada URL y obtenemos los detalles del producto
for url in urls_productos:
    detalles_producto = obtener_detalles_producto(url)
    detalles_productos.append(detalles_producto)

# Finalmente, imprimimos los detalles de todos los productos de manera legible
pprint.pprint(detalles_productos)

# Cerramos el navegador al final
driver.quit()

