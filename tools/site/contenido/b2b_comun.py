"""Piezas comunes de las páginas para empresas (Etapa 2d): documentación para compras, dos preguntas de compras, los
sectores, la cobertura y las páginas B2B que se enlazan entre sí. Las usan contenido/mayoreo_pasto.py y
contenido/palmas_proyectos.py; la página /empresas de la Etapa 3 (spec §3.1 y §3.5) tomará de aquí su índice
(PAGINAS) sin repetir textos. Mientras /empresas no exista, ninguna página la enlaza (test_b2b.py lo prueba).
Solo datos de datos.py: ninguna escala, capacidad ni plazo que el dueño no haya dado."""
import datos
from componentes import dinero

P = datos.PRECIOS
OBRA = "/img/obra"
MINIMO = P["pasto_mayoreo_minimo_m2"]
PADRON = f'<a href="{datos.REPSE_PADRON}" target="_blank" rel="noopener">padrón público de la STPS</a>'

DOCUMENTACION = (
    {"titulo": f"Factura {datos.FACTURA}",
     "texto": "Para persona física o moral, emitida el día del pago. Solo necesitamos tu RFC y tus datos fiscales."},
    {"titulo": f"REPSE {datos.REPSE}",
     "texto": f"Registro de la STPS para prestar servicios especializados a empresas. Consulta el folio en el {PADRON}."},
    {"titulo": "Anticipo y avances de obra",
     "texto": ("Confirmas con un anticipo; los pagos siguientes se acuerdan contra avances de obra y quedan por escrito "
               "en la cotización.")},
    {"titulo": "Entregas por etapas",
     "texto": "Un pedido global con entregas parciales en las fechas que tu obra necesita, para que cada entrega llegue fresca."},
)
PREGUNTA_PAGO = ("¿Cómo se paga un proyecto?",
                 f"{datos.ANTICIPO_PROYECTOS} Cada pago lleva su factura {datos.FACTURA}.")
PREGUNTA_REPSE = ("¿Están dados de alta en el REPSE?",
                  f"Sí: REPSE {datos.REPSE}, el registro de la STPS para prestar servicios especializados a empresas. "
                  f"Puedes consultar el folio en el {PADRON}.")
SECTORES = (
    ("Constructoras y desarrolladoras", "Fraccionamientos, vivienda y casa muestra"),
    ("Arquitectos y paisajistas", "Proyectos con especificación"),
    ("Hoteles y comercios", "Áreas verdes de imagen"),
    ("Industria", "Parques industriales y áreas perimetrales"),
    ("Gobierno", "Parques y áreas públicas"),
)
COBERTURA = {
    "zonas": datos.ZONAS, "por_proyecto": datos.ZONAS_POR_PROYECTO, "sectores": SECTORES,
}
PAGINAS = (
    {"titulo": "Mayoreo de pasto", "href": "/mayoreo-pasto-tampico",
     "img": f"{OBRA}/rollos-pasto-san-agustin-camioneta.webp", "ancho": 900, "alto": 1111,
     "texto": f"San Agustín desde {dinero(P['pasto_mayoreo_m2'])}/m² en pedidos de {MINIMO} m² o más · entregas por etapas"},
    {"titulo": "Palmas para proyectos", "href": "/palmas-mayoreo-proyectos",
     "img": f"{OBRA}/palmas-en-costal-vivero.webp", "ancho": 640, "alto": 961,
     "texto": (f"Areca y coco plumoso desde {dinero(P['palma_desde'])} y palma real desde {dinero(P['palma_real'])} en "
               "tamaño chico")},
    {"titulo": "Mantenimiento de áreas verdes", "href": "/mantenimiento-jardines-tampico",
     "img": f"{OBRA}/mantenimiento-areas-verdes-empresa.webp", "ancho": 640, "alto": 961,
     "texto": f"Empresas, fraccionamientos e industria · REPSE {datos.REPSE} y factura {datos.FACTURA}"},
    {"titulo": "Riego para grandes áreas", "href": "/sistema-riego-tampico",
     "img": f"{OBRA}/riego-tecnico-sistema-industrial.webp", "ancho": 960, "alto": 640,
     "texto": "Parques industriales, escuelas y campos deportivos con pasto natural"},
)


def relacionados(excepto):
    """Las otras páginas para empresas (la propia no se enlaza)."""
    return tuple(p for p in PAGINAS if p["href"] != excepto)
