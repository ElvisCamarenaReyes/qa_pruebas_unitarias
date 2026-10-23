from playwright.sync_api import Page
import re

class ExportarPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.perucris.pe/exportar"
        
        # --- SELECTORES ROBUSTOS Y ESTABLES ---
        # Usamos atributos específicos encontrados en el HTML inspeccionado
        self.input_palabras = page.locator("textarea[maxlength='2000']")
        
        # Usamos los placeholders, que son únicos para cada año
        self.input_anio_inicio = page.locator("input[placeholder='Ej: 2024']")
        self.input_anio_fin = page.locator("input[placeholder='Ej: 2025']")
        
        # El tipo de ítem es el único input de texto con maxlength 150
        self.input_tipo_item = page.locator("input[maxlength='150']")
        
        # Botones
        self.btn_consultar = page.get_by_role("button", name="Consultar", exact=False)
        self.btn_descargar_json = page.get_by_role("button", name="DESCARGAR JSON", exact=False)
        self.btn_descargar_csv = page.get_by_role("button", name="DESCARGAR CSV", exact=False)
        
        # El contador
        self.contador_registros = page.get_by_text("TOTAL DE REGISTROS ENCONTRADOS").locator("..").locator("h3,h2, span, div").filter(has_text=re.compile(r"^\d+$")).first

    def navegar(self):
        self.page.goto(self.url, wait_until="networkidle")
        
        # Cerrar banner de cookies
        try:
            btn_cookies = self.page.get_by_role("button", name="Descartar todas")
            if btn_cookies.is_visible(timeout=3000):
                btn_cookies.click()
                self.page.wait_for_timeout(500) 
        except Exception:
            pass 

    def llenar_filtros(self, palabras, anio_inicio, anio_fin, tipo_item):
        self.input_palabras.fill(palabras)
        self.input_anio_inicio.fill(str(anio_inicio))
        self.input_anio_fin.fill(str(anio_fin))
        self.input_tipo_item.fill(tipo_item)

    def consultar(self):
        self.btn_consultar.click()