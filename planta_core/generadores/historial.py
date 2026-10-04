"""Historial sintético de fallas (órdenes correctivas) de la planta de referencia.

Reglas del manual: entre 3 y 15 eventos por equipo crítico en cinco años; modos muestreados
de la distribución de la clase (ver ontologia/iso14224.PERFIL_FALLAS, pesos supuestos);
textos en el estilo corto de una orden real. Un 15 % de las órdenes trae el tag mal escrito
para ejercitar la normalización, con el tag verdadero guardado aparte como etiqueta.
"""
from __future__ import annotations

import random
from datetime import date, timedelta

from ..ontologia.iso14224 import PERFIL_FALLAS
from ..planta import EQUIPOS
from ..tags import parse

INICIO, FIN = date(2021, 10, 1), date(2026, 9, 30)

FLUIDO = {"1105": "GLICOL", "1205": "GAS", "1305": "AIRE", "1405": "AGUA"}
CORTO = {"P": "BBA", "C": "COMP", "V": "REC", "E": "INTERC", "K": "SOPL", "PCV": "VALV", "PT": "TX"}

SINTOMA = {
    "ELP": ["FUGA DE {fluido} POR {comp}", "GOTEO CONTINUO EN {comp}"],
    "ELU": ["FUGA DE ACEITE EN {comp}", "PERDIDA DE ACEITE POR {comp}"],
    "VIB": ["ALTA VIBRACION LADO {comp}", "VIBRACION FUERA DE LIMITE EN {comp}"],
    "LOO": ["BAJO CAUDAL, BAJA PRESION DE DESCARGA", "NO ENTREGA CAUDAL, REVISAR {comp}"],
    "HIO": ["SALIDA ALTA, REVISAR {comp}"],
    "FTS": ["NO ARRANCA, DISPARO EN ARRANQUE", "FALLA AL ARRANCAR, REVISAR {comp}"],
    "OHE": ["ALTA TEMPERATURA EN {comp}", "SOBRECALENTAMIENTO {comp}"],
    "NOI": ["RUIDO ANORMAL EN {comp}", "GOLPETEO EN {comp}"],
    "PDE": ["PARAMETRO FUERA DE RANGO EN {comp}"],
    "BRD": ["FALLA DE {comp}, EQUIPO FUERA DE SERVICIO"],
    "SER": ["DETALLE MENOR EN {comp}"],
    "UST": ["PARADA ESPURIA POR {comp}", "DISPARO SIN CAUSA DE PROCESO, {comp}"],
    "PLU": ["TAPONAMIENTO EN {comp}, ALTO DIFERENCIAL"],
    "STD": ["CORROSION EXTERNA EN {comp}"],
    "AIR": ["LECTURA ANORMAL EN {comp}", "INDICACION CONGELADA, {comp}"],
    "OTH": ["REVISION DE {comp} POR ANOMALIA"],
    "IHT": ["ALTA TEMPERATURA DE SALIDA, {comp} SUCIAS"],
    "INL": ["FUGA INTERNA POR {comp}"],
    "FTO": ["VALVULA NO ABRE, {comp} PEGADO"],
    "FTC": ["VALVULA NO CIERRA, {comp} DAÑADO"],
    "DOP": ["RESPUESTA LENTA, REVISAR {comp}"],
    "ERO": ["SEÑAL INESTABLE, {comp}"],
}
ACCION = {
    "ELP": ["SE CAMBIA {comp}", "SE AJUSTA {comp} Y SE PRUEBA SIN FUGA"],
    "ELU": ["SE CAMBIA EMPAQUE Y SE REPONE ACEITE", "SE AJUSTA {comp}"],
    "VIB": ["SE ALINEA Y SE CAMBIA {comp}", "SE BALANCEA Y SE CAMBIA {comp}"],
    "LOO": ["SE DESARMA, SE CAMBIA {comp}", "SE LIMPIA SUCCION Y SE CAMBIA {comp}"],
    "HIO": ["SE CALIBRA {comp}"],
    "FTS": ["SE REVISA {comp} Y ARRANQUE, SE NORMALIZA", "SE CAMBIA {comp}"],
    "OHE": ["SE CAMBIA {comp} Y SE LUBRICA", "SE LIMPIA Y SE CAMBIA {comp}"],
    "NOI": ["SE CAMBIA {comp}"],
    "PDE": ["SE INSPECCIONA Y SE CAMBIA {comp}"],
    "BRD": ["SE REEMPLAZA {comp}"],
    "SER": ["SE CORRIGE {comp}"],
    "UST": ["SE CAMBIA {comp} Y SE PRUEBA DISPARO"],
    "PLU": ["SE LIMPIA {comp}"],
    "STD": ["SE LIMPIA Y SE PINTA {comp}, SE PROGRAMA UT"],
    "AIR": ["SE CALIBRA {comp}", "SE CAMBIA {comp}"],
    "OTH": ["SE INSPECCIONA {comp}, SIN HALLAZGO"],
    "IHT": ["SE LAVA {comp}"],
    "INL": ["SE TAPONAN TUBOS, SE PROGRAMA CAMBIO DE {comp}"],
    "FTO": ["SE LIBERA Y SE LUBRICA {comp}"],
    "FTC": ["SE CAMBIA {comp}"],
    "DOP": ["SE CALIBRA {comp}"],
    "ERO": ["SE CAMBIA {comp}"],
}
# Horas-hombre medianas por modo (supuesto declarado); se muestrean con dispersión lognormal.
HORAS_BASE = {"BRD": 24, "ELP": 8, "ELU": 4, "VIB": 10, "LOO": 12, "HIO": 3, "FTS": 5, "OHE": 8, "NOI": 6, "PDE": 6,
              "SER": 2, "UST": 4, "PLU": 10, "STD": 16, "AIR": 2, "OTH": 3, "IHT": 14, "INL": 18, "FTO": 4, "FTC": 5,
              "DOP": 3, "ERO": 2}
CUADRILLA = {"P": "mecánica", "C": "mecánica", "V": "mecánica", "E": "mecánica", "K": "mecánica",
             "PCV": "instrumentación", "PT": "instrumentación"}


def tag_mal_escrito(tag: str, rng: random.Random) -> str:
    t = parse(tag)
    variantes = [
        f"{t.area}{t.tipo}{t.num}",
        f"{t.area}-{t.tipo.lower()}-{int(t.num)}",
        f"{t.area} {t.tipo} {t.num}",
        f"{t.area}-{t.tipo}-{t.num.replace('0', 'O')}",
        f"{t.area}_{t.tipo}_{t.num}",
        f"{t.area}-{t.tipo}-{t.num[0]}",  # número incompleto: debe ir al reporte de conflictos
    ]
    return rng.choice(variantes)


def generar(seed: int) -> list[dict]:
    rng = random.Random(seed)
    eventos = []
    dias = (FIN - INICIO).days
    for tag, (desc, _sist, critico, _modelo) in EQUIPOS.items():
        tipo = parse(tag).tipo
        n = rng.randint(3, 15) if critico else rng.randint(0, 3)
        perfil = PERFIL_FALLAS[tipo]
        for _ in range(n):
            modo, _w, comp, mec, causa = rng.choices(perfil, weights=[p[1] for p in perfil])[0]
            fecha = INICIO + timedelta(days=rng.randrange(dias))
            escrito = tag_mal_escrito(tag, rng) if rng.random() < 0.15 else tag
            fmt = {"fluido": FLUIDO[tag[:4]], "comp": comp.upper()}
            sintoma = rng.choice(SINTOMA[modo]).format(**fmt)
            accion = rng.choice(ACCION[modo]).format(**fmt)
            horas = round(HORAS_BASE[modo] * rng.lognormvariate(0, 0.35), 1)
            eventos.append({
                "tag_escrito": escrito, "tag": tag, "fecha": fecha.isoformat(), "tipo_orden": "correctiva",
                "modo": modo, "mecanismo": mec, "causa": causa, "componente": comp,
                "descripcion": f"{CORTO[tipo]} {escrito} - {sintoma}",
                "accion": accion, "horas": horas, "cuadrilla": CUADRILLA[tipo],
            })
    eventos.sort(key=lambda e: (e["fecha"], e["tag"]))
    for i, e in enumerate(eventos, 1):
        e["id"] = f"OT-{e['fecha'][:4]}-{i:05d}"
    return [{"id": e.pop("id"), **e} for e in eventos]
