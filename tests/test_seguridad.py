import pytest
import os
import re
from playwright.sync_api import Page, expect
from pages.exportar_page import ExportarPage

# PRUEBA RNF-03: Límite de longitud (ReDoS) en Palabras Clave
def test_limite_longitud_palabras_clave(page: Page):
    exportar = ExportarPage(page)
    exportar.navegar()
    
    # Intentar escribir 2100 caracteres (el límite según el documento es 2000)
    texto_largo = "a" * 2100
    exportar.input_palabras.fill(texto_largo)
    
    # Verificar que el input solo tenga hasta 2000 caracteres
    valor_actual = exportar.input_palabras.input_value()
    assert len(valor_actual) <= 2000, f"Fallo RNF-03: Se permitieron {len(valor_actual)} caracteres."

# PRUEBA RNF-04: Prevención de XSS
def test_mitigacion_xss(page: Page):
    alert_fired = False
    def handle_dialog(dialog):
        nonlocal alert_fired
        alert_fired = True
        dialog.dismiss()
        
    page.on("dialog", handle_dialog)
    
    exportar = ExportarPage(page)
    exportar.navegar()
    
    # Inyectar script malicioso
    exportar.input_palabras.fill('<script>alert("XSS")</script>')
    exportar.consultar()
    
    page.wait_for_timeout(3000) # Esperar 3 segundos para ver si salta la alerta
    
    # Verificar que el script NO se ejecutó
    assert alert_fired is False, "Fallo RNF-04: ¡Se ejecutó un script XSS!"

# PRUEBA RNF-02: Neutralización de Inyección CSV
def test_inyeccion_csv(page: Page):
    exportar = ExportarPage(page)
    exportar.navegar()
    
    exportar.llenar_filtros("Artificial Intelligence", "2020", "2023", "artículo")
    exportar.consultar()
    
    # Esperamos a que el contador se actualice antes de descargar
    expect(exportar.contador_registros).to_be_visible(timeout=15000)

    # Descargar CSV
    with page.expect_download() as download_info:
        exportar.btn_descargar_csv.click()
    download = download_info.value
    
    # Guardar en la carpeta temporal de pytest
    csv_path = "test_inyeccion.csv"
    download.save_as(csv_path)
    
    # Leer el archivo (usando utf-8-sig por el BOM que menciona el documento)
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        contenido = f.read()
        
    # Buscar si hay celdas maliciosas sin neutralizar
    lineas = contenido.split("\n")
    for linea in lineas:
        # Si la línea empieza estrictamente con =, +, - o @ (sin el apóstrofe de protección)
        if re.match(r'^[=+\-@]', linea):
            pytest.fail(f"Fallo RNF-02: Inyección CSV detectada: {linea}")
            
    print("\nRNF-02 superado: El CSV está protegido.")
    
    # Limpieza: borrar el archivo después de la prueba
    if os.path.exists(csv_path):
        os.remove(csv_path)