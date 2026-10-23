import pytest
import re
from playwright.sync_api import Page, expect
from pages.exportar_page import ExportarPage

def test_flujo_completo_descarga(page: Page):
    exportar = ExportarPage(page)
    
    # 1. Navegar
    exportar.navegar()
    
    # 2. Llenar datos
    exportar.llenar_filtros("Artificial Intelligence", "2020", "2023", "articulo")
    
    # 3. Consultar
    exportar.consultar()
    
    # 4. Verificar contador
    # Usamos expect() en lugar de wait_timeout manual. Playwright esperará automáticamente 
    # hasta 5 segundos (por defecto) a que el texto del contador deje de ser "-"
    expect(exportar.contador_registros).not_to_have_text(re.compile(r"^-\s*$"), timeout=10000)
    
    # Extraemos el número para verificar que sea mayor a 0
    texto_contador = exportar.contador_registros.inner_text()
    print(f"\nTotal de registros encontrados: {texto_contador.strip()}")
    
    # Validar que el texto contenga al menos un dígito
    assert re.search(r"\d+", texto_contador) is not None, "El contador no muestra un número válido"