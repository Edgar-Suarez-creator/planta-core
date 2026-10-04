"""Catálogos ISO 14224 usados como nodos (no como texto libre).

Contenido:
- Jerarquía taxonómica de nueve niveles.
- Códigos de modo de falla (subconjunto usado por las clases de la planta).
- Códigos de mecanismo y de causa de falla.
- Pesos de muestreo de modos por clase de equipo.

Declaración de origen: los códigos y sus nombres siguen la norma; los PESOS por clase son
SUPUESTOS del autor para el generador sintético (la norma define qué modos aplican, no su
frecuencia). La calibración contra OREDA queda pendiente y así se dice en el README.
"""
from __future__ import annotations

NIVELES = [
    (1, "Industria"),
    (2, "Categoría de negocio"),
    (3, "Instalación"),
    (4, "Planta/Unidad"),
    (5, "Sección/Sistema"),
    (6, "Unidad de equipo"),
    (7, "Subunidad"),
    (8, "Componente/Ítem mantenible"),
    (9, "Parte"),
]

MODOS = {
    "BRD": "Avería",
    "ELP": "Fuga externa de fluido de proceso",
    "ELU": "Fuga externa de fluido de servicio",
    "ERO": "Salida errática",
    "FTS": "Falla al arrancar",
    "FTO": "Falla al abrir",
    "FTC": "Falla al cerrar",
    "DOP": "Operación demorada",
    "HIO": "Salida alta",
    "LOO": "Salida baja",
    "INL": "Fuga interna",
    "IHT": "Transferencia de calor insuficiente",
    "NOI": "Ruido",
    "OHE": "Sobrecalentamiento",
    "PDE": "Desviación de parámetro",
    "PLU": "Taponamiento",
    "SER": "Problemas menores en servicio",
    "STD": "Deficiencia estructural",
    "UST": "Parada espuria",
    "VIB": "Vibración",
    "AIR": "Lectura anormal de instrumento",
    "OTH": "Otro",
}

MECANISMOS = {
    "1.1": "Fuga",
    "1.2": "Vibración",
    "1.3": "Holgura/desalineación",
    "1.6": "Agarrotamiento",
    "2.1": "Cavitación",
    "2.2": "Corrosión",
    "2.3": "Erosión",
    "2.4": "Desgaste",
    "2.6": "Fatiga",
    "2.7": "Sobrecalentamiento",
    "3.1": "Falla de control",
    "3.3": "Falla de señal",
    "4.3": "Sin energía",
    "5.1": "Bloqueo/taponamiento",
    "5.2": "Contaminación",
}

CAUSAS = {
    "1": "Relacionada con el diseño",
    "2": "Fabricación/instalación",
    "3": "Operación/mantenimiento",
    "4": "Gestión",
    "5": "Misceláneas",
}

# Clase de equipo por tipo de tag. `codigo` es el código de clase de la norma cuando el
# autor lo tiene verificado; None queda como pendiente de verificación.
CLASES = {
    "P": {"nombre": "Bomba centrífuga", "codigo": "PU"},
    "C": {"nombre": "Compresor", "codigo": "CO"},
    "V": {"nombre": "Recipiente", "codigo": "VE"},
    "E": {"nombre": "Intercambiador de calor", "codigo": "HE"},
    "K": {"nombre": "Soplador", "codigo": None},
    "PCV": {"nombre": "Válvula de control", "codigo": "VA"},
    "PT": {"nombre": "Transmisor de presión", "codigo": None},
}

# Subunidades e ítems mantenibles por clase (niveles 7 y 8).
SUBUNIDADES = {
    "P": {"Transmisión": ["acople", "rodamiento motor"], "Unidad de bombeo": ["sello mecánico", "impulsor", "rodamiento", "carcasa"],
          "Control y monitoreo": ["sensor de vibración"], "Lubricación": ["aceite", "visor de nivel"]},
    "C": {"Transmisión": ["acople", "caja multiplicadora"], "Unidad de compresión": ["válvula de succión", "válvula de descarga", "anillos de pistón", "empaquetadura"],
          "Control y monitoreo": ["sensor de vibración", "transmisor de temperatura"], "Lubricación": ["bomba de aceite", "filtro de aceite"]},
    "V": {"Recipiente": ["cuerpo", "boquilla", "internos", "demister"], "Instrumentación": ["visor de nivel"]},
    "E": {"Intercambiador": ["haz de tubos", "carcasa", "empaques", "aletas"]},
    "K": {"Transmisión": ["correas", "rodamiento"], "Soplador": ["rotor", "carcasa"]},
    "PCV": {"Válvula": ["cuerpo", "asiento", "empaquetadura"], "Actuador": ["diafragma", "posicionador"]},
    "PT": {"Instrumento": ["sensor", "electrónica", "manifold"]},
}

# (modo, peso, componente típico, mecanismo, causa). Pesos supuestos, ver docstring.
PERFIL_FALLAS = {
    "P": [("ELP", .24, "sello mecánico", "1.1", "3"), ("VIB", .16, "rodamiento", "1.2", "3"), ("LOO", .12, "impulsor", "2.4", "3"),
          ("FTS", .10, "acople", "4.3", "5"), ("OHE", .08, "rodamiento", "2.7", "3"), ("NOI", .07, "rodamiento", "2.4", "3"),
          ("ELU", .07, "visor de nivel", "1.1", "2"), ("PDE", .06, "impulsor", "2.1", "1"), ("BRD", .05, "acople", "2.6", "2"),
          ("SER", .05, "carcasa", "2.2", "5")],
    "C": [("UST", .20, "sensor de vibración", "3.3", "3"), ("VIB", .14, "acople", "1.3", "2"), ("ELP", .12, "empaquetadura", "1.1", "3"),
          ("FTS", .12, "bomba de aceite", "4.3", "5"), ("OHE", .10, "válvula de descarga", "2.7", "3"), ("PDE", .10, "válvula de succión", "2.4", "3"),
          ("NOI", .08, "anillos de pistón", "2.4", "3"), ("ELU", .08, "filtro de aceite", "1.1", "3"), ("BRD", .06, "caja multiplicadora", "2.6", "1")],
    "V": [("ELP", .32, "boquilla", "1.1", "2"), ("PLU", .24, "demister", "5.1", "3"), ("STD", .18, "cuerpo", "2.2", "5"),
          ("AIR", .16, "visor de nivel", "3.3", "3"), ("OTH", .10, "internos", "2.3", "5")],
    "E": [("PLU", .30, "haz de tubos", "5.1", "3"), ("IHT", .25, "aletas", "5.2", "3"), ("INL", .20, "haz de tubos", "2.2", "5"),
          ("ELP", .20, "empaques", "1.1", "3"), ("STD", .05, "carcasa", "2.2", "5")],
    "K": [("VIB", .30, "rodamiento", "1.2", "3"), ("NOI", .25, "correas", "2.4", "3"), ("FTS", .20, "correas", "4.3", "5"),
          ("OHE", .15, "rodamiento", "2.7", "3"), ("BRD", .10, "rotor", "2.6", "2")],
    "PCV": [("FTO", .22, "actuador", "1.6", "3"), ("FTC", .20, "asiento", "1.6", "3"), ("ELP", .20, "empaquetadura", "1.1", "3"),
            ("INL", .18, "asiento", "2.3", "5"), ("DOP", .10, "posicionador", "3.1", "3"), ("SER", .10, "diafragma", "2.4", "3")],
    "PT": [("AIR", .45, "sensor", "3.3", "5"), ("ERO", .35, "electrónica", "3.3", "5"), ("OTH", .20, "manifold", "1.1", "3")],
}
