import requests # Importamos la librería requests para realizar solicitudes HTTP
from bs4 import BeautifulSoup # Importamos BeautifulSoup de bs4 para analizar documentos HTML y XML
import pprint # Importamos pprint para imprimir estructuras de datos de manera legible

# Función para realizar la búsqueda de un producto y obtener las primeras 10 URLs de resultados
def obtener_urls_productos(busqueda, cantidad=10):
    try:
        # Construimos la URL de búsqueda con el término proporcionado
        url_busqueda = f"https://listado.mercadolibre.com.co/{busqueda}"

        # Enviamos una solicitud GET a la URL de búsqueda
        response = requests.get(url_busqueda, timeout=10)
        response.raise_for_status()

        # Analizamos el contenido HTML de la respuesta
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontramos los elementos de la lista de resultados de búsqueda
        items = soup.find_all('li', class_='ui-search-layout__item', limit=cantidad)
        # Obtenemos los enlaces de los productos
        urls = [item.find('a', href=True)['href'] for item in items if item.find('a', href=True)]

        # Retornamos la lista de URLs
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return []


# Función para obtener los detalles de un producto
def obtener_detalles_producto(url_producto):
    try:
        # Enviamos una solicitud GET a la URL del producto
        response = requests.get(url_producto)
        # Analizamos el contenido HTML de la página del producto
        soup = BeautifulSoup(response.content, 'html.parser')

        # Creamos un diccionario para almacenar los datos del producto
        data = {}

        # Extraemos la categoría del producto
        category = soup.find('div', class_='ui-pdp-breadcrumb')
        data['Categoria'] = category.get_text(strip=True) if category else None

        # Extraemos el título del producto
        title = soup.find('h1', class_='ui-pdp-title')
        data['Titulo'] = title.get_text(strip=True) if title else None

        # Extraemos el precio del producto
        price_div = soup.find('div', class_='ui-pdp-price__second-line')
        price = price_div.find('span', class_='andes-money-amount__fraction') if price_div else None
        data['Precio'] = price.get_text(strip=True) if price else None

        # Buscamos un elemento que indique si hay un descuento
        discount = soup.find('s', {'role': 'img', 'aria-label': lambda x: x and x.startswith('Antes:')})
        data['Descuento'] = bool(discount)

        # Extraemos el nombre del vendedor
        seller_button = soup.find('button', class_='ui-pdp-seller__link-trigger-button non-selectable')
        seller = seller_button.find_all('span')[1].get_text(strip=True) if seller_button else None
        data['Vendedor'] = seller

        # Extraemos la calificación promedio del producto
        rating = soup.find('span', {'aria-hidden': 'true', 'class': 'ui-pdp-review__rating'})
        data['Calificacion promedio'] = rating.get_text(strip=True) if rating else None

        # Extraemos la cantidad de calificaciones
        reviews_count = soup.find('span', {'aria-hidden': 'true', 'class': 'ui-pdp-review__amount'})
        data['Cantidad de Calificaciones'] = reviews_count.get_text(strip=True) if reviews_count else None

        # Extraemos la garantía del producto
        warranty = soup.find('p', class_='ui-pdp-family--REGULAR ui-pdp-media__title', string=lambda text: text and text.endswith('garant√≠a de f√°brica.'))
        data['Garantia'] = warranty.get_text(strip=True) if warranty else None

        # Extraemos la descripción del producto
        description = soup.find('p', class_='ui-pdp-description__content')
        data['Descripcion'] = description.get_text(strip=True) if description else None

        # Extraemos información de stock
        stock_info = soup.find('p', class_='ui-pdp-stock-information__title')
        data['Stock'] = stock_info.get_text(strip=True) if stock_info else None

        # Extraemos la cantidad total de opiniones
        total_opinions = soup.find('span', class_='total-opinion')
        data['Cantidad de Opiniones'] = total_opinions.get_text(strip=True) if total_opinions else None

        # Extraemos el número de publicación del producto
        publication_number = soup.find('span', class_='ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD')
        data['Numero de Publicacion'] = publication_number.get_text(strip=True) if publication_number else None

        # Agregamos la URL del producto al diccionario
        data['URL del Producto'] = url_producto

        # Retornamos el diccionario con los datos del producto
        return data
    except Exception as e:
        print(f"Error al procesar un producto: {e}")
        return {}

