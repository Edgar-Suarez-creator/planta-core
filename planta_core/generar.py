"""Genera los datos versionables de la planta de referencia en datos/.

Uso: python -m planta_core.generar [--seed 14224] [--salida datos]
La semilla por defecto (14224) está declarada en el README; misma semilla, mismos archivos.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import planta
from .generadores import documentos, historial
from .ontologia import clases, iso14224

SEMILLA = 14224


def topologia() -> dict:
    return {
        "areas": planta.AREAS,
        "sistemas": {k: {"area": a, "nombre": n} for k, (a, n) in planta.SISTEMAS.items()},
        "equipos": {t: {"descripcion": d, "sistema": s, "critico": c, "modelo": m, "tipo": planta.tipo_de(t)}
                    for t, (d, s, c, m) in planta.EQUIPOS.items()},
        "valvulas_bloqueo": planta.valvulas_bloqueo(),
        "instrumentos": planta.INSTRUMENTOS,
        "conexiones": planta.conexiones(),
    }


def catalogos() -> dict:
    return {"niveles": iso14224.NIVELES, "modos": iso14224.MODOS, "mecanismos": iso14224.MECANISMOS,
            "causas": iso14224.CAUSAS, "clases": iso14224.CLASES, "subunidades": iso14224.SUBUNIDADES,
            "propiedades_obligatorias": {k: [p for p, _ in v] for k, v in clases.PROPIEDADES.items()}}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=SEMILLA)
    ap.add_argument("--salida", default=str(Path(__file__).resolve().parents[1] / "datos"))
    a = ap.parse_args(argv)
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    hojas, huecos = documentos.generar_hojas(a.seed)
    archivos = {
        "topologia.json": topologia(),
        "catalogos_iso14224.json": catalogos(),
        "historial_fallas.json": historial.generar(a.seed),
        "documentos.json": hojas + documentos.generar_manuales(),
        "etiquetas_huecos.json": huecos,
    }
    manifiesto = []
    for nombre, contenido in archivos.items():
        texto = json.dumps(contenido, ensure_ascii=False, indent=1)
        (out / nombre).write_text(texto, encoding="utf-8")
        manifiesto.append(f"{hashlib.sha256(texto.encode()).hexdigest()}  {nombre}")
    (out / "MANIFEST.txt").write_text(f"semilla {a.seed}\n" + "\n".join(manifiesto) + "\n", encoding="utf-8")
    print(f"datos generados en {out} (semilla {a.seed})")
    print("\n".join(manifiesto))


if __name__ == "__main__":
    main()
