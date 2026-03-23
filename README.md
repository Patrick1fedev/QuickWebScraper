# Quick Web Scraper

Este script extrae información de productos de cualquier página web y guarda los datos en un archivo CSV.

## Cómo usarlo:

1. Instala Python 3 y las librerías necesarias:
   pip install requests beautifulsoup4

2. Abre `scraper.py`

3. Cambia la variable `url` a la web que quieres scrapear

4. Ajusta los selectores `.product`, `.name`, `.price` según la estructura de la web

5. Ejecuta el script:
   python scraper.py

6. Obtén `products.csv` con los datos listos para usar