"""Miniproyecto 1: la serie del grupo, de las líneas base al mejor modelo clásico.

Se corre de principio a fin con

    python miniproyecto.py

y deja las figuras en figuras/ y la tabla en resultados/metricas.csv. Las
partes marcadas con TODO las completa el grupo; mientras falten, el guion las
reporta como pendientes y sigue. El informe, docs/informe.md, cita las cifras
y las figuras que produce este guion.
"""
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import holidays

from comun import (RAIZ, backtest, cargar_serie, estacional_ingenuo,  # noqa: E402
                   fechas_siguientes, ingenuo)

from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
FIGURAS = RAIZ / "figuras"
RESULTADOS = RAIZ / "resultados"
FIGURAS.mkdir(exist_ok=True)
RESULTADOS.mkdir(exist_ok=True)

# ============================================================
# 1. La serie
# ============================================================
# Cambie estos cuatro datos por los de la serie del grupo y documente la
# fuente en datos/README.md. La serie de ejemplo solo sirve para probar que
# el guion corre.
ARCHIVO = "datos/prendas_vestir.csv"
FECHA = "fecha"
VALOR = "indice_ventas"
PERIODO = 12

# Lo que se hizo con los huecos y con los datos atípicos, en una línea. Va
# a la columna `decision` de la tabla de métricas.
DECISION = (
    "Sin huecos: no se imputa. Se conservan todas las observaciones, "
    "incluidos los picos estacionales y la caída excepcional de 2020."
)


def preparar(serie):
    """Conservar la serie original y comprobar que no tenga valores faltantes."""
    if serie.isna().any():
        raise ValueError(
            "La serie contiene valores faltantes; revise la fuente."
        )

    return serie.copy()


def graficar_serie(serie):
    figura, eje = plt.subplots(figsize=(9, 3.4))
    eje.plot(serie.index, serie.to_numpy())
    eje.set_title(f"{VALOR}: serie mensual")
    eje.set_ylabel(VALOR)
    figura.tight_layout()
    figura.savefig(FIGURAS / "serie.png", dpi=120)
    plt.close(figura)


# ============================================================
# 2. Descomposición
# ============================================================

def descomponer(serie):
    """Descomponer la serie mediante STL robusta y guardar la figura."""

    # Separar tendencia, estacionalidad y residuo.
    resultado = STL(
        serie,
        period=PERIODO,
        robust=True
    ).fit()

    # Crear la gráfica de los componentes.
    figura = resultado.plot()
    figura.set_size_inches(10, 8)

    figura.axes[0].set_title(
        "Descomposición STL del índice de ventas de prendas de vestir"
    )

    # Identificar los componentes en español.
    etiquetas = [
        "Serie observada",
        "Tendencia",
        "Estacionalidad",
        "Residuo"
    ]

    for eje, etiqueta in zip(figura.axes, etiquetas):
        eje.set_ylabel(etiqueta)

    figura.tight_layout()

    # Guardar y cerrar la figura.
    figura.savefig(FIGURAS / "stl.png", dpi=150)
    plt.close(figura)

    print("Descomposición STL guardada en figuras/stl.png")

     # Promedio del componente estacional por mes calendario.
    estacionalidad = resultado.seasonal.groupby(
        resultado.seasonal.index.month
    ).mean()
    estacionalidad.index.name = "mes"

    print("\nEstacionalidad promedio por mes (puntos del índice):")
    print(estacionalidad.to_string(float_format=lambda x: f"{x:.3f}"))

    # Mayor residuo en magnitud absoluta, conservando su signo.
    fecha_extrema = resultado.resid.abs().idxmax()
    residuo_extremo = resultado.resid.loc[fecha_extrema]

    print(
        "\nMayor residuo absoluto de STL: "
        f"{fecha_extrema:%Y-%m}, "
        f"residuo = {residuo_extremo:.3f} puntos del índice"
    )


# ============================================================
# 3. Estacionariedad e identificación
# ============================================================

def estacionariedad(serie):
    """Evaluar la serie original y tres combinaciones de diferencias."""

    # Serie, diferencia regular, estacional y ambas.
    versiones = [
        ("Original", serie, 0, 0, "ct"),
        ("Diferencia regular", serie.diff(), 1, 0, "c"),
        ("Diferencia estacional", serie.diff(PERIODO), 0, 1, "c"),
        (
            "Ambas diferencias",
            serie.diff(PERIODO).diff(),
            1, 1, "c"
        )
    ]

    filas = []

    for nombre, datos, d, D, regresion in versiones:
        # Las diferencias generan valores iniciales vacíos.
        datos = datos.dropna()

        resultado = adfuller(
            datos,
            regression=regresion,
            autolag="AIC"
        )

        filas.append({
            "version": nombre,
            "d": d,
            "D": D,
            "regresion": regresion,
            "meses": len(datos),
            "ADF": resultado[0],
            "valor_p": resultado[1],
            "rezagos_ADF": resultado[2]
        })

    tabla = pd.DataFrame(filas)

    print("\nResultados de la prueba ADF:")
    print(
        tabla.to_string(
            index=False,
            float_format=lambda valor: f"{valor:.6f}"
        )
    )

    # Guardar los resultados para documentarlos.
    tabla.to_csv(RESULTADOS / "adf.csv", index=False)

 # Comparar las cuatro versiones y sus autocorrelaciones.
    figura, ejes = plt.subplots(
        4, 2,
        figsize=(12, 11)
    )

    for fila, (nombre, datos, d, D, regresion) in enumerate(versiones):
        datos = datos.dropna()

        # Columna izquierda: comportamiento de la serie.
        ejes[fila, 0].plot(
            datos.index,
            datos.to_numpy(),
            linewidth=1
        )

        ejes[fila, 0].set_title(
            f"{nombre}: d={d}, D={D}"
        )

        ejes[fila, 0].set_ylabel("Puntos del índice")
        ejes[fila, 0].grid(alpha=0.25)

        # Columna derecha: autocorrelaciones hasta tres años.
        plot_acf(
            datos,
            lags=36,
            zero=False,
            ax=ejes[fila, 1]
        )

        ejes[fila, 1].set_title(
            f"ACF: {nombre}"
        )

        ejes[fila, 1].set_xlabel("Rezago en meses")

    figura.tight_layout()

    figura.savefig(
        FIGURAS / "diagnostico_diferencias.png",
        dpi=150
    )

    plt.close(figura)

     # Elección provisional basada en ADF y diagnóstico gráfico.
    d = 1
    D = 1

    # Aplicar una diferencia estacional y una regular.
    serie_elegida = (
        serie
        .diff(PERIODO)
        .diff()
        .dropna()
    )

    print(f"\nElección provisional: d={d}, D={D}")
    print(
        "ADF no rechaza raíz unitaria al 5 %; "
        "se continuará con diagnóstico de modelos."
    )

    # Graficar ACF y PACF de la serie diferenciada.
    figura, ejes = plt.subplots(
        2, 1,
        figsize=(10, 7)
    )

    plot_acf(
        serie_elegida,
        lags=36,
        zero=False,
        ax=ejes[0]
    )

    plot_pacf(
        serie_elegida,
        lags=36,
        zero=False,
        method="ywm",
        ax=ejes[1]
    )

    ejes[0].set_title(
        f"ACF de la serie diferenciada: d={d}, D={D}"
    )

    ejes[1].set_title(
        f"PACF de la serie diferenciada: d={d}, D={D}"
    )

    for eje in ejes:
        eje.set_xlabel("Rezago en meses")

    figura.tight_layout()

    figura.savefig(
        FIGURAS / "acf_pacf.png",
        dpi=150
    )

    plt.close(figura)

    return d, D

# ============================================================
# 4. Modelos clásicos
# ============================================================
# Cada modelo es una función modelo(entrenamiento, h) que devuelve h
# pronósticos y solo usa `entrenamiento`. Así entra al backtest común.


def elegir_sarima(serie, d, D):
    """Comparar 16 modelos SARIMA y diagnosticar el de menor AIC."""

    filas = []
    ajustes = {}

    # p, q, P y Q toman los valores 0 o 1:
    # 2 × 2 × 2 × 2 = 16 combinaciones.
    combinaciones = list(product([0, 1], repeat=4))

    for numero, (p, q, P, Q) in enumerate(combinaciones, start=1):
        orden = (p, d, q)
        estacional = (P, D, Q, PERIODO)

        print(
            f"Ajustando {numero}/16: "
            f"SARIMA{orden}{estacional}"
        )

        try:
            # Se utiliza la serie original preparada.
            # El modelo aplica internamente las diferencias d y D.
            ajuste = SARIMAX(
                serie,
                order=orden,
                seasonal_order=estacional,
                trend="n",
                enforce_stationarity=True,
                enforce_invertibility=True
            ).fit(disp=False, maxiter=500)

            convergio = bool(
                ajuste.mle_retvals.get("converged", False)
            )

            filas.append({
                "orden": orden,
                "orden_estacional": estacional,
                "AIC": ajuste.aic,
                "convergio": convergio,
                "error": ""
            })

            if convergio and np.isfinite(ajuste.aic):
                ajustes[(orden, estacional)] = ajuste

        except Exception as error:
            # Registrar el fallo sin perder las otras combinaciones.
            filas.append({
                "orden": orden,
                "orden_estacional": estacional,
                "AIC": np.nan,
                "convergio": False,
                "error": str(error)
            })

    tabla = (
        pd.DataFrame(filas)
        .sort_values("AIC", na_position="last")
        .reset_index(drop=True)
    )

    tabla.to_csv(
        RESULTADOS / "rejilla_sarima.csv",
        index=False
    )

    print("\nComparación de modelos por AIC:")
    print(
        tabla.to_string(
            index=False,
            float_format=lambda valor: f"{valor:.3f}"
        )
    )

    # Seleccionar únicamente ajustes convergentes y con AIC finito.
    candidatos = tabla.loc[
        tabla["convergio"] & np.isfinite(tabla["AIC"])
    ]

    if candidatos.empty:
        raise RuntimeError(
            "Ningún modelo convergió con AIC finito."
        )

    mejor = candidatos.iloc[0]
    orden = mejor["orden"]
    estacional = mejor["orden_estacional"]
    ajuste = ajustes[(orden, estacional)]

    print(f"\nElegido por AIC: SARIMA{orden}{estacional}")
    print(f"AIC: {ajuste.aic:.3f}")

    # Excluir el tramo inicial afectado por la inicialización.
    inicio = max(
        PERIODO + 1,
        int(ajuste.loglikelihood_burn)
    )

    residuos = ajuste.resid.iloc[inicio:].dropna()

    # Ajustar los grados de libertad por los términos AR y MA.
    grados_modelo = (
        orden[0] + orden[2]
        + estacional[0] + estacional[2]
    )

    ljung_box = acorr_ljungbox(
        residuos,
        lags=[12, 24],
        model_df=grados_modelo,
        return_df=True
    )

    print("\nLjung-Box de los residuos:")
    print(ljung_box.to_string())

    ljung_box.to_csv(
        RESULTADOS / "ljung_box_sarima.csv",
        index_label="rezago"
    )

    # Gráfica temporal y ACF de los residuos.
    figura, ejes = plt.subplots(
        2, 1,
        figsize=(10, 7)
    )

    ejes[0].plot(
        residuos.index,
        residuos.to_numpy(),
        linewidth=1
    )
    ejes[0].axhline(0, color="black", linewidth=0.8)
    ejes[0].set_title(
        f"Residuos de SARIMA{orden}{estacional}"
    )
    ejes[0].set_ylabel("Puntos del índice")

    plot_acf(
        residuos,
        lags=min(36, len(residuos) - 1),
        zero=False,
        ax=ejes[1]
    )
    ejes[1].set_title("ACF de los residuos")
    ejes[1].set_xlabel("Rezago en meses")

    figura.tight_layout()
    figura.savefig(
        FIGURAS / "residuos.png",
        dpi=150
    )
    plt.close(figura)

    return orden, estacional


def modelo_sarima(orden, orden_estacional):

    def modelo(entrenamiento, h):
        # Ajustar exclusivamente con los datos de entrenamiento
        # disponibles en cada origen del backtest.
        ajuste = SARIMAX(
            entrenamiento,
            order=orden,
            seasonal_order=orden_estacional,
            trend="n",
            enforce_stationarity=True,
            enforce_invertibility=True
        ).fit(disp=False, maxiter=500)

        # Detectar ajustes que no hayan convergido.
        if not ajuste.mle_retvals.get("converged", False):
            raise RuntimeError(
                "SARIMA no convergió en el entrenamiento "
                f"terminado en {entrenamiento.index[-1]:%Y-%m}."
            )

        # Devolver exactamente h pronósticos en la escala original.
        pronosticos = np.asarray(
            ajuste.forecast(steps=h),
            dtype=float
        )

        if not np.isfinite(pronosticos).all():
            raise ValueError(
                "SARIMA produjo pronósticos no finitos."
            )

        return pronosticos

    return modelo

def exogenas(serie):

    # Unir las fechas históricas con los siguientes 12 meses.
    fechas_futuras = fechas_siguientes(serie, 12)
    fechas = serie.index.append(fechas_futuras)

    # Crear el calendario para todos los años necesarios.
    calendario = holidays.country_holidays(
        "CO",
        years=range(
            fechas.min().year,
            fechas.max().year + 1
        )
    )

    # Contar las fechas festivas dentro de cada mes.
    cantidades = []

    for fecha in fechas:
        dias_del_mes = pd.date_range(
            start=fecha,
            end=fecha + pd.offsets.MonthEnd(0),
            freq="D"
        )

        cantidad = sum(
            dia.date() in calendario
            for dia in dias_del_mes
        )

        cantidades.append(cantidad)

    # Conservar el mismo índice mensual que utiliza la serie.
    x = pd.DataFrame(
        {"festivos": cantidades},
        index=fechas,
        dtype=float
    )

    x.index.name = "fecha"

    # Comprobar la cobertura y ausencia de faltantes.
    if x.index.has_duplicates or x.isna().any().any():
        raise ValueError(
            "Revise las fechas y los valores de las exógenas."
        )

    x.to_csv(RESULTADOS / "exogenas.csv")

    print("\nFestivos mensuales de Colombia:")
    print(x.head(12).to_string())

    print(
        f"\nCobertura de exógenas: "
        f"{x.index.min():%Y-%m} a {x.index.max():%Y-%m}"
    )

    return x


def modelo_sarimax(orden, orden_estacional, x):
    
    def modelo(entrenamiento, h):
        # Festivos de los meses usados para entrenar.
        x_entrenamiento = x.loc[entrenamiento.index]

        # Festivos de los meses que se van a pronosticar.
        fechas_futuras = fechas_siguientes(entrenamiento, h)
        x_futuras = x.loc[fechas_futuras]

        if (
            x_entrenamiento.isna().any().any()
            or x_futuras.isna().any().any()
        ):
            raise ValueError(
                "Hay valores faltantes en las variables exógenas."
            )

        # Ajustar usando únicamente las ventas del entrenamiento.
        ajuste = SARIMAX(
            entrenamiento,
            exog=x_entrenamiento,
            order=orden,
            seasonal_order=orden_estacional,
            trend="n",
            enforce_stationarity=True,
            enforce_invertibility=True
        ).fit(disp=False, maxiter=500)

        if not ajuste.mle_retvals.get("converged", False):
            raise RuntimeError(
                "SARIMAX no convergió en el entrenamiento "
                f"terminado en {entrenamiento.index[-1]:%Y-%m}."
            )

        # Pronosticar con el calendario conocido de los meses futuros.
        pronosticos = np.asarray(
            ajuste.forecast(
                steps=h,
                exog=x_futuras
            ),
            dtype=float
        )

        if not np.isfinite(pronosticos).all():
            raise ValueError(
                "SARIMAX produjo pronósticos no finitos."
            )

        return pronosticos

    return modelo


# ============================================================
# 5. La tabla de métricas
# ============================================================

def fila(nombre, serie, modelo):
    _, promedio = backtest(serie, modelo)
    return {"modelo": nombre, "decision": DECISION,
            "RMSE": round(promedio["RMSE"], 2), "MAE": round(promedio["MAE"], 2),
            "MAPE": round(promedio["MAPE"], 2)}


def pendiente(parte, error):
    print(f"  pendiente: {parte} ({error})")


def main():
    cruda = cargar_serie(ARCHIVO, FECHA, VALOR)
    print(f"Serie: {len(cruda)} meses, de {cruda.index[0]:%Y-%m} a "
          f"{cruda.index[-1]:%Y-%m}, {cruda.isna().sum()} vacíos")
    serie = preparar(cruda)
    graficar_serie(serie)

    filas = [fila("ingenuo", serie, ingenuo),
             fila("estacional ingenuo", serie,
                  lambda t, h: estacional_ingenuo(t, h, PERIODO))]

    try:
        descomponer(serie)
    except NotImplementedError as error:
        pendiente("parte 2", error)

    try:
        d, D = estacionariedad(serie)
    except NotImplementedError as error:
        pendiente("parte 3", error)
        d = D = None

    if d is not None:
        try:
            orden, estacional = elegir_sarima(serie, d, D)
            filas.append(fila(f"SARIMA{orden}{estacional}", serie,
                              modelo_sarima(orden, estacional)))
            x = exogenas(serie)
            filas.append(fila(f"SARIMAX{orden}{estacional} + exógenas", serie,
                              modelo_sarimax(orden, estacional, x)))
        except NotImplementedError as error:
            pendiente("parte 4", error)

    tabla = pd.DataFrame(filas).sort_values("RMSE")
    tabla.to_csv(RESULTADOS / "metricas.csv", index=False)
    print(tabla.drop(columns="decision").to_string(index=False))
    print("Mejor modelo por RMSE:", tabla.iloc[0]["modelo"])


if __name__ == "__main__":
    main()
