"""Capturas de verificación: 10 páginas a 320, 375, 768 y 1440 px (página completa) y reporte de
desbordamiento horizontal. El desbordamiento del cuerpo viejo se anota para la Etapa 2; el del shell no se acepta.

Uso: python3 tools/site/capturas.py <carpeta-de-salida>
Requiere Playwright: python3 -m pip install playwright==1.48.0 && python3 -m playwright install chromium
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import servidor  # noqa: E402

PAGINAS = ("/", "/pasto-en-rollo-tampico/", "/pasto-sintetico/", "/pasto-sintetico/toscana-28/",
           "/diseno-jardines-tampico/", "/plantas-palmas-arboles-tampico/", "/catalogo.html", "/blog/",
           "/blog/cuando-regar-pasto-san-agustin-tampico/", "/precios/")
ANCHOS = (320, 375, 768, 1440)
# Desbordes conocidos del cuerpo viejo (no del shell, que test_navegador cubre): se anotan, no se esconden.
# Baja la página de a una pantalla para que carguen las imágenes lazy y vuelve arriba (si no, la captura de página
# completa las deja vacías).
CARGAR_LAZY = """async () => {
  for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) {
    scrollTo(0, y); await new Promise((r) => setTimeout(r, 60));
  }
  scrollTo(0, 0);
  const cargas = Array.from(document.images).map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }));
  await Promise.race([Promise.all(cargas), new Promise((r) => setTimeout(r, 3000))]);  // las ocultas nunca cargan
}"""
CONOCIDOS = {
    "/pasto-sintetico/": "fila de chips de filtro de la tienda a 320 px (Etapa 2)",
}


def nombre_archivo(ruta, ancho):
    limpio = ruta.strip("/").replace("/", "_").replace(".html", "") or "inicio"
    return f"{limpio}-{ancho}.png"


def main(salida):
    from playwright.sync_api import sync_playwright

    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    base, srv = servidor.iniciar()
    desbordes = []
    try:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            for ancho in ANCHOS:
                contexto = navegador.new_context(viewport={"width": ancho, "height": 900})
                contexto.route("**/*", lambda route: route.continue_()
                               if route.request.url.startswith(base) and "/api/" not in route.request.url
                               else route.abort())
                page = contexto.new_page()
                for ruta in PAGINAS:
                    page.goto(base + ruta, wait_until="load")
                    page.evaluate(CARGAR_LAZY)
                    page.screenshot(path=str(salida / nombre_archivo(ruta, ancho)), full_page=True)
                    sobra = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    if sobra > 1:
                        nota = f" · conocido: {CONOCIDOS[ruta]}" if ruta in CONOCIDOS else ""
                        desbordes.append(f"{ruta} a {ancho}px: {sobra}px de más{nota}")
                contexto.close()
            navegador.close()
    finally:
        srv.shutdown()
        srv.server_close()
    print(f"{len(PAGINAS) * len(ANCHOS)} capturas en {salida}")
    print("desbordamiento horizontal:" if desbordes else "sin desbordamiento horizontal")
    for linea in desbordes:
        print(" -", linea)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 tools/site/capturas.py <carpeta-de-salida>")
    main(sys.argv[1])
