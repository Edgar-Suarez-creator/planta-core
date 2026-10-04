"""Hojas de datos y manuales sintéticos, como texto paginado.

Simulan lo que en producción sale de PDFs del fabricante. Huecos inyectados de forma
controlada y registrados como etiqueta: ~12 % de los equipos sin hoja de datos y ~15 % de
las hojas con una propiedad obligatoria ausente. Fabricantes y modelos son ficticios.
"""
from __future__ import annotations

import random

from ..ontologia.clases import PROPIEDADES
from ..ontologia.iso14224 import MODOS, PERFIL_FALLAS
from ..planta import EQUIPOS
from ..tags import parse

FABRICANTES = {"P": "Bombas Andinas S.A.", "C": "Compresores del Valle", "V": "Calderería Industrial del Norte",
               "E": "Termotecnia Andina", "K": "Ventiladores Sabana", "PCV": "Válvulas Cordillera", "PT": "Instrumentos Magdalena"}

RANGOS = {
    "caudal_nominal": (5, 400), "cabeza_nominal": (20, 180), "potencia_motor": (4, 1500), "velocidad": (1200, 3600),
    "presion_succion": (20, 45), "presion_descarga": (60, 95), "presion_diseno": (5, 110), "temperatura_diseno": (60, 220),
    "volumen": (1, 120), "carga_termica": (50, 4000), "area_transferencia": (10, 600), "presion_diferencial": (50, 400),
    "diametro": (1, 8), "cv": (10, 600), "rango_min": (0, 0), "rango_max": (10, 120),
}
TEXTO = {"material_carcasa": ["acero al carbono", "acero inoxidable 316", "hierro dúctil"],
         "material_cuerpo": ["SA-516 Gr.70", "SA-240 316L"], "tipo_tema": ["AES", "BEM", "AKT"],
         "clase_ansi": ["150", "300", "600"], "accion_falla": ["falla abierta", "falla cerrada"], "salida": ["4-20 mA HART"]}

TAREAS = {
    "P": [("Inspección de fugas en sello mecánico", 7), ("Análisis de vibraciones", 30), ("Cambio de aceite de rodamientos", 180),
          ("Cambio de sello mecánico", 730)],
    "C": [("Análisis de vibraciones", 30), ("Inspección de válvulas de succión y descarga", 180), ("Cambio de filtro de aceite", 90),
          ("Overhaul de cilindros", 1460)],
    "V": [("Inspección visual externa", 90), ("Medición de espesores por UT", 730), ("Inspección interna", 1825)],
    "E": [("Limpieza de aletas o haz", 180), ("Prueba hidrostática", 1825)],
    "K": [("Tensión y cambio de correas", 90), ("Lubricación de rodamientos", 90)],
    "PCV": [("Prueba de carrera", 180), ("Cambio de empaquetadura", 730)],
    "PT": [("Calibración", 365), ("Verificación de lazo", 180)],
}


def _valor(prop: str, rng: random.Random):
    if prop in TEXTO:
        return rng.choice(TEXTO[prop])
    lo, hi = RANGOS[prop]
    return round(rng.uniform(lo, hi), 1) if hi > lo else lo


def generar_hojas(seed: int) -> tuple[list[dict], dict]:
    """Devuelve (documentos, etiqueta de huecos)."""
    rng = random.Random(seed + 1)
    docs, sin_hoja, faltantes = [], [], {}
    for tag, (desc, _s, _c, modelo) in EQUIPOS.items():
        tipo = parse(tag).tipo
        if rng.random() < 0.12:
            sin_hoja.append(tag)
            continue
        props = {}
        for prop, unidad in PROPIEDADES[tipo]:
            if prop == "fabricante":
                v = FABRICANTES[tipo]
            elif prop == "modelo":
                v = modelo
            elif prop == "numero_serie":
                v = f"SN-{rng.randrange(10**5, 10**6)}"
            else:
                v = _valor(prop, rng)
            props[prop] = (v, unidad)
        if rng.random() < 0.15:
            quitar = rng.choice([p for p in props if p not in ("fabricante", "modelo")])
            faltantes[tag] = [quitar]
            props.pop(quitar)
        comunes = [p for p in ("fabricante", "modelo", "numero_serie") if p in props]
        resto = [p for p in props if p not in comunes]
        linea = lambda p: f"{p.replace('_', ' ').capitalize()}: {props[p][0]}" + (f" {props[p][1]}" if props[p][1] else "")
        paginas = [
            f"HOJA DE DATOS DE EQUIPO\nTag: {tag}\nServicio: {desc}\n" + "\n".join(linea(p) for p in comunes),
            "DATOS DE DISEÑO Y OPERACIÓN\n" + "\n".join(linea(p) for p in resto),
        ]
        docs.append({"id": f"DS-{tag}", "tipo": "hoja_de_datos", "tag": tag, "paginas": paginas})
    return docs, {"sin_hoja": sorted(sin_hoja), "propiedades_faltantes": faltantes}


def generar_manuales() -> list[dict]:
    modelos: dict[str, str] = {}
    for tag, (_d, _s, _c, modelo) in EQUIPOS.items():
        modelos.setdefault(modelo, parse(tag).tipo)
    docs = []
    for modelo, tipo in sorted(modelos.items()):
        fab = FABRICANTES[tipo]
        tareas = "\n".join(f"- {t}: cada {d} días" for t, d in TAREAS[tipo])
        problemas = "\n".join(
            f"- Síntoma: {MODOS[m].lower()}. Revisar {comp}. Acción recomendada: inspeccionar y reemplazar {comp} si presenta daño."
            for m, _w, comp, _me, _ca in PERFIL_FALLAS[tipo])
        paginas = [
            f"MANUAL DE OPERACIÓN Y MANTENIMIENTO\nModelo {modelo} · {fab}\nDescripción general del equipo y de sus subunidades.",
            f"OPERACIÓN\nAntes de arrancar el modelo {modelo}, verificar alineación, nivel de lubricante y válvulas de bloqueo abiertas.",
            f"MANTENIMIENTO PREVENTIVO · modelo {modelo}\n{tareas}",
            f"SOLUCIÓN DE PROBLEMAS · modelo {modelo}\n{problemas}",
        ]
        docs.append({"id": f"MAN-{modelo}", "tipo": "manual", "modelo": modelo, "fabricante": fab, "paginas": paginas})
    return docs
