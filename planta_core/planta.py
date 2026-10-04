"""Planta de referencia: estación de compresión de gas con cuatro unidades.

1105 Deshidratación con TEG · 1205 Compresión · 1305 Aire de instrumentos · 1405 Agua contra incendio.

La topología se declara como cadenas de línea (en el sentido del flujo). Cada elemento de una
cadena es un tag de equipo o válvula, un cabezal (HDR-…) o un límite de batería (LIM-…).
Este módulo es la fuente de verdad que en el proyecto 2 saldrá del P&ID digitalizado; aquí
está escrita a mano y es el insumo DEXPI-equivalente del proyecto 1.
"""
from __future__ import annotations

from .tags import parse

AREAS = {
    "1105": "Deshidratación con glicol (TEG)",
    "1205": "Compresión de gas",
    "1305": "Aire de instrumentos",
    "1405": "Agua contra incendio",
}

SISTEMAS = {
    "1105-S01": ("1105", "Separación de entrada"),
    "1105-S02": ("1105", "Contacto con glicol"),
    "1105-S03": ("1105", "Regeneración de glicol"),
    "1205-S01": ("1205", "Compresión de gas"),
    "1205-S02": ("1205", "Aceite de lubricación"),
    "1305-S01": ("1305", "Generación de aire"),
    "1305-S02": ("1305", "Secado de aire"),
    "1405-S01": ("1405", "Bombeo contra incendio"),
}

# tag: (descripción, sistema, crítico, modelo)
EQUIPOS: dict[str, tuple[str, str, bool, str | None]] = {
    "1105-V-01": ("Separador de entrada", "1105-S01", True, "SEP-H-1800"),
    "1105-PT-01": ("Transmisor de presión del separador de entrada", "1105-S01", False, "PTX-3051"),
    "1105-V-02": ("Torre contactora de TEG", "1105-S02", True, "TC-24"),
    "1105-PT-02": ("Transmisor de presión de la contactora", "1105-S02", False, "PTX-3051"),
    "1105-E-02": ("Enfriador de glicol pobre", "1105-S02", False, "AC-G40"),
    "1105-PCV-01": ("Válvula de control de presión del tanque flash", "1105-S03", False, "CV-2-300"),
    "1105-V-03": ("Tanque flash de glicol rico", "1105-S03", False, "FT-6"),
    "1105-E-01": ("Intercambiador glicol rico / glicol pobre", "1105-S03", True, "HX-GG-120"),
    "1105-V-04": ("Rehervidor de glicol", "1105-S03", True, "RB-350"),
    "1105-V-05": ("Acumulador de glicol pobre", "1105-S03", False, "AC-8"),
    "1105-P-01": ("Bomba de glicol pobre A", "1105-S03", True, "BCA-50-200"),
    "1105-P-02": ("Bomba de glicol pobre B", "1105-S03", True, "BCA-50-200"),
    "1205-V-01": ("Depurador de succión", "1205-S01", True, "SCR-36"),
    "1205-PT-01": ("Transmisor de presión de succión", "1205-S01", False, "PTX-3051"),
    "1205-C-01": ("Compresor reciprocante A", "1205-S01", True, "RC-2400"),
    "1205-C-02": ("Compresor reciprocante B", "1205-S01", True, "RC-2400"),
    "1205-PCV-01": ("Válvula de reciclo de compresión", "1205-S01", False, "CV-4-600"),
    "1205-E-01": ("Aeroenfriador de descarga", "1205-S01", True, "AC-D90"),
    "1205-V-02": ("Depurador de descarga", "1205-S01", False, "SCR-30"),
    "1205-PT-02": ("Transmisor de presión de descarga", "1205-S01", False, "PTX-3051"),
    "1205-V-03": ("Tanque de aceite de lubricación", "1205-S02", False, "TK-LO-2"),
    "1205-P-01": ("Bomba de aceite de lubricación A", "1205-S02", True, "BEN-25"),
    "1205-P-02": ("Bomba de aceite de lubricación B", "1205-S02", True, "BEN-25"),
    "1205-E-02": ("Enfriador de aceite de lubricación", "1205-S02", False, "HX-LO-15"),
    "1305-C-01": ("Compresor de aire de tornillo A", "1305-S01", True, "SA-75"),
    "1305-C-02": ("Compresor de aire de tornillo B", "1305-S01", True, "SA-75"),
    "1305-E-01": ("Posenfriador de aire", "1305-S01", True, "AC-A12"),
    "1305-V-01": ("Pulmón de aire húmedo", "1305-S01", False, "RV-3"),
    "1305-V-02": ("Torre secadora A", "1305-S02", True, "DS-400"),
    "1305-V-03": ("Torre secadora B", "1305-S02", True, "DS-400"),
    "1305-K-01": ("Soplador de regeneración del secador", "1305-S02", False, "BL-15"),
    "1305-V-04": ("Pulmón de aire seco", "1305-S02", False, "RV-5"),
    "1305-PT-01": ("Transmisor de presión del cabezal de aire", "1305-S02", False, "PTX-3051"),
    "1405-V-01": ("Tanque de agua contra incendio", "1405-S01", True, "TK-FW-900"),
    "1405-P-01": ("Bomba contra incendio eléctrica", "1405-S01", True, "BCI-1500"),
    "1405-P-02": ("Bomba contra incendio diésel", "1405-S01", True, "BCI-1500D"),
    "1405-P-03": ("Bomba jockey", "1405-S01", True, "BJ-10"),
    "1405-PCV-01": ("Válvula de alivio de presión de la red", "1405-S01", False, "CV-3-150"),
    "1405-PT-01": ("Transmisor de presión de la red contra incendio", "1405-S01", False, "PTX-3051"),
}

# Instrumento → equipo que mide (relación de medición, no de proceso).
INSTRUMENTOS = {
    "1105-PT-01": "1105-V-01",
    "1105-PT-02": "1105-V-02",
    "1205-PT-01": "1205-V-01",
    "1205-PT-02": "1205-V-02",
    "1305-PT-01": "1305-V-04",
    "1405-PT-01": "1405-P-03",
}

LINEAS: list[list[str]] = [
    # 1105 · gas
    ["LIM-GAS-ENTRADA", "1105-HV-01", "1105-V-01", "1105-HV-02", "1105-V-02", "1105-HV-03", "1205-HV-01"],
    # 1105 · glicol rico → regeneración → glicol pobre
    ["1105-V-02", "1105-HV-05", "1105-PCV-01", "1105-V-03", "1105-HV-06", "1105-E-01", "1105-HV-07", "1105-V-04",
     "1105-V-05", "1105-HV-08", "1105-E-01", "1105-HV-04", "HDR-1105-SUC"],
    ["HDR-1105-SUC", "1105-HV-09", "1105-P-01", "1105-HV-10", "HDR-1105-DES"],
    ["HDR-1105-SUC", "1105-HV-11", "1105-P-02", "1105-HV-12", "HDR-1105-DES"],
    ["HDR-1105-DES", "1105-E-02", "1105-HV-13", "1105-V-02"],
    # 1205 · gas
    ["1205-HV-01", "1205-V-01", "HDR-1205-SUC"],
    ["HDR-1205-SUC", "1205-HV-02", "1205-C-01", "1205-HV-03", "HDR-1205-DES"],
    ["HDR-1205-SUC", "1205-HV-04", "1205-C-02", "1205-HV-05", "HDR-1205-DES"],
    ["HDR-1205-DES", "1205-E-01", "1205-V-02", "1205-HV-06", "LIM-GAS-EXPORTACION"],
    ["HDR-1205-DES", "1205-PCV-01", "1205-HV-07", "HDR-1205-SUC"],
    # 1205 · aceite de lubricación
    ["1205-V-03", "1205-HV-08", "1205-P-01", "1205-HV-09", "HDR-1205-ACE"],
    ["1205-V-03", "1205-HV-11", "1205-P-02", "1205-HV-12", "HDR-1205-ACE"],
    ["HDR-1205-ACE", "1205-E-02", "1205-HV-10", "1205-V-03"],
    # 1305 · aire
    ["LIM-ATM-1305-A", "1305-C-01", "1305-HV-01", "HDR-1305-AH"],
    ["LIM-ATM-1305-B", "1305-C-02", "1305-HV-02", "HDR-1305-AH"],
    ["HDR-1305-AH", "1305-E-01", "1305-V-01", "1305-HV-03", "HDR-1305-SEC"],
    ["HDR-1305-SEC", "1305-HV-04", "1305-V-02", "1305-HV-05", "HDR-1305-SECO"],
    ["HDR-1305-SEC", "1305-HV-06", "1305-V-03", "1305-HV-07", "HDR-1305-SECO"],
    ["HDR-1305-SECO", "1305-V-04", "1305-HV-08", "LIM-CABEZAL-AIRE"],
    ["LIM-ATM-1305-K", "1305-K-01", "1305-HV-09", "HDR-1305-REG"],
    ["HDR-1305-REG", "1305-HV-10", "1305-V-02"],
    ["HDR-1305-REG", "1305-HV-11", "1305-V-03"],
    # 1405 · agua contra incendio
    ["LIM-AGUA-CRUDA", "1405-HV-09", "1405-V-01", "HDR-1405-SUC"],
    ["HDR-1405-SUC", "1405-HV-01", "1405-P-01", "1405-HV-02", "HDR-1405-DES"],
    ["HDR-1405-SUC", "1405-HV-03", "1405-P-02", "1405-HV-04", "HDR-1405-DES"],
    ["HDR-1405-SUC", "1405-HV-05", "1405-P-03", "1405-HV-06", "HDR-1405-DES"],
    ["HDR-1405-DES", "1405-HV-07", "LIM-RED-CI"],
    ["HDR-1405-DES", "1405-PCV-01", "1405-HV-08", "1405-V-01"],
]


def tipo_de(nodo: str) -> str:
    """'HDR', 'LIM' o el tipo ISA del tag."""
    if nodo.startswith(("HDR-", "LIM-")):
        return nodo[:3]
    return parse(nodo).tipo


def valvulas_bloqueo() -> list[str]:
    vistos = {n for cadena in LINEAS for n in cadena}
    return sorted(n for n in vistos if not n.startswith(("HDR-", "LIM-")) and tipo_de(n) == "HV")


def conexiones() -> list[tuple[str, str]]:
    """Aristas dirigidas en el sentido del flujo, sin duplicados."""
    vistas: list[tuple[str, str]] = []
    for cadena in LINEAS:
        for a, b in zip(cadena, cadena[1:]):
            if (a, b) not in vistas:
                vistas.append((a, b))
    return vistas
