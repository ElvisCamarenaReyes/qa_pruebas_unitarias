import pytest
import re
from playwright.sync_api import Page, expect
from pages.exportar_page import ExportarPage
import os # Ponlo arriba del archivo con los otros imports

def test_flujo_completo_descarga(page: Page):
    exportar = ExportarPage(page)
    exportar.navegar()
    exportar.llenar_filtros("Artificial Intelligence", "2020", "2023", "articulo")
    exportar.consultar()
    
    # Esperamos a que el contador deje de ser un guion "-"
    expect(exportar.contador_registros).not_to_have_text("-", timeout=15000)
    
    # Extraemos el número
    texto_contador = exportar.contador_registros.inner_text()
    print(f"\nTotal de registros encontrados: {texto_contador}")
    
    # Validar que es un número mayor a 0
    assert int(texto_contador) > 0, "El contador no muestra un número válido o es 0"
    
    
def test_descarga_archivos(page: Page):
    exportar = ExportarPage(page)
    exportar.navegar()
    exportar.llenar_filtros("Artificial Intelligence", "2020", "2023", "articulo")
    exportar.consultar()
    
    # Esperar que cargue el contador
    expect(exportar.contador_registros).not_to_have_text("-", timeout=15000)

    # 1. Probar Descarga JSON
    with page.expect_download() as download_info_json:
        exportar.btn_descargar_json.click()
    download_json = download_info_json.value
    
    json_path = "export.json"
    download_json.save_as(json_path)
    assert os.path.getsize(json_path) > 0, "El archivo JSON está vacío"
    print("\nRF-03: Descarga JSON exitosa")

    # 2. Probar Descarga CSV
    with page.expect_download() as download_info_csv:
        exportar.btn_descargar_csv.click()
    download_csv = download_info_csv.value
    
    csv_path = "export.csv"
    download_csv.save_as(csv_path)
    assert os.path.getsize(csv_path) > 0, "El archivo CSV está vacío"
    print("RF-03: Descarga CSV exitosa")
    
    # Limpieza
    os.remove(json_path)
    os.remove(csv_path)