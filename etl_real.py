from bs4 import BeautifulSoup
from database import SessionLocal
from models import Propiedad, Precio
import re


def limpiar_precio(texto_precio):
    "clean the input "
    if not texto_precio:
        return 0.0

    # Regex
    numeros = re.findall(r'\d+', texto_precio)
    if not numeros:
        return 0.0

    # Join the numbers and apply float
    precio_limpio = "".join(numeros)
    return float(precio_limpio)


def procesar_html_real():
    print("Iniciando extracción profunda del archivo local...")
    db = SessionLocal()

    try:
        with open("pagina.html", "r", encoding="utf-8") as file:
            html = file.read()
    except FileNotFoundError:
        print("No se encontró el archivo 'pagina_prueba.html'.")
        return

    soup = BeautifulSoup(html, 'html.parser')

    tarjetas = soup.find_all('section', class_="pcom-property-card")

    print(f"Buscando... Encontramos {len(tarjetas)} posibles tarjetas HTML.")

    casas_guardadas = 0

    for card in tarjetas:
        try:
            elemento_titulo = card.find('div', class_="sc-4eeee890-0 jMZElt")
            titulo = elemento_titulo.text.strip() if elemento_titulo else "Sin título"

            elemento_precio = card.find('div', class_="sc-c1af3d6f-2 bxbIOz")
            texto_precio = elemento_precio.text.strip() if elemento_precio else "0"
            precio_final = limpiar_precio(texto_precio)

            elemento_link = card.find('a')
            url_parcial = elemento_link[
                'href'] if elemento_link and 'href' in elemento_link.attrs else f"url-aleatoria-{casas_guardadas}"

            url_completa = url_parcial if url_parcial.startswith("http") else f"https://propiedades.com{url_parcial}"

            propiedad_existente = db.query(Propiedad).filter_by(url_origen=url_completa).first()

            if not propiedad_existente:
                nueva_prop = Propiedad(
                    titulo=titulo,
                    url_origen=url_completa,
                    colonia="Zapopan",  # Podrías extraer esto también
                    municipio="Zapopan"
                )
                db.add(nueva_prop)
                db.commit()
                db.refresh(nueva_prop)
                id_propiedad = nueva_prop.id
            else:
                id_propiedad = propiedad_existente.id

            nuevo_precio_db = Precio(propiedad_id=id_propiedad, precio=precio_final)
            db.add(nuevo_precio_db)
            db.commit()

            casas_guardadas += 1
            print(f"{titulo[:30]}... | ${precio_final}")

        except Exception as e:
            print(f"⚠️ Error al procesar una tarjeta: {e}")
            continue

    db.close()
    print(f"\nProceso terminado. Se guardaron {casas_guardadas} propiedades en la Base de Datos.")


if __name__ == "__main__":
    procesar_html_real()