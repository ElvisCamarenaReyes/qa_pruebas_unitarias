from playwright.sync_api import Page

class ExportarPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.perucris.pe/exportar"
        
        # --- SELECTORES DE ENTRADA ---
        self.input_palabras = page.locator("textarea[maxlength='2000']")
        self.input_anio_inicio = page.locator("input[placeholder='Ej: 2024']")
        self.input_anio_fin = page.locator("input[placeholder='Ej: 2025']")
        self.input_tipo_item = page.locator("input[maxlength='150']")
        
        # --- BOTONES ---
        self.btn_consultar = page.get_by_role("button", name="Consultar", exact=False)
        self.btn_descargar_json = page.get_by_role("button", name="DESCARGAR JSON", exact=False)
        self.btn_descargar_csv = page.get_by_role("button", name="DESCARGAR CSV", exact=False)
        
        # --- CONTADOR (LA SOLUCIÓN DEFINITIVA) ---
        # Busca el texto "Total de registros encontrados" y luego selecciona el <h1> que está a su lado.
        # El texto en el HTML real está en minúsculas y mezclado, usamos regex para no fallar.
        self.contador_registros = page.locator("xpath=//h6[contains(translate(text(), 'TOTAL DE REGISTROS ENCONTRADOS', 'total de registros encontrados'), 'total de registros encontrados')]/following-sibling::h1")

    def navegar(self):
        self.page.goto(self.url, wait_until="networkidle")
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