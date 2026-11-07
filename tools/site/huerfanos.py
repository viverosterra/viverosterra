"""CSS y scripts que quedan huérfanos al retirar el shell viejo (menú terra-nav, header del blog, pies, botón flotante).

Conservador a propósito: una regla se quita solo si TODOS los selectores de su lista apuntan a algo retirado, es decir,
una clase, id o elemento (header/footer/nav) que salió con el marcado viejo (o una clase de las familias terra-nav* y
wa-float) y que ya no aparece en ninguna parte del resto de la página, ni en el marcado ni en sus scripts. Un script se
quita solo si es una IIFE que sale de inmediato cuando no encuentra un elemento retirado. Los @keyframes que solo
usaban las reglas quitadas también se van, y un <style> que queda vacío se borra completo.
"""
import re

FAMILIA_RE = re.compile(r"\.((?:terra-nav(?:__[\w-]+)?|wa-float))(?![\w-])")
ELEMENTOS = ("header", "footer", "nav")
STYLE_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>[ \t]*\n?)", re.S | re.I)
SCRIPT_RE = re.compile(r"<script>(.*?)</script>[ \t]*\n?", re.S)
IIFE_GUARDA_RE = re.compile(
    r"\s*(?:/\*.*?\*/\s*|//[^\n]*\n\s*)*\(function\s*\(\)\s*\{\s*(?:'use strict';\s*)?var (\w+)\s*=\s*document\."
    r"(?:querySelector\(\s*'([^']+)'\s*\)|getElementById\(\s*'([^']+)'\s*\))\s*;\s*if\s*\(\s*!\1\s*\)\s*return;",
    re.S,
)
COMENTARIO_HTML_RE = re.compile(r"<!--.*?-->", re.S)
AGRUPADORES = ("@media", "@supports", "@layer", "@container")


# ---------- lectura de CSS: piezas de primer nivel ----------
def _saltar_comentario(css, i):
    fin = css.find("*/", i + 2)
    return len(css) if fin < 0 else fin + 2


def _fin_bloque(css, i):
    """Índice justo después de la llave que cierra la que abre en `i` (respeta cadenas y comentarios)."""
    nivel, cadena = 0, None
    while i < len(css):
        c = css[i]
        if cadena:
            if c == "\\":
                i += 1
            elif c == cadena:
                cadena = None
        elif css.startswith("/*", i):
            i = _saltar_comentario(css, i) - 1
        elif c in "'\"":
            cadena = c
        elif c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return i + 1
        i += 1
    return len(css)


def piezas(css):
    """Lista de (previo, preludio, cuerpo) de primer nivel y el resto final. `cuerpo` es None en sentencias con ';'."""
    salida, i = [], 0
    while True:
        inicio = i
        while i < len(css):
            if css[i].isspace():
                i += 1
            elif css.startswith("/*", i):
                i = _saltar_comentario(css, i)
            else:
                break
        if i >= len(css):
            return salida, css[inicio:]
        previo = css[inicio:i]
        j = i
        while j < len(css) and css[j] not in "{;":
            j = _saltar_comentario(css, j) if css.startswith("/*", j) else j + 1
        if j >= len(css):
            return salida, css[inicio:]
        if css[j] == ";":
            salida.append((previo, css[i:j + 1], None))
            i = j + 1
            continue
        fin = _fin_bloque(css, j)
        salida.append((previo, css[i:j], css[j + 1:fin - 1]))
        i = fin


def _solo_comentarios(css):
    return not re.sub(r"/\*.*?\*/", "", css, flags=re.S).strip()


def _selectores(preludio):
    partes, nivel, actual = [], 0, ""
    for c in preludio:
        if c == "," and nivel == 0:
            partes.append(actual)
            actual = ""
            continue
        nivel += c == "("
        nivel -= c == ")"
        actual += c
    return [p.strip() for p in partes + [actual] if p.strip()]


def _tokens(selector):
    """Clases, ids y elementos de un selector, sin contar lo que va dentro de :not() ni de [atributos]."""
    s = re.sub(r":not\([^()]*\)", "", selector)
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"::?[\w-]+(?:\([^()]*\))?", "", s)
    clases = set(re.findall(r"\.([\w-]+)", s))
    ids = set(re.findall(r"#([\w-]+)", s))
    elementos = {t.lower() for t in re.findall(r"(?:^|[\s>+~])([a-zA-Z][\w-]*)", s)}
    return clases, ids, elementos


class _Huerfanos:
    def __init__(self, clases, ids, elementos):
        self.clases, self.ids, self.elementos = clases, ids, elementos

    def selector(self, selector):
        clases, ids, elementos = _tokens(selector)
        return bool(clases & self.clases or ids & self.ids or elementos & self.elementos)

    def regla(self, preludio):
        selectores = _selectores(preludio)
        return bool(selectores) and all(self.selector(s) for s in selectores)


def _animaciones(cuerpo):
    nombres = set()
    for valor in re.findall(r"animation(?:-name)?\s*:\s*([^;}]+)", cuerpo):
        nombres |= set(re.findall(r"[A-Za-z_][\w-]*", valor))
    return nombres


def _filtrar(css, huerfanos, cuenta, animaciones):
    """CSS sin las reglas huérfanas (recorre @media y similares; quita los que quedan vacíos)."""
    lista, resto = piezas(css)
    salida = []
    for previo, preludio, cuerpo in lista:
        cabeza = preludio.strip().lower()
        if cuerpo is not None and cabeza.startswith(AGRUPADORES):
            nuevo = _filtrar(cuerpo, huerfanos, cuenta, animaciones)
            if _solo_comentarios(nuevo):
                continue
            salida.append(f"{previo}{preludio}{{{nuevo}}}")
        elif cuerpo is not None and not cabeza.startswith("@") and huerfanos.regla(preludio):
            cuenta["reglas"] += 1
            animaciones |= _animaciones(cuerpo)
        else:
            salida.append(previo + preludio + ("" if cuerpo is None else f"{{{cuerpo}}}"))
    return "".join(salida) + resto


def _sin_keyframes(css, nombres, cuenta):
    lista, resto = piezas(css)
    salida = []
    for previo, preludio, cuerpo in lista:
        m = re.match(r"@(?:-webkit-)?keyframes\s+([\w-]+)", preludio.strip())
        if cuerpo is not None and m and m.group(1) in nombres:
            cuenta["keyframes"] += 1
            continue
        salida.append(previo + preludio + ("" if cuerpo is None else f"{{{cuerpo}}}"))
    return "".join(salida) + resto


# ---------- presencia en el resto de la página ----------
def _presente(nombre, texto):
    return re.search(rf"(?<![\w-]){re.escape(nombre)}(?![\w-])", texto) is not None


def _scripts_con_guarda(html):
    """(match, selector) de cada IIFE que sale si no encuentra su elemento."""
    salida = []
    for m in SCRIPT_RE.finditer(html):
        g = IIFE_GUARDA_RE.match(m.group(1))
        if g and m.group(1).rstrip().endswith(("})();", "})()")):
            salida.append((m, g.group(2) or f"#{g.group(3)}"))
    return salida


def _candidatos(html, quitados):
    clases, ids, elementos = set(), set(), set()
    for fragmento in quitados:
        for valor in re.findall(r'\bclass="([^"]*)"', fragmento):
            clases |= set(valor.split())
        ids |= set(re.findall(r'\bid="([^"]+)"', fragmento))
        elementos |= {e for e in ELEMENTOS if re.search(rf"<{e}\b", fragmento, re.I)}
    clases |= set(FAMILIA_RE.findall(html))
    return clases, ids, elementos


def limpiar(html, quitados):
    """Página sin el CSS ni los scripts que solo servían al marcado retirado. Devuelve (html, cuenta)."""
    cuenta = {"reglas": 0, "keyframes": 0, "bloques": 0, "scripts": 0}
    guardas = _scripts_con_guarda(html)
    resto = STYLE_RE.sub("", html)
    for m, _ in guardas:
        resto = resto.replace(m.group(0), "")
    resto = COMENTARIO_HTML_RE.sub("", resto)
    clases, ids, elementos = _candidatos(html, quitados)
    huerfanos = _Huerfanos(
        {c for c in clases if not _presente(c, resto)},
        {i for i in ids if not _presente(i, resto)},
        {e for e in elementos if not re.search(rf"<{e}\b", resto, re.I)},
    )
    for m, selector in reversed(guardas):
        if huerfanos.selector(selector):
            html = html[:m.start()] + html[m.end():]
            cuenta["scripts"] += 1

    animaciones = set()
    html = STYLE_RE.sub(lambda m: m.group(1) + _filtrar(m.group(2), huerfanos, cuenta, animaciones) + m.group(3), html)
    sin_definiciones = re.sub(r"@(?:-webkit-)?keyframes\s+[\w-]+", "", html)
    sin_uso = {n for n in animaciones if not _presente(n, sin_definiciones)}
    if sin_uso:
        html = STYLE_RE.sub(lambda m: m.group(1) + _sin_keyframes(m.group(2), sin_uso, cuenta) + m.group(3), html)

    def _vaciar(m):
        if _solo_comentarios(m.group(2)):
            cuenta["bloques"] += 1
            return ""
        return m.group(0)

    return STYLE_RE.sub(_vaciar, html), cuenta
