import requests
from bs4 import BeautifulSoup
import csv

# CAMBIA ESTA URL POR LA DEL CLIENTE
url = "https://example.com/products"

# Hacer request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Lista de productos (ajusta los selectores según la web)
products = []
for item in soup.select(".product"):  # Cambia '.product' por la clase correcta
    name = item.select_one(".name").text.strip()  # Cambia '.name'
    price = item.select_one(".price").text.strip()  # Cambia '.price'
    products.append([name, price])

# Guardar en CSV
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Price"])
    writer.writerows(products)

print("Scraping completo! CSV generado: products.csv")