"""Servidor HTTP local de public/ (127.0.0.1, puerto libre) para las pruebas de navegador y las capturas."""
import functools
import http.server
import json
import threading

import paginas


VERCEL = paginas.PUBLIC.parent / "vercel.json"


def cabeceras_globales(vercel=VERCEL):
    """Cabeceras de vercel.json que aplican a todas las rutas ("/(.*)"), para que el navegador local vea la misma CSP."""
    cfg = json.loads(vercel.read_text(encoding="utf-8"))
    return {h["key"]: h["value"] for r in cfg.get("headers", []) if r["source"] == "/(.*)" for h in r["headers"]}


class _Silencioso(http.server.SimpleHTTPRequestHandler):
    cabeceras = {}

    def end_headers(self):
        for clave, valor in self.cabeceras.items():
            self.send_header(clave, valor)
        super().end_headers()

    def log_message(self, *args):
        pass


def iniciar(public=paginas.PUBLIC):
    """Arranca el servidor en un hilo; devuelve (url_base, servidor). Al terminar: shutdown() y server_close()."""
    clase = type("_ConCabeceras", (_Silencioso,), {"cabeceras": cabeceras_globales()})
    manejador = functools.partial(clase, directory=str(public))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{servidor.server_address[1]}", servidor


def url_de(path, public=paginas.PUBLIC):
    """URL local de un archivo de public/ (las carpetas con index.html terminan en /)."""
    rel = path.relative_to(public).as_posix()
    return "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
