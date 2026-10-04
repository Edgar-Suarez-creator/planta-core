"""Propiedades obligatorias por clase de equipo.

Declaración de origen: la lista sigue el enfoque del diccionario CFIHOS 2.0 (clase de
equipo → propiedades requeridas con unidad), pero los nombres están en español y el mapeo a
los códigos oficiales CFIHOS está PENDIENTE. No se publican códigos que no se verificaron.
"""
from __future__ import annotations

COMUNES = [("fabricante", None), ("modelo", None), ("numero_serie", None)]

PROPIEDADES = {
    "P": COMUNES + [("caudal_nominal", "m3/h"), ("cabeza_nominal", "m"), ("potencia_motor", "kW"),
                    ("velocidad", "rpm"), ("material_carcasa", None)],
    "C": COMUNES + [("caudal_nominal", "MMSCFD"), ("presion_succion", "barg"), ("presion_descarga", "barg"),
                    ("potencia_motor", "kW"), ("velocidad", "rpm")],
    "V": COMUNES + [("presion_diseno", "barg"), ("temperatura_diseno", "°C"), ("volumen", "m3"),
                    ("material_cuerpo", None)],
    "E": COMUNES + [("carga_termica", "kW"), ("presion_diseno", "barg"), ("area_transferencia", "m2"),
                    ("tipo_tema", None)],
    "K": COMUNES + [("caudal_nominal", "m3/h"), ("presion_diferencial", "mbar"), ("potencia_motor", "kW")],
    "PCV": COMUNES + [("diametro", "in"), ("clase_ansi", None), ("cv", None), ("accion_falla", None)],
    "PT": COMUNES + [("rango_min", "barg"), ("rango_max", "barg"), ("salida", None)],
}


def obligatorias(tipo: str) -> list[str]:
    return [p for p, _ in PROPIEDADES[tipo]]


def unidad(tipo: str, prop: str) -> str | None:
    return dict(PROPIEDADES[tipo]).get(prop)
