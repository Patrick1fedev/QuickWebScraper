import requests
from bs4 import BeautifulSoup
import csv
import os
from requests.exceptions import RequestException, Timeout, ConnectionError

def extract_product_data(url):
    """Extrae datos de productos de una URL"""
    products = []
    
    # Manejo de errores de red
    try:
        print(f"Conectando a {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Timeout:
        print(f"Error: Tiempo de espera agotado al conectar a {url}")
        return None
    except ConnectionError:
        print(f"Error: No se pudo conectar a {url}")
        return None
    except RequestException as e:
        print(f"Error de red: {e}")
        return None
    
    # Procesar contenido
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all(["div", "li", "article"])
    
    for item in items[:100]:  # Limitar a los primeros 100 items para evitar sobrecarga
        text = item.get_text(strip=True)
        if len(text) > 30 and any(char.isdigit() for char in text):
            # Extraer más información útil
            price = item.find(class_=["price", "precio"])
            name = item.find(class_=["name", "title", "product-name"])
            
            product_data = [
                text[:100],  # Descripción corta
                price.get_text(strip=True) if price else "No price",
                name.get_text(strip=True) if name else "No name"
            ]
            products.append(product_data)
    
    return products

def save_to_csv(products, filename="data.csv"):
    """Guarda los datos en CSV con manejo de errores"""
    if not products:
        print("No hay datos para guardar")
        return False
    
    try:
        # Verificar si podemos escribir en el directorio
        current_dir = os.getcwd()
        test_file = os.path.join(current_dir, "test_write.tmp")
        
        # Probar permisos de escritura
        try:
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except IOError as e:
            print(f"No se puede escribir en {current_dir}: {e}")
            return False
        
        # Guardar datos
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Extracted Data", "Price", "Name"])
            writer.writerows(products)
        
        print(f"Datos guardados en {filename}")
        print(f"Total de items extraídos: {len(products)}")
        
        # Mostrar información del archivo
        file_size = os.path.getsize(filename)
        print(f"Tamaño del archivo: {file_size} bytes")
        
        return True
        
    except PermissionError:
        print(f"Error: Permiso denegado para escribir {filename}")
        print("Sugerencia: Intenta guardar en otra ubicación")
        return False
    except OSError as e:
        print(f"Error del sistema al guardar archivo: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al guardar: {e}")
        return False

def main():
    """Función principal con manejo de errores"""
    print("=== Web Scraper de Productos ===")
    
    # Obtener URL con validación básica
    while True:
        url = input("Enter the website URL: ").strip()
        if url:
            if url.startswith(("http://", "https://")):
                break
            else:
                print("La URL debe comenzar con http:// o https://")
        else:
            print("Por favor ingresa una URL válida")
    
    # Extraer datos
    products = extract_product_data(url)
    
    if products is None:
        print("No se pudo completar la extracción")
        return
    
    if not products:
        print("No se encontraron productos en la página")
        return
    
    if len(products) < 5:
        print("Advertencia: pocos datos encontrados, la página puede requerir ajustes específicos")
    
    # Preguntar nombre del archivo
    filename = input(f"Nombre del archivo CSV (default: data.csv): ").strip()
    if not filename:
        filename = "data.csv"
    elif not filename.endswith(".csv"):
        filename += ".csv"
    
    # Guardar datos
    save_to_csv(products, filename)

if __name__ == "__main__":
    main()