from planta_core import planta
from planta_core.generadores import documentos, historial
from planta_core.generar import SEMILLA, topologia
from planta_core.tags import es_valido, normalizar, parse


def test_tags_canonicos():
    assert parse("1105-P-01").tipo == "P"
    assert parse("1205-PCV-01").tipo == "PCV"
    assert not es_valido("1105-X-01")
    assert not es_valido("1105-P-1")


def test_normalizacion():
    assert normalizar("BBA 1105P01 fuga") == "1105-P-01"
    assert normalizar("1105-p-1") == "1105-P-01"
    assert normalizar("1205 PCV 01") == "1205-PCV-01"
    assert normalizar("1305-C-O2") == "1305-C-02"
    assert normalizar("1405_P_03") == "1405-P-03"
    assert normalizar("sin tag aquí") is None


def test_topologia_consistente():
    nodos = {n for cadena in planta.LINEAS for n in cadena}
    for tag in planta.EQUIPOS:
        assert es_valido(tag)
        if planta.tipo_de(tag) != "PT":
            assert tag in nodos, f"{tag} no aparece en ninguna línea"
    for n in nodos:
        assert n.startswith(("HDR-", "LIM-")) or es_valido(n)
    assert set(planta.INSTRUMENTOS) <= set(planta.EQUIPOS)
    assert len(topologia()["valvulas_bloqueo"]) > 30


def test_historial_reproducible_y_en_rango():
    a, b = historial.generar(SEMILLA), historial.generar(SEMILLA)
    assert a == b
    por_tag = {}
    for e in a:
        por_tag[e["tag"]] = por_tag.get(e["tag"], 0) + 1
    for tag, (_d, _s, critico, _m) in planta.EQUIPOS.items():
        n = por_tag.get(tag, 0)
        assert (3 <= n <= 15) if critico else (0 <= n <= 3)


def test_hojas_con_huecos_etiquetados():
    docs, huecos = documentos.generar_hojas(SEMILLA)
    con_hoja = {d["tag"] for d in docs}
    assert not con_hoja & set(huecos["sin_hoja"])
    assert set(huecos["propiedades_faltantes"]) <= con_hoja
