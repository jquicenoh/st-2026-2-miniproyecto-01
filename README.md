[informe.md](https://github.com/user-attachments/files/34201793/informe.md)
# Miniproyecto 1 — De las líneas base al mejor modelo clásico

**Pronóstico de Series Temporales con IA · Universidad Autónoma de Occidente · 2026-II**  
**Serie:** Índice mensual de ventas reales de prendas de vestir y textiles — total nacional, DANE  
**Periodo:** enero de 2019 a agosto de 2026 (92 observaciones)  
**Fecha del informe:** 30 de octubre de 2026

## Integrantes

Los grupos son de 3 integrantes.

Esta tabla identifica al grupo. Sin ella, o con algún dato incompleto, la
entrega pierde el 20 %; quien no aparezca aquí no cuenta como parte del grupo.

| Nombre completo | Código | Correo institucional |
|---|---|---|
|Jessica Quiceno | | jessica.quiceno@uao.edu.co|
|Melissa Muñoz | | melissa.munoz@uao.edu.co|

# Miniproyecto 1 — De las líneas base al mejor modelo clásico

**Pronóstico de Series Temporales con IA · Universidad Autónoma de Occidente · 2026-II**  
**Serie:** Índice mensual de ventas reales de prendas de vestir y textiles — total nacional, DANE  
**Periodo:** enero de 2019 a agosto de 2026 (92 observaciones)  
**Fecha del informe:** 30 de octubre de 2026

> Este informe corresponde al archivo exigido por el curso: `docs/informe.md`. Las figuras se referencian mediante rutas relativas a `figuras/`. Los resultados numéricos provienen de las ejecuciones y verificaciones consignadas en el informe técnico del grupo. Las cifras complementarias reproducidas se identifican como tales.

## 1. La serie

Analizamos el **índice mensual nacional de ventas reales de prendas de vestir y textiles** de la Encuesta Mensual de Comercio (EMC) del Departamento Administrativo Nacional de Estadística (DANE). La fuente es el anexo `anex-EMC-ComercioMinorista-ago2026.xlsx`, hoja **2.2**, columna **«4. Prendas de vestir y textiles»**, cuya base es **2019 = 100**. La serie comprende **92 meses consecutivos**, desde enero de 2019 hasta agosto de 2026, con frecuencia mensual y fechas fijadas al inicio de cada mes (`MS`). La marca `p` del anexo indica información provisional. El índice expresa evolución relativa de ventas reales: no es un conteo de prendas ni un ingreso en pesos.

La elección responde a la presencia de un patrón anual marcado —con máximos recurrentes hacia diciembre—, cambios de nivel y una caída excepcional en 2020. El objetivo experimental es evaluar si modelos SARIMA y SARIMAX mejoran dos líneas base sencillas bajo el mismo procedimiento de evaluación temporal.

**Fuente y condiciones de uso.** El archivo proviene de los [históricos de la EMC del DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/encuesta-mensual-de-comercio-emc/encuesta-mensual-de-comercio-emc-historicos); [anexo de agosto de 2026](https://www.dane.gov.co/files/operaciones/EMC/anex-EMC-ComercioMinorista-ago2026.xlsx). Las [condiciones generales de uso del DANE](https://www.dane.gov.co/index.php/en/terrminos-y-condiciones-dane) se citan para documentar la reutilización y atribución, sin adjudicar al anexo una licencia Creative Commons no constatada. **Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co.** La ficha detallada debe conservarse en `datos/README.md`.

![Serie mensual original del índice de ventas reales](/figuras/serie.png)

*Figura 1. Serie mensual nacional del índice de ventas reales de prendas de vestir y textiles, 2019–2026. Fuente: DANE, elaboración del grupo.*

Para preparar la serie, `preparar_datos.py` lee la hoja 2.2 mediante `pandas.read_excel(..., header=7)`, normaliza encabezados, reconstruye las **etiquetas de año** vacías mediante `ffill`, convierte los meses a números y construye las fechas. Este procedimiento completa únicamente información de estructura temporal: **no imputa ventas**. Se verificaron ausencia de duplicados, meses faltantes y valores nulos en el índice. Se exportó `datos/prendas_vestir.csv`, con columnas `fecha` e `indice_ventas`.

El mínimo registrado es **9,258 puntos en abril de 2020** y el máximo **303,508 puntos en diciembre de 2022**. Los máximos de diciembre se conservaron porque forman parte de un patrón repetido; también se mantuvo la caída de 2020, sin atribuirle causalidad exclusivamente por la gráfica. **Decisión sobre los datos:** «Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020». No se recortaron valores, sustituyeron observaciones ni aplicaron logaritmos.

## 2. Componentes

Se utilizó una **descomposición STL robusta** (`period=12`, `robust=True`) bajo el esquema aditivo:

$$
y_t = T_t + S_t + R_t,
$$

donde $T_t$ es la tendencia, $S_t$ es la estacionalidad y $R_t$ el residuo de descomposición. STL describe los componentes y **no es, por sí misma, el modelo de pronóstico evaluado**. El ajuste robusto reduce el peso de observaciones excepcionales al estimar los componentes, sin alterar la serie original.

![Descomposición STL robusta](/figuras/stl.png)

*Figura 2. Tendencia, estacionalidad y residuo de la descomposición STL robusta.*

La tendencia aumenta aproximadamente hasta 2022, disminuye hasta 2024 y luego muestra recuperación parcial y estabilización. El componente estacional presenta una elevación pronunciada en diciembre. La caída de 2020 aparece principalmente como residuo negativo de la descomposición, lo que **no** significa que aquella caída no haya ocurrido.

El promedio del componente estacional por mes calendario —calculado en una reproducción del procedimiento sobre el mismo anexo— es:

| Mes | Estacionalidad promedio (puntos del índice) |
|---|---:|
| Enero | -23,370 |
| Febrero | -34,361 |
| Marzo | -25,824 |
| Abril | -27,034 |
| Mayo | -13,861 |
| Junio | -1,567 |
| Julio | -11,822 |
| Agosto | -17,789 |
| Septiembre | -15,743 |
| Octubre | -12,115 |
| Noviembre | 17,878 |
| Diciembre | **167,232** |

Diciembre sobresale con un componente promedio de **+167,232 puntos** respecto a la tendencia; febrero presenta el valor más bajo (**−34,361**). Los componentes negativos no representan ventas negativas. Estos son **promedios descriptivos**, ya que STL permite que la estacionalidad varíe entre años. Enero–agosto tienen ocho observaciones por mes y septiembre–diciembre, siete. El residuo de mayor magnitud absoluta se sitúa en abril de 2020 (**−65,108 puntos**), según la misma reproducción. Este residuo no debe confundirse con un error de pronóstico fuera de muestra.

## 3. Líneas base y *backtest*

Se conservó **sin modificaciones** `comun.py`, que proporciona la carga, las métricas, las líneas base y el procedimiento compartido de *backtest* del curso. Con `n_prueba=24` y horizonte $H=12$, la ventana susceptible de evaluación abarca **septiembre de 2024 a agosto de 2026**. Puesto que cada origen debe contar con doce observaciones futuras, se obtienen **13 orígenes**, no 24:

| Elemento | Definición |
|---|---|
| Primer origen | Agosto de 2024 (68 meses de entrenamiento) |
| Primera ventana de evaluación | Septiembre de 2024 – agosto de 2025 |
| Último origen | Agosto de 2025 (80 meses de entrenamiento) |
| Última ventana de evaluación | Septiembre de 2025 – agosto de 2026 |
| Orígenes | $24-12+1=13$ |
| Horizontes por origen | 1 a 12 meses |
| Comparaciones por modelo | $13\times 12=156$ (superpuestas) |

El entrenamiento **se expande** desde enero de 2019 y el origen avanza un mes en cada iteración. Las 156 comparaciones no representan 156 meses distintos ni errores independientes: un mismo mes puede evaluarse desde varios orígenes y horizontes. En cada origen los modelos ajustados reciben solo las ventas disponibles hasta ese momento. **Limitación:** las diferencias y los órdenes del SARIMA se seleccionaron previamente usando toda la serie, lo cual incorpora información del periodo evaluado en la **selección de estructura**, aunque no en el ajuste de parámetros por origen. Por tanto, la comparación es exploratoria y no constituye una evaluación completamente libre de fuga de información.

Para los $H=12$ pronósticos de cada origen se calcularon:

$$
\mathrm{MAE}=\frac{1}{H}\sum_{j=1}^{H}|y_j-\hat y_j|,
$$

$$
\mathrm{RMSE}=\sqrt{\frac{1}{H}\sum_{j=1}^{H}(y_j-\hat y_j)^2},
$$

$$
\mathrm{MAPE}=\frac{100}{H}\sum_{j=1}^{H}\left|\frac{y_j-\hat y_j}{y_j}\right|.
$$

Cada métrica final es el **promedio de la métrica calculada en los 13 orígenes**. En particular, el RMSE informado es un promedio de RMSE por origen y **no** la raíz del promedio de los 156 errores cuadrados reunidos. RMSE y MAE se expresan en **puntos del índice** y MAPE en **porcentaje**; MAPE no equivale a una «exactitud» o a un intervalo de confianza.

| Línea base | RMSE | MAE | MAPE (%) |
|---|---:|---:|---:|
| **Estacional ingenuo** | **6,26** | **5,54** | **4,87** |
| Ingenuo | 63,08 | 38,41 | 30,10 |

El **ingenuo** repite el último valor observado en todos los meses futuros. El **estacional ingenuo** repite el valor del mismo mes del año anterior. Este último logra menor error en las tres métricas y demuestra que la información de la estacionalidad anual constituye una referencia exigente en el periodo reciente. La caída de 2020 se encuentra en los entrenamientos, pero fuera de la ventana evaluada.

## 4. Estacionariedad e identificación

Se aplicó la prueba **Augmented Dickey–Fuller (ADF)**, cuya hipótesis nula corresponde a presencia de raíz unitaria. Se seleccionaron rezagos por AIC. En la serie original se utilizó `regression="ct"` (constante y tendencia) y en las series diferenciadas `regression="c"` (constante).

| Versión | $d$ | $D$ | Observaciones | Valor $p$ ADF | Rezagos |
|---|---:|---:|---:|---:|---:|
| Original | 0 | 0 | 92 | 0,590762 | 12 |
| Diferencia regular | 1 | 0 | 91 | 0,113224 | 11 |
| Diferencia estacional | 0 | 1 | 80 | 0,139772 | 12 |
| Ambas diferencias | 1 | 1 | 79 | 0,100338 | 11 |

**Ninguna versión rechaza la hipótesis nula al 5 %.** El menor valor $p$ no se utilizó como criterio suficiente de selección. La decisión **provisional** fue $d=1$, $D=1$, apoyada además en los patrones gráficos y de autocorrelación; no se afirma que la estacionariedad haya quedado confirmada.

Con $B$ como operador de rezago y estacionalidad anual $s=12$:

$$
\Delta y_t=(1-B)y_t=y_t-y_{t-1},
$$

$$
\Delta_{12} y_t=(1-B^{12})y_t=y_t-y_{t-12},
$$

$$
w_t=(1-B)(1-B^{12})y_t=y_t-y_{t-1}-y_{t-12}+y_{t-13}.
$$

La diferencia regular conserva picos anuales pronunciados. La estacional atenúa ese patrón pero mantiene persistencia de corto plazo; la combinación reduce más dicha persistencia. Diferenciar no garantiza varianza constante ni demuestra por sí solo estacionariedad.

![Serie original y diferencias con autocorrelaciones](/figuras/diferencias.png)

*Figura 3. Serie original y transformaciones regular, estacional y combinada, con sus ACF.*

![ACF y PACF de la serie diferenciada](/figuras/acf_pacf.png)

*Figura 4. ACF y PACF de $w_t$, con $d=D=1$ y ciclo de doce meses.*

En una reproducción numérica de la ACF/PACF de la serie doblemente diferenciada, la ACF presenta rezagos fuera de las bandas aproximadas del 95 % en **3, 9 y 12**, y la PACF en **3, 9, 12, 24 y 36** (`method="ywm"`). Son indicios de dependencia y no pruebas causales ni una selección automática de órdenes. No apareció un corte inequívoco; se decidió explorar una rejilla compacta con $p,q,P,Q\in\{0,1\}$, que no abarca directamente todos los rezagos destacados.

## 5. Modelos clásicos

### 5.1 Selección SARIMA mediante AIC

Se ajustaron **16 especificaciones SARIMA** variando $p,q,P,Q\in\{0,1\}$, manteniendo $d=D=1$, periodo $s=12$ y `trend="n"`. Las diferencias se aplicaron **internamente** al modelo sobre la serie preparada; no se entregó una serie previamente diferenciada. Se reportó convergencia de los 16 ajustes.

| Orden $(p,d,q)$ | Estacional $(P,D,Q,12)$ | AIC |
|---|---|---:|
| (0,1,0) | (1,1,1,12) | **632,719** |
| (0,1,0) | (0,1,1,12) | 632,936 |
| (1,1,1) | (0,1,1,12) | 633,122 |
| (1,1,1) | (1,1,1,12) | 633,228 |
| (0,1,1) | (1,1,1,12) | 634,289 |
| (1,1,0) | (1,1,1,12) | 634,443 |
| (0,1,1) | (0,1,1,12) | 634,449 |
| (1,1,0) | (0,1,1,12) | 634,654 |
| (0,1,0) | (1,1,0,12) | 646,293 |
| (1,1,1) | (1,1,0,12) | 647,209 |
| (0,1,1) | (1,1,0,12) | 647,626 |
| (1,1,0) | (1,1,0,12) | 647,832 |
| (1,1,1) | (0,1,0,12) | 654,806 |
| (0,1,0) | (0,1,0,12) | 655,999 |
| (0,1,1) | (0,1,0,12) | 657,427 |
| (1,1,0) | (0,1,0,12) | 657,523 |

El criterio fue

$$
\mathrm{AIC}=-2\log L+2k,
$$

que equilibra ajuste y número de parámetros; **no mide directamente el error predictivo**. El mínimo se obtuvo para **SARIMA$(0,1,0)(1,1,1)_{12}$** con AIC **632,719**. La diferencia frente al segundo modelo (**0,217**) es pequeña: justifica documentar la selección automática, pero no afirmar una superioridad concluyente. El modelo se describe mediante:

$$
(1-\Phi B^{12})(1-B)(1-B^{12})y_t=(1+\Theta B^{12})\varepsilon_t.
$$

En la reproducción sobre el mismo Excel se estimaron $\Phi\approx0,181652$, $\Theta\approx-0,999776$ y $\sigma^2\approx125,856801$; el AIC fue **632,718646**, compatible con el valor reportado redondeado. En consecuencia:

$$
(1-0,181652 B^{12})(1-B)(1-B^{12})y_t\approx(1-0,999776 B^{12})\varepsilon_t.
$$

El MA estacional muy próximo a $-1$ exige cautela por su cercanía a la frontera de invertibilidad y posible cancelación con la diferenciación estacional. **No demuestra**, por sí solo, sobrediferenciación.

### 5.2 Diagnóstico de residuos

Para revisar la dependencia no explicada se excluyeron los primeros 13 residuos —o más si la inicialización lo exigía— y se aplicó Ljung–Box con `model_df=2`, correspondiente a los términos AR y MA estacionales.

![Residuos y ACF del SARIMA](/figuras/residuos.png)

*Figura 5. Residuos históricos del SARIMA seleccionado y su autocorrelación.*

| Rezago | Estadístico Ljung–Box | Valor $p$ |
|---:|---:|---:|
| 12 | 23,151039 | **0,010203** |
| 24 | 34,360534 | **0,045129** |

Los valores $p$ son inferiores a 0,05 en ambos rezagos; por tanto, **se rechaza ausencia conjunta de autocorrelación**. El diagnóstico residual no es plenamente satisfactorio y el modelo no captura toda la estructura de la serie. La reproducción señala residuos destacados en diciembre de 2020 (−45,762), diciembre de 2021 (+44,865), marzo de 2020 (−40,289) y enero de 2022 (−37,262) puntos. No se realizaron verificaciones formales de normalidad u homocedasticidad.

### 5.3 SARIMAX con exógena de festivos

Se utilizó como variable exógena el **número mensual de fechas festivas nacionales de Colombia** generado con `holidays`, incluyendo aquellas que coinciden con fines de semana. Es un conteo de fechas festivas, **no** de días hábiles ni de eventos de consumo. La motivación es que el calendario podría contener información predictiva conocida antes del periodo pronosticado; **no** se identifica un efecto causal de los festivos sobre las ventas.

El calendario exógeno se construyó para los 92 meses históricos y 12 meses posteriores, hasta agosto de 2027 (**104 registros**). Disponer de valores futuros de calendario no implica haber calculado pronósticos finales para 2026–2027. Se conservaron los órdenes SARIMA seleccionados y se reestimaron los coeficientes con la exógena en cada origen. Una representación es:

$$
y_t=\beta x_t+u_t,
\qquad
(1-\Phi B^{12})(1-B)(1-B^{12})u_t=(1+\Theta B^{12})\varepsilon_t.
$$

El SARIMAX con festivos obtuvo **RMSE 8,56; MAE 7,31; MAPE 7,30 %**, frente a **8,54; 7,30; 7,29 %** de SARIMA. **No hubo mejora observada** al incorporar la exógena. No se realizó una prueba formal de significación de la diferencia de precisión, por lo que no se deduce equivalencia estadística ni irrelevancia general de los festivos.

## 6. Tabla de métricas

La siguiente tabla reproduce la comparación final del procedimiento, ordenada de menor a mayor RMSE. La columna de decisión documenta el tratamiento aplicado a la serie.

| Modelo | Decisión | RMSE | MAE | MAPE (%) |
|---|---|---:|---:|---:|
| **Estacional ingenuo** | Sin huecos; no se imputa; se conservan picos y caída de 2020 | **6,26** | **5,54** | **4,87** |
| SARIMA$(0,1,0)(1,1,1)_{12}$ | Misma decisión | 8,54 | 7,30 | 7,29 |
| SARIMAX$(0,1,0)(1,1,1)_{12}$ + festivos | Misma decisión | 8,56 | 7,31 | 7,30 |
| Ingenuo | Misma decisión | 63,08 | 38,41 | 30,10 |

La salida reproducible prevista por el programa es `resultados/metricas.csv`. **El mejor método evaluado es el estacional ingenuo**, no el SARIMA ni el SARIMAX. La comparación demuestra que una especificación más compleja no garantiza mejor pronóstico en esta serie.

## 7. Conclusión

El **modelo estacional ingenuo** alcanzó los menores errores entre las cuatro alternativas, con **RMSE 6,26**, **MAE 5,54** y **MAPE 4,87 %**. Entre los modelos clásicos ajustados, SARIMA superó marginalmente a SARIMAX, pero **ninguno mejoró la mejor línea base**. Frente al estacional ingenuo, SARIMA incrementó el RMSE en **2,28 puntos del índice**, el MAE en **1,76 puntos** y el MAPE en **2,42 puntos porcentuales**. Por lo tanto, no corresponde declarar una mejora inexistente.

La comparación proporciona una conclusión útil para el siguiente miniproyecto: la referencia que debe superarse, **bajo un protocolo comparable**, es el estacional ingenuo. La estacionalidad anual tiene considerable poder descriptivo y predictivo durante la evaluación reciente, aunque repetir el año anterior no anticipa perfectamente cambios en la amplitud de los máximos.

En la reproducción de los errores por fecha, la línea base estacional presentó diferencias absolutas destacadas en diciembre de 2024 (**17,024 puntos; sobreestimación**), septiembre de 2024 (**14,776; sobreestimación**), diciembre de 2025 (**9,987; subestimación**) y noviembre de 2024 (**8,398; sobreestimación**). Para SARIMA, los mayores errores absolutos medios por fecha se ubicaron en mayo de 2025 (**15,339**), abril de 2025 (**14,457**), junio de 2025 (**9,999**) y agosto de 2026 (**9,606**). Abril y mayo de 2025 reflejaron subestimaciones. Estos resúmenes por mes mezclan horizontes y no disponen del mismo número de evaluaciones por fecha; se ofrecen como **diagnóstico complementario** y no reemplazan las métricas agregadas del *backtest*.

![Ejemplo de pronósticos del último origen](/figuras/ultimo_origen.png)

*Figura 6. Ilustración del último origen (agosto de 2025) y sus pronósticos a septiembre de 2025–agosto de 2026. Es un ejemplo, no la totalidad del backtest.*

Los hallazgos deben leerse dentro de sus límites: la selección de diferencias y órdenes utilizó toda la serie; se consideró una rejilla restringida; ADF no confirmó estacionariedad al 5 %; el SARIMA mantuvo autocorrelación residual; el *backtest* utiliza ventanas superpuestas y una etapa reciente, y solo se estudió una exógena agregada. No se realizaron pruebas formales de diferencia de precisión ni se evaluó la anticipación de la caída extraordinaria de 2020 (ubicada fuera de la ventana de prueba). Como continuación, procede revisar la estrategia de diferenciación, separar estrictamente selección y evaluación y explorar especificaciones adicionales solo cuando exista una justificación diagnóstica.

---

### Referencias y trazabilidad

1. **DANE.** *Encuesta Mensual de Comercio (EMC)*, anexo del comercio minorista de agosto de 2026, hoja 2.2, índice base 2019 = 100. [Archivo Excel](https://www.dane.gov.co/files/operaciones/EMC/anex-EMC-ComercioMinorista-ago2026.xlsx) · [Históricos EMC](https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/encuesta-mensual-de-comercio-emc/encuesta-mensual-de-comercio-emc-historicos).
2. **DANE.** [Términos y condiciones generales de uso](https://www.dane.gov.co/index.php/en/terrminos-y-condiciones-dane). Atribución conservada: «Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co».
3. **statsmodels.** [STL](https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.STL.html) y [prueba Ljung–Box](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html).
4. **Código del curso.** `comun.py` (no modificado) y `miniproyecto.py`, con parámetros de evaluación `n_prueba=24` y `h=12`.
5. **Resultados del grupo y verificación complementaria.** Salidas de Codespaces (ADF, AIC, Ljung–Box, métricas) y reproducción con el mismo Excel; algunos componentes STL, coeficientes y análisis por fecha proceden de la reproducción descrita en el informe técnico de origen (30 de octubre de 2026). Versiones de la reproducción: `statsmodels 0.15.0`, `holidays 0.107`.

> **Verificación antes de entregar:** confirmar que las imágenes referenciadas realmente existen en `figuras/` con los nombres `serie.png`, `stl.png`, `diferencias.png`, `acf_pacf.png`, `residuos.png` y `ultimo_origen.png`. Si el guion genera nombres distintos, actualizar las rutas **sin cambiar las cifras**. Ejecutar `python miniproyecto.py` y comprobar que `resultados/metricas.csv` coincide. Las figuras deben ser las generadas por el guion definitivo del grupo.

| | | |


[informe.md](https://github.com/user-attachments/files/34202435/informe.md)
