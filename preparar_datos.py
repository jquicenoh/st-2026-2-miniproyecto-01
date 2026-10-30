from pathlib import Path

import pandas as pd

# Ubicación de la carpeta donde está este programa
RAIZ = Path(__file__).resolve().parent

# Ubicación del Excel original
archivo_excel = (
    RAIZ / "datos" / "anex-EMC-ComercioMinorista-ago2026.xlsx"
)

# Leer la hoja de índices de ventas reales
tabla = pd.read_excel(
    archivo_excel,
    sheet_name="2.2",
    header=7
)

# Quitar espacios al inicio y al final de los encabezados
tabla.columns = tabla.columns.astype(str).str.strip()

# Seleccionar año, mes e índice de prendas de vestir y textiles
datos = tabla[
    ["Año", "Mes", "4. Prendas de vestir y textiles"]
].copy()

# Mostrar las primeras filas en la terminal
print(datos.head(15).to_string(index=False))

# Completar el año con el último año disponible
datos["Año"] = pd.to_numeric(
    datos["Año"],
    errors="coerce"
).ffill()

# Relacionar cada nombre de mes con su número
meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

# Limpiar los nombres de los meses y obtener su número
datos["numero_mes"] = (
    datos["Mes"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(meses)
)

# Conservar solamente las filas correspondientes a meses
datos = datos.loc[datos["numero_mes"].notna()].copy()

print("\nDatos con año completo y mes numérico:")
print(datos.head(15).to_string(index=False))

# Crear una fecha para cada mes
datos["fecha"] = pd.to_datetime({
    "year": datos["Año"].astype(int),
    "month": datos["numero_mes"].astype(int),
    "day": 1
})

# Convertir el índice de ventas a valores numéricos
datos["indice_ventas"] = pd.to_numeric(
    datos["4. Prendas de vestir y textiles"],
    errors="raise"
)

# Conservar únicamente fecha e índice, ordenados por fecha
serie_final = (
    datos[["fecha", "indice_ventas"]]
    .sort_values("fecha")
    .reset_index(drop=True)
)

# Comprobar la estructura antes de guardar
assert not serie_final["fecha"].duplicated().any(), "Hay fechas duplicadas"
assert not serie_final["indice_ventas"].isna().any(), "Hay ventas faltantes"

fechas_esperadas = pd.date_range(
    start=serie_final["fecha"].min(),
    end=serie_final["fecha"].max(),
    freq="MS"
)

assert pd.DatetimeIndex(serie_final["fecha"]).equals(
    fechas_esperadas
), "La serie tiene meses faltantes"

# Guardar la serie en un archivo CSV
archivo_csv = RAIZ / "datos" / "prendas_vestir.csv"

serie_final.to_csv(
    archivo_csv,
    index=False,
    date_format="%Y-%m-%d"
)

# Mostrar el resultado
print("\nPrimeras cinco filas:")
print(serie_final.head().to_string(index=False))

print("\nÚltimas cinco filas:")
print(serie_final.tail().to_string(index=False))

print("\nTotal de meses:", len(serie_final))
print("Archivo generado:", archivo_csv.name)