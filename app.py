# main.py

# main.py en el directorio gcloud
import sys
import os

# Añadir el directorio src al path para poder importar desde allí
sys.path.append(os.path.join(os.path.dirname(__file__), './src'))

# Ahora podemos importar los módulos de scraping
from webscrapping.beautifulSoup.beautifulSoup import obtener_urls_productos, obtener_detalles_producto


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    busqueda = request.args.get('busqueda', 'portatil')  # Obtener la búsqueda desde los parámetros
    cantidad = int(request.args.get('cantidad', 1))  # Obtener la cantidad de productos

    try:
        urls_productos = obtener_urls_productos(busqueda, cantidad)
        resultados = []
        for url in urls_productos:
            detalles = obtener_detalles_producto(url)
            resultados.append(detalles)

        return jsonify(resultados)  # Retornar los resultados como JSON
    except Exception as e:
        return str(e), 500


#if __name__ == "__main__":
#   app.run(debug=True)
