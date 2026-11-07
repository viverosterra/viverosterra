"""Servidor HTTP local de public/ (127.0.0.1, puerto libre) para las pruebas de navegador y las capturas."""
import functools
import http.server
import threading

import paginas


class _Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def iniciar(public=paginas.PUBLIC):
    """Arranca el servidor en un hilo; devuelve (url_base, servidor). Al terminar: shutdown() y server_close()."""
    manejador = functools.partial(_Silencioso, directory=str(public))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{servidor.server_address[1]}", servidor


def url_de(path, public=paginas.PUBLIC):
    """URL local de un archivo de public/ (las carpetas con index.html terminan en /)."""
    rel = path.relative_to(public).as_posix()
    return "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
