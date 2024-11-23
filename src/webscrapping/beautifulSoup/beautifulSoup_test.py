import unittest
import requests_mock
# Cambia 'your_script_name' por el nombre de tu archivo
from beautifulSoup import obtener_urls_productos, obtener_detalles_producto


class TestScraper(unittest.TestCase):

    @requests_mock.Mocker()
    def test_obtener_urls_productos(self, mocker):
        # Simula una respuesta de búsqueda en MercadoLibre
        html_content = """
        <html>
            <body>
                <ul>
                    <li class="ui-search-layout__item">
                        <a href="https://example.com/producto1"></a>
                    </li>
                    <li class="ui-search-layout__item">
                        <a href="https://example.com/producto2"></a>
                    </li>
                </ul>
            </body>
        </html>
        """
        mocker.get("https://listado.mercadolibre.com.co/portatil", text=html_content)

        urls = obtener_urls_productos("portatil")
        self.assertEqual(len(urls), 2)
        self.assertIn("https://example.com/producto1", urls)
        self.assertIn("https://example.com/producto2", urls)

    @requests_mock.Mocker()
    def test_obtener_detalles_producto(self, mocker):
        # Simula una respuesta de detalles del producto
        html_content = """
        <html>
            <body>
                <h1 class="ui-pdp-title">Producto de prueba</h1>
                <div class="ui-pdp-breadcrumb">Categoría de prueba</div>
                <div class="ui-pdp-price__second-line">
                    <span class="andes-money-amount__fraction">50000</span>
                </div>
            </body>
        </html>
        """
        mocker.get("https://example.com/producto1", text=html_content)

        detalles = obtener_detalles_producto("https://example.com/producto1")
        self.assertEqual(detalles["Titulo"], "Producto de prueba")
        self.assertEqual(detalles["Categoria"], "Categoría de prueba")
        self.assertEqual(detalles["Precio"], "50000")


if __name__ == '__main__':
    unittest.main()
