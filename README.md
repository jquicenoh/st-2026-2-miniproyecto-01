[informe.md](https://github.com/user-attachments/files/34201793/informe.md)
# Miniproyecto 1 — De las líneas base al mejor modelo clásico

**Pronóstico de Series Temporales con IA**  
**Universidad Autónoma de Occidente · 2026-II**

## Integrantes

Grupo de dos integrantes autorizado por el docente.

| Nombre completo | Código | Correo institucional |
|---|---|---|
| Jessica Quiceno Henao | Pendiente de completar | jessica.quiceno@uao.edu.co |
| Melissa Muñoz Buitrón | Pendiente de completar | melissa.munoz@uao.edu.co |

## Objetivo

Analizar una serie mensual de ventas, identificar sus componentes y comparar
dos líneas base con modelos SARIMA y SARIMAX mediante el backtest común del curso.

## Serie utilizada

Índice mensual de ventas reales de prendas de vestir y textiles, total nacional,
de la Encuesta Mensual de Comercio del DANE, con base 2019 = 100.

- **Periodo:** enero de 2019–agosto de 2026.
- **Observaciones:** 92.
- **Frecuencia:** mensual.
- **Periodo estacional:** 12 meses.
- **Archivo preparado:** `datos/prendas_vestir.csv`.
- **Tratamiento:** se conservan todas las observaciones; no se imputan valores,
  no se eliminan los picos estacionales ni la caída excepcional de 2020.

La fuente, las condiciones de uso y la preparación se documentan en
[datos/README.md](datos/README.md).

## Instalación y ejecución

Ejecutar los siguientes comandos desde la carpeta principal del proyecto.

### 1. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 2. Preparar la serie desde el Excel original

El archivo `anex-EMC-ComercioMinorista-ago2026.xlsx` debe estar en `datos/`.

```bash
python preparar_datos.py
```

Este comando genera `datos/prendas_vestir.csv`. Si el CSV preparado ya está
disponible y actualizado, puede omitirse este paso.

### 3. Ejecutar el análisis

```bash
python miniproyecto.py
```

El programa genera las figuras principales en `figuras/` y los resultados
numéricos en `resultados/`.

## Archivos principales

| Archivo o carpeta | Contenido |
|---|---|
| `preparar_datos.py` | Extracción del Excel, validación y generación del CSV. |
| `miniproyecto.py` | Análisis, identificación, ajuste y evaluación de modelos. |
| `comun.py` | Carga, métricas, líneas base y backtest del curso; se conserva sin modificaciones. |
| `requirements.txt` | Dependencias necesarias para ejecutar el proyecto. |
| `datos/` | Excel original, CSV preparado y documentación de la fuente. |
| `figuras/` | Gráficas del análisis. |
| `resultados/` | Resultados ADF, rejilla SARIMA, Ljung–Box, exógenas y métricas. |
| `docs/informe.md` | Informe completo con las siete secciones solicitadas. |

## Evaluación y resultados

Se utilizó el backtest del curso con `n_prueba=24` y `h=12`: produce 13
orígenes de entrenamiento expansivo y 12 pronósticos por origen. Los meses
evaluados abarcan septiembre de 2024–agosto de 2026, con ventanas superpuestas.

Las métricas finales son el promedio de las métricas calculadas en cada origen.

| Modelo | RMSE | MAE | MAPE (%) |
|---|---:|---:|---:|
| **Estacional ingenuo** | **6,26** | **5,54** | **4,87** |
| SARIMA(0,1,0)(1,1,1,12) | 8,54 | 7,30 | 7,29 |
| SARIMAX(0,1,0)(1,1,1,12) + festivos | 8,56 | 7,31 | 7,30 |
| Ingenuo | 63,08 | 38,41 | 30,10 |

RMSE y MAE se expresan en puntos del índice; MAPE, en porcentaje.

El estacional ingenuo obtuvo los menores errores en las tres métricas.
SARIMA y SARIMAX no superaron esta línea base. Incorporar el número mensual
de festivos no mejoró al SARIMA en esta evaluación.

## Alcance y limitaciones

La elección de diferencias y órdenes utilizó la serie completa antes del
backtest, por lo que la comparación es exploratoria. En cada origen se
reajustan los parámetros utilizando únicamente las ventas del entrenamiento.

ADF no permitió confirmar estacionariedad al 5 % y Ljung–Box detectó
autocorrelación residual en el SARIMA seleccionado. Estas limitaciones se
analizan en el informe.

## Informe completo

[Consultar el informe del miniproyecto](docs/informe.md)

## Fuente

Departamento Administrativo Nacional de Estadística — DANE.
Encuesta Mensual de Comercio, anexo de agosto de 2026, hoja 2.2,
columna «4. Prendas de vestir y textiles».

Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co