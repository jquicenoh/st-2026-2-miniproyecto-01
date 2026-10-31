# datos

# Datos del proyecto

## Descripción de la serie

Se utiliza el índice mensual de ventas reales de prendas de vestir y
textiles, total nacional, publicado por el Departamento Administrativo
Nacional de Estadística (DANE) en la Encuesta Mensual de Comercio (EMC).

El índice tiene base 2019 = 100 y representa la evolución relativa de
las ventas a precios constantes. No representa cantidades de prendas
ni ingresos expresados en pesos.

| Campo | Valor |
|---|---|
| Archivo utilizado por el análisis | `prendas_vestir.csv` |
| Qué mide | Índice de ventas reales de prendas de vestir y textiles, total nacional, base 2019 = 100. |
| Fuente | DANE — Encuesta Mensual de Comercio (EMC), anexo de agosto de 2026. |
| Archivo original | `anex-EMC-ComercioMinorista-ago2026.xlsx` |
| Hoja del Excel | `2.2` |
| Columna del Excel | `4. Prendas de vestir y textiles` |
| Condiciones de uso | Términos y condiciones generales del DANE; se conserva la atribución de la fuente. |
| Frecuencia | Mensual; fechas al inicio de cada mes (`MS`). |
| Periodo | Enero de 2019 a agosto de 2026. |
| Número de observaciones | 92 |
| Columna de fecha | `fecha` |
| Columna que se pronostica | `indice_ventas` |
| Unidad | Puntos del índice. |
| Periodo estacional utilizado | 12 meses. |

## Fuente y condiciones de uso

- [DANE — EMC, información histórica](https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/encuesta-mensual-de-comercio-emc/encuesta-mensual-de-comercio-emc-historicos).
- [Anexo EMC de agosto de 2026](https://www.dane.gov.co/files/operaciones/EMC/anex-EMC-ComercioMinorista-ago2026.xlsx).
- [Términos y condiciones del DANE](https://www.dane.gov.co/index.php/en/terrminos-y-condiciones-dane).

Se remite a las condiciones generales de uso del DANE, sin atribuir una
licencia Creative Commons específica al archivo.

**Atribución:** Fuente: Departamento Administrativo Nacional de
Estadística: www.dane.gov.co

## Preparación del CSV

El programa `preparar_datos.py`, ubicado en la carpeta principal del
proyecto, realiza los siguientes pasos:

1. Lee la hoja `2.2` del Excel original.
2. Elimina espacios al inicio y al final de los encabezados.
3. Selecciona las columnas de año, mes e índice de ventas.
4. Completa las etiquetas de año de las filas intermedias con el último
   año disponible.
5. Convierte los nombres de los meses a números.
6. Conserva las filas correspondientes a meses y construye sus fechas.
7. Convierte el índice de ventas a valores numéricos.
8. Ordena las observaciones por fecha.
9. Comprueba que no existan fechas duplicadas, ventas faltantes ni meses
   ausentes entre la primera y la última observación.
10. Exporta `prendas_vestir.csv`, con las columnas `fecha` e `indice_ventas`.

Completar las etiquetas de año no implica imputar valores de ventas.

Para regenerar el CSV, ejecutar desde la carpeta principal:

    python preparar_datos.py

El Excel original debe encontrarse en esta carpeta `datos/`.

## Calidad y tratamiento de los datos

La serie preparada contiene 92 observaciones mensuales consecutivas,
sin valores faltantes de ventas ni fechas duplicadas.

Se conservan todas las observaciones, incluidos los máximos estacionales
recurrentes y la caída excepcional de 2020. No se imputan, eliminan,
recortan ni sustituyen valores observados.

La función `preparar` de `miniproyecto.py` comprueba la ausencia de
valores faltantes y devuelve una copia de la serie original.

La decisión registrada en la tabla de métricas es:

> Sin huecos: no se imputa. Se conservan todas las observaciones,
> incluidos los picos estacionales y la caída excepcional de 2020.

## Serie de ejemplo del repositorio base

El archivo `air_passengers.csv`, si permanece en esta carpeta,
corresponde al ejemplo del curso y no se utiliza en este proyecto.
El análisis de `miniproyecto.py` utiliza exclusivamente
`prendas_vestir.csv`.

## Informe

El análisis y los resultados se presentan en
[el informe del miniproyecto](../docs/informe.md).