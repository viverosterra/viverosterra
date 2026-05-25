// Función para construir URL de imagen via API proxy
function img(id){ return '/api/img?id=' + id; }

const plants = [
  // ÁRBOLES
  {cat:'arboles',name:'Olivo Negro',sc:'Bucida Buceras',sz:['1 m','2-3 m','4-5 m'],b:['bb'],i:'🌳',img:'1TR82jlLbrXUPt6f9gZoFcrH5GkhbQbSb',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 15 m',flor:'No',mant:'Bajo',tipo:'Árbol grande banqueta',desc:'Árbol ornamental resistente, ideal para banquetas y espacios amplios. Muy tolerante al calor y sal marina. Excelente para dar sombra y delimitar espacios en Tampico.'},
  {cat:'arboles',name:'Encino Siempreverde',sc:'Quercus Virginiana',sz:['1 m','1-2 m','2-3 m','3-4 m'],b:['bb'],i:'🌳',img:'1L1L4nhFnA1VKlVNnboRHoWv455DFFAOq',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 20 m',flor:'No',mant:'Bajo',tipo:'Árbol grande banqueta',desc:'Roble siempreverde de gran porte. Muy longevo y resistente. Excelente para banquetas, parques y jardines que necesitan sombra densa permanente.'},
  {cat:'arboles',name:'Crespón Astronómica',sc:'Lagerstroemia Indica',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌸',img:'1eTgwu_mJpK3v1ZHjuTR1lm3t5F68sqXS',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 7 m',flor:'Sí — rosa/lila/blanca',mant:'Bajo',tipo:'Árbol florido banqueta',desc:'Árbol de floración espectacular en verano. Sus racimos de flores cubren toda la copa. Muy popular en jardines residenciales y avenidas por su espectacular belleza.'},
  {cat:'arboles',name:'Lluvia de Oro',sc:'Cassia Fistula',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌼',img:'1CIZhdd22WzC5E3IWT_ZakMjKVQcXrCiL',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 8 m',flor:'Sí — amarilla espectacular',mant:'Bajo',tipo:'Árbol florido',desc:'Uno de los árboles de flor más llamativos. Sus racimos de flores amarillas intensas cubren el árbol entero en primavera. Perfecto para jardines y banquetas.'},
  {cat:'arboles',name:'Flamboyán Tabachín',sc:'Delonix Regia',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌺',img:'1aSLqV6wIrI5GjRUoKH1WWfrA9LVjNhLC',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 12 m',flor:'Sí — roja/naranja',mant:'Bajo',tipo:'Árbol grande',desc:'El árbol más llamativo del trópico. Sus flores rojo-naranja brillante lo convierten en el protagonista de cualquier jardín. Crece rápido y da excelente sombra.'},
  {cat:'arboles',name:'Neem',sc:'Azadirachta indica',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌿',img:'1FavAREwVmwV-ePnTOILuldS15VbjNkbj',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 20 m',flor:'Sí (blanca pequeña)',mant:'Muy bajo',tipo:'Árbol grande banqueta',desc:'Árbol de rápido crecimiento y follaje denso. Muy resistente al calor y la sequía. Ideal para banquetas y camellones. Propiedades naturales contra insectos.'},
  {cat:'arboles',name:'Jacaranda',sc:'Jacaranda Mimisfolia',sz:['1 m','1-2 m','2-3 m'],b:[],i:'💜',img:'1Hdh5Ykn1csYcbPUTzQxOfv--alaLfvBV',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 15 m',flor:'Sí — morada espectacular',mant:'Bajo',tipo:'Árbol grande',desc:'Uno de los árboles más bellos del mundo. En temporada de floración se cubre de racimos morados que crean un espectáculo visual único. Ideal para jardines amplios.'},
  {cat:'arboles',name:'Palo de Rosa Guayacán',sc:'Tabubeia Rosea',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌸',img:'1xHPQxJZ7fh_tLWQJuMzJcPsmgKYvK0pZ',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 30 m',flor:'Sí — rosa brillante',mant:'Bajo',tipo:'Árbol grande',desc:'Árbol de floración masiva color rosa. Cuando florece, sus ramas se cubren completamente antes de que salgan las hojas, creando un efecto visual de gran impacto.'},
  {cat:'arboles',name:'Fresno',sc:'Fraxinus sp.',sz:['1 m','1-2 m','2-3 m','4-5 m'],b:['bb'],i:'🍃',img:'1JB3WqvJYHkO86fjCo5zLFKhJatLecFxu',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 20 m',flor:'No',mant:'Medio',tipo:'Árbol grande banqueta',desc:'Árbol de follaje frondoso ideal para sombra. Crece rápido y tiene buena adaptación al clima de la región. Muy usado en banquetas, camellones y jardines amplios.'},
  {cat:'arboles',name:'Sauce Llorón',sc:'Salix babylonica',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌿',img:'1ybrFPWRG8p9lBgmdFTEfbY5maVl0hSHK',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Abundante',altura:'Hasta 20 m',flor:'No',mant:'Medio',tipo:'Árbol grande banqueta',desc:'Árbol de silueta inconfundible con ramas colgantes elegantes. Requiere riego abundante. Perfecto cerca de fuentes de agua y jardines con sistema de riego.'},
  {cat:'arboles',name:'Magnolia',sc:'Magnolia grandiflora',sz:['1 m','1-2 m','2-3 m','4-5 m'],b:['bb'],i:'🌸',img:'1gUOjcdFsPvdL0K7cTpv_7q_dWdRAle2E',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Regular',altura:'Hasta 25 m',flor:'Sí — blanca grande fragante',mant:'Medio',tipo:'Árbol grande banqueta',desc:'Árbol de gran porte con flores blancas de aroma intenso. Muy apreciado en jardines formales y residencias de alto nivel. Una de las especies más elegantes.'},
  {cat:'arboles',name:'Liquidambar',sc:'Liquidambar styraciflua',sz:['1 m','1-2 m','2-3 m','4-5 m'],b:['bb'],i:'🍂',img:'1g0KJoVEpEBYUCU9liUhib6mwbSjPYTrg',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 25 m',flor:'No',mant:'Bajo',tipo:'Árbol grande banqueta',desc:'Árbol de hojas estrelladas que cambian de color en otoño. Sus colores rojos, naranjas y dorados son espectaculares. Excelente para banquetas y parques.'},
  {cat:'arboles',name:'Níspero',sc:'Eriobotrya japonica',sz:['1 m','1-2 m','2-3 m','3-4 m'],b:['bb'],i:'🍑',img:'1kN1j8I5ttfhBWgKgA-2H2FttCs4QzKW1',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 10 m',flor:'Sí — blanca fragante',mant:'Bajo',tipo:'Árbol frutal ornamental',desc:'Árbol frutal muy ornamental con frutos comestibles. Sus hojas grandes y brillantes son muy decorativas. Excelente para jardines que quieren fruto y sombra.'},
  {cat:'arboles',name:'Eucalipto',sc:'Eucalyptus sp.',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🍃',img:'1AEPUs8_RX60NicSnC_C1GbhwHpyPn8Bk',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 30 m',flor:'Sí (pequeña)',mant:'Muy bajo',tipo:'Árbol rápido crecimiento',desc:'Árbol de crecimiento muy rápido. Su aroma mentolado es muy agradable. Excelente para cortinas rompevientos y proyectos que necesitan sombra rápida.'},
  {cat:'arboles',name:'Parota Orejon',sc:'Enterolobium cyclocarpum',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌳',img:'1oCDAXja-z-1EG8ocItcR2l5PwEliKsmV',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 40 m',flor:'Sí (pequeña)',mant:'Bajo',tipo:'Árbol gigante',desc:'Uno de los árboles más grandes de México. Copa muy amplia que da sombra abundante. Muy resistente al calor y sequía. Ideal para proyectos de gran escala.'},
  {cat:'arboles',name:'Acacia Negra',sc:'Acacia melanoxylon',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌿',img:'1mRiIS7Gv2eQhK2kNAqfLYhfIqYXR1w89',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 15 m',flor:'Sí — amarilla',mant:'Muy bajo',tipo:'Árbol banqueta',desc:'Árbol de rápido crecimiento y bajo mantenimiento. Sus flores amarillas son muy ornamentales. Excelente para banquetas y camellones. Muy resistente al calor.'},
  {cat:'arboles',name:'Ficus Benjamin',sc:'Ficus benjamina',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🍃',img:'1pqmt1VfOkeKrpoETiYFwsXwA58WHEjdu',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Moderado',altura:'Hasta 15 m',flor:'No',mant:'Medio',tipo:'Árbol ornamental',desc:'Árbol muy popular para jardines y exteriores. Su follaje brillante y copa densa lo hacen muy ornamental. Excelente para crear privacidad y sombra.'},
  {cat:'arboles',name:'Tronadora',sc:'Tecoma Stans',sz:['1-2 m','2-3 m'],b:[],i:'🌻',img:'19ecEa8ReXUZzeiEShv16SWlrsThQFyO8',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 8 m',flor:'Sí — amarilla abundante',mant:'Muy bajo',tipo:'Árbol florido',desc:'Árbol de flores amarillas trompeta muy llamativas. Florece casi todo el año. Muy resistente al calor y sequía. Árbol nacional de Trinidad y Tobago.'},
  {cat:'arboles',name:'Huizache',sc:'Acacia farnesiana',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌼',img:'1mkGux-kfluVbLcBWXSqYCUlHLnBacO-D',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 8 m',flor:'Sí — amarilla fragante',mant:'Muy bajo',tipo:'Árbol xérico',desc:'Árbol nativo muy resistente. Sus flores amarillas son intensamente fragantes. Perfecta para jardines xéricos y proyectos de reforestación con plantas nativas.'},
  {cat:'arboles',name:'Sabino Ahuehuete',sc:'Taxodium mucronatum',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌲',img:'15x9FXXh32_oJ1Yy0DRdEUjb2eDXLBTfu',luz:'☀️ Pleno Sol',agua:'Abundante',altura:'Hasta 40 m',flor:'No',mant:'Bajo',tipo:'Árbol patrimonial',desc:'El árbol nacional de México. Muy longevo, puede vivir miles de años. Su follaje caduco crea efectos visuales únicos. Perfecto cerca del agua.'},
  {cat:'arboles',name:'Polyalthia',sc:'Polyalthia longifolia',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌲',img:'1Lqal7lZ1jiIHERml2bIUmy0aGzziWc98',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 15 m',flor:'Sí (discreta)',mant:'Bajo',tipo:'Árbol columnar banqueta',desc:'Árbol de porte columnar muy elegante. Sus hojas onduladas son muy ornamentales. Excelente para banquetas, ya que crece hacia arriba sin invadir espacio lateral.'},
  {cat:'arboles',name:'Flor de Mayo',sc:'Plumeria sp.',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌼',img:'1O813sCMGAr6p_C0PLC9s1BZpKb1cGAaO',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 8 m',flor:'Sí — muy fragante',mant:'Bajo',tipo:'Árbol florido banqueta',desc:'El árbol más fragante del trópico. Sus flores de cinco pétalos en blanco, rosa y amarillo son icónicas. Muy resistente al calor y la sequía.'},
  {cat:'arboles',name:'Hule',sc:'Ficus Elastica',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌿',img:'1gUEZLF50_KVvRNT4NoVBW4hdI6w592W4',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Moderado',altura:'Hasta 30 m',flor:'No',mant:'Bajo',tipo:'Árbol interior/exterior',desc:'Árbol de hojas grandes brillantes muy decorativas. Disponible en verde, variegado y púrpura. Uno de los árboles más versátiles para interior y exterior.'},
  {cat:'arboles',name:'Orquídea Pata de Vaca',sc:'Bahuinia sp.',sz:['1 m','1-2 m','2-3 m'],b:['bb'],i:'🌸',img:'17r2f7WY8RvJfFCN53aLpeFuHAdPrN1CA',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 10 m',flor:'Sí — rosa/morada',mant:'Bajo',tipo:'Árbol florido banqueta',desc:'Árbol de flores similares a orquídeas muy llamativas. Sus hojas en forma de pezuña de vaca son únicas. Una de las floaciones más elegantes de la región.'},
  {cat:'arboles',name:'Ceiba',sc:'Ceiba pentandra',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌲',img:'1KXi4c_bYqC95mDjz0iNDNZiAcnhC9hJZ',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 70 m',flor:'Sí — blanca',mant:'Bajo',tipo:'Árbol gigante',desc:'Árbol sagrado de la cultura maya. Uno de los árboles más grandes del mundo. Su tronco con contrafuertes es espectacular. Para proyectos de gran escala.'},

  // PALMAS
  {cat:'palmas',name:'Coco Plumoso',sc:'Syagrus romanzoffiana',sz:['1-2 m','2-3 m','3-4 m','+5 m'],b:[],i:'🌴',img:'1VQ2urkzIqBFO4rZeKHQpe-c3X9TViVWJ',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 15 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Palma elegante de plumas arqueadas. Muy resistente al viento y al calor tropical. Excelente para jardines residenciales y proyectos paisajísticos de impacto.'},
  {cat:'palmas',name:'Palma Cola de Zorra',sc:'Wodyetia bifurcata',sz:['1-2 m','2-3 m','3-4 m','+5 m'],b:[],i:'🌴',img:'1kIwetkOcVkm7Wb7xvVaEeMcvAdl_nDMO',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 10 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Una de las palmas más elegantes del mercado. Su follaje denso en forma de cola de zorro la hace muy llamativa. Ideal para entradas de casas, hoteles y fraccionamientos.'},
  {cat:'palmas',name:'Palma Real',sc:'Roystonea regia',sz:['1-2 m','2-3 m','3-4 m','+5 m'],b:[],i:'🌴',img:'1xlji_TnPZ_Gn0nouFx8oMhEnsifD_R10',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 30 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'La palma más majestuosa. Su tronco gris plateado y follaje erguido le da un porte regio incomparable. Muy usada en avenidas, hoteles y proyectos de gran escala.'},
  {cat:'palmas',name:'Palma Areca',sc:'Dypsis lutescens',sz:['1-2 m','2-3 m','3-4 m'],b:['bi'],i:'🪴',img:'1f9yY6hRqr0lf47QeunWBgNR_RXqZHHZM',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 8 m',flor:'Sí',mant:'Medio',tipo:'Palma interior/exterior',desc:'La palma de interior más popular del mundo. Sus tallos múltiples y follaje plumoso crean una atmósfera tropical. Excelente purificadora de aire para interiores.'},
  {cat:'palmas',name:'Palma Washingtona',sc:'Washingtonia robusta',sz:['1 m','1-2 m','2-3 m','+4 m'],b:[],i:'🌴',img:'12Q_2nhBba8CGei_eHrUAUSZognx9OP6O',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 30 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Palma de gran altura con faldilla de hojas secas característica. Muy resistente al calor y la sequía. Icónica en avenidas y espacios industriales o comerciales.'},
  {cat:'palmas',name:'Palma Cica Revoluta',sc:'Cycas revoluta',sz:['-0.60 m','0.60 m','1 m'],b:[],i:'🌿',img:'1Pp66DaLg1hg0YvVA6ZUxpT8hkgmCcdKJ',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Poco',altura:'Hasta 3 m',flor:'No',mant:'Muy bajo',tipo:'Cica / Fósil viviente',desc:'Una de las plantas más antiguas del planeta. Su forma simétrica perfecta y hojas arqueadas brillantes la hacen ideal para jardines formales y entradas.'},
  {cat:'palmas',name:'Palma Kerpis',sc:'Chamaedorea sp.',sz:['1-2 m','2-3 m','3-4 m'],b:[],i:'🪴',img:'1rD9tgujODXJ03znMkru4eB1wvMuardSJ',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 5 m',flor:'Sí',mant:'Bajo',tipo:'Palma sombra',desc:'Palma de porte elegante y crecimiento lento. Muy decorativa en jardines con sombra. Sus tallos esbeltos y follaje plumoso la hacen muy apreciada.'},
  {cat:'palmas',name:'Palma Bismarkia',sc:'Bismarckia nobilis',sz:['1 m','1-2 m','3-4 m'],b:[],i:'🌴',img:'1ZXrrCE0wKFFnRef4q_r28E9XozUhkG1m',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 25 m',flor:'Sí',mant:'Muy bajo',tipo:'Palma',desc:'Palma de hojas color plateado-azulado única en el mundo. Su color metálico la hace completamente diferente a cualquier otra. Un punto focal incomparable en jardines de diseño.'},
  {cat:'palmas',name:'Palma Cola de Pescado',sc:'Caryota sp.',sz:['1-2 m','2-3 m','3-4 m'],b:[],i:'🌿',img:'1DkGR-wrPQ47YYaIsg9ZoI2Z82mi79--G',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 25 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Palma de hojas con forma de cola de pez única. Sus folíolos irregulares le dan una textura muy especial. Muy decorativa en jardines tropicales y exteriores.'},
  {cat:'palmas',name:'Palma Mascareña',sc:'Hyophorbe lagenicaulis',sz:['1-2 m','+2 m'],b:[],i:'🌴',img:'1wqbhMQ0luL52V5e4uffu8DujrQvC3rdE',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 9 m',flor:'Sí',mant:'Bajo',tipo:'Palma botella',desc:'La palma botella. Su tronco hinchado en el centro es completamente único. Muy lenta en crecimiento, lo que la hace muy valiosa como pieza de colección.'},
  {cat:'palmas',name:'Palma Triangular',sc:'Dypsis decaryi',sz:['1-2 m','2-3 m','3-4 m'],b:[],i:'🌴',img:'1kLvHe-AawLvdRWOaI4kD1wSDT6GX4RLQ',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 8 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Palma única cuyas hojas surgen de tres lados formando un triángulo perfecto. Un diseño arquitectónico muy codiciado en jardines de alto nivel y resorts.'},
  {cat:'palmas',name:'Palma Cocotera',sc:'Cocos nucifera',sz:['1 m','2-3 m','+4 m'],b:[],i:'🌴',img:'1Sri_rLN0YlZh9rYQDt1xyPfOrGikxX_j',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 30 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'La palma tropical por excelencia. Evoca playa y paraíso. Muy resistente al viento y la salinidad costera. Perfecta para casas de playa y jardines costeros de Tampico.'},
  {cat:'palmas',name:'Palma Estrella',sc:'Rhapis excelsa',sz:['1 m','1-2 m'],b:['bi'],i:'🪴',img:'1rAAH0YxLrAgu_1W_67BEZzF8_UDaibce',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 4 m',flor:'Sí',mant:'Bajo',tipo:'Palma interior',desc:'Palma de interior con múltiples tallos esbeltos y hojas en abanico. Muy apreciada en decoración de interiores por su elegancia y resistencia a la sombra.'},
  {cat:'palmas',name:'Palma Seifrixi Bambú',sc:'Chamaedorea seifrizii',sz:['1 m','2 m'],b:['bi'],i:'🪴',img:'1-FRocM765ANJ2RYgxf7KKoKpno23TwwO',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 4 m',flor:'Sí',mant:'Bajo',tipo:'Palma interior',desc:'Palma de tallos delgados similares al bambú. Excelente para interiores. Muy resistente a la poca luz y el aire acondicionado. Popular en oficinas y lobbies.'},
  {cat:'palmas',name:'Palma Licuala',sc:'Licuala grandis',sz:['1 m','1-2 m'],b:['bi'],i:'🪴',img:'12Hz-U6IuzPzzS3jfQGdE_Jeahm6Tc28A',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 3 m',flor:'Sí',mant:'Medio',tipo:'Palma interior exótica',desc:'Palma de hojas redondas plisadas completamente únicas. Una de las palmas más exóticas y codiciadas. Su hoja circular es un diseño de la naturaleza sin igual.'},
  {cat:'palmas',name:'Palma Datilera',sc:'Phoenix dactylifera',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌴',img:'17ysEJFyKHctatMsAWwbbDZXlaqJldueQ',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 25 m',flor:'Sí',mant:'Bajo',tipo:'Palma',desc:'Palma icónica del desierto con gran resistencia al calor extremo. Sus penachos arqueados son muy decorativos. Excelente para proyectos con look mediterráneo.'},
  {cat:'palmas',name:'Palma Rubelina',sc:'Phoenix roebelenii',sz:['-1 m','1-2 m','2-3 m'],b:[],i:'🌴',img:'1EJPLtM5-mPO2BmQrrrfNAK6Q4KtsDVA6',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Moderado',altura:'Hasta 4 m',flor:'Sí',mant:'Bajo',tipo:'Palma pequeña',desc:'Versión miniatura de la palma datilera. Sus hojas arqueadas finísimas son muy ornamentales. Perfecta para jardines pequeños, macetones y espacios reducidos.'},
  {cat:'palmas',name:'Palma Viajera Ravenala',sc:'Ravenala madagascariensis',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌿',img:'157tCw_yF6zs2npPx4BmisT-vMu7-Hca0',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 10 m',flor:'Sí — blanca',mant:'Bajo',tipo:'Palma-Árbol',desc:'La palma del viajero. Sus hojas en abanico bidimensional perfecto son únicas. Planta arquitectónica de gran impacto visual para jardines de diseño.'},
  {cat:'palmas',name:'Palma de Madagascar',sc:'Pachypodium lamerei',sz:['1 m','2 m'],b:[],i:'🌵',img:'1mJ8k8jw6szm9wQgpb9Bnb8ls2qVNB62V',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 8 m',flor:'Sí — blanca',mant:'Muy bajo',tipo:'Suculenta árbol',desc:'Tronco espinoso plateado con corona de hojas largas. Parece una palma del desierto. Muy resistente. Una pieza única y llamativa para jardines de colección.'},

  // PLANTAS
  {cat:'plantas',name:'Ave de Paraíso',sc:'Strelitzia reginae',sz:['30 cm','60 cm','80 cm'],b:['bv'],i:'🌺',img:'1AP3FbBUp3js1lZnSHmw8QPFemXzBkXww',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 1.5 m',flor:'Sí — naranja/morada',mant:'Bajo',tipo:'Planta tropical',desc:'Una de las flores más elegantes del mundo. Su forma imita la cabeza de un ave tropical. Muy resistente y de larga duración. Ideal para jardines modernos y minimalistas.'},
  {cat:'plantas',name:'Monstera Piñanona',sc:'Monstera deliciosa',sz:['30 cm','60 cm','80 cm'],b:['bv'],i:'🍃',img:'1C4zUYrj3Iv1S5BAjzrpsDfzMGqxQ69oR',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 4 m',flor:'Rara',mant:'Bajo',tipo:'Planta tropical',desc:'La planta tropical de moda. Sus hojas grandes con perforaciones naturales son un ícono del diseño moderno. Perfecta para interiores luminosos y jardines sombreados.'},
  {cat:'plantas',name:'Sansiviera',sc:'Sansevieria trifasciata',sz:['60-70 cm'],b:['bv'],i:'🌿',img:'1IeuS5ZJlowycNcexuJBaevU6wa1FTavo',luz:'🌤 Media Sombra / ☀️ Sol',agua:'Muy poco',altura:'Hasta 1.2 m',flor:'Rara (fragante)',mant:'Muy bajo',tipo:'Interior resistente',desc:'Casi indestructible. Purifica el aire de toxinas y funciona en interiores con poca luz. Perfecta para oficinas, lobbies y espacios comerciales con mínimo mantenimiento.'},
  {cat:'plantas',name:'Bambú Tarro',sc:'Bambusa vulgaris',sz:['Sencillo 3-4 m','Doble 1.8 m','+4 m'],b:['bv'],i:'🌿',img:'1uXtiicBu9i7QBMdl8IcoPSb0833BYkHo',luz:'☀️ Sol / 🌤 Media',agua:'Regular',altura:'Hasta 20 m',flor:'Rara',mant:'Medio',tipo:'Gramínea gigante',desc:'El bambú más popular para cercos vivos. Crece muy rápido. Sus cañas lisas son perfectas para privacidad y barreras acústicas naturales. Un clásico del paisajismo.'},
  {cat:'plantas',name:'Palma ZZ Plant',sc:'Zamioculcas zamiifolia',sz:['30 cm','50 cm','70 cm'],b:['bv','bi'],i:'🪴',img:'1GnD6p6bAy5FH_BIIFDMkgb4VPu49uw2O',luz:'🌑 Sombra / 🌤 Media',agua:'Muy poco',altura:'Hasta 1 m',flor:'Rara',mant:'Muy bajo',tipo:'Interior resistente',desc:'La planta perfecta para interiores oscuros. Funciona con muy poca luz natural. Extremadamente resistente a la falta de riego. Ideal para oficinas y baños.'},
  {cat:'plantas',name:'Agapando',sc:'Agapanthus africanus',sz:['30-40 cm'],b:[],i:'💜',img:'1kpeqUB0wgCFWVtMYGjnmsk05Xx74nD-7',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 60 cm',flor:'Sí — azul/morada',mant:'Bajo',tipo:'Planta bulbosa',desc:'Flores en racimos azul-morado muy vistosas. Floración de primavera-verano. Excelente para bordes y jardines que buscan color prolongado.'},
  {cat:'plantas',name:'Bugambilea Mini Morada',sc:'Bougainvillea sp.',sz:['25-30 cm','50-60 cm','1 m'],b:[],i:'💜',img:'1sZD_bR56XTn6OtkUq-BKVEmCDsM9i0LK',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 3 m',flor:'Sí — morada intensa',mant:'Bajo',tipo:'Arbusto trepador',desc:'Versión compacta de bugambilea en morado intenso. Florece casi todo el año con pleno sol y muy poco riego. Perfecta para macetones, bardas bajas y jardines pequeños.'},
  {cat:'plantas',name:'Bugambilea Envarada',sc:'Bougainvillea sp.',sz:['0.80 m','1 m'],b:[],i:'🌸',img:'1PQHRsGnbn6G5-0s93wNV9B8iLp_AHf5Y',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Trepadora hasta 12 m',flor:'Sí — roja/naranja/lila',mant:'Bajo',tipo:'Trepadora envarada',desc:'Bugambilea ya formada en vara. Lista para plantar con efecto inmediato. Florece casi todo el año. La reina de las plantas de exterior en clima cálido.'},
  {cat:'plantas',name:'Plumbago',sc:'Plumbago auriculata',sz:['40 cm','80 cm'],b:['bv'],i:'💙',img:'1OY2LnExTjU39Bhbw5V0Oy5BP-RL5G7wR',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 2 m',flor:'Sí — azul celeste',mant:'Bajo',tipo:'Arbusto florido',desc:'Arbusto de flores azul celeste que florece casi todo el año. Su color es raro y muy codiciado en jardines. Ideal para setos bajos con contraste de color.'},
  {cat:'plantas',name:'Agave Atenuata',sc:'Agave attenuata',sz:['30 cm','80 cm-1 m'],b:[],i:'🌵',img:'1_ymnFLK8cBiSjI0ggLcFd4wFVZxnZmGR',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 1.5 m',flor:'Sí (1 vez al madurar)',mant:'Muy bajo',tipo:'Suculenta / Agave',desc:'El agave sin espinas. Sus hojas suaves y arqueadas lo hacen seguro para jardines familiares. Muy resistente al calor. Forma rosetas perfectas muy decorativas.'},
  {cat:'plantas',name:'Árbol de la Abundancia',sc:'Pachira aquatica',sz:['20-30 cm'],b:[],i:'🌿',img:'1G536Zq546RnMWRc8h_dyCGkU6J2OfZvE',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 18 m',flor:'Sí',mant:'Bajo',tipo:'Interior / Exterior',desc:'Símbolo de buena suerte y prosperidad. Su tronco trenzado y follaje exuberante lo hacen muy decorativo. Muy popular en oficinas, lobbies y espacios corporativos.'},
  {cat:'plantas',name:'Aralia Golden',sc:'Schefflera arboricola var.',sz:['20-25 cm','80 cm'],b:[],i:'🌿',img:'1gxwIwcw243Gfso-EVVUd15QPj1xHbN--',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Hasta 4 m',flor:'No',mant:'Bajo',tipo:'Arbusto',desc:'Follaje multicolor en tonos verdes y dorados muy decorativo. Muy resistente y fácil de mantener. Perfecta para exteriores e interiores luminosos.'},
  {cat:'plantas',name:'Aralia Elegantísima',sc:'Schefflera elegantissima',sz:['1 m','1.5 m'],b:[],i:'🌿',img:'1pghtMQSQ4O0-_aJUafx9_M3m8b6GHBxb',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 3 m',flor:'No',mant:'Bajo',tipo:'Arbusto interior',desc:'Hojas delgadas y elegantes en tonos oscuros. Muy apreciada en diseño de interiores. Su porte esbelto la hace perfecta para espacios modernos y minimalistas.'},
  {cat:'plantas',name:'Azalea',sc:'Rhododendron sp.',sz:['0.25 m','1 m'],b:[],i:'🌺',img:'1ctIMQEz71IvaQ9km70o6Kx3vqA67OFh4',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 2 m',flor:'Sí — múltiples colores',mant:'Medio',tipo:'Arbusto florido',desc:'Una de las plantas de flor más espectaculares. En floración se cubre completamente. Disponible en rosa, rojo, blanco y lila. Muy vistosa en jardines.'},
  {cat:'plantas',name:'Adelfa Enana',sc:'Nerium oleander nana',sz:['30-50 cm'],b:[],i:'🌺',img:'1em_Wx4Rxh_35trX0XMzlyAsCyYF5Xsj2',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 1 m',flor:'Sí — rosa/roja',mant:'Muy bajo',tipo:'Arbusto florido',desc:'Versión compacta de la adelfa. Muy resistente al calor y la sequía. Florece casi todo el año con muy poco mantenimiento. Ideal para bordes y jardines.'},
  {cat:'plantas',name:'Adenium Rosa del Desierto',sc:'Adenium obesum',sz:['20-30 cm','50-70 cm'],b:[],i:'🌸',img:'1HVOWle5lFxezfSlsKJHwBJrhr5Fgfr7X',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 80 cm',flor:'Sí — rosa espectacular',mant:'Muy bajo',tipo:'Suculenta florida',desc:'Planta de flores rosadas intensas sobre tronco carnoso muy llamativo. Requiere muy poca agua. Excelente como planta de colección y jardines de diseño contemporáneo.'},
  {cat:'plantas',name:'Beucarnea Soyate',sc:'Beaucarnea recurvata',sz:['20-30 cm','1 m','+1 m'],b:[],i:'🌴',img:'1nbuXOmnGL0QYOkUBH-Q_nM1_ptydvn-k',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 9 m',flor:'Rara',mant:'Muy bajo',tipo:'Árbol suculento',desc:'El pata de elefante. Su tronco hinchado almacena agua. Follaje largo y ondulado muy ornamental. Muy resistente a la sequía. Codiciado en jardines modernos.'},
  {cat:'plantas',name:'Box Arrayán Bola',sc:'Buxus sempervirens',sz:['30-40 cm','50-60 cm','70-80 cm'],b:['bv'],i:'🟢',img:'1WAN-77xq-lxXIRakKSIhm4MVG9YscJUH',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Formado según tamaño',flor:'No',mant:'Medio',tipo:'Topiario',desc:'Arbusto formado en esfera perfecta. Da un toque formal y elegante a entradas y jardines de diseño. Disponible en varios tamaños listo para plantar.'},
  {cat:'plantas',name:'Cactus Órgano',sc:'Stenocereus sp.',sz:['80 cm-1 m','+1 m'],b:[],i:'🌵',img:'1Tqwp_2SYARAYJ5LY9KJDOOyLOr4ipbqt',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 10 m',flor:'Sí (nocturna)',mant:'Muy bajo',tipo:'Cactus columnar',desc:'Cactus columnar imponente. Requiere casi nada de agua. Da un carácter muy especial a jardines desérticos y xeroscape modernos. Casi inmortal.'},
  {cat:'plantas',name:'Casuarina',sc:'Casuarina equisetifolia',sz:['50-60 cm','+1 m'],b:[],i:'🌲',img:'1YEUyJ4xIYG8murecTZatUD9jogKUZMHn',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 35 m',flor:'No',mant:'Muy bajo',tipo:'Árbol costero',desc:'Árbol de follaje muy fino y plumoso. Muy resistente a la sal marina y el viento costero. Ideal para jardines cerca del mar y cortinas rompevientos.'},
  {cat:'plantas',name:'Cipres Italiano',sc:'Cupressus sempervirens',sz:['60 cm','1.20 m','1.8 m','+2 m'],b:['bv'],i:'🌲',img:'1dXREZpp2iPK_lXZaJy2RYafpuzaqqQIY',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 35 m',flor:'No',mant:'Muy bajo',tipo:'Conífera columnar',desc:'El árbol columnar más elegante. Su forma perfectamente vertical le da un look mediterráneo incomparable. Ideal para enmarcar entradas y delimitar propiedades.'},
  {cat:'plantas',name:'Citronella',sc:'Cymbopogon nardus',sz:['20-30 cm'],b:[],i:'🌿',img:'1oIvS48sngxOG6zatv6vUHXVK_tPlM6K4',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 1.8 m',flor:'Rara',mant:'Bajo',tipo:'Aromática / Repelente',desc:'Planta repelente de mosquitos natural. Su aroma cítrico intenso aleja insectos. Perfecta para terrazas y áreas de convivencia al aire libre en Tampico.'},
  {cat:'plantas',name:'Cola de Caballo',sc:'Equisetum hyemale',sz:['60-80 cm'],b:[],i:'🌿',img:'1AkAma3foJsSDReMa3rwmjPDFc0wxxNDv',luz:'☀️ Sol / 🌤 Media',agua:'Abundante',altura:'Hasta 1.5 m',flor:'No',mant:'Bajo',tipo:'Ribereña / Acuática',desc:'Planta de tallos segmentados muy ornamental. Perfecta cerca de fuentes. Le da un toque asiático y minimalista a cualquier jardín o área de agua.'},
  {cat:'plantas',name:'Copa de Oro',sc:'Solandra maxima',sz:['40-60 cm','80 cm'],b:['bv'],i:'🌻',img:'1bwGQOIoz2jnxdSe3rEVHy3JhYXSpxXj4',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Trepadora hasta 15 m',flor:'Sí — amarilla gigante',mant:'Bajo',tipo:'Trepadora',desc:'Flores amarillas de gran tamaño muy llamativas. Una de las trepadoras más impresionantes del trópico. Perfecta para cubrir muros y pérgolas.'},
  {cat:'plantas',name:'Croto Petra',sc:'Codiaeum variegatum',sz:['25 cm','60-70 cm'],b:[],i:'🍂',img:'1Wg2HzkOME_lMfSEbODYp0P9EAiX0ir08',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 3 m',flor:'No',mant:'Bajo',tipo:'Arbusto colorido',desc:'Hojas multicolor en rojo, amarillo, naranja y verde. Una de las plantas más coloridas del jardín tropical. Perfecta para dar contraste y vida a jardines.'},
  {cat:'plantas',name:'Croto Tornillo',sc:'Codiaeum sp.',sz:['30-50 cm'],b:['bv'],i:'🍂',img:'1rjDtGotBSxyjuCFZKLxbpPTMIYY4nqM-',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 2 m',flor:'No',mant:'Bajo',tipo:'Arbusto colorido',desc:'Variedad de croto con hojas en espiral muy llamativas. Sus colores brillantes hacen de este arbusto un punto focal irresistible en cualquier jardín.'},
  {cat:'plantas',name:'Cuna de Moisés',sc:'Spathiphyllum sp.',sz:['30 cm'],b:[],i:'🤍',img:'17RFLZsuCbeXlBECOlsvW873mNT_w5u9j',luz:'🌑 Sombra / 🌤 Media',agua:'Regular',altura:'Hasta 50 cm',flor:'Sí — blanca elegante',mant:'Bajo',tipo:'Interior / Sombra',desc:'Planta de interior con elegantes flores blancas. Una de las mejores purificadoras de aire. Muy popular en oficinas, consultorios y hogares.'},
  {cat:'plantas',name:'Duranta Cubana',sc:'Duranta erecta',sz:['25-30 cm','40-60 cm'],b:['bv'],i:'🟢',img:'1DaHl79oILg8OBCpYUSTVNAHAP1DH_IQl',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 6 m',flor:'Sí — lila pequeña',mant:'Bajo',tipo:'Arbusto / Seto',desc:'Uno de los mejores arbustos para setos vivos. Muy resistente al calor. Crece rápido y se puede podar fácilmente para mantener formas. Un clásico de Tampico.'},
  {cat:'plantas',name:'Duranta Golden',sc:'Duranta erecta var.',sz:['30 cm','40-60 cm'],b:[],i:'🌿',img:'1P4T0n7LhQ7E2MXcDpRwFNnIxi93ol5oL',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 4 m',flor:'Sí',mant:'Bajo',tipo:'Arbusto colorido',desc:'Variedad dorada de la duranta. Follaje amarillo-dorado brillante contrasta perfectamente con plantas verdes. Muy popular en paisajismo moderno.'},
  {cat:'plantas',name:'Duranta Zafiro',sc:'Duranta erecta',sz:['60-70 cm'],b:['bv'],i:'🌸',img:'1Msm_jCbZFEASib-6oWPrktjCVlJdpkye',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 4 m',flor:'Sí — lila/morada',mant:'Bajo',tipo:'Arbusto florido',desc:'La más vendida por su floración continua y resistencia. Flores lila-moradas muy abundantes. Excelente para setos con color todo el año.'},
  {cat:'plantas',name:'Esparrago Springery',sc:'Asparagus densiflorus',sz:['20 cm'],b:[],i:'🌿',img:'1iXJstx1vlsfXNpX6gsQwi1rnvzUjR2zt',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 60 cm colgante',flor:'Sí (pequeña)',mant:'Bajo',tipo:'Colgante / Interior',desc:'Follaje muy fino y plumoso ideal para macetas colgantes y espacios sombreados. Su textura suave contrasta perfectamente con hojas más grandes.'},
  {cat:'plantas',name:'Esparrago Meyeri',sc:'Asparagus meyeri',sz:['20 cm','30-40 cm'],b:[],i:'🌿',img:'131sDbYulpLdMr646jxYTvFH4xk29Z45n',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 60 cm',flor:'Sí (pequeña)',mant:'Bajo',tipo:'Interior / Exterior',desc:'Tallos erectos muy densos como plumas verdes. Más compacto que el springery. Ideal para composiciones en maceta y jardines sombreados.'},
  {cat:'plantas',name:'Eugenia',sc:'Syzygium sp.',sz:['20-30 cm','50-60 cm'],b:[],i:'🌿',img:'1Wwrf6sUIk3n1BSqGgarVqaF_2NqPzLe-',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 15 m',flor:'Sí (pequeña)',mant:'Bajo',tipo:'Árbol / Seto',desc:'Excelente para setos y topiarios. Follaje denso muy fácil de podar. Sus brotes nuevos rojizos son muy decorativos. Muy usado en jardinería formal.'},
  {cat:'plantas',name:'Ficus Lyrata Pandurata',sc:'Ficus lyrata',sz:['25-30 cm','60 cm','+1 m'],b:['bv'],i:'🍃',img:'1BJ7asY8_nkVrQzkFXE_qGe0YyflktpD1',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 12 m',flor:'No',mant:'Bajo',tipo:'Árbol interior',desc:'La planta de diseño de interiores más popular del mundo. Sus hojas gigantes en forma de violín son únicas. Imprescindible en espacios modernos y oficinas de lujo.'},
  {cat:'plantas',name:'Floripondio',sc:'Brugmansia sp.',sz:['60 cm-1 m'],b:[],i:'🌼',img:'1FB3HEjFyWqyipYuxSyjZIvz3OL28FXWm',luz:'☀️ Sol / 🌤 Media',agua:'Regular',altura:'Hasta 5 m',flor:'Sí — trompeta gigante',mant:'Medio',tipo:'Árbol/Arbusto',desc:'Flores en trompeta gigante colgante con aroma nocturno intenso. Una de las plantas más impresionantes del jardín tropical. Blanco, amarillo y rosa.'},
  {cat:'plantas',name:'Fornio Phormium',sc:'Phormium tenax',sz:['80 cm-1 m'],b:[],i:'🌿',img:'1KYRExkM1w94O6sRBhuUdZTfAbFYyDH5R',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 3 m',flor:'Sí',mant:'Bajo',tipo:'Planta arquitectónica',desc:'Hojas largas y erectas como espadas. Efecto arquitectónico y moderno inigualable. Disponible en verde, rojo y variegado. Perfecta para jardines contemporáneos.'},
  {cat:'plantas',name:'Helecho Boston',sc:'Nephrolepis exaltata',sz:['20-30 cm'],b:[],i:'🌿',img:'1uAvjLr5K9TAiHVIJBmdwxHUsfPelf7_p',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 90 cm',flor:'No',mant:'Medio',tipo:'Helecho colgante',desc:'El helecho más popular del mundo. Sus frondas largas y arqueadas son perfectas para macetas colgantes. Excelente purificador de aire. Muy fresco visualmente.'},
  {cat:'plantas',name:'Helecho Macho',sc:'Dryopteris sp.',sz:['20 cm','30-40 cm'],b:['bv'],i:'🌿',img:'1NmDqxKUb00U8gHAk2HLxEEtvwqZFXpU3',luz:'🌤 Media / 🌑 Sombra',agua:'Regular',altura:'Hasta 1 m',flor:'No',mant:'Bajo',tipo:'Helecho',desc:'Helecho grande y robusto. Muy resistente. Perfecto para jardines sombreados y áreas húmedas. Sus hojas arqueadas crean un efecto de selva tropical.'},
  {cat:'plantas',name:'Helecho Peine',sc:'Blechnum sp.',sz:['40-50 cm'],b:[],i:'🌿',img:'1WmFt1SVxVYx6uNEcqXkh8GbKO0Dd_kel',luz:'🌑 Sombra',agua:'Regular',altura:'Hasta 60 cm',flor:'No',mant:'Bajo',tipo:'Helecho sombra',desc:'Helecho de frondas rígidas muy decorativas. Sus nuevas frondas de color rojizo-bronce son llamativas. Ideal para jardines tropicales sombreados.'},
  {cat:'plantas',name:'Hoja Elegante Alocasia',sc:'Alocasia macrorrhiza',sz:['70 cm','1 m','+1 m'],b:[],i:'🍃',img:'1yo8jlcB5sLYsHk_OCrEOOUWZiOsVi28h',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 4 m',flor:'Rara',mant:'Medio',tipo:'Tropical gigante',desc:'Hojas gigantes en forma de oreja de elefante. Crea un efecto tropical dramático inmediato. Muy valorada en jardines de diseño y exteriores contemporáneos.'},
  {cat:'plantas',name:'Ixora Karla',sc:'Ixora javanica',sz:['30-40 cm'],b:['bv'],i:'🌺',img:'13PLyS4DeHVOA0gu12D_4sRZ3PAilnrPM',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 2 m',flor:'Sí — naranja/roja',mant:'Bajo',tipo:'Arbusto florido',desc:'Arbusto de floración continua en tonos naranja-rojo. Sus flores en racimos compactos se mantienen casi todo el año. Perfecta para setos con color.'},
  {cat:'plantas',name:'Jazmín',sc:'Jasminum sp.',sz:['25-40 cm'],b:[],i:'🤍',img:'1jKlhI0E5sd6zE6081E0Zx_pRgB7b5H3v',luz:'☀️ Sol / 🌤 Media',agua:'Regular',altura:'Trepadora hasta 6 m',flor:'Sí — blanca fragante',mant:'Bajo',tipo:'Trepadora fragante',desc:'Una de las plantas más fragantes. Su aroma es inconfundible y muy agradable. Perfecta para pérgolas y jardines donde se quiere perfume natural.'},
  {cat:'plantas',name:'Kalanchoe',sc:'Kalanchoe blossfeldiana',sz:['20 cm'],b:['bv'],i:'🌺',img:'1m7Khtf6sVlmB0bOs42RIE5AYNkL2CSVJ',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 45 cm',flor:'Sí — múltiples colores',mant:'Muy bajo',tipo:'Suculenta florida',desc:'Planta suculenta de flores muy vistosas en amarillo, naranja, rosa y rojo. Larga duración de floración. Perfecta para macetones en terrazas.'},
  {cat:'plantas',name:'Limonaria',sc:'Murraya paniculata',sz:['30-50 cm'],b:[],i:'🌿',img:'1n7VYd3siJj8Otrv4xOb5Utmv4oK6Q0yZ',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 7 m',flor:'Sí — blanca muy fragante',mant:'Bajo',tipo:'Árbol / Seto',desc:'Uno de los arbustos más perfumados. Sus flores blancas tienen un aroma a azahar intenso. Excelente para setos aromáticos y jardines sensoriales.'},
  {cat:'plantas',name:'Papiro Egipcio',sc:'Cyperus papyrus',sz:['1.20-1.5 m'],b:[],i:'🌿',img:'1ZvI5ANdoJ8qRMc28kLcvAh5Bc9ywvCu6',luz:'☀️ Sol / 🌤 Media',agua:'Abundante',altura:'Hasta 3 m',flor:'Sí',mant:'Bajo',tipo:'Acuática / Ribereña',desc:'La planta del papel del antiguo Egipto. Sus tallos triangulares terminan en plumeros muy decorativos. Perfecta cerca de fuentes y jardines húmedos.'},
  {cat:'plantas',name:'Papiro Estrella',sc:'Cyperus alternifolius',sz:['80 cm'],b:[],i:'🌿',img:'1FShWEJlNhGHi7K9J-iB7F0f2MKyA4bhF',luz:'☀️ Sol / 🌤 Media',agua:'Abundante',altura:'Hasta 1.5 m',flor:'Sí',mant:'Bajo',tipo:'Acuática / Ribereña',desc:'Versión compacta del papiro. Sus hojas en estrella son muy ornamentales. Ideal para fuentes y bordes de jardines húmedos.'},
  {cat:'plantas',name:'Pasto Dianela',sc:'Dianella tasmanica',sz:['30 cm'],b:[],i:'🌿',img:'1HpFCEwmOlA_rXoZZwsVtiDLvoPvfm1gp',luz:'☀️ Sol / 🌤 Media',agua:'Poco',altura:'Hasta 1 m',flor:'Sí — azul',mant:'Muy bajo',tipo:'Gramínea ornamental',desc:'Gramínea ornamental moderna. Muy usada en paisajismo contemporáneo. Excelente cubresuelos y planta de borde de bajo mantenimiento.'},
  {cat:'plantas',name:'Pasto Liriope',sc:'Liriope muscari',sz:['25 cm'],b:[],i:'🌿',img:'1HbGR8_NXgA8Xl6Ku6PfIL4wrCVLMalBZ',luz:'🌤 Media / 🌑 Sombra',agua:'Poco',altura:'Hasta 40 cm',flor:'Sí — morada',mant:'Muy bajo',tipo:'Cubresuelos',desc:'El mejor cubresuelos para sombra. Muy resistente y de bajo mantenimiento. Sus flores moradas en espigas son muy ornamentales. Ideal bajo árboles.'},
  {cat:'plantas',name:'Philodendro Xanadu',sc:'Thaumatophyllum xanadu',sz:['30 cm','60 cm'],b:[],i:'🍃',img:'1DxPrCUUi0gqifdpP2L8GsB7g03yXvSJd',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 1.5 m',flor:'Rara',mant:'Bajo',tipo:'Tropical',desc:'Hojas grandes profundamente recortadas muy decorativas. Una de las plantas tropicales más valoradas en diseño de interiores y jardines contemporáneos.'},
  {cat:'plantas',name:'Sansiviera Variegada',sc:'Sansevieria trifasciata',sz:['60-70 cm'],b:['bv'],i:'🌿',img:'1IeuS5ZJlowycNcexuJBaevU6wa1FTavo',luz:'🌤 Media Sombra',agua:'Muy poco',altura:'Hasta 1.2 m',flor:'Rara',mant:'Muy bajo',tipo:'Interior resistente',desc:'Variedad variegada con bordes amarillos. Casi indestructible. Purifica el aire y tolera cualquier condición de interior.'},
  {cat:'plantas',name:'Uva de Playa',sc:'Coccoloba uvifera',sz:['80 cm-1 m'],b:[],i:'🍃',img:'14Xq1BSGA0MJF1VIZx3D8NNIBWBbywNpu',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 15 m',flor:'Sí',mant:'Muy bajo',tipo:'Árbol costero',desc:'Árbol costero de hojas redondas grandes y brillantes. Muy resistente a la sal y el viento. Ideal para jardines en zona costera de Tampico.'},
  {cat:'plantas',name:'Wudelia Rastrera',sc:'Wedelia trilobata',sz:['20-25 cm'],b:[],i:'🌼',img:'1MbNqUWWXlah_79CoinEswxFJWJteXvGg',luz:'☀️ Sol / 🌤 Media',agua:'Poco',altura:'Rastrera 15 cm',flor:'Sí — amarilla',mant:'Muy bajo',tipo:'Cubresuelos',desc:'Cubresuelos de flores amarillas que florece casi todo el año. Crece muy rápido. Perfecta para taludes, bordes y jardines de bajo mantenimiento.'},
  {cat:'plantas',name:'Mussaenda',sc:'Mussaenda sp.',sz:['50 cm','80 cm'],b:[],i:'🌸',img:'1nETDOzwNVZTgVoPRjaS_W4Dz73dhZ6Fn',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 4 m',flor:'Sí — muy llamativa',mant:'Medio',tipo:'Arbusto florido',desc:'Arbusto de gran impacto visual con brácteas brillantes en rosa, rojo y blanco. Floración prolongada. Una de las plantas más llamativas del jardín tropical.'},

  // PLANTAS NUEVAS
  {cat:'palmas',name:'Palma Cica Circinalis',sc:'Cycas circinalis',sz:['1 m','1-2 m','2-3 m'],b:[],i:'🌿',img:'1uw1fBpfrnXp3iRjTfNqvZeYxjMYE51Vx',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Poco',altura:'Hasta 6 m',flor:'No',mant:'Muy bajo',tipo:'Cica',desc:'Prima de la Cica Revoluta, de porte más erguido y elegante. Sus hojas arqueadas brillantes la hacen ideal para jardines formales. Resistente y de muy bajo mantenimiento.'},
  {cat:'palmas',name:'Palma Cartón',sc:'Zamia furfuracea',sz:['30 cm','60 cm','1 m'],b:[],i:'🌿',img:'1h5O3MpxTQ8dwDpdihfKsbeOgZ7qC3W-M',luz:'☀️ Sol / 🌤 Media Sombra',agua:'Poco',altura:'Hasta 1.2 m',flor:'No',mant:'Muy bajo',tipo:'Zamia / Cica',desc:'Planta de hojas rígidas color verde azulado muy ornamental. Extremadamente resistente a la sequía y al calor. Perfecta para jardines de bajo mantenimiento.'},
  {cat:'plantas',name:'Arbusto de Playa',sc:'Scaevola taccada',sz:['40-60 cm','80 cm-1 m'],b:[],i:'🌿',img:'1Uyuaff-bdm665Ck426fa0HH3r9LPTLlh',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 2 m',flor:'Sí — blanca',mant:'Muy bajo',tipo:'Arbusto costero',desc:'Arbusto nativo de zonas costeras. Muy resistente a la sal marina, el viento y el calor. Excelente para jardines cerca del mar en Tampico. Florece casi todo el año.'},
  {cat:'plantas',name:'Aralia Shaflera',sc:'Schefflera arboricola',sz:['30 cm','60 cm','1 m','1.5 m'],b:[],i:'🌿',img:'13TbartQTxY8Z7BfkDzzhvGYwvQPToSuT',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Hasta 4 m',flor:'No',mant:'Bajo',tipo:'Arbusto',desc:'Aralia de hojas compuestas muy decorativas. Disponible como árbol de tallos múltiples. Muy resistente y adaptable a interior y exterior. Popular en oficinas y hogares.'},
  {cat:'plantas',name:'Box Arrayán Pino',sc:'Buxus sempervirens',sz:['30-50 cm','60-80 cm'],b:['bv'],i:'🌲',img:'1udwupYiTe0d_3WB4zR6uklycOlyueIUi',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Formado según tamaño',flor:'No',mant:'Medio',tipo:'Topiario columnar',desc:'Arbusto formado en columna o cono tipo pino. Da un toque formal y mediterráneo a entradas y jardines. Disponible en varios tamaños listo para plantar.'},
  {cat:'plantas',name:'Aspidistra',sc:'Aspidistra elatior',sz:['30-40 cm','50-70 cm'],b:['bi'],i:'🍃',img:'1abciYCcuVNWTV92LIsdmMzFIEFG3Wbnm',luz:'🌑 Sombra / 🌤 Media',agua:'Poco',altura:'Hasta 60 cm',flor:'Rara',mant:'Muy bajo',tipo:'Interior sombra',desc:'La planta más resistente para interiores oscuros. Sobrevive con muy poca luz y agua. Hojas largas brillantes muy decorativas. Ideal para pasillos, baños y oficinas.'},
  {cat:'plantas',name:'Tradescantia Barquilla Morada',sc:'Tradescantia spathacea',sz:['20-30 cm','40 cm'],b:[],i:'🟣',img:'1xz150FKLjdQtQZge37YUqiD0kCNumzsu',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Hasta 40 cm',flor:'Sí — blanca pequeña',mant:'Bajo',tipo:'Planta ornamental',desc:'Hojas bicolor verde por arriba y morado intenso por abajo. Muy llamativa en bordes y macetones. Una de las plantas de follaje más vistosas para exteriores.'},
  {cat:'plantas',name:'Heliconia Baby Enana',sc:'Heliconia sp.',sz:['40-60 cm','80 cm-1 m'],b:[],i:'🌺',img:'1I0y6eStyk1RVyolv8WJL4Mq3q7kS2l19',luz:'☀️ Pleno Sol',agua:'Regular',altura:'Hasta 1.5 m',flor:'Sí — colorida tropical',mant:'Bajo',tipo:'Tropical florida',desc:'Versión compacta de la heliconia tropical. Sus flores de colores brillantes son muy llamativas. Perfecta para jardines tropicales y macetones de gran tamaño.'},
  {cat:'plantas',name:'Laurel de la India Formado',sc:'Ficus microcarpa',sz:['40-60 cm','80 cm-1.5 m','+2 m'],b:['bv'],i:'🌳',img:'1yO3frSlCRK5EfSBueH7_UFE56o6vnL4b',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Hasta 15 m',flor:'No',mant:'Bajo',tipo:'Árbol topiario',desc:'Laurel de la India ya formado y podado. Ideal para entradas y jardines formales. Su follaje denso y brillante lo hace muy ornamental. Disponible en bola, columna y árbol.'},
  {cat:'plantas',name:'Clavo Enano Pittosporum',sc:'Pittosporum tobira',sz:['30-40 cm','50-70 cm'],b:[],i:'🌿',img:'1ivXVDRRd1iv-pZw3-gr4-deZL0ABTQLd',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 3 m',flor:'Sí — blanca fragante',mant:'Muy bajo',tipo:'Arbusto seto',desc:'Arbusto compacto de hojas brillantes y flores blancas con aroma a azahar. Muy resistente al calor y sequía. Excelente para setos y jardines de bajo mantenimiento.'},
  {cat:'plantas',name:'Lirio Persa',sc:'Iris sp.',sz:['30-40 cm'],b:[],i:'💜',img:'1EG0myJU-ngzppq82T-O8rN3iwzS1Plmu',luz:'☀️ Pleno Sol',agua:'Moderado',altura:'Hasta 80 cm',flor:'Sí — morada/lila',mant:'Bajo',tipo:'Bulbosa florida',desc:'Flores de gran elegancia en tonos morados y lila. De larga duración y muy ornamental. Perfecta para bordes de jardín y macetones que buscan color refinado.'},
  {cat:'plantas',name:'Dracena Compacta',sc:'Dracaena deremensis',sz:['30-40 cm','60-80 cm','1 m'],b:['bi'],i:'🌿',img:'1i1i2FNi_9tVVGSdbpun6Iidbg9TwOfrv',luz:'🌤 Media Sombra',agua:'Poco',altura:'Hasta 2 m',flor:'Rara',mant:'Muy bajo',tipo:'Interior resistente',desc:'Dracena de crecimiento muy lento y hojas densas color verde oscuro. Muy popular en interiores. Excelente purificadora de aire. Tolera muy poca luz y agua.'},
  {cat:'plantas',name:'Galatea Amoena',sc:'Calathea amoena',sz:['20-30 cm','40-50 cm'],b:['bi'],i:'🍃',img:'1UjESgWHHQNGtzQtw3qnJlZFE1Rc7iqs7',luz:'🌤 Media Sombra',agua:'Regular',altura:'Hasta 50 cm',flor:'No',mant:'Medio',tipo:'Interior tropical',desc:'Planta de hojas con patrones exóticos en verde y crema. Sus hojas se abren de día y se cierran de noche. Muy apreciada en decoración de interiores modernos.'},
  {cat:'plantas',name:'Eleagnus',sc:'Elaeagnus pungens',sz:['40-60 cm','80 cm-1 m'],b:[],i:'🌿',img:'1sdu-rL3XG1rbigjcF9PX8N6yKZjcaDpC',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 4 m',flor:'Sí — pequeña fragante',mant:'Muy bajo',tipo:'Arbusto seto',desc:'Arbusto de hojas plateadas brillantes muy decorativo. Resistente al calor, sequía y vientos. Excelente para setos mixtos y jardines de bajo mantenimiento.'},
  {cat:'plantas',name:'Dracena Marginata',sc:'Dracaena marginata',sz:['40-60 cm','80 cm-1 m','+1.5 m'],b:['bi'],i:'🌿',img:'1QcRkzm1iRQvShiMzlGlj8hjqnPB1pY1V',luz:'☀️ Sol / 🌤 Media',agua:'Poco',altura:'Hasta 5 m',flor:'Rara',mant:'Muy bajo',tipo:'Interior / Exterior',desc:'Árbol de interior con troncos esbeltos y hojas con bordes rojos característicos. Muy popular en diseño de interiores modernos. Tolera condiciones difíciles.'},
  {cat:'plantas',name:'Lápiz Tirucalli',sc:'Euphorbia tirucalli',sz:['30-50 cm','80 cm-1 m'],b:[],i:'🌵',img:'1PKzpiEaoqaQ9_RPXL9sMK6bnaqM0BFJC',luz:'☀️ Pleno Sol',agua:'Muy poco',altura:'Hasta 10 m',flor:'No',mant:'Muy bajo',tipo:'Suculenta árbol',desc:'Suculenta de tallos cilíndricos como lápices de color verde brillante. Sin hojas, solo tallos. Muy resistente a la sequía. Da un efecto moderno y escultórico único.'},
  {cat:'plantas',name:'Moneda Enredadera',sc:'Dichondra argentea',sz:['10-20 cm colgante'],b:[],i:'🟡',img:'13CLoB6ExRQc-hhXkh7g2EoelrZicsaoC',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Colgante hasta 60 cm',flor:'No',mant:'Bajo',tipo:'Colgante / Cubresuelos',desc:'Enredadera colgante de hojas redondas color verde plateado similar a monedas. Perfecta para macetas colgantes y bordes de jardín. Efecto muy decorativo.'},
  {cat:'plantas',name:'Petunia Silvestre',sc:'Ruellia simplex',sz:['20-30 cm','40-50 cm'],b:[],i:'💜',img:'124xVn7sBoe2YZ0dfxqLIgja94gt2uAxP',luz:'☀️ Pleno Sol',agua:'Poco',altura:'Hasta 60 cm',flor:'Sí — morada continua',mant:'Muy bajo',tipo:'Cubresuelos florida',desc:'Floración casi todo el año en morado intenso. Crece y se multiplica sola. Excelente cubresuelos para jardines tropicales. Muy resistente al calor de Tampico.'},
  {cat:'plantas',name:'Podocarpus Japanese Yew',sc:'Podocarpus macrophyllus',sz:['50-80 cm','1-1.5 m','+2 m'],b:['bv'],i:'🌲',img:'1T265TQXc9GMbozMLezEREO0-EKwoEYkB',luz:'☀️ Sol / 🌤 Media',agua:'Moderado',altura:'Hasta 20 m',flor:'No',mant:'Bajo',tipo:'Conífera tropical',desc:'Conífera de hojas largas brillantes muy ornamental. Excelente para topiarios, setos formales y jardines japoneses. Una de las coníferas más elegantes para clima cálido.'},
  {cat:'plantas',name:'Clorofito Listón',sc:'Chlorophytum comosum',sz:['20-30 cm','40 cm colgante'],b:['bi'],i:'🌿',img:'1LFzD4F1wfpi1au082xJ6oI6DEIvERAOk',luz:'🌤 Media Sombra',agua:'Moderado',altura:'Hasta 40 cm colgante',flor:'Sí — pequeña blanca',mant:'Muy bajo',tipo:'Interior / Colgante',desc:'Planta colgante con hojas verdes y blancas rayadas. Purificadora de aire muy eficiente. Produce pequeñas plantas bebé colgantes muy decorativas. Clásica e indestructible.'},
];

let tab='todos', q='', expId=null;

function setTab(t,el){
  tab=t; q=''; document.getElementById('si').value='';
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  const isPasto=t==='pasto';
  document.getElementById('pastoSection').style.display=isPasto?'block':'none';
  document.getElementById('grid').style.display=isPasto?'none':'grid';
  document.getElementById('cnt').style.display=isPasto?'none':'block';
  document.getElementById('searchWrap').style.display=isPasto?'none':'block';
  document.getElementById('solsec').style.display=isPasto?'none':'block';
  expId=null; render();
}

function doFilter(){q=document.getElementById('si').value.toLowerCase();expId=null;render();}

function toggleExp(id,e){
  if(e){e.stopPropagation();}
  expId=expId===id?null:id;render();
  if(expId===id){
    setTimeout(()=>{const el=document.getElementById(id);if(el)el.scrollIntoView({behavior:'smooth',block:'nearest'});},50);
  }
}

function render(){
  const g=document.getElementById('grid');
  const c=document.getElementById('cnt');
  if(tab==='pasto')return;
  const f=plants.filter(p=>{
    const mt=tab==='todos'||p.cat===tab;
    const ms=!q||p.name.toLowerCase().includes(q)||p.sc.toLowerCase().includes(q)||p.tipo.toLowerCase().includes(q)||p.luz.toLowerCase().includes(q);
    return mt&&ms;
  });
  f.sort((a,b)=>a.name.localeCompare(b.name,'es'));
  document.getElementById('totalCount').textContent=plants.length+'+';
  c.textContent=f.length+' variedades encontradas';
  if(!f.length){
    g.innerHTML='<div class="empty"><div class="empty-icon">🌱</div>Sin resultados para "'+q+'"<br><small style="display:block;margin-top:.5rem">Usa el formulario de abajo para solicitar lo que buscas</small></div>';
    return;
  }
  g.innerHTML=f.map(p=>{
    const id='c_'+p.name.replace(/\s+/g,'_').replace(/[^a-zA-Z0-9_]/g,'');
    const isExp=expId===id;
    const bd=p.b.map(x=>{
      if(x==='bb')return'<span class="badge bb">Banqueta</span>';
      if(x==='bi')return'<span class="badge bi">Interior</span>';
      if(x==='bv')return'<span class="badge bv">+ Vendido</span>';
      return'';
    }).join('');
    const imgHtml=p.img
      ? `<img src="/api/img?id=${p.img}" alt="${p.name}" loading="lazy" onload="this.classList.add('loaded')" onerror="this.style.display='none'"/><span class="emoji">${p.i}</span>`
      : `<span class="emoji">${p.i}</span>`;
    const szCats=p.sz.map(s=>'<span class="sz">'+s+'</span>').join('');
    const szTags=p.sz.map(s=>'<span class="sztag">'+s+'</span>').join('');
    const ficha=isExp?`
    <div class="ficha">
      <div class="ficons">
        <span class="fi">${p.luz}</span>
        <span class="fi">💧 ${p.agua}</span>
        <span class="fi">📏 ${p.altura}</span>
        <span class="fi">🌸 Flor: ${p.flor}</span>
        <span class="fi">🔧 Mant: ${p.mant}</span>
      </div>
      <div class="fgrid">
        <div class="fitem"><div class="flabel">Clasificación</div><div class="fval">${p.tipo}</div></div>
        <div class="fitem"><div class="flabel">Nombre científico</div><div class="fval" style="font-style:italic;font-size:11px">${p.sc}</div></div>
        <div class="fitem"><div class="flabel">Agua requerida</div><div class="fval">${p.agua}</div></div>
        <div class="fitem"><div class="flabel">Altura adulta</div><div class="fval">${p.altura}</div></div>
      </div>
      <div class="fdesc">${p.desc}</div>
      <div class="fsizes">
        <div class="flabel" style="margin-bottom:5px">Tamaños disponibles:</div>
        ${szTags}
        <span class="szspec">+ Otras medidas disponibles</span>
      </div>
      <div class="factions">
        <button class="fa-wa" onclick="cotizar('${p.name.replace(/'/g,"\\'")}')">📲 Cotizar por WhatsApp</button>
        <button class="fa-esp" onclick="solMedida('${p.name.replace(/'/g,"\\'")}')">📐 Medida especial</button>
        <button class="fa-close" onclick="toggleExp('${id}',event)">✕ Cerrar</button>
      </div>
    </div>`:'';
    return`<article class="card${isExp?' exp':''}" id="${id}" role="article">
      <div class="cimg" onclick="toggleExp('${id}',event)" role="button" tabindex="0" aria-label="Ver ficha de ${p.name}">
        ${imgHtml}
        ${bd?'<div class="badges">'+bd+'</div>':''}
        <button class="btn-add" onclick="addToCart(event,'${p.name.replace(/'/g,'&#39;')}')">+</button>
      </div>
      <div class="cbody">
        <h3 class="cname" onclick="toggleExp('${id}',event)">${p.name}</h3>
        <p class="csc">${p.sc}</p>
        ${!isExp?`<div class="sizes">${szCats}</div><div class="btns"><button class="btn-sec" onclick="toggleExp('${id}',event)">Ver ficha técnica ↓</button><button class="btn-main" onclick="cotizar('${p.name.replace(/'/g,"\\'")}')">Cotizar ahora</button></div>`:''}
      </div>
      ${ficha}
    </article>`;
  }).join('');
}

function cotizar(n){
  const m=encodeURIComponent('Hola Viveros Terra 🌿\n\nMe interesa cotizar: *'+n+'*\n¿Pueden darme precio y disponibilidad por tamaño?');
  window.open('https://wa.me/528333268008?text='+m,'_blank');
}
function solMedida(n){
  const m=encodeURIComponent('Hola Viveros Terra 🌿\n\nBusco *'+n+'* en una medida o tamaño especial.\n¿Pueden conseguirla o cotizarme?');
  window.open('https://wa.me/528333268008?text='+m,'_blank');
}
function solEsp(){
  const v=document.getElementById('solinput').value.trim();
  if(!v)return;
  const m=encodeURIComponent('Hola Viveros Terra 🌿\n\nBusco: *'+v+'*\nNo lo encontré en el catálogo. ¿Lo manejan o pueden cotizarme?');
  window.open('https://wa.me/528333268008?text='+m,'_blank');
}
function solPasto(){
  const v=document.getElementById('solpasto').value.trim();
  if(!v)return;
  const m=encodeURIComponent('Hola Viveros Terra 🌿\n\nMe interesa cotizar: *'+v+'*\n¿Pueden asesorarme?');
  window.open('https://wa.me/528333268008?text='+m,'_blank');
}
function openWA(){
  window.open('https://wa.me/528333268008?text='+encodeURIComponent('Hola Viveros Terra 🌿\n\nVi su catálogo y quisiera asesoría para mi jardín.'),'_blank');
}

render();

// =================== COTIZADOR ===================
let cart = []; // [{name, sc, emoji, sz, qty}]
let pendingPlant = null;

function addToCart(e, name) {
  e.stopPropagation();
  const plant = plants.find(p => p.name === name);
  if(plant) openAddModal(plant, e);
}

function openAddModal(plant, e) {
  if(e) e.stopPropagation();
  pendingPlant = plant;
  document.getElementById('modalTitle').textContent = plant.name;
  document.getElementById('modalSc').textContent = plant.sc;
  const sel = document.getElementById('modalSize');
  sel.innerHTML = plant.sz.map(s => `<option value="${s}">${s}</option>`).join('') + '<option value="__otro__">📐 Otro tamaño / Medida especial</option>';
  // Si ya está en carrito, preseleccionar el mismo tamaño
  const existing = cart.find(i => i.name === plant.name);
  if(existing) sel.value = existing.sz;
  document.getElementById('modalQty').value = existing ? existing.qty : 1;
  document.getElementById('modalOverlay').classList.add('open');
  document.getElementById('modalSize').focus();
}

function closeModal(e) {
  if(e && e.target !== document.getElementById('modalOverlay')) return;
  document.getElementById('modalOverlay').classList.remove('open');
  pendingPlant = null;
}

function onSizeChange(sel) {
  const row = document.getElementById('otroSizeRow');
  row.classList.toggle('visible', sel.value === '__otro__');
  if(sel.value === '__otro__') {
    setTimeout(()=>document.getElementById('otroSizeInput').focus(), 50);
  }
}

function changeQty(delta) {
  const inp = document.getElementById('modalQty');
  const val = Math.max(1, Math.min(9999, (parseInt(inp.value)||1) + delta));
  inp.value = val;
}

function confirmAdd() {
  if(!pendingPlant) return;
  const selVal = document.getElementById('modalSize').value;
  const sz = selVal === '__otro__'
    ? (document.getElementById('otroSizeInput').value.trim() || 'Medida especial')
    : selVal;
  const qty = Math.max(1, parseInt(document.getElementById('modalQty').value)||1);
  // Si ya existe misma planta+tamaño, actualizar cantidad
  const idx = cart.findIndex(i => i.name === pendingPlant.name && i.sz === sz);
  if(idx >= 0) {
    cart[idx].qty = qty;
  } else {
    cart.push({ name: pendingPlant.name, sc: pendingPlant.sc, emoji: pendingPlant.i, sz, qty });
  }
  document.getElementById('modalOverlay').classList.remove('open');
  pendingPlant = null;
  updateCartUI();
  // Feedback visual en la card
  const btn = document.querySelector(`[data-plant="${CSS.escape(cart[cart.length-1]?.name || '')}"]`);
  if(btn) btn.classList.add('added');
}

function updateCartUI() {
  const total = cart.reduce((s,i) => s+i.qty, 0);
  const fab = document.getElementById('cartFab');
  const badge = document.getElementById('cartBadge');
  badge.textContent = cart.length;
  fab.classList.toggle('visible', cart.length > 0);
  document.getElementById('cartHCount').textContent = cart.length > 0
    ? `${cart.length} variedad${cart.length>1?'es':''} · ${total} unidad${total>1?'es':''}`
    : '';
}

function openCart() {
  renderCartBody();
  document.getElementById('cartOverlay').classList.add('open');
  document.getElementById('cartPanel').classList.add('open');
}

function closeCart(e) {
  if(e && e.target !== document.getElementById('cartOverlay')) return;
  document.getElementById('cartOverlay').classList.remove('open');
  document.getElementById('cartPanel').classList.remove('open');
}

function renderCartBody() {
  const body = document.getElementById('cartBody');
  const footer = document.getElementById('cartFooter');
  if(cart.length === 0) {
    body.innerHTML = '<div class="cart-empty">Tu lista está vacía.<br><small>Toca el <strong>+</strong> en cualquier planta para agregarla.</small></div>';
    footer.style.display = 'none';
    document.getElementById('cartHCount').textContent = '';
    return;
  }
  const total = cart.reduce((s,i) => s+i.qty, 0);
  body.innerHTML = cart.map((item, idx) => `
    <div class="cart-item">
      <div class="cart-item-emoji">${item.emoji}</div>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-sz">${item.sz}</div>
      </div>
      <div class="cart-item-qty">
        <button class="cart-qty-btn" onclick="cartChangeQty(${idx},-1)" aria-label="Reducir">−</button>
        <span class="cart-qty-n">${item.qty}</span>
        <button class="cart-qty-btn" onclick="cartChangeQty(${idx},1)" aria-label="Aumentar">+</button>
      </div>
      <button class="cart-del" onclick="removeItem(${idx})" aria-label="Eliminar">✕</button>
    </div>
  `).join('');
  footer.style.display = 'block';
  document.getElementById('cartSummaryText').textContent = `${cart.length} variedad${cart.length>1?'es':''}`;
  document.getElementById('cartSummaryUnits').textContent = `${total} unidad${total>1?'es':''}`;
  document.getElementById('cartHCount').textContent = `${cart.length} variedad${cart.length>1?'es':''} · ${total} unidad${total>1?'es':''}`;
}

function cartChangeQty(idx, delta) {
  cart[idx].qty = Math.max(1, cart[idx].qty + delta);
  updateCartUI();
  renderCartBody();
}

function removeItem(idx) {
  cart.splice(idx, 1);
  updateCartUI();
  renderCartBody();
}

function clearCart() {
  if(!confirm('¿Vaciar toda la lista?')) return;
  cart = [];
  updateCartUI();
  renderCartBody();
  // Quitar clase added de todos los botones
  document.querySelectorAll('.btn-add.added').forEach(b => b.classList.remove('added'));
}

function sendWA() {
  if(cart.length === 0) return;
  const lines = cart.map(i => `• ${i.name} (${i.sz}) × ${i.qty}`).join('\n');
  const total = cart.reduce((s,i) => s+i.qty, 0);
  const msg = `Hola Viveros Terra 🌿\n\nQuisiera cotizar lo siguiente:\n\n${lines}\n\nTotal: ${cart.length} variedad${cart.length>1?'es':''}, ${total} unidad${total>1?'es':''}\n\n¿Pueden darme precio y disponibilidad?`;
  window.open('https://wa.me/528333268008?text=' + encodeURIComponent(msg), '_blank');
}

render();
