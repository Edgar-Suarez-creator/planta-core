"""Codificación de tags ISA 5.1 de la planta de referencia: AREA-TIPO-NN (ej. 1105-P-01).

Tipos del manual: P bomba, C compresor, V recipiente, E intercambiador, K soplador,
PCV válvula de control, PT transmisor de presión. Se añade HV (válvula manual de bloqueo),
necesaria para calcular aislamientos; es una extensión declarada, no parte del manual.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

TIPOS: dict[str, str] = {
    "P": "bomba",
    "C": "compresor",
    "V": "recipiente",
    "E": "intercambiador",
    "K": "soplador",
    "PCV": "válvula de control",
    "PT": "transmisor de presión",
    "HV": "válvula manual de bloqueo",
}

TAG_RE = re.compile(r"^(?P<area>\d{4})-(?P<tipo>[A-Z]{1,3})-(?P<num>\d{2})$")


@dataclass(frozen=True)
class Tag:
    area: str
    tipo: str
    num: str

    def __str__(self) -> str:
        return f"{self.area}-{self.tipo}-{self.num}"


def parse(tag: str) -> Tag:
    """Valida un tag canónico. Lanza ValueError si no cumple el formato."""
    m = TAG_RE.match(tag)
    if not m or m["tipo"] not in TIPOS:
        raise ValueError(f"tag fuera de formato ISA de la planta: {tag!r}")
    return Tag(m["area"], m["tipo"], m["num"])


def es_valido(tag: str) -> bool:
    try:
        parse(tag)
    except ValueError:
        return False
    return True


# Reglas de normalización para tags escritos a mano en órdenes y avisos.
# Orden de tipos de mayor a menor longitud para que "PCV" no se lea como "P".
_TIPOS_ORD = sorted(TIPOS, key=len, reverse=True)
_SUELTO_RE = re.compile(
    r"(?P<area>[0-9OIl]{4})\s*[-_./ ]?\s*(?P<tipo>" + "|".join(_TIPOS_ORD) + r")\s*[-_./ ]?\s*(?P<num>[0-9OIl]{1,2})(?![0-9A-Za-z])",
    re.IGNORECASE,
)
_DIGITOS = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1"})


def normalizar(texto: str) -> str | None:
    """Devuelve el primer tag canónico que aparezca en `texto`, o None.

    Corrige guiones faltantes o distintos, minúsculas, letra O por cero, I/l por uno
    y número de un dígito ("1105-p-1" -> "1105-P-01"). No inventa tags: si el área o el
    número no son legibles, devuelve None y el caso va al reporte de conflictos.
    """
    t = texto.replace("–", "-").replace("—", "-")
    for m in _SUELTO_RE.finditer(t):
        area = m["area"].translate(_DIGITOS)
        num = m["num"].translate(_DIGITOS)
        if not (area.isdigit() and num.isdigit()):
            continue
        cand = f"{area}-{m['tipo'].upper()}-{int(num):02d}"
        if es_valido(cand):
            return cand
    return None
