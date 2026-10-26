# Automatización QA - Exportación PerúCRIS

Este proyecto contiene las pruebas automatizadas (E2E) para el submódulo de Exportación de publicaciones científicas de PerúCRIS, desarrollado con **Python**, **Playwright** y **Pytest**.

## Estructura del Proyecto

- `pages/`: Contiene el Page Object Model (`exportar_page.py`) con los selectores robustos de la página.
- `tests/`: Contiene las pruebas divididas en funcionales (`test_funcionales.py`) y de seguridad (`test_seguridad.py`).
- `pytest.ini`: Configuración del entorno de ejecución de Playwright.

## Cobertura de Pruebas

1. **Requisitos Funcionales (RF):**
   - `test_flujo_completo_descarga`: Valida filtros y contador (RF-01, RF-02).
   - `test_descarga_archivos`: Valida exportación en CSV y JSON (RF-03).
2. **Requisitos No Funcionales / Seguridad (RNF):**
   - `test_limite_longitud_palabras_clave`: Mitigación ReDoS (RNF-03).
   - `test_mitigacion_xss`: Mitigación de XSS (RNF-04).
   - `test_inyeccion_csv`: Mitigación de Inyección de fórmulas (RNF-02).

## ¿Cómo ejecutar las pruebas?

1. Activar el entorno virtual:
   - Windows: `.venv\Scripts\activate`
2. Ejecutar Pytest:
   ```bash
   pytest -v
   ```
