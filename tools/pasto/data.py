"""Catálogo de pasto sintético de Viveros Terra.

Fuente única de verdad para el hub /pasto-sintetico y las 9 fichas.
Datos técnicos: fichas del fabricante (Toscana 18, Toscana 28R, Capri 20,
Irlanda 25, Viena 30, Bali 35). Aruba 10, Japonés 35 y Mónaco 35 solo
tienen datos principales publicados. Nunca mencionar al fabricante.
"""

SITE = "https://www.viverosterra.com"
WA_NUMBER = "528333268008"
PHONE_DISPLAY = "833 326 8008"
UPDATED = "septiembre 2026"
ASSET_VERSION = "20260923"

ZONAS = {"A": 900, "B": 1150, "C": 1400}

COMMON_TREATMENTS = "UV, antibacterial, retardante al fuego"

USO_FILTERS = [
    ("todos", "Todos"),
    ("mascotas", "Niños y mascotas"),
    ("terraza", "Terraza y balcón"),
    ("precio", "Mejor precio"),
    ("intenso", "Uso intenso"),
    ("realismo", "Máximo realismo"),
]


def _full_specs(*, altura, peso, fibra_peso, puntadas, puntadas10, color,
                dtex1, espesor1, ancho1, dtex2, temp2, temp2_label,
                capa1, capa2, normas):
    """Ficha técnica completa en grupos, tal como la publica el fabricante."""
    return [
        ("Césped", [
            ("Altura", "ISO 2549", f"{altura} mm ± 1"),
            ("Peso total", "", f"{peso} g/m²"),
            ("Peso de la fibra", "ISO 2549", f"{fibra_peso} g/m²"),
            ("Puntadas por m²", "ISO 1763", f"{puntadas} ± 100"),
            ("Puntadas por 10 cm", "", f"{puntadas10} ± 1"),
            ("Hilos por mechón", "", "6"),
            ("Gauge", "ASTM D5793", "3/8″"),
            ("Color", "", color),
        ]),
        ("Fibra principal", [
            ("Estructura", "", "Monofilamento"),
            ("Material", "ISO 11357", "Polietileno (PE)"),
            ("Dtex", "ASTM D1907", dtex1),
            ("Espesor", "ASTM D3218", espesor1),
            ("Ancho", "", ancho1),
            ("Resistencia UV", "EN ISO 20105", "Escala de gris 4 a 5"),
            ("Prueba de quemadura", "ASTM D2859", "Aprobada"),
        ]),
        ("Fibra de soporte", [
            ("Estructura", "", "Monofilamento"),
            ("Material", "", "Polipropileno (PP)"),
            ("Dtex", "", dtex2),
            (temp2_label, "", temp2),
        ]),
        ("Base y rollo", [
            ("Capa 1", "ASTM D5848", capa1),
            ("Capa 2", "ASTM D5848", capa2),
            ("Medida del rollo", "", "2 × 25 m, 50 m²"),
            ("Uso", "", "Residencial"),
            ("Tratamientos", "", COMMON_TREATMENTS),
            ("Normas", "", normas),
        ]),
    ]


def _basic_specs(*, altura, peso, color, garantia):
    rows = [
        ("Altura", "", f"{altura} mm"),
        ("Peso total", "", f"{peso} g/m²"),
        ("Color", "", color),
        ("Medida del rollo", "", "2 × 25 m, 50 m²"),
        ("Uso", "", "Residencial"),
        ("Tratamientos", "", COMMON_TREATMENTS),
    ]
    if garantia:
        rows.append(("Garantía", "", f"{garantia} años"))
    return [("Datos principales", rows)]


MODELOS = [
    {
        "slug": "aruba-10", "id": "aruba10", "nombre": "Aruba 10", "n": 1,
        "mm": 10, "peso": "1,050", "peso_num": 1050, "garantia": "3 a 5",
        "color": "Verde olivo", "tag": "Decorativo", "stock": False,
        "t1": 189, "t2": 159, "rollo": 139,
        "usos": ["terraza", "precio"],
        "scores": {"precio": 5, "realismo": 1, "resistencia": 2, "ligero": 2},
        "ideal": "Balcones, terrazas y muros",
        "lede": "Un tapete verde de 10 mm para balcones, terrazas y muros. Ligero y fácil de colocar.",
        "resumen": "El Aruba 10 es un pasto sintético tipo tapete de <strong>10 mm</strong> y <strong>1,050 g/m²</strong> en verde olivo, con <strong>garantía de 3 a 5 años</strong>. Es el modelo más bajo y ligero de la colección, pensado para decorar balcones, terrazas, muros y áreas de poco paso. Cuesta <strong>desde $139/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Balcones y terrazas de departamento", "Muros verdes y jardineras", "Eventos, stands y locales", "Áreas de poco paso"],
        "fit_no": ["Jardines de uso diario: mejor Toscana 18", "Perros grandes: mejor Irlanda 25"],
        "specstrip": [("Altura", "10", "mm"), ("Peso total", "1,050", "g/m²"), ("Color", "Olivo", ""), ("Garantía", "3–5", "años")],
        "specs": _basic_specs(altura=10, peso="1,050", color="Verde olivo", garantia="3 a 5"),
        "specs_note": "Para este modelo publicamos los datos principales del fabricante. Si necesitas otro dato técnico, pregúntanos por WhatsApp.",
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "textura", "Vista general")],
        "faq_extra": [
            ("¿El Aruba 10 sirve para jardín?", "Sirve para áreas decorativas o de poco uso. Con 10 mm se siente como tapete, no como césped. Para un jardín que se pisa a diario conviene Toscana 18 o Toscana 28."),
            ("¿Aruba 10 o Toscana 18: cuál conviene?", "Aruba 10 es más bajo y más barato: $139/m² en rollo. Toscana 18 ya parece césped, tiene 5 años de garantía y cuesta $149/m². Para balcón o muro, Aruba 10. Para un jardín chico, Toscana 18."),
        ],
        "mascotas": "Aguanta mascotas chicas en áreas pequeñas, aunque con 10 mm se siente firme. Para jardines con perros conviene Irlanda 25 o Toscana 28.",
    },
    {
        "slug": "toscana-18", "id": "toscana18", "nombre": "Toscana 18", "n": 2,
        "mm": 18, "peso": "950", "peso_num": 950, "garantia": 5,
        "color": "Verde olivo y esmeralda", "tag": "El más económico", "stock": True,
        "t1": 199, "t2": 169, "rollo": 149,
        "usos": ["precio", "terraza"],
        "scores": {"precio": 5, "realismo": 2, "resistencia": 2, "ligero": 1},
        "ideal": "Jardines chicos y uso ligero",
        "lede": "El precio más bajo con aspecto de jardín, para áreas de poco uso.",
        "resumen": "El Toscana 18 es un pasto sintético de <strong>18 mm</strong> y <strong>950 g/m²</strong> en verde olivo y esmeralda, con <strong>garantía de 5 años</strong>. Es la forma más económica de tener un jardín verde todo el año en áreas de poco uso. Cuesta <strong>desde $149/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Jardines chicos o de uso ligero", "Terrazas y patios", "Presupuestos ajustados", "Frentes de casa y áreas decorativas"],
        "fit_no": ["Uso diario con niños y perros: mejor Toscana 28", "Máximo volumen: mejor un 30 o 35 mm"],
        "specstrip": [("Altura", "18", "mm"), ("Peso total", "950", "g/m²"), ("Puntadas por m²", "13,650", ""), ("Garantía", "5", "años")],
        "specs": _full_specs(altura=18, peso="950", fibra_peso="315", puntadas="13,650", puntadas10="13",
                             color="Verde olivo y esmeralda", dtex1="2,700", espesor1="0.09 a 0.11 mm",
                             ancho1="0.8 a 0.9 mm", dtex2="2,200", temp2="120 °C", temp2_label="Temperatura de prueba",
                             capa1="PP con malla, 135 g/m²", capa2="Látex, 500 g/m²", normas="UV, DIN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra"), (4, "instalado", "Jardín con andadores")],
        "faq_extra": [
            ("¿El Toscana 18 se ve natural?", "Sí, en áreas de poco uso. Es bicolor, verde olivo y esmeralda, con rizo café de soporte. Se ve menos lleno que un 28 mm porque tiene 13,650 puntadas por m² y pesa 950 g/m²."),
            ("¿Toscana 18 o Toscana 28: cuál conviene?", "Toscana 18 cuesta $149/m² en rollo y pesa 950 g/m². Toscana 28 cuesta $199/m², es 10 mm más alto y pesa 1,380 g/m². Si el jardín se usa todos los días, conviene Toscana 28."),
        ],
        "mascotas": "Sí, para mascotas chicas y uso moderado. Tiene fibra de polietileno suave, tratamiento antibacterial y es retardante al fuego. Para perros grandes conviene Irlanda 25.",
    },
    {
        "slug": "capri-20", "id": "capri20", "nombre": "Capri 20", "n": 3,
        "mm": 20, "peso": "1,580", "peso_num": 1580, "garantia": 8,
        "color": "Verde lima y esmeralda", "tag": "Alta densidad", "stock": False,
        "t1": 279, "t2": 239, "rollo": 209,
        "usos": ["mascotas", "intenso"],
        "scores": {"precio": 3, "realismo": 3, "resistencia": 4, "ligero": 0},
        "ideal": "Uso diario con look corto y parejo",
        "lede": "Solo 20 mm, pero con 16,800 puntadas por m². Denso, parejo y fácil de limpiar.",
        "resumen": "El Capri 20 es un pasto sintético de <strong>20 mm</strong> y <strong>1,580 g/m²</strong> en verde lima y esmeralda, con <strong>garantía de 8 años</strong>. Tiene 16,800 puntadas por m², así que se ve lleno aunque sea bajo, y se barre y limpia con facilidad. Cuesta <strong>desde $209/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Patios con perros: se limpia fácil", "Jardines de uso diario", "Áreas de juego para niños", "Quien prefiere un look corto y parejo"],
        "fit_no": ["Look alto y frondoso: mejor Viena 30", "Presupuesto mínimo: mejor Toscana 18"],
        "specstrip": [("Altura", "20", "mm"), ("Peso total", "1,580", "g/m²"), ("Puntadas por m²", "16,800", ""), ("Garantía", "8", "años")],
        "specs": _full_specs(altura=20, peso="1,580", fibra_peso="530", puntadas="16,800", puntadas10="16",
                             color="Verde lima y esmeralda", dtex1="4,000", espesor1="0.18 a 0.22 mm",
                             ancho1="0.8 a 1.0 mm", dtex2="2,200", temp2="120 °C", temp2_label="Temperatura de prueba",
                             capa1="PP con malla, 150 g/m²", capa2="Látex, 900 g/m²", normas="UV, ASTM, EN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra"), (4, "instalado", "Jardín amplio"), (5, "instalado", "Jardín con muro")],
        "faq_extra": [
            ("¿Por qué el Capri 20 es tan denso con solo 20 mm?", "Tiene 16,800 puntadas por m², más que Toscana 18 y Toscana 28, y fibra de 4,000 Dtex. Por eso pesa 1,580 g/m² y se ve parejo aunque sea bajo."),
            ("¿Capri 20 o Irlanda 25: cuál conviene?", "Los dos cuestan $209/m² en rollo y tienen 8 años de garantía. Capri 20 es más bajo y más denso. Irlanda 25 es más alto y su fibra es la más gruesa de la colección. Para un look corto y parejo, Capri 20. Para más volumen, Irlanda 25."),
        ],
        "mascotas": "Sí, es de los mejores para perros. Al ser bajo y denso se limpia fácil y no atrapa tanto pelo. Tiene tratamiento antibacterial y es retardante al fuego.",
    },
    {
        "slug": "irlanda-25", "id": "irlanda25", "nombre": "Irlanda 25", "n": 4,
        "mm": 25, "peso": "1,400", "peso_num": 1400, "garantia": 8,
        "color": "Verde lima y esmeralda", "tag": "Fibra más resistente", "stock": False,
        "t1": 279, "t2": 239, "rollo": 209,
        "usos": ["mascotas", "intenso"],
        "scores": {"precio": 3, "realismo": 3, "resistencia": 5, "ligero": 0},
        "ideal": "Niños, perros y pisoteo diario",
        "lede": "La fibra más gruesa de la colección, para jardines que se usan todos los días.",
        "resumen": "El Irlanda 25 es un pasto sintético de <strong>25 mm</strong> y <strong>1,400 g/m²</strong> en verde lima y esmeralda, con <strong>garantía de 8 años</strong>. Su fibra principal es la más gruesa de la colección, de 0.37 a 0.50 mm, y recupera su forma después del pisoteo. Cuesta <strong>desde $209/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Familias con niños y perros", "Jardines con pisoteo diario", "Áreas de juego y convivencia", "Quien busca la garantía más larga"],
        "fit_no": ["Balcones donde importa el peso: mejor Aruba 10", "Máximo volumen visual: mejor un 35 mm"],
        "specstrip": [("Altura", "25", "mm"), ("Peso total", "1,400", "g/m²"), ("Dtex", "4,000", ""), ("Garantía", "8", "años")],
        "specs": _full_specs(altura=25, peso="1,400", fibra_peso="520", puntadas="13,600", puntadas10="13",
                             color="Verde lima y esmeralda", dtex1="4,000", espesor1="0.37 a 0.50 mm",
                             ancho1="0.8 a 1.2 mm", dtex2="2,200", temp2="100 °C", temp2_label="Temperatura de prueba",
                             capa1="PP con malla, 130 g/m²", capa2="Látex, 750 g/m²", normas="ASTM, DIN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra"), (4, "instalado", "Patio con alberca")],
        "faq_extra": [
            ("¿Qué hace más resistente al Irlanda 25?", "Su fibra principal mide de 0.37 a 0.50 mm de espesor, la más gruesa de la colección, y tiene 4,000 Dtex. Eso le ayuda a levantarse después del pisoteo diario."),
            ("¿Irlanda 25 o Toscana 28: cuál conviene?", "Toscana 28 es más alto y frondoso a la vista y cuesta $199/m² en rollo. Irlanda 25 tiene fibra más gruesa y 8 años de garantía por $209/m². Para lucir, Toscana 28. Para uso muy intenso, Irlanda 25."),
        ],
        "mascotas": "Sí, es el más recomendado para perros y niños. Su fibra gruesa aguanta el pisoteo, tiene tratamiento antibacterial y es retardante al fuego.",
    },
    {
        "slug": "toscana-28", "id": "toscana28", "nombre": "Toscana 28", "n": 5, "badge": "Reforzado",
        "mm": 28, "peso": "1,380", "peso_num": 1380, "garantia": 5,
        "color": "Verde olivo y esmeralda", "tag": "El más vendido", "stock": True,
        "t1": 279, "t2": 229, "rollo": 199,
        "usos": ["mascotas", "terraza", "precio"],
        "scores": {"precio": 4, "realismo": 4, "resistencia": 3, "ligero": 0},
        "ideal": "Jardines familiares",
        "lede": "Se ve frondoso, aguanta a la familia entera y no cuesta como un pasto de lujo.",
        "resumen": "El Toscana 28 es un pasto sintético de <strong>28 mm</strong> y <strong>1,380 g/m²</strong> en verde olivo y esmeralda, con base reforzada y <strong>garantía de 5 años</strong>. Es la opción más vendida para jardines familiares porque se ve frondoso sin llegar al precio de los modelos de 35 mm. Cuesta <strong>desde $199/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Jardines familiares con uso diario", "Niños y mascotas: fibra suave y antibacterial", "Terrazas, patios y áreas de alberca", "Buen volumen sin pagar un 35 mm"],
        "fit_no": ["Pisoteo muy intenso todos los días: mejor Irlanda 25", "Balcones donde importa el peso: mejor Aruba 10"],
        "specstrip": [("Altura", "28", "mm"), ("Peso total", "1,380", "g/m²"), ("Puntadas por m²", "15,750", ""), ("Garantía", "5", "años")],
        "specs": _full_specs(altura=28, peso="1,380", fibra_peso="520", puntadas="15,750", puntadas10="15",
                             color="Verde olivo y esmeralda", dtex1="2,700", espesor1="0.09 a 0.11 mm",
                             ancho1="0.8 a 0.9 mm", dtex2="2,200", temp2="120 °C", temp2_label="Temperatura de prueba",
                             capa1="PP con malla, 130 g/m²", capa2="Látex, 730 g/m²", normas="UV, DIN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base reforzada"), (4, "instalado", "Jardín con andadores")],
        "faq_extra": [
            ("¿Qué significa que el Toscana 28 sea reforzado?", "La versión reforzada tiene una base más pesada: 130 g/m² de polipropileno con malla y 730 g/m² de látex, para un peso total de 1,380 g/m². La base sostiene mejor la fibra y resiste más el uso diario."),
            ("¿Toscana 28 o Irlanda 25: cuál conviene?", "Toscana 28 es más alto y frondoso a la vista y cuesta $199/m² en rollo. Irlanda 25 tiene fibra más gruesa y 8 años de garantía por $209/m². Para lucir, Toscana 28. Para uso muy intenso, Irlanda 25."),
        ],
        "mascotas": "Sí. Tiene fibra suave de polietileno, tratamiento antibacterial y es retardante al fuego. Para mascotas conviene enjuagar con agua una o dos veces por semana las zonas de más uso.",
    },
    {
        "slug": "viena-30", "id": "viena30", "nombre": "Viena 30", "n": 6,
        "mm": 30, "peso": "1,800", "peso_num": 1800, "garantia": 8,
        "color": "Verde lima y esmeralda", "tag": "Natural premium", "stock": False,
        "t1": 339, "t2": 279, "rollo": 249,
        "usos": ["realismo", "mascotas"],
        "scores": {"precio": 2, "realismo": 4, "resistencia": 4, "ligero": 0},
        "ideal": "Jardines premium de uso familiar",
        "lede": "30 mm en verde lima con la densidad de un pasto premium y 8 años de garantía.",
        "resumen": "El Viena 30 es un pasto sintético de <strong>30 mm</strong> y <strong>1,800 g/m²</strong> en verde lima y esmeralda, con <strong>garantía de 8 años</strong>. Combina 16,800 puntadas por m² con fibra de 4,000 Dtex, así que se ve lleno y brillante. Cuesta <strong>desde $249/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Jardines protagonistas de la casa", "Uso familiar con buen volumen", "Quien quiere un verde claro y brillante", "8 años de garantía"],
        "fit_no": ["Verde más oscuro y natural: mejor Japonés 35", "Presupuesto ajustado: mejor Toscana 28"],
        "specstrip": [("Altura", "30", "mm"), ("Peso total", "1,800", "g/m²"), ("Puntadas por m²", "16,800", ""), ("Garantía", "8", "años")],
        "specs": _full_specs(altura=30, peso="1,800", fibra_peso="750", puntadas="16,800", puntadas10="16",
                             color="Verde lima y esmeralda", dtex1="4,000", espesor1="0.18 a 0.22 mm",
                             ancho1="0.8 a 1.0 mm", dtex2="2,200", temp2="120 °C", temp2_label="Prueba de fusión",
                             capa1="PP con malla, 150 g/m²", capa2="Látex, 900 g/m²", normas="UV, ASTM, EN, DIN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra"), (4, "instalado", "Jardín con muro de piedra"), (5, "instalado", "Jardín con árboles")],
        "faq_extra": [
            ("¿El Viena 30 se calienta con el sol?", "Como todo pasto sintético, se calienta con el sol directo del mediodía. Un riego ligero con manguera baja la temperatura en minutos. En el blog explicamos cómo manejar el calor."),
            ("¿Viena 30 o Japonés 35: cuál conviene?", "Viena 30 pesa 1,800 g/m² y cuesta $249/m² en rollo. Japonés 35 es 5 mm más alto, en verde bosque, y cuesta $269/m². Viena se ve más claro y brillante. Japonés, más oscuro y natural."),
        ],
        "mascotas": "Sí. Tiene fibra de 4,000 Dtex que aguanta el uso diario, tratamiento antibacterial y es retardante al fuego. Para mascotas conviene enjuagar una o dos veces por semana las zonas de más uso.",
    },
    {
        "slug": "japones-35", "id": "japones35", "nombre": "Japonés 35", "n": 7,
        "mm": 35, "peso": "1,740", "peso_num": 1740, "garantia": 8,
        "color": "Verde bosque y esmeralda", "tag": "Verde natural", "stock": False,
        "t1": 359, "t2": 299, "rollo": 269,
        "usos": ["realismo"],
        "scores": {"precio": 2, "realismo": 5, "resistencia": 4, "ligero": 0},
        "ideal": "Jardines de aspecto natural",
        "lede": "35 mm en verde bosque para un jardín que parece pasto natural bien cuidado.",
        "resumen": "El Japonés 35 es un pasto sintético de <strong>35 mm</strong> y <strong>1,740 g/m²</strong> en verde bosque y esmeralda, con <strong>garantía de 8 años</strong>. Su tono oscuro se parece al pasto natural recién regado, y es el 35 mm más accesible de la colección. Cuesta <strong>desde $269/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Jardines que deben parecer naturales", "Residencias y áreas sociales", "El 35 mm más accesible", "8 años de garantía"],
        "fit_no": ["Verde claro y brillante: mejor Viena 30", "Máximo peso y volumen: mejor Bali 35"],
        "specstrip": [("Altura", "35", "mm"), ("Peso total", "1,740", "g/m²"), ("Color", "Bosque", ""), ("Garantía", "8", "años")],
        "specs": _basic_specs(altura=35, peso="1,740", color="Verde bosque y esmeralda", garantia=8),
        "specs_note": "Para este modelo publicamos los datos principales del fabricante. Si necesitas otro dato técnico, pregúntanos por WhatsApp.",
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "base", "Base y fibra"), (3, "textura", "Detalle de la fibra")],
        "faq_extra": [
            ("¿Por qué el Japonés 35 se ve más oscuro?", "Combina verde bosque y esmeralda. Es un tono más profundo que el verde lima de Viena 30 o Capri 20 y se parece al pasto natural bien regado."),
            ("¿Japonés 35 o Bali 35: cuál conviene?", "Tienen la misma altura y el mismo color. Bali 35 pesa 2,100 g/m² contra 1,740 del Japonés, así que se ve más lleno. Japonés cuesta $269/m² en rollo y Bali $299/m²."),
        ],
        "mascotas": "Sí. Tiene tratamiento antibacterial y es retardante al fuego. Con 35 mm la fibra es larga, así que conviene cepillarlo de vez en cuando en las zonas donde juegan las mascotas.",
    },
    {
        "slug": "monaco-35", "id": "monaco35", "nombre": "Mónaco 35", "n": 8,
        "mm": 35, "peso": "2,100", "peso_num": 2100, "garantia": 8,
        "color": "Verde esmeralda y lima", "tag": "Verde brillante", "stock": False,
        "t1": 399, "t2": 339, "rollo": 299,
        "usos": ["realismo", "intenso"],
        "scores": {"precio": 1, "realismo": 5, "resistencia": 5, "ligero": 0},
        "ideal": "Residencias y espacios de lujo",
        "lede": "35 mm y 2,100 g/m² en verde esmeralda brillante. Lleno, alto y suave.",
        "resumen": "El Mónaco 35 es un pasto sintético de <strong>35 mm</strong> y <strong>2,100 g/m²</strong> en verde esmeralda y lima, con <strong>garantía de 8 años</strong>. Es de los más pesados de la colección, así que se ve lleno y se siente mullido. Cuesta <strong>desde $299/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Residencias y jardines de lujo", "Hoteles, restaurantes y terrazas de eventos", "Quien quiere un verde vivo y brillante", "Máximo volumen de la colección"],
        "fit_no": ["Verde oscuro y natural: mejor Bali 35 o Japonés 35", "Presupuesto ajustado: mejor Toscana 28"],
        "specstrip": [("Altura", "35", "mm"), ("Peso total", "2,100", "g/m²"), ("Color", "Esmeralda", ""), ("Garantía", "8", "años")],
        "specs": _basic_specs(altura=35, peso="2,100", color="Verde esmeralda y lima", garantia=8),
        "specs_note": "Para este modelo publicamos los datos principales del fabricante. Si necesitas otro dato técnico, pregúntanos por WhatsApp.",
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra")],
        "faq_extra": [
            ("¿En qué se distingue el Mónaco 35 del Bali 35?", "Tienen la misma altura y el mismo peso, 2,100 g/m². Mónaco es verde esmeralda y lima, más brillante. Bali es verde bosque y esmeralda, más oscuro. Cuestan lo mismo: $299/m² en rollo."),
            ("¿Mónaco 35 o Japonés 35: cuál conviene?", "Mónaco pesa 2,100 g/m² y Japonés 1,740 g/m². Mónaco se ve más lleno y cuesta $299/m² en rollo. Japonés cuesta $269/m² y su verde es más oscuro."),
        ],
        "mascotas": "Sí. Tiene tratamiento antibacterial y es retardante al fuego. Con 35 mm la fibra es larga, así que conviene cepillarlo de vez en cuando en las zonas donde juegan las mascotas.",
    },
    {
        "slug": "bali-35", "id": "bali35", "nombre": "Bali 35", "n": 9,
        "mm": 35, "peso": "2,100", "peso_num": 2100, "garantia": 8,
        "color": "Verde bosque y esmeralda", "tag": "El más completo", "stock": False,
        "t1": 399, "t2": 339, "rollo": 299,
        "usos": ["realismo", "intenso"],
        "scores": {"precio": 1, "realismo": 5, "resistencia": 5, "ligero": 0},
        "ideal": "Jardines exclusivos",
        "lede": "El más completo de la colección: 35 mm, 2,100 g/m² y fibra de 5,500 Dtex.",
        "resumen": "El Bali 35 es un pasto sintético de <strong>35 mm</strong> y <strong>2,100 g/m²</strong> en verde bosque y esmeralda, con <strong>garantía de 8 años</strong>. Tiene 16,800 puntadas por m² y la fibra de 5,500 Dtex, la más alta de los modelos con ficha publicada. Cuesta <strong>desde $299/m²</strong> en rollo de 50 m² y llega a todo México en 3 a 5 días hábiles.",
        "fit_si": ["Jardines exclusivos y residencias", "Terrazas sociales y áreas de eventos", "Quien busca el look más natural", "Uso intenso con máximo volumen"],
        "fit_no": ["Verde claro y brillante: mejor Mónaco 35", "Presupuesto ajustado: mejor Viena 30"],
        "specstrip": [("Altura", "35", "mm"), ("Peso total", "2,100", "g/m²"), ("Dtex", "5,500", ""), ("Garantía", "8", "años")],
        "specs": _full_specs(altura=35, peso="2,100", fibra_peso="1,050", puntadas="16,800", puntadas10="16",
                             color="Verde bosque y esmeralda", dtex1="5,500", espesor1="0.05 a 0.35 mm",
                             ancho1="0.5 a 1.0 mm", dtex2="2,200", temp2="120 °C", temp2_label="Temperatura de prueba",
                             capa1="PP con malla, 150 g/m²", capa2="Látex, 900 g/m²", normas="UV, DIN, SGS, Trace"),
        "gallery": [(1, "rollo", "Rollo y textura"), (2, "textura", "Detalle de la fibra"), (3, "base", "Base y fibra"), (4, "instalado", "Jardín iluminado de noche"), (5, "instalado", "Terraza con comedor"), (6, "instalado", "Jardín bajo árboles")],
        "faq_extra": [
            ("¿Qué significa que el Bali 35 tenga 5,500 Dtex?", "Dtex es el grosor del hilo. Bali 35 tiene 5,500 Dtex, el más alto de los modelos con ficha publicada. Un hilo más grueso se siente más firme y se levanta mejor después de pisarlo."),
            ("¿Bali 35 o Viena 30: cuál conviene?", "Bali 35 pesa 2,100 g/m², es 5 mm más alto y cuesta $299/m² en rollo. Viena 30 pesa 1,800 g/m² y cuesta $249/m². Para el máximo volumen, Bali 35. Para ahorrar sin bajar mucho de nivel, Viena 30."),
        ],
        "mascotas": "Sí. Su fibra gruesa aguanta el uso diario, tiene tratamiento antibacterial y es retardante al fuego. Con 35 mm conviene cepillarlo de vez en cuando en las zonas de más uso.",
    },
]

BY_SLUG = {m["slug"]: m for m in MODELOS}

OBRAS = [
    ("obra-proyecto-04", 960, 540, "Jardín con alberca y pasto sintético instalado junto a la terraza", "Jardín con alberca"),
    ("obra-proyecto-02", 960, 1280, "Residencia moderna con escalones de piedra y pasto sintético hasta el deck", "Residencia con deck"),
    ("obra-proyecto-03", 960, 1280, "Jardín frontal con palmas y pasto sintético en una residencia", "Jardín con palmas"),
    ("obra-proyecto-05", 960, 1280, "Jardín lateral largo con pasto sintético junto a un muro verde", "Jardín lateral"),
    ("obra-proyecto-01", 900, 756, "Pasto sintético en un jardín con portería de futbol al fondo", "Jardín de juego"),
]
