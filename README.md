# planta-core

Planta de referencia compartida por los ocho proyectos del portafolio: todos leen y escriben sobre los mismos
tags, de modo que el portafolio sea un sistema y no ocho ejercicios.

**Planta:** estación de compresión de gas con cuatro unidades · 1105 deshidratación con TEG · 1205 compresión ·
1305 aire de instrumentos · 1405 agua contra incendio. 39 equipos, 45 válvulas de bloqueo, 28 cadenas de línea.

**Tags ISA 5.1** `AREA-TIPO-NN` (ej. `1105-P-01`). Tipos: P bomba, C compresor, V recipiente, E intercambiador,
K soplador, PCV válvula de control, PT transmisor de presión, y HV válvula manual de bloqueo (extensión
declarada, necesaria para calcular aislamientos).

```
planta_core/
  tags.py                 formato, validación y normalización de tags mal escritos
  planta.py               áreas, sistemas, equipos y topología (cadenas de línea en sentido del flujo)
  ontologia/iso14224.py   jerarquía de 9 niveles, modos, mecanismos, causas, subunidades, perfil de fallas
  ontologia/clases.py     propiedades obligatorias por clase (enfoque CFIHOS 2.0)
  generadores/            historial de fallas, hojas de datos y manuales sintéticos
  generar.py              escribe datos/ con manifiesto SHA-256
datos/                    salidas versionadas (DVC pendiente: hoy van en git porque pesan < 1 MB)
```

```bash
python -m planta_core.generar          # semilla 14224 por defecto
python -m pytest -q
```

## Declaración de origen

| Dato | Origen |
|---|---|
| Topología, equipos, modelos | sintético, escrito a mano |
| Historial de fallas | sintético, semilla 14224 · 3–15 eventos por equipo crítico en 5 años (2021-10 a 2026-09) · 15 % de tags mal escritos a propósito |
| Pesos de modos de falla por clase | **supuestos** del autor; la norma dice qué modos aplican, no su frecuencia. Calibración contra OREDA pendiente |
| Hojas de datos y manuales | sintéticos · fabricantes ficticios · ~12 % de equipos sin hoja y ~15 % de hojas con una propiedad faltante, etiquetados en `datos/etiquetas_huecos.json` |
| Códigos ISO 14224 | públicos (norma); códigos de clase sin verificar quedan en `None` |
| Propiedades por clase | derivadas del enfoque CFIHOS; mapeo a códigos oficiales pendiente |
| Generadores de ITR y materiales | pendientes (proyectos 5 y 6) |
