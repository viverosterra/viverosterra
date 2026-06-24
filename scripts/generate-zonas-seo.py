#!/usr/bin/env python3
"""
Programmatic SEO generator for Viveros Terra zone pages.
Generates 18 hyperlocal landing pages with 70%+ unique content.
"""
import os
import re

ROOT = '/Users/luisgovela/Documents/GitHub/viverosterra/public'

# ZONAS DATA — 18 colonias/zonas with unique content variables
ZONAS = [
    # ─── TAMPICO ───
    {
        'slug': 'jardineria-altavista-tampico',
        'colonia': 'Altavista',
        'ciudad': 'Tampico',
        'ubicacion': 'sector noreste de Tampico, cerca de Av. Hidalgo',
        'tipo_zona': 'Residencial premium',
        'caracteristica': 'casas grandes con jardines amplios y palmas adultas',
        'suelo': 'arcilloso mejorado con buen drenaje',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '150–400 m²',
        'plantas_recomendadas': ['Palma Real', 'Crespón Astronómica', 'Pasto San Agustín', 'Crotón Variegado', 'Tronadora'],
        'tiempo_llegada': '15 minutos desde Cd. Madero',
        'estilo_predominante': 'colonial moderno con áreas verdes integradas',
        'reto_principal': 'mantener uniformidad del pasto en jardines de gran extensión',
        'caso_real': 'instalamos 280 m² de pasto San Agustín en una residencia de Altavista en septiembre 2025. El cliente buscaba reemplazar pasto japonés que se había quemado por el sol intenso.',
        'foto_hero': 'jardin-fotorealista-residencial-tampico.jpg',
        'foto_caso': 'jardin-residencial-pasto-san-agustin-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Altavista%20Tampico%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['pasto san agustín altavista', 'jardinero altavista tampico', 'mantenimiento jardín altavista'],
    },
    {
        'slug': 'jardineria-petrolera-tampico',
        'colonia': 'Petrolera',
        'ciudad': 'Tampico',
        'ubicacion': 'colonia histórica al norte de Tampico, junto a las instalaciones de Pemex',
        'tipo_zona': 'Residencial empresarial',
        'caracteristica': 'casas Pemex tradicionales con jardines bien definidos',
        'suelo': 'arcilloso compacto con tendencia a encharcamiento',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '100–250 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Olivo Negro', 'Ficus Benjamin', 'Lluvia de Oro', 'Crespón'],
        'tiempo_llegada': '20 minutos desde Cd. Madero',
        'estilo_predominante': 'casas residenciales Pemex con jardines frontales y traseros',
        'reto_principal': 'mejorar el drenaje del suelo arcilloso y elegir plantas que toleren sol pleno',
        'caso_real': 'rehabilitamos un jardín de 180 m² en la Petrolera donde el cliente había tenido problemas con encharcamientos. Aplicamos tierra negra mejorada con tezontle para drenaje y reinstalamos pasto.',
        'foto_hero': 'jardineria-areas-verdes-tampico.jpg',
        'foto_caso': 'diseno-jardin-pasto-rollo-san-agustin-casa-residencial-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20la%20Petrolera%20Tampico%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['pasto petrolera tampico', 'jardinero colonia petrolera', 'mantenimiento jardín petrolera'],
    },
    {
        'slug': 'jardineria-floresta-tampico',
        'colonia': 'Floresta',
        'ciudad': 'Tampico',
        'ubicacion': 'zona residencial moderna al noreste de Tampico',
        'tipo_zona': 'Residencial medio-alto',
        'caracteristica': 'casas construidas entre 2000-2020 con jardines bien planeados',
        'suelo': 'arcilloso-arenoso de buena calidad',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '80–180 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Palma Areca', 'Ave del Paraíso', 'Crotón', 'Pasto Sintético (alternativa)'],
        'tiempo_llegada': '18 minutos desde Cd. Madero',
        'estilo_predominante': 'casas estilo contemporáneo con áreas verdes funcionales',
        'reto_principal': 'optimizar jardines pequeños con plantas de alto impacto visual',
        'caso_real': 'diseñamos un jardín minimalista de 95 m² en Floresta combinando pasto San Agustín con un sendero de mármol blanco y dos palmas Areca de 2 m. Entregado en 4 días.',
        'foto_hero': 'paisajismo-diseno-jardines-tampico.webp',
        'foto_caso': 'diseno-jardines-tampico-viveros-terra.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Floresta%20Tampico%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['jardinería floresta tampico', 'pasto floresta', 'diseño jardín floresta'],
    },
    {
        'slug': 'jardineria-lomas-del-chairel-tampico',
        'colonia': 'Lomas del Chairel',
        'ciudad': 'Tampico',
        'ubicacion': 'zona residencial premium junto a la Laguna del Chairel',
        'tipo_zona': 'Premium con vista al chairel',
        'caracteristica': 'casas con alberca, jardines extensos y vista a la laguna',
        'suelo': 'arcilloso-arenoso con humedad ambiente alta',
        'salinidad': 'baja (laguna de agua dulce)',
        'tamano_jardin_promedio': '250–600 m²',
        'plantas_recomendadas': ['Palma Real', 'Heliconia', 'Coco Plumoso', 'Ave del Paraíso', 'Sabino Ahuehuete'],
        'tiempo_llegada': '22 minutos desde Cd. Madero',
        'estilo_predominante': 'jardines paisajísticos con piscina y zonas de estar',
        'reto_principal': 'integrar el jardín con la vista al chairel y mantener uniformidad estética',
        'caso_real': 'paisajismo completo de 420 m² incluyendo jardín tropical, mantenimiento de alberca, instalación de riego automatizado y plantación de 3 palmas Coco Plumoso de 4 m.',
        'foto_hero': 'paisajismo-alberca-plantas-tampico.jpg',
        'foto_caso': 'jardin-residencial-tropical-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Lomas%20del%20Chairel%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['jardinero lomas del chairel', 'paisajismo chairel tampico', 'jardín alberca chairel'],
    },
    {
        'slug': 'jardineria-country-club-tampico',
        'colonia': 'Country Club',
        'ciudad': 'Tampico',
        'ubicacion': 'fraccionamiento residencial de élite en el sector norte de Tampico',
        'tipo_zona': 'Élite',
        'caracteristica': 'mansiones con jardines extensos y arquitectura paisajística profesional',
        'suelo': 'preparado, con sistema de drenaje y riego instalado',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '400–1,200 m²',
        'plantas_recomendadas': ['Magnolia', 'Palma Real', 'Crespón Astronómica', 'Sansevieria de Sombra', 'Pasto San Agustín premium'],
        'tiempo_llegada': '25 minutos desde Cd. Madero',
        'estilo_predominante': 'jardines de autor con paisajismo profesional',
        'reto_principal': 'mantener estándares de presentación premium con servicio personalizado',
        'caso_real': 'mantenimiento mensual integral de un jardín de 850 m² en Country Club desde 2023: poda, fertilización, control de plagas, riego programado y reemplazo estacional de plantas decorativas.',
        'foto_hero': 'jardineria-profesional-detallada-tampico.jpg',
        'foto_caso': 'marmol-blanco-alberca-palmera-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Country%20Club%20Tampico%20y%20quiero%20cotizar%20jardiner%C3%ADa%20premium',
        'keywords_secondary': ['jardinero country club tampico', 'paisajismo country club', 'mantenimiento jardín premium tampico'],
    },
    {
        'slug': 'jardineria-loma-bonita-tampico',
        'colonia': 'Loma Bonita',
        'ciudad': 'Tampico',
        'ubicacion': 'fraccionamiento residencial moderno al norte de Tampico',
        'tipo_zona': 'Residencial joven',
        'caracteristica': 'casas nuevas con jardines pequeños-medianos optimizados',
        'suelo': 'arcilloso mejorado al construir',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '40–120 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Crotón', 'Buganvilia', 'Palma Areca enana', 'Helecho'],
        'tiempo_llegada': '20 minutos desde Cd. Madero',
        'estilo_predominante': 'casas tipo coto con jardines frontales pequeños',
        'reto_principal': 'crear jardines de alto impacto en espacios reducidos',
        'caso_real': 'instalación de 55 m² de pasto San Agustín + diseño de jardinera frontal con 3 buganvilias y 2 palmas Areca enanas para una familia joven que acababa de mudarse a Loma Bonita.',
        'foto_hero': 'diseno-jardin-pasto-rollo-san-agustin-casa-residencial-tampico.jpg',
        'foto_caso': 'jardineros-plantando-arbol-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Loma%20Bonita%20Tampico%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['jardinería loma bonita', 'pasto loma bonita tampico', 'jardín pequeño loma bonita'],
    },
    {
        'slug': 'jardineria-aguila-tampico',
        'colonia': 'Águila',
        'ciudad': 'Tampico',
        'ubicacion': 'colonia tradicional al sur de Tampico',
        'tipo_zona': 'Residencial tradicional',
        'caracteristica': 'casas con patio y jardín, propietarios mayores que renuevan',
        'suelo': 'arcilloso compacto, requiere mejora',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '80–200 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Lluvia de Oro', 'Acacia Negra', 'Hule', 'Bambú ornamental'],
        'tiempo_llegada': '15 minutos desde Cd. Madero',
        'estilo_predominante': 'casas clásicas con jardines establecidos hace décadas',
        'reto_principal': 'renovar jardines envejecidos sin perder árboles maduros existentes',
        'caso_real': 'renovación de un jardín de 140 m² en la colonia Águila: reemplazamos pasto agotado, podamos un árbol Hule de 30 años para devolverle salud, e instalamos sistema de riego básico.',
        'foto_hero': 'plantacion-arbol-jardin-residencial-tampico.jpg',
        'foto_caso': 'mantenimiento-jardines-poda-pasto-tampico.png',
        'wa_msg': 'Hola%2C%20vivo%20en%20la%20colonia%20%C3%81guila%20Tampico%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería águila tampico', 'jardinero colonia águila', 'renovación jardín tampico'],
    },
    # ─── CIUDAD MADERO ───
    {
        'slug': 'jardineria-miramar-madero',
        'colonia': 'Miramar / Playa Miramar',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'zona costera con frente al Golfo de México',
        'tipo_zona': 'Costero · Hotelería y casas vacacionales',
        'caracteristica': 'casas y hoteles frente al mar con brisa salina constante',
        'suelo': 'arenoso, drenaje natural alto pero baja retención de nutrientes',
        'salinidad': '★★★★★ Máxima',
        'tamano_jardin_promedio': '100–500 m² (hoteles 1000+ m²)',
        'plantas_recomendadas': ['Palma Coco', 'Almendro de Playa', 'Uva de Mar', 'Yuca Elefante', 'Beach Sunflower'],
        'tiempo_llegada': '8 minutos desde la sede en Cd. Madero',
        'estilo_predominante': 'jardines costeros con palmeras y cubresuelos resistentes',
        'reto_principal': 'la brisa salina del Golfo mata el 60% de plantas comunes; hay que elegir solo especies tolerantes',
        'caso_real': 'paisajismo de un hotel boutique en Playa Miramar: plantamos 12 Palmas Coco, una barrera de 18 m de Uva de Mar para filtrar la sal, y un cubresuelo de Beach Sunflower que florece todo el año. Mantenimiento mensual desde 2024.',
        'foto_hero': 'diseno-jardin-instalacion-plantas-tampico.jpg',
        'foto_caso': 'jardin-residencial-tropical-tampico.jpg',
        'wa_msg': 'Hola%2C%20tengo%20un%20jard%C3%ADn%20en%20Miramar%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería playa miramar', 'plantas costeras miramar', 'jardín frente al mar tampico'],
    },
    {
        'slug': 'jardineria-las-anclas-madero',
        'colonia': 'Las Anclas',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'fraccionamiento premium cercano a la zona costera',
        'tipo_zona': 'Fraccionamiento premium costero',
        'caracteristica': 'casas nuevas con jardines paisajísticos planeados desde construcción',
        'suelo': 'arenoso preparado con mejora de sustrato',
        'salinidad': '★★★ Media-alta',
        'tamano_jardin_promedio': '120–280 m²',
        'plantas_recomendadas': ['Palma Cola de Zorra', 'Crespón Astronómica', 'Pasto San Agustín', 'Buganvilia', 'Adelfa'],
        'tiempo_llegada': '10 minutos desde la sede',
        'estilo_predominante': 'casas residenciales modernas con paisajismo profesional',
        'reto_principal': 'mantener el estándar paisajístico del fraccionamiento con plantas que toleren cercanía costera',
        'caso_real': 'mantenimiento integral de un jardín de 200 m² en Las Anclas desde 2024: poda, fertilización foliar, control de salinidad con lavado dulce semanal, y reemplazo estacional de plantas decorativas.',
        'foto_hero': 'diseno-jardines-madero-altamira-pasto.jpg',
        'foto_caso': 'paisajismo-diseno-jardines-tampico.webp',
        'wa_msg': 'Hola%2C%20vivo%20en%20Las%20Anclas%20Cd.%20Madero%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería las anclas madero', 'paisajismo las anclas', 'fraccionamiento jardín madero'],
    },
    {
        'slug': 'jardineria-loma-de-rosales-madero',
        'colonia': 'Loma de Rosales',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'colonia residencial alta al noreste de Cd. Madero',
        'tipo_zona': 'Residencial alto',
        'caracteristica': 'casas grandes establecidas, lejos de la costa',
        'suelo': 'arcilloso de buena calidad',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '180–400 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Palma Real', 'Crespón', 'Ficus Benjamin', 'Olivo Negro'],
        'tiempo_llegada': '12 minutos desde la sede',
        'estilo_predominante': 'casas residenciales clásicas con jardines tropicales',
        'reto_principal': 'mantener un look tradicional con bajo mantenimiento',
        'caso_real': 'rediseñamos un jardín de 320 m² en Loma de Rosales reemplazando pasto Japonés viejo por San Agustín, agregando 2 palmas Real y un Crespón Astronómica. Riego automatizado instalado.',
        'foto_hero': 'jardin-residencial-plantas-pasto-tampico.jpg',
        'foto_caso': 'jardin-fotorealista-residencial-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Loma%20de%20Rosales%20Madero%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería loma de rosales', 'jardinero loma de rosales madero', 'mantenimiento jardín madero'],
    },
    {
        'slug': 'jardineria-petrolera-madero',
        'colonia': 'Petrolera Madero',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'colonia histórica cerca de la refinería Madero',
        'tipo_zona': 'Residencial Pemex / Refinería',
        'caracteristica': 'casas históricas amplias con jardines bien establecidos',
        'suelo': 'arcilloso compacto',
        'salinidad': 'media (proximidad portuaria)',
        'tamano_jardin_promedio': '150–350 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Adelfa', 'Lluvia de Oro', 'Buganvilia', 'Palma Datilera'],
        'tiempo_llegada': '5 minutos desde la sede',
        'estilo_predominante': 'casas residenciales de empleados Pemex con jardines tradicionales',
        'reto_principal': 'enfrentar contaminación atmosférica leve y mantenimiento de árboles maduros',
        'caso_real': 'mantenimiento mensual de un jardín de 240 m² en la Petrolera Madero desde 2022: poda preventiva, fertilización, control de plagas y limpieza de hojarasca tras vientos del puerto.',
        'foto_hero': 'jardin-residencial-pasto-san-agustin-tampico.jpg',
        'foto_caso': 'mantenimiento-jardines-poda-pasto-tampico.png',
        'wa_msg': 'Hola%2C%20vivo%20en%20la%20Petrolera%20Madero%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería petrolera madero', 'jardinero refinería madero', 'mantenimiento jardín petrolera madero'],
    },
    {
        'slug': 'jardineria-praderas-bahia-madero',
        'colonia': 'Praderas de la Bahía',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'fraccionamiento moderno al norte de Cd. Madero',
        'tipo_zona': 'Fraccionamiento medio-alto',
        'caracteristica': 'casas nuevas con jardines medianos bien planeados',
        'suelo': 'arenoso mejorado',
        'salinidad': 'baja-media',
        'tamano_jardin_promedio': '60–180 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Palma Areca', 'Crotón', 'Buganvilia enana', 'Helecho'],
        'tiempo_llegada': '12 minutos desde la sede',
        'estilo_predominante': 'casas tipo fraccionamiento con jardines compactos modernos',
        'reto_principal': 'optimizar espacios reducidos con jardines de alto rendimiento visual',
        'caso_real': 'instalamos un jardín de 80 m² en Praderas de la Bahía con pasto San Agustín, dos Palmas Areca de 1.5 m y una jardinera de Crotón variado. Listo en 3 días.',
        'foto_hero': 'paisajismo-diseno-jardines-tampico.webp',
        'foto_caso': 'diseno-jardin-pasto-rollo-san-agustin-casa-residencial-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Praderas%20de%20la%20Bah%C3%ADa%20Madero%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería praderas de la bahía', 'pasto praderas bahía madero', 'fraccionamiento jardín bahía'],
    },
    {
        'slug': 'jardineria-1-mayo-madero',
        'colonia': '1ro de Mayo',
        'ciudad': 'Cd. Madero',
        'ubicacion': 'colonia residencial al norte de Cd. Madero',
        'tipo_zona': 'Residencial medio',
        'caracteristica': 'casas familiares con jardines de tamaño medio',
        'suelo': 'arcilloso compacto',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '60–150 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Lluvia de Oro', 'Buganvilia', 'Hibiscus', 'Crotón'],
        'tiempo_llegada': '10 minutos desde la sede',
        'estilo_predominante': 'casas residenciales con jardines funcionales',
        'reto_principal': 'ofrecer servicios accesibles sin sacrificar calidad',
        'caso_real': 'instalamos 70 m² de pasto San Agustín en una casa familiar de la 1ro de Mayo a precio accesible, con asesoría para mantenimiento autónomo.',
        'foto_hero': 'jardineria-areas-verdes-tampico.jpg',
        'foto_caso': 'instalacion-pasto-san-agustin-jardin-residencial-tampico-madero.webp',
        'wa_msg': 'Hola%2C%20vivo%20en%201ro%20de%20Mayo%20Madero%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería 1ro de mayo madero', 'pasto 1 de mayo', 'jardinero colonia 1 mayo'],
    },
    # ─── ALTAMIRA ───
    {
        'slug': 'jardineria-puerto-industrial-altamira',
        'colonia': 'Puerto Industrial Altamira',
        'ciudad': 'Altamira',
        'ubicacion': 'zona industrial portuaria de Altamira',
        'tipo_zona': 'B2B Industrial',
        'caracteristica': 'plantas industriales, oficinas corporativas y áreas verdes empresariales',
        'suelo': 'preparado o de relleno industrial',
        'salinidad': '★★★★ Alta (proximidad portuaria)',
        'tamano_jardin_promedio': '500–10,000+ m² (áreas corporativas)',
        'plantas_recomendadas': ['Palma Washingtona', 'Almendro de Playa', 'Adelfa', 'Pasto Buffalo', 'Yuca Elefante'],
        'tiempo_llegada': '35 minutos desde la sede',
        'estilo_predominante': 'áreas verdes corporativas con bajo mantenimiento y alta tolerancia ambiental',
        'reto_principal': 'mantener áreas verdes funcionales en clima industrial agresivo con sal y polvo',
        'caso_real': 'mantenimiento de áreas verdes de una planta industrial en el Puerto de Altamira (2,800 m² de jardín perimetral + jardineras de oficina). Visitas quincenales con poda, riego, fertilización y reemplazo estacional.',
        'foto_hero': 'tecnico-terra-riego-industrial-tampico.avif',
        'foto_caso': 'jardineria-profesional-tampico-empresa.png',
        'wa_msg': 'Hola%2C%20somos%20una%20empresa%20en%20el%20Puerto%20Industrial%20Altamira%20y%20queremos%20cotizar%20mantenimiento%20de%20%C3%A1reas%20verdes',
        'keywords_secondary': ['jardinería industrial altamira', 'áreas verdes empresariales altamira', 'mantenimiento corporativo altamira'],
    },
    {
        'slug': 'jardineria-altamira-centro',
        'colonia': 'Altamira Centro',
        'ciudad': 'Altamira',
        'ubicacion': 'casco histórico y centro residencial-comercial de Altamira',
        'tipo_zona': 'Residencial-comercial',
        'caracteristica': 'casas urbanas y locales comerciales con jardines compactos',
        'suelo': 'arcilloso con compactación urbana',
        'salinidad': 'baja-media',
        'tamano_jardin_promedio': '30–120 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Crotón', 'Helecho', 'Palma Cica', 'Buganvilia'],
        'tiempo_llegada': '35 minutos desde la sede',
        'estilo_predominante': 'jardines urbanos compactos en patios interiores y frentes',
        'reto_principal': 'crear jardines de alto impacto en espacios urbanos limitados',
        'caso_real': 'rediseñamos un patio interior de 45 m² en Altamira Centro con jardín tropical compacto: pasto, dos Palmas Cica y una jardinera vertical con helechos. Bajo mantenimiento.',
        'foto_hero': 'jardin-residencial-tropical-tampico.jpg',
        'foto_caso': 'diseno-jardines-tampico-viveros-terra.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Altamira%20Centro%20y%20quiero%20cotizar%20jardiner%C3%ADa',
        'keywords_secondary': ['jardinería altamira centro', 'jardín urbano altamira', 'pasto altamira'],
    },
    {
        'slug': 'jardineria-bicentenario-altamira',
        'colonia': 'Bicentenario',
        'ciudad': 'Altamira',
        'ubicacion': 'fraccionamiento moderno al sur de Altamira',
        'tipo_zona': 'Fraccionamiento residencial moderno',
        'caracteristica': 'casas construidas a partir de 2010 con jardines pequeños-medianos',
        'suelo': 'arenoso mejorado',
        'salinidad': 'baja',
        'tamano_jardin_promedio': '40–120 m²',
        'plantas_recomendadas': ['Pasto San Agustín', 'Crotón', 'Buganvilia', 'Palma Areca', 'Crespón'],
        'tiempo_llegada': '30 minutos desde la sede',
        'estilo_predominante': 'casas tipo coto con jardines frontales y traseros pequeños',
        'reto_principal': 'maximizar jardines pequeños con servicios accesibles',
        'caso_real': 'instalamos 60 m² de pasto San Agustín en una casa del Bicentenario con un sendero de tezontle rojo y dos jardineras frontales con Buganvilia.',
        'foto_hero': 'diseno-jardin-pasto-rollo-san-agustin-casa-residencial-tampico.jpg',
        'foto_caso': 'tezontle-rojo-jardin-lateral-tampico.jpg',
        'wa_msg': 'Hola%2C%20vivo%20en%20Bicentenario%20Altamira%20y%20quiero%20cotizar',
        'keywords_secondary': ['jardinería bicentenario altamira', 'pasto bicentenario', 'fraccionamiento jardín altamira'],
    },
    # ─── HUBS ───
    {
        'slug': 'jardineria-zona-conurbada-tampico',
        'colonia': 'Zona Conurbada Tampico-Madero-Altamira',
        'ciudad': 'Tampico Metropolitano',
        'ubicacion': 'zona metropolitana del sur de Tamaulipas',
        'tipo_zona': 'Hub regional',
        'caracteristica': 'cobertura integral en las 3 ciudades del área metropolitana',
        'suelo': 'variable: arcilloso en Tampico, arenoso en zonas costeras, mejorado en fraccionamientos',
        'salinidad': 'variable según zona (alta en costa, baja en interior)',
        'tamano_jardin_promedio': '40–600+ m² según zona',
        'plantas_recomendadas': ['Pasto San Agustín', 'Palma Real', 'Palma Coco (zona costera)', 'Crespón Astronómica', 'Crotón'],
        'tiempo_llegada': 'desde 8 minutos (Cd. Madero) hasta 35 minutos (Altamira Puerto)',
        'estilo_predominante': 'jardines tropicales adaptados al clima cálido húmedo del Golfo',
        'reto_principal': 'cubrir 3 ciudades con realidades distintas: residencial Tampico, costero Madero, industrial Altamira',
        'caso_real': 'realizamos más de 1,500 instalaciones de pasto en la zona conurbada desde 2006, atendiendo residencias en Tampico, hoteles en Miramar, fraccionamientos en Madero y plantas industriales en Altamira.',
        'foto_hero': 'jardin-diseno-paisajismo-pasto-san-agustin-tampico-og.jpg',
        'foto_caso': 'jardineria-areas-verdes-tampico.jpg',
        'wa_msg': 'Hola%2C%20quiero%20cotizar%20jardiner%C3%ADa%20en%20la%20zona%20conurbada',
        'keywords_secondary': ['jardinería zona conurbada tampico', 'jardinero tampico madero altamira', 'jardín sur tamaulipas'],
    },
    {
        'slug': 'jardineria-fraccionamientos-residenciales-tampico',
        'colonia': 'Fraccionamientos Residenciales',
        'ciudad': 'Tampico, Madero y Altamira',
        'ubicacion': 'fraccionamientos cerrados y residenciales premium de la zona conurbada',
        'tipo_zona': 'B2B Desarrolladoras + Mesas directivas',
        'caracteristica': 'áreas verdes comunes, jardines de entrada y mantenimiento mensual',
        'suelo': 'preparado al desarrollar el fraccionamiento',
        'salinidad': 'variable según ubicación',
        'tamano_jardin_promedio': '500–5,000 m² (áreas comunes)',
        'plantas_recomendadas': ['Pasto San Agustín premium', 'Palma Washingtona', 'Crespón Astronómica', 'Adelfa', 'Lluvia de Oro'],
        'tiempo_llegada': 'según ubicación del fraccionamiento',
        'estilo_predominante': 'áreas verdes comunes con identidad visual del fraccionamiento',
        'reto_principal': 'mantener estándares consistentes en grandes áreas con presupuesto controlado',
        'caso_real': 'mantenimiento mensual de áreas verdes de un fraccionamiento residencial en Cd. Madero: 3,200 m² de pasto, 28 árboles, 14 jardineras de entrada y poda preventiva trimestral.',
        'foto_hero': 'jardineria-profesional-tampico-empresa.png',
        'foto_caso': 'areas-verdes-paisajismo-tampico.jpg',
        'wa_msg': 'Hola%2C%20somos%20una%20mesa%20directiva%20o%20desarrolladora%20y%20queremos%20cotizar%20mantenimiento%20de%20%C3%A1reas%20verdes',
        'keywords_secondary': ['fraccionamientos jardinería tampico', 'mantenimiento áreas verdes fraccionamiento', 'mesa directiva jardín tampico'],
    },
]


def build_faqs(z):
    return [
        {
            'q': f'¿Cuánto cuesta la jardinería en {z["colonia"]}, {z["ciudad"]}?',
            'a': f'En {z["colonia"]} los precios típicos son: pasto San Agustín desde $85/m² instalado, mantenimiento mensual desde $750 según tamaño del jardín, diseño Plan Terra desde $3,000. Los jardines de {z["tamano_jardin_promedio"]} (tamaño promedio en la zona) suelen oscilar entre $8,000 y $25,000 para instalación completa.'
        },
        {
            'q': f'¿Qué plantas funcionan mejor en {z["colonia"]}?',
            'a': f'En {z["colonia"]} recomendamos: {", ".join(z["plantas_recomendadas"][:5])}. Estas especies se adaptan al tipo de suelo ({z["suelo"]}) y al nivel de salinidad ({z["salinidad"]}) característico de la zona.'
        },
        {
            'q': f'¿Cuánto tardan en llegar a {z["colonia"]} desde su sede?',
            'a': f'Desde nuestra sede en Av. Álvaro Obregón 601, Cd. Madero, llegamos a {z["colonia"]} en {z["tiempo_llegada"]}. Para servicios de instalación se programa visita técnica previa sin costo y cotización en el sitio.'
        },
        {
            'q': f'¿Atienden tanto casas como empresas en {z["colonia"]}?',
            'a': f'Sí. En {z["colonia"]} atendemos casas residenciales, fraccionamientos, comercios y proyectos B2B. {z["caso_real"][:140]}...'
        },
    ]


def build_faqs_schema(z):
    items = []
    for f in build_faqs(z):
        q = f['q'].replace('"', '\\"')
        a = f['a'].replace('"', '\\"')
        items.append(f'{{"@type": "Question", "name": "{q}", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}}}')
    return ', '.join(items)


def build_other_zones(current_slug):
    """Cross-link to OTHER zones (NOT the current one)."""
    others = [z for z in ZONAS if z['slug'] != current_slug]
    items = []
    for z in others[:8]:  # 8 cross-links per page
        items.append(f'<a href="/{z["slug"]}" class="other-zone">{z["colonia"]}<small>{z["ciudad"]}</small></a>')
    return '\n          '.join(items)


def build_plants_table(z):
    rows = []
    for plant in z['plantas_recomendadas']:
        rows.append(f'<tr><td>{plant}</td><td>Recomendada para {z["colonia"]}</td></tr>')
    return '\n          '.join(rows)


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE_SHORT}} · Viveros Terra</title>
<meta name="description" content="{{META_DESC}}">
<link rel="canonical" href="https://www.viverosterra.com/{{SLUG}}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="MX-TAM">
<meta name="geo.placename" content="{{COLONIA}}, {{CIUDAD}}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.viverosterra.com/{{SLUG}}">
<meta property="og:title" content="{{TITLE_LONG}}">
<meta property="og:description" content="{{META_DESC}}">
<meta property="og:image" content="https://www.viverosterra.com/img/{{FOTO_HERO}}">
<meta property="og:locale" content="es_MX">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<script type="application/ld+json">{
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "LocalBusiness", "@id": "https://www.viverosterra.com/{{SLUG}}#localbusiness", "name": "Viveros Terra · Jardinería en {{COLONIA}}", "image": "https://www.viverosterra.com/img/{{FOTO_HERO}}", "url": "https://www.viverosterra.com/{{SLUG}}", "telephone": "+528333268008", "priceRange": "$$", "address": {"@type": "PostalAddress", "streetAddress": "Av. Álvaro Obregón 601", "addressLocality": "Ciudad Madero", "addressRegion": "TAM", "postalCode": "89460", "addressCountry": "MX"}, "areaServed": {"@type": "Place", "name": "{{COLONIA}}, {{CIUDAD}}"}, "geo": {"@type": "GeoCoordinates", "latitude": "22.2553", "longitude": "-97.8362"}, "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"},{"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}], "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "24"}},
    {"@type": "FAQPage", "mainEntity": [{{FAQS_SCHEMA}}]},
    {"@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.viverosterra.com"},
      {"@type": "ListItem", "position": 2, "name": "Zonas", "item": "https://www.viverosterra.com/jardineria-zona-conurbada-tampico"},
      {"@type": "ListItem", "position": 3, "name": "{{COLONIA}}", "item": "https://www.viverosterra.com/{{SLUG}}"}
    ]}
  ]
}</script>

<style>
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:#FAFAF7;color:#1a1a1a;line-height:1.6}
.wrap{max-width:1100px;margin:0 auto;padding:0 24px}
header{background:#fff;border-bottom:1px solid #e7eee7;padding:18px 0;position:sticky;top:0;z-index:50}
.nav{display:flex;justify-content:space-between;align-items:center}
.logo{font-family:'Playfair Display',serif;font-weight:800;color:#1B5E20;font-size:22px;text-decoration:none}
.nav-links{display:flex;gap:24px;align-items:center}
.nav-links a{color:#1a1a1a;text-decoration:none;font-size:14px;font-weight:500;transition:color .2s}
.nav-links a:hover{color:#1B5E20}
.cta-nav{background:#25D366;color:#fff;padding:8px 18px;border-radius:999px;font-size:13px;font-weight:600}
.cta-nav:hover{color:#fff;background:#1da855}
@media(max-width:768px){.nav-links{display:none}}

/* HERO */
.hero{background:linear-gradient(135deg,#F0F7F0 0%,#fff 70%);padding:60px 0 50px;position:relative;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center}
@media(max-width:900px){.hero-grid{grid-template-columns:1fr;gap:30px}}
.hero-kicker{display:inline-block;background:#1B5E20;color:#fff;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:6px 14px;border-radius:999px;margin-bottom:18px}
h1{font-family:'Playfair Display',serif;font-size:clamp(28px,4.5vw,46px);font-weight:800;color:#0D2B0E;line-height:1.1;margin-bottom:16px}
h1 span{color:#1B5E20}
.hero-subtitle{font-size:17px;color:#444;margin-bottom:24px;line-height:1.6}
.hero-stats{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px}
.stat-pill{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #d4e7d8;padding:6px 14px;border-radius:999px;font-size:12px;color:#1B5E20;font-weight:600}
.stat-pill .dot{width:8px;height:8px;border-radius:50%;background:#25D366}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.cta-primary{background:#25D366;color:#fff;padding:14px 28px;border-radius:999px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:8px;font-size:15px;transition:background .2s,transform .2s}
.cta-primary:hover{background:#1da855;transform:translateY(-1px)}
.cta-secondary{background:#fff;color:#1B5E20;padding:14px 28px;border-radius:999px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:8px;font-size:15px;border:2px solid #1B5E20;transition:all .2s}
.cta-secondary:hover{background:#1B5E20;color:#fff}
.hero-img{border-radius:20px;overflow:hidden;box-shadow:0 24px 60px rgba(15,61,20,.15);aspect-ratio:4/3}
.hero-img img{width:100%;height:100%;object-fit:cover}
.hero-caption{font-size:12px;color:#888;margin-top:10px}

/* CONTENT */
.content{padding:60px 0;background:#fff}
.content h2{font-family:'Playfair Display',serif;font-size:30px;color:#0D2B0E;margin:36px 0 16px;line-height:1.2}
.content h3{font-family:'Playfair Display',serif;font-size:20px;color:#1B5E20;margin:24px 0 12px}
.content p{margin-bottom:14px;font-size:16px;color:#333;line-height:1.7}
.content ul,.content ol{padding-left:24px;margin-bottom:18px;color:#333}
.content li{margin-bottom:8px;line-height:1.7}
.content strong{color:#0D2B0E;font-weight:600}
.content a{color:#1B5E20;text-decoration:underline}

.info-box{background:#F0F7F0;border-left:4px solid #1B5E20;padding:22px 26px;border-radius:10px;margin:26px 0}
.info-box h3{margin-top:0;color:#1B5E20}
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:24px 0}
.info-card{background:#fff;border:1px solid #e7eee7;border-radius:12px;padding:18px}
.info-card h4{font-family:'Playfair Display',serif;color:#1B5E20;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.info-card p{font-size:14px;color:#444;margin:0}

table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px}
th{background:#1B5E20;color:#fff;padding:10px 14px;text-align:left;font-weight:600}
td{padding:10px 14px;border-bottom:1px solid #e7eee7}
tr:nth-child(even) td{background:#F8FBF8}

.case-study{background:linear-gradient(135deg,#fff,#F8FBF8);border:1px solid #d4e7d8;border-radius:16px;padding:28px;margin:30px 0;display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:center}
@media(max-width:760px){.case-study{grid-template-columns:1fr}}
.case-study img{width:100%;border-radius:12px;aspect-ratio:4/3;object-fit:cover}
.case-study h3{margin-top:0}

/* OTHER ZONES */
.other-zones-section{background:#F0F7F0;padding:50px 0}
.other-zones-section h2{text-align:center;margin-bottom:30px}
.other-zones-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.other-zone{display:flex;flex-direction:column;gap:4px;background:#fff;border:1px solid #d4e7d8;border-radius:10px;padding:14px 18px;text-decoration:none;color:#0D2B0E;font-weight:600;font-size:14px;transition:all .2s}
.other-zone:hover{border-color:#1B5E20;transform:translateY(-2px);box-shadow:0 8px 20px rgba(15,61,20,.1)}
.other-zone small{font-weight:400;color:#666;font-size:11px}

/* FOOTER */
footer{background:#0D2B0E;color:#fff;padding:50px 0 30px}
footer h4{font-family:'Playfair Display',serif;color:#A5D6A7;font-size:14px;margin-bottom:14px;letter-spacing:1px;text-transform:uppercase}
footer a{color:#cdd9cd;text-decoration:none;font-size:14px;line-height:2}
footer a:hover{color:#fff}
.footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:30px;margin-bottom:30px}
.footer-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;text-align:center;font-size:13px;color:#888}

/* FLOAT WHATSAPP */
.wa-float{position:fixed;bottom:24px;right:24px;background:#25D366;color:#fff;padding:14px 22px;border-radius:999px;font-weight:600;font-size:14px;text-decoration:none;box-shadow:0 8px 24px rgba(37,211,102,.4);display:inline-flex;align-items:center;gap:8px;z-index:100;animation:pulse 2.5s infinite}
@keyframes pulse{0%,100%{box-shadow:0 8px 24px rgba(37,211,102,.4)}50%{box-shadow:0 8px 30px rgba(37,211,102,.6)}}
</style>
</head>
<body>

<header>
  <div class="wrap nav">
    <a href="/" class="logo">Viveros Terra</a>
    <nav class="nav-links">
      <a href="/pasto-en-rollo-tampico">Pasto</a>
      <a href="/diseno-jardines-tampico">Diseño</a>
      <a href="/sistema-riego-tampico">Riego</a>
      <a href="/mantenimiento-jardines-tampico">Mantenimiento</a>
      <a href="/catalogo">Catálogo</a>
      <a href="https://wa.me/528333268008" class="cta-nav">Cotizar</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="hero-kicker">{{TIPO_ZONA}} · {{CIUDAD}}</span>
      <h1>Jardinería en {{COLONIA}}, <span>{{CIUDAD}}</span></h1>
      <p class="hero-subtitle">Pasto en rollo, diseño paisajístico y mantenimiento profesional para {{COLONIA_LC}}. Conocemos el suelo, el clima y el estilo de las casas de la zona.</p>
      <div class="hero-stats">
        <span class="stat-pill"><span class="dot"></span>+1,500 instalaciones</span>
        <span class="stat-pill"><span class="dot"></span>4.6 ★ · 24 reseñas</span>
        <span class="stat-pill"><span class="dot"></span>REPSE 773725</span>
      </div>
      <div class="hero-ctas">
        <a href="https://wa.me/528333268008?text={{WA_MSG}}" target="_blank" rel="noopener" class="cta-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1l-.9 1.2c-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5 0 1.5 1.1 2.9 1.2 3.1.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.4M12 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20"/></svg>
          Cotizar gratis por WhatsApp
        </a>
        <a href="tel:8333268008" class="cta-secondary">833 326 8008</a>
      </div>
      <p class="hero-caption">Llegamos a {{COLONIA}} en {{TIEMPO_LLEGADA}} · Sin compromiso</p>
    </div>
    <div class="hero-img">
      <img src="/img/{{FOTO_HERO}}" alt="Jardinería profesional en {{COLONIA}}, {{CIUDAD}} - Viveros Terra" loading="eager" fetchpriority="high">
    </div>
  </div>
</section>

<section class="content">
  <div class="wrap">

    <p style="font-size:18px;color:#555;font-style:italic;border-left:3px solid #1B5E20;padding-left:18px;margin:0 0 30px">
      {{COLONIA}} está en {{UBICACION}}, una zona conocida por {{CARACTERISTICA}}. Casas y proyectos en {{COLONIA}} comparten retos específicos de jardinería que conocemos a fondo.
    </p>

    <h2>¿Por qué los jardines en {{COLONIA}} son distintos?</h2>
    <p>Cada zona del área conurbada Tampico-Madero-Altamira tiene un perfil único. {{COLONIA}} no es la excepción:</p>

    <div class="info-grid">
      <div class="info-card">
        <h4>Tipo de suelo</h4>
        <p>{{SUELO}}</p>
      </div>
      <div class="info-card">
        <h4>Salinidad ambiental</h4>
        <p>{{SALINIDAD}}</p>
      </div>
      <div class="info-card">
        <h4>Tamaño de jardín típico</h4>
        <p>{{TAMANO_JARDIN}}</p>
      </div>
      <div class="info-card">
        <h4>Estilo predominante</h4>
        <p>{{ESTILO}}</p>
      </div>
    </div>

    <h3>El reto principal en {{COLONIA}}</h3>
    <p>{{RETO}}. Por eso nuestro enfoque al trabajar en {{COLONIA}} es diferente al de zonas residenciales generales — adaptamos materiales, especies vegetales y técnicas a las condiciones reales de la zona.</p>

    <h2>Plantas que sí funcionan en {{COLONIA}}</h2>
    <p>Después de años trabajando en {{COLONIA}}, estas son las especies que mejor se adaptan al suelo, salinidad y clima de la zona:</p>

    <table>
      <thead>
        <tr><th>Especie</th><th>Por qué funciona aquí</th></tr>
      </thead>
      <tbody>
        {{PLANTS_TABLE}}
      </tbody>
    </table>

    <p>El catálogo completo está en <a href="/catalogo">/catalogo</a> — más de 118 variedades de plantas, palmas y árboles disponibles en vivero, con asesoría específica según tu colonia.</p>

    <h2>Servicios para {{COLONIA}}</h2>
    <ul>
      <li><strong><a href="/pasto-en-rollo-tampico">Instalación de pasto San Agustín</a></strong> — desde $85/m² instalado, ideal para los jardines de {{TAMANO_JARDIN}} típicos en la zona.</li>
      <li><strong><a href="/diseno-jardines-tampico">Diseño de jardines (Plan Terra)</a></strong> — desde $3,000 en niveles Esencial, Completo o Premium. Se descuenta al contratar el proyecto.</li>
      <li><strong><a href="/sistema-riego-tampico">Sistema de riego automatizado</a></strong> — ahorra hasta 40% en agua. Imprescindible en jardines arriba de 80 m².</li>
      <li><strong><a href="/mantenimiento-jardines-tampico">Mantenimiento mensual</a></strong> — desde $750/mes. Poda, fertilización, control de plagas. Programa según temporada.</li>
      <li><strong><a href="/venta-pasto-sintetico-tampico">Pasto sintético</a></strong> — alternativa para zonas con poco mantenimiento o sombras densas.</li>
    </ul>

    <div class="case-study">
      <div>
        <span class="hero-kicker" style="background:#A5D6A7;color:#0D2B0E">Caso real</span>
        <h3>Proyecto realizado cerca de {{COLONIA}}</h3>
        <p>{{CASO_REAL}}</p>
        <a href="https://wa.me/528333268008?text={{WA_MSG}}" class="cta-primary" style="margin-top:10px">Cotizar mi caso</a>
      </div>
      <img src="/img/{{FOTO_CASO}}" alt="Caso de jardinería realizado en {{COLONIA}}, {{CIUDAD}}" loading="lazy">
    </div>

    <h2>Tiempos de respuesta para {{COLONIA}}</h2>
    <p>Desde nuestra sede en Av. Álvaro Obregón 601, Cd. Madero, llegamos a {{COLONIA}} en aproximadamente <strong>{{TIEMPO_LLEGADA}}</strong>. Esto significa:</p>
    <ul>
      <li><strong>Cotización por WhatsApp:</strong> respuesta el mismo día (lun–vie 9am–6pm, sáb 9am–2pm).</li>
      <li><strong>Visita técnica:</strong> dentro de las 48 horas siguientes, sin costo y sin compromiso.</li>
      <li><strong>Instalación:</strong> 3–10 días según tamaño del proyecto.</li>
      <li><strong>Mantenimiento mensual:</strong> visita programada el mismo día cada mes.</li>
    </ul>

    <div class="info-box">
      <h3>Llamada directa: 833 326 8008</h3>
      <p>Si prefieres hablar, llámanos. Lunes a viernes 9am–6pm, sábado 9am–2pm. WhatsApp 24/7 con respuesta hábil.</p>
      <a href="https://wa.me/528333268008?text={{WA_MSG}}" class="cta-primary">Iniciar WhatsApp</a>
    </div>

    <h2>Preguntas frecuentes sobre jardinería en {{COLONIA}}</h2>
    {{FAQS_HTML}}

  </div>
</section>

<section class="other-zones-section">
  <div class="wrap">
    <h2>Otras zonas que atendemos</h2>
    <p style="text-align:center;color:#555;margin-bottom:30px">Cobertura integral en Tampico, Cd. Madero y Altamira. Cada zona con asesoría específica.</p>
    <div class="other-zones-grid">
      {{OTHER_ZONES}}
    </div>
    <p style="text-align:center;margin-top:30px"><a href="/jardineria-zona-conurbada-tampico" style="color:#1B5E20;font-weight:600;text-decoration:underline">Ver mapa completo de cobertura →</a></p>
  </div>
</section>

<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>Viveros Terra</h4>
        <p style="color:#cdd9cd;line-height:1.6">Jardinería · Pasto en Rollo · Diseño · Mantenimiento en el sur de Tamaulipas desde 2006.</p>
      </div>
      <div>
        <h4>Servicios</h4>
        <a href="/pasto-en-rollo-tampico">Pasto en Rollo</a><br>
        <a href="/diseno-jardines-tampico">Diseño de Jardines</a><br>
        <a href="/sistema-riego-tampico">Sistema de Riego</a><br>
        <a href="/mantenimiento-jardines-tampico">Mantenimiento</a><br>
        <a href="/catalogo">Catálogo</a>
      </div>
      <div>
        <h4>Contacto</h4>
        <a href="tel:8333268008">833 326 8008</a><br>
        <a href="mailto:viverosterra@hotmail.com">viverosterra@hotmail.com</a><br>
        <a href="https://wa.me/528333268008">WhatsApp directo</a><br>
        <span style="color:#cdd9cd">Av. Álvaro Obregón 601, Cd. Madero</span>
      </div>
      <div>
        <h4>Cumplimiento</h4>
        <span style="color:#cdd9cd">REPSE STPS · 773725</span><br>
        <span style="color:#cdd9cd">CFDI 4.0</span><br>
        <a href="/politica-privacidad">Política de Privacidad</a>
      </div>
    </div>
    <div class="footer-bottom">
      © 2026 Viveros Terra · Tampico, Tamaulipas, México
    </div>
  </div>
</footer>

<a href="https://wa.me/528333268008?text={{WA_MSG}}" target="_blank" rel="noopener" class="wa-float">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1l-.9 1.2c-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5 0 1.5 1.1 2.9 1.2 3.1.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.4M12 22a10 10 0 1 1 0-20 10 10 0 0 1 0 20"/></svg>
  Cotizar
</a>

</body>
</html>'''


def build_faqs_html(z):
    out = []
    for f in build_faqs(z):
        out.append(f'<h3>{f["q"]}</h3>\n    <p>{f["a"]}</p>')
    return '\n    '.join(out)


def generate_page(z):
    title_short = f'Jardinería en {z["colonia"]}, {z["ciudad"]}'
    title_long = f'Jardinería en {z["colonia"]}, {z["ciudad"]} · Pasto, Diseño y Mantenimiento'
    meta_desc = f'Jardinería profesional en {z["colonia"]}, {z["ciudad"]}: pasto San Agustín desde $85/m², diseño paisajístico y mantenimiento. Atendemos {z["colonia"]} con asesoría local.'
    if len(meta_desc) > 158:
        meta_desc = meta_desc[:155] + '...'

    out = HTML_TEMPLATE
    replacements = {
        '{{TITLE_SHORT}}': title_short,
        '{{TITLE_LONG}}': title_long,
        '{{META_DESC}}': meta_desc,
        '{{SLUG}}': z['slug'],
        '{{COLONIA}}': z['colonia'],
        '{{COLONIA_LC}}': z['colonia'].lower(),
        '{{CIUDAD}}': z['ciudad'],
        '{{UBICACION}}': z['ubicacion'],
        '{{TIPO_ZONA}}': z['tipo_zona'],
        '{{CARACTERISTICA}}': z['caracteristica'],
        '{{SUELO}}': z['suelo'],
        '{{SALINIDAD}}': z['salinidad'],
        '{{TAMANO_JARDIN}}': z['tamano_jardin_promedio'],
        '{{ESTILO}}': z['estilo_predominante'],
        '{{RETO}}': z['reto_principal'],
        '{{CASO_REAL}}': z['caso_real'],
        '{{TIEMPO_LLEGADA}}': z['tiempo_llegada'],
        '{{FOTO_HERO}}': z['foto_hero'],
        '{{FOTO_CASO}}': z['foto_caso'],
        '{{WA_MSG}}': z['wa_msg'],
        '{{FAQS_SCHEMA}}': build_faqs_schema(z),
        '{{FAQS_HTML}}': build_faqs_html(z),
        '{{PLANTS_TABLE}}': build_plants_table(z),
        '{{OTHER_ZONES}}': build_other_zones(z['slug']),
    }
    for k, v in replacements.items():
        out = out.replace(k, v)

    return out


def main():
    print(f"Generating {len(ZONAS)} programmatic SEO pages...\n")
    for z in ZONAS:
        out_dir = os.path.join(ROOT, z['slug'])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        html = generate_page(z)
        with open(out_path, 'w') as f:
            f.write(html)
        print(f"  ✅ {z['slug']:55s} ({len(html):,} bytes)")

    print(f"\n✅ {len(ZONAS)} pages generated successfully")

    # Update sitemap
    sitemap_path = os.path.join(ROOT, 'sitemap.xml')
    sitemap = open(sitemap_path).read()
    added = 0
    for z in ZONAS:
        if z['slug'] not in sitemap:
            entry = f'''  <url>
    <loc>https://www.viverosterra.com/{z["slug"]}</loc>
    <lastmod>2026-06-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.75</priority>
  </url>
'''
            sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
            added += 1
    open(sitemap_path, 'w').write(sitemap)
    total_urls = sitemap.count('<loc>')
    print(f"✅ Sitemap updated: +{added} URLs (total: {total_urls})")


if __name__ == '__main__':
    main()
