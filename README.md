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
| | | |


> Este informe corresponde al archivo exigido por el curso: `docs/informe.md`. Las figuras se referencian mediante rutas relativas a `figuras/`. Los resultados numéricos provienen de las ejecuciones y verificaciones consignadas en el informe técnico del grupo. Las cifras complementarias reproducidas se identifican como tales.# Pronóstico de ventas reales de prendas de vestir y textiles

Informe técnico y guía de sustentación del miniproyecto 1

Serie mensual nacional del DANE · Enero de 2019 a agosto de 2026  
Versión consolidada · 30 de octubre de 2026

# Parte I Desarrollo técnico del proyecto

## 1 Objetivo y alcance

El objetivo fue preparar una serie mensual propia, describir su comportamiento y comparar dos líneas base con modelos SARIMA y SARIMAX mediante el backtest común del curso. La pregunta práctica fue si un modelo clásico ajustado podía reducir los errores de una referencia que repite el patrón anual de ventas.

Se estudia una sola categoría del comercio nacional. No se modelan ventas de una empresa particular ni se dispone de información individual de consumidores. El índice resume una evolución relativa; no debe interpretarse como número de prendas vendidas, ingresos en pesos o probabilidad de compra.

## 2 Entorno y organización del trabajo

Se creó un fork del proyecto del docente y se abrió un Codespace en la rama Jessica-datos. Se instalaron las dependencias mediante requirements.txt y se hizo una primera ejecución con Air Passengers para comprobar el funcionamiento del guion. Esa serie fue una prueba del entorno y no es la serie del análisis final.

| **Archivo**       | **Responsabilidad**                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------|
| preparar_datos.py | Extraer y validar la serie del anexo Excel.                                                   |
| miniproyecto.py   | Preparación, figuras, diagnósticos, modelos y tabla final.                                    |
| comun.py          | Carga, fechas futuras, métricas, líneas base y backtest del docente. Se conserva sin cambios. |
| requirements.txt  | Dependencias; se añadieron openpyxl y holidays.                                               |
| datos/README.md   | Fuente, variable, cobertura, tratamiento y condiciones de uso.                                |
| docs/informe.md   | Informe analítico con las siete secciones obligatorias.                                       |
| README.md         | Descripción general y guía de reproducción.                                                   |

Se registró el avance de preparación de datos y posteriormente la implementación de STL mediante commits. Se explicó el uso de ramas, sincronización y pull requests, y se envió una invitación a Mel2230. La aceptación de esa invitación, los commits posteriores y la integración final en main deben verificarse en GitHub; no se dan por realizados solo por haber sido propuestos.

```bash
python -m pip install -r requirements.txt
python preparar_datos.py
python miniproyecto.py
```

# 3 Fuente y significado del índice

La fuente es la Encuesta Mensual de Comercio del DANE. El archivo utilizado es anex-EMC-ComercioMinorista-ago2026.xlsx. La hoja 2.2 se titula “Índices de las ventas en valores reales según grupo de mercancía - Total nacional” y declara base 2019 = 100. Se seleccionó “4. Prendas de vestir y textiles”.

| **Característica** | **Valor**                              |
|--------------------|----------------------------------------|
| Cobertura          | Total nacional                         |
| Frecuencia         | Mensual con fechas de inicio de mes MS |
| Periodo            | Enero de 2019 a agosto de 2026         |
| Observaciones      | 92                                     |
| Base del índice    | 2019 = 100                             |
| CSV derivado       | datos/prendas_vestir.csv               |
| Columnas           | fecha e indice_ventas                  |
| Mínimo observado   | 9,258 puntos en abril de 2020          |
| Máximo observado   | 303,508 puntos en diciembre de 2022    |

La base 2019 = 100 proporciona una referencia de comparación. Un índice de 120 representa un nivel 20 % superior a esa base, sujeto a la definición estadística del índice; no significa necesariamente un aumento del 20 % respecto al mes anterior. “Ventas reales” distingue la evolución en volumen o a precios constantes de la evolución nominal; el proyecto usa el índice publicado y no realiza una deflactación adicional.

La marca p del encabezado del anexo indica información provisional. Conservar el archivo de origen y el corte temporal facilita reproducir el análisis aunque el DANE publique revisiones posteriores.

## Condiciones de uso

Se consultaron las condiciones generales del portal del DANE. Permiten el uso, transformación y análisis de la información con reconocimiento de la fuente. No se asigna por inferencia una licencia Creative Commons de otro producto institucional. La atribución que debe conservarse es: “Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co”. Véanse las referencias al final del documento.

# 4 Extracción y validación de los datos

El Excel contiene títulos, encabezados y años agrupados. Por ello se creó preparar_datos.py en la raíz del proyecto, en lugar de intentar usar directamente el anexo como si fuera una tabla CSV simple.

## Lectura del anexo

Se utilizó pandas.read_excel con sheet_name="2.2" y header=7. La octava fila del archivo se interpreta como encabezado porque Python cuenta desde cero. Se limpiaron los espacios en los extremos de los nombres de columnas.

## Selección de campos

Se conservaron Año, Mes y la columna de prendas de vestir y textiles. No se mezclaron índices de otras categorías ni el total del comercio con la serie seleccionada.

## Reconstrucción temporal

Año se convirtió a número y se completó hacia adelante con ffill. El Excel escribe el año al comienzo de cada bloque; completar esa etiqueta no cambia ni estima ventas. Los meses se normalizaron a minúsculas y se relacionaron con números de 1 a 12.

## Filtrado y fechas

Se conservaron las filas con un mes reconocido, se combinaron año, mes y día 1 y se ordenaron cronológicamente. El día 1 identifica el mes completo, no una medición diaria.

## Valores numéricos

El índice se convirtió mediante to_numeric con errors="raise". De este modo, un texto inesperado interrumpe el proceso en lugar de convertirse silenciosamente en un dato válido.

## Controles de integridad

Se comprobaron fechas no duplicadas, ausencia de NaN en ventas y coincidencia con un calendario mensual continuo. Estos controles detectan problemas de estructura, pero no certifican por sí solos toda la exactitud económica de la fuente.

## Exportación

Se generó prendas_vestir.csv con las columnas fecha e indice_ventas, sin columna adicional de número de fila. El Excel original permanece como fuente trazable.

La configuración activa quedó como ARCHIVO="datos/prendas_vestir.csv", FECHA="fecha", VALOR="indice_ventas" y PERIODO=12. La función preparar comprueba faltantes y devuelve una copia de la serie original. No se imputó, recortó, transformó con logaritmos ni sustituyó ningún índice de ventas.

# 5 Comportamiento y decisión sobre observaciones excepcionales

![Figura del informe](../figuras/serie.png)

*Figura 1. Serie nacional mensual original. Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co. Elaboración a partir del anexo de agosto de 2026.*

La serie combina oscilaciones mensuales con incrementos que se repiten al final de cada año. Los máximos de diciembre son consistentes con estacionalidad. Una regla que eliminara automáticamente todos los valores altos eliminaría información relevante para pronosticar.

Abril de 2020 presenta el mínimo de 9,258 puntos. La caída coincide temporalmente con el periodo de pandemia, pero no se estimó un efecto causal. Se conserva como parte de la historia observada. Una perturbación histórica no se convierte en error de registro únicamente por ser extrema.

La decisión final fue no imputar porque no existen huecos y conservar tanto los picos recurrentes como la caída excepcional. Esto mantiene el significado de la variable y evita introducir valores artificiales; a cambio, los modelos deben aprender de una historia con cambios importantes.

## Interpretación para la sustentación

La limpieza consistió en organizar y validar los datos, no en hacer que la gráfica se viera uniforme. Se distinguieron tres situaciones: etiquetas temporales vacías del Excel, meses o ventas faltantes y valores observados excepcionales. Solo la primera requirió completar información de estructura.

# 6 Descomposición STL robusta

![Figura del informe](../figuras/stl.png)

*Figura 2. Descomposición aditiva con period=12 y robust=True. Componentes regenerados con el mismo procedimiento del proyecto.*

STL separa la serie en tendencia suavizada, componente estacional y residuo: $$y_t = T_t + S_t + R_t$$. No es un modelo de pronóstico en este proyecto. La robustez reduce el peso de observaciones excepcionales al estimar los componentes; no elimina ni reemplaza los datos originales.

La tendencia crece hasta aproximadamente 2022, desciende hasta 2024 y luego recupera parcialmente su nivel. La caída abrupta de 2020 aparece sobre todo como residuo negativo, pues la tendencia robusta sigue la evolución más persistente. Esta forma no significa que en 2020 no hubiera una caída real.

# 7 Interpretación numérica de los componentes

Para resumir la estacionalidad se promedió el componente Sₜ por mes calendario. STL permite que este componente cambie entre años: los valores siguientes son promedios descriptivos, no doce constantes impuestas al ajuste. Enero a agosto tienen ocho observaciones por mes y septiembre a diciembre tienen siete.

| **Mes**    | **Componente promedio en puntos** |
|------------|-----------------------------------|
| enero      | -23,370                           |
| febrero    | -34,361                           |
| marzo      | -25,824                           |
| abril      | -27,034                           |
| mayo       | -13,861                           |
| junio      | -1,567                            |
| julio      | -11,822                           |
| agosto     | -17,789                           |
| septiembre | -15,743                           |
| octubre    | -12,115                           |
| noviembre  | 17,878                            |
| diciembre  | 167,232                           |

Diciembre aporta en promedio +167,232 puntos respecto a la tendencia; noviembre aporta +17,878. Los demás meses presentan componentes promedio negativos, con febrero como mínimo de −34,361. Un valor negativo significa estar por debajo de la tendencia estimada, no ventas negativas. Junio, con −1,567, es el más cercano a cero.

El residuo de mayor magnitud absoluta se ubica en abril de 2020: −65,108 puntos. En ese mes la observación queda aproximadamente 65,108 puntos por debajo de la suma de tendencia y estacionalidad. Es un residuo de descomposición y no debe confundirse con un error de pronóstico fuera de muestra.

Estos valores se obtuvieron en la verificación reproducida con el mismo Excel y STL. El gráfico compartido por el grupo presenta la misma estructura. Los promedios estacionales no permiten atribuir causas específicas al consumo ni medir el efecto aislado de la Navidad.

# 8 Estacionariedad y diferencias

Un proceso estacionario mantiene propiedades estadísticas estables en el tiempo, como una media que no se desplaza persistentemente y una estructura de dependencia que depende del rezago. Una gráfica que fluctúa alrededor de cero no basta para demostrarlo.

Se aplicó ADF con selección de rezagos por AIC. Su hipótesis nula es raíz unitaria. En la original se incluyeron constante y tendencia lineal ct; en las diferencias se incluyó constante c. Cambiar esa especificación cambia la hipótesis alternativa, por lo que no se deben ordenar los valores p como si fueran puntajes de calidad de modelos.

| **Versión** | **d** | **D** | **Reg.** | **n** | **Valor p** | **Rezagos** |
|-------------|-------|-------|----------|-------|-------------|-------------|
| Original    | 0     | 0     | ct       | 92    | 0,590762    | 12          |
| Regular     | 1     | 0     | c        | 91    | 0,113224    | 11          |
| Estacional  | 0     | 1     | c        | 80    | 0,139772    | 12          |
| Ambas       | 1     | 1     | c        | 79    | 0,100338    | 11          |

Diferencia regular: $\Delta y_t = y_t - y_{t-1}$

Diferencia estacional: $\Delta_{12} y_t = y_t - y_{t-12}$

Ambas: $w_t = y_t-y_{t-1}-y_{t-12}+y_{t-13}$

La diferencia regular pierde una observación; la estacional pierde doce y la combinación pierde trece, por lo que quedan 91, 80 y 79 datos, respectivamente. Esos valores iniciales indefinidos son consecuencia matemática de diferenciar, no huecos de la fuente.

Todos los valores p superan 0,05. No se rechazó la raíz unitaria en ninguna versión. No se concluye por ello que sea necesario aumentar indefinidamente las diferencias. La muestra corta, los cambios de nivel y la cantidad de rezagos pueden limitar la evidencia, aunque no se cuantificó por separado su efecto.

Se adoptó d=1 y D=1 como decisión provisional sustentada también en el diagnóstico gráfico. No se afirmó estacionariedad confirmada y no se eligió la combinación simplemente por tener el menor valor p.

# 9 Comparación gráfica de las diferencias

![Figura del informe](../figuras/diferencias.png)

*Figura 3. Serie original y tres transformaciones con su ACF hasta 36 meses.*

La original presenta picos anuales; la diferencia regular los conserva. La diferencia estacional reduce el patrón anual pero deja una ACF inicialmente positiva y persistente. Ambas diferencias reducen esa persistencia. La heterogeneidad de amplitud entre los primeros y los últimos años sigue siendo una limitación: diferenciar no garantiza varianza constante.

# 10 Identificación mediante ACF y PACF

![Figura del informe](../figuras/acf_pacf.png)

*Figura 4. ACF y PACF de wₜ con d=1, D=1 y periodo de 12 meses.*

La ACF mide la relación entre observaciones separadas por un rezago; la PACF mide la relación una vez descontada la contribución de los rezagos intermedios. Se usaron 36 meses y method="ywm" para la PACF, sobre 79 observaciones diferenciadas.

La verificación numérica identifica picos fuera de las bandas aproximadas del 95 % en ACF para 3, 9 y 12 y en PACF para 3, 9, 12, 24 y 36. Las bandas son referencias puntuales: examinar muchos rezagos aumenta la posibilidad de encontrar algunos picos por azar y no identifica causalidad.

No existe un corte simple que determine un único modelo. Se exploraron p,q,P,Q en {0,1}, manteniendo d=D=1. La rejilla es deliberadamente pequeña y no modela directamente todos los rezagos destacados, como 3 o 9. Sus resultados son los mejores dentro del espacio explorado, no entre todos los SARIMA posibles.

# 11 Diseño de la evaluación temporal

Se conservó intacta la función backtest de comun.py. Con n_prueba=24 y h=12, los últimos 24 meses delimitan la ventana evaluable; solo se utilizan orígenes con doce observaciones futuras disponibles. Por eso hay 13 orígenes y no 24.

| **Elemento**             | **Definición exacta**                     |
|--------------------------|-------------------------------------------|
| Ventana evaluada         | Septiembre de 2024 a agosto de 2026       |
| Primer origen            | Agosto de 2024; entrenamiento de 68 meses |
| Primera evaluación       | Septiembre de 2024 a agosto de 2025       |
| Último origen            | Agosto de 2025; entrenamiento de 80 meses |
| Última evaluación        | Septiembre de 2025 a agosto de 2026       |
| Número de orígenes       | 24 − 12 + 1 = 13                          |
| Horizontes por origen    | De 1 a 12 meses                           |
| Comparaciones por modelo | 13 × 12 = 156, con ventanas superpuestas  |

El entrenamiento siempre comienza en enero de 2019 y crece un mes entre orígenes. Es entrenamiento expansivo. Un mes de prueba puede evaluarse desde varios orígenes y a distintos horizontes; por ello las 156 comparaciones no son 156 meses distintos ni observaciones independientes.

## Prevención de fuga y límite del procedimiento

En cada ajuste, SARIMA y SARIMAX reciben solo las ventas hasta el origen. El calendario futuro puede utilizarse porque se conoce de antemano. Sin embargo, la selección de d, D y de los órdenes por AIC se realizó con toda la serie antes de evaluar. Existe información del periodo evaluado en esa selección, aunque no en el ajuste de parámetros de cada origen.

La comparación debe presentarse como exploratoria con estructura seleccionada previamente. Una validación estricta exigiría fijar las decisiones con un tramo anterior o repetir la selección dentro de cada entrenamiento. La caída de 2020 está en el entrenamiento, no en la ventana de prueba; no se midió la capacidad de anticipar esa crisis.

# 12 Métricas y líneas base

$$\mathrm{MAE}=\operatorname{promedio}(|y-\hat y|)$$

$$\mathrm{RMSE}=\sqrt{\operatorname{promedio}((y-\hat y)^2)}$$

$$\mathrm{MAPE}=100\operatorname{promedio}\left(\left|\frac{y-\hat y}{y}\right|\right)$$

Cada métrica se calcula primero con los doce errores de un origen. Después se promedian los trece resultados. El RMSE final es el promedio de trece raíces de errores cuadrados medios; no es la raíz calculada juntando los 156 errores. RMSE penaliza más los errores grandes; MAE resume su magnitud absoluta y MAPE los expresa en relación con el valor observado.

MAE y RMSE se expresan en puntos del índice. Un MAPE de 4,87 % no debe traducirse como una exactitud de 95,13 %. Tampoco equivale a un intervalo de confianza ni informa por sí solo sobre el signo del error. La fuente tiene valores positivos, por lo que no hay divisiones entre cero en MAPE; valores muy bajos pueden, no obstante, amplificarlo.

## Ingenuo

Repite el último valor observado durante los doce meses siguientes. Es una referencia sencilla y útil para verificar si una propuesta aprovecha información adicional. Un único valor constante no recoge los grandes incrementos de diciembre y obtiene RMSE 63,08, MAE 38,41 y MAPE 30,10 %.

## Estacional ingenuo

Repite la secuencia de los últimos doce meses. Por ejemplo, al pronosticar septiembre utiliza septiembre del año anterior. Con horizonte doce basta con copiar una vez esa secuencia. Obtiene RMSE 6,26, MAE 5,54 y MAPE 4,87 %.

La ventaja del estacional ingenuo es consistente con una estacionalidad anual útil en el periodo reciente. No prueba que el nivel sea constante o que las ventas de cada diciembre sean idénticas. El método no ajusta automáticamente cambios de nivel ni anticipa perturbaciones nuevas.

# 13 Rejilla SARIMA y criterio AIC

Se ajustaron las 16 combinaciones de p,q,P,Q en {0,1}, d=D=1, periodo 12 y trend="n". Se impusieron estacionariedad e invertibilidad a los componentes AR y MA estimados y se permitieron hasta 500 iteraciones. Las diferencias se aplican internamente: al modelo se entrega la serie original preparada, no wₜ ya diferenciada.

| **Orden p d q** | **Orden P D Q m** | **AIC** |
|-----------------|-------------------|---------|
| (0,1,0)         | (1,1,1,12)        | 632,719 |
| (0,1,0)         | (0,1,1,12)        | 632,936 |
| (1,1,1)         | (0,1,1,12)        | 633,122 |
| (1,1,1)         | (1,1,1,12)        | 633,228 |
| (0,1,1)         | (1,1,1,12)        | 634,289 |
| (1,1,0)         | (1,1,1,12)        | 634,443 |
| (0,1,1)         | (0,1,1,12)        | 634,449 |
| (1,1,0)         | (0,1,1,12)        | 634,654 |
| (0,1,0)         | (1,1,0,12)        | 646,293 |
| (1,1,1)         | (1,1,0,12)        | 647,209 |
| (0,1,1)         | (1,1,0,12)        | 647,626 |
| (1,1,0)         | (1,1,0,12)        | 647,832 |
| (1,1,1)         | (0,1,0,12)        | 654,806 |
| (0,1,0)         | (0,1,0,12)        | 655,999 |
| (0,1,1)         | (0,1,0,12)        | 657,427 |
| (1,1,0)         | (0,1,0,12)        | 657,523 |

AIC combina ajuste y penalización por cantidad de parámetros: AIC = −2 log L + 2k. Menor es preferible dentro de una comparación compatible, pero no mide directamente el error de pronóstico ni es un porcentaje. Todos los modelos convergieron; convergencia no garantiza que el modelo sea adecuado.

El mínimo fue 632,719 para SARIMA(0,1,0)(1,1,1,12). El modelo sin AR estacional tuvo 632,936, una diferencia de solo 0,217. La selección automática por mínimo se conserva para reproducir el guion, pero esa ventaja es muy pequeña y la alternativa más sencilla sigue siendo plausible.

# 14 Ecuación e interpretación del SARIMA

El modelo seleccionado no contiene términos AR o MA regulares: p=q=0. Incluye una diferencia regular, una estacional, un AR estacional y un MA estacional. El operador B desplaza un mes; B¹² desplaza doce meses.

$$ (1-\Phi B^{12})(1-B)(1-B^{12})y_t=(1+\Theta B^{12})\varepsilon_t $$

Si wₜ=(1−B)(1−B¹²)yₜ, la ecuación también se escribe wₜ = Φwₜ₋₁₂ + εₜ + Θεₜ₋₁₂. εₜ representa la innovación del modelo, no el residuo de STL. La ausencia de tendencia determinista corresponde a trend="n" y no significa ausencia de evolución en la serie original.

| **Parámetro** | **Estimación reproducida** | **Lectura**                                                        |
|---------------|----------------------------|--------------------------------------------------------------------|
| Φ estacional  | 0,181652                   | Relaciona wₜ con w de doce meses antes.                            |
| Θ estacional  | −0,999776                  | Relaciona la innovación actual con la de doce meses antes.         |
| σ²            | 125,856801                 | Varianza estimada de las innovaciones; no es el RMSE del backtest. |

$$ (1-0{,}181652B^{12})(1-B)(1-B^{12})y_t\approx(1-0{,}999776B^{12})\varepsilon_t $$

Los parámetros se recalcularon con statsmodels 0.15.0 y el mismo Excel. El AIC resultante fue 632,718646, consistente con 632,719 publicado por el grupo. Pequeñas diferencias en los últimos decimales pueden depender de versiones y optimización.

## Advertencia técnica sobre el término estacional

El MA estacional está muy cerca de −1, la frontera de invertibilidad en esta parametrización. Puede ser una señal de una diferencia estacional innecesaria o una cancelación aproximada, entre otras explicaciones. No demuestra por sí sola sobrediferenciación. Refuerza la necesidad de revisar D=1 y comparar especificaciones alternativas en trabajo posterior, sin afirmar que aquí se haya realizado esa comparación.

# 15 Diagnóstico de residuos del SARIMA

![Figura del informe](../figuras/residuos.png)

*Figura 5. Residuos del ajuste histórico y su ACF; se excluyen los primeros 13 meses. Verificación reproducida.*

| **Rezago** | **Ljung Box** | **Valor p reportado** | **Conclusión al 5 %**                            |
|------------|---------------|-----------------------|--------------------------------------------------|
| 12         | 23,151039     | 0,010203              | Se rechaza ausencia conjunta de autocorrelación. |
| 24         | 34,360534     | 0,045129              | Se rechaza; resultado próximo al umbral.         |

La hipótesis nula evalúa conjuntamente autocorrelaciones hasta el rezago indicado; un rechazo a 12 no significa que solo la correlación del mes 12 sea significativa. Se descontaron dos grados de libertad por los términos AR y MA estacionales. La réplica produjo valores prácticamente iguales, con variaciones menores en los últimos decimales.

Los mayores residuos absolutos reproducidos incluyen diciembre de 2020 (−45,762), diciembre de 2021 (+44,865), marzo de 2020 (−40,289) y enero de 2022 (−37,262). La dispersión es mayor en los primeros años y disminuye en el tramo reciente. La ACF y Ljung-Box indican dependencia no capturada. No se afirma normalidad ni homocedasticidad porque no se verificaron formalmente.

# 16 Variable exógena y SARIMAX

Se instaló holidays y se generó el calendario nacional de Colombia. Para cada mes se contó el número de fechas que la biblioteca identifica como festivas, incluidas las que caen en fines de semana. No es un conteo de días hábiles, de personas que compran o de ventas realizadas en festivos.

La tabla x cubre los 92 meses históricos y doce meses adicionales, hasta agosto de 2027: 104 filas. Las fechas futuras permiten pronosticar al terminar la serie, pero construirlas no equivale a haber generado un pronóstico final para 2026–2027. El backtest sigue evaluando únicamente meses observados.

La motivación fue que los festivos pueden relacionarse con oportunidades de compra, movilidad o funcionamiento comercial. Se planteó como hipótesis de utilidad predictiva, no como efecto causal demostrado. Al estar definido por calendario, su valor futuro puede conocerse sin consultar ventas futuras.

$$ y_t=\beta x_t+u_t;\quad (1-\Phi B^{12})(1-B)(1-B^{12})u_t=(1+\Theta B^{12})\varepsilon_t $$

SARIMAX usa una regresión con errores SARIMA. Los mismos órdenes se conservaron para evaluar la adición de la exógena; los coeficientes se vuelven a estimar, por lo que no se mantienen fijos los parámetros del SARIMA. En cada origen se usa x.loc\[entrenamiento.index\] para ajustar y las fechas futuras correspondientes para pronosticar.

Con festivos se obtuvo RMSE 8,56, MAE 7,31 y MAPE 7,30 %. Sin ellos los valores fueron 8,54, 7,30 y 7,29 %. La diferencia es pequeña y desfavorable a la adición de festivos. No se hizo una prueba formal de diferencia de precisión: se concluye ausencia de mejora observada, no equivalencia estadística ni irrelevancia universal de los festivos.

## Reproducibilidad del calendario

La verificación utilizó holidays 0.107. Conviene registrar la versión empleada en Codespaces porque los calendarios de las bibliotecas pueden revisarse. El proyecto utiliza conteos nacionales mensuales; no incorpora fechas comerciales específicas, promociones, restricciones sanitarias ni calendarios regionales.

# 17 Comparación final y magnitud de las diferencias

| **Modelo**           | **RMSE** | **MAE** | **MAPE %** |
|----------------------|----------|---------|------------|
| Estacional ingenuo   | 6,26     | 5,54    | 4,87       |
| SARIMA               | 8,54     | 7,30    | 7,29       |
| SARIMAX con festivos | 8,56     | 7,31    | 7,30       |
| Ingenuo              | 63,08    | 38,41   | 30,10      |

![Figura del informe](../figuras/comparacion_metricas.png)

*Figura 6. Comparación con las métricas reproducidas. Valores menores indican menor error; el orden coincide con las salidas de Codespaces.*

Frente al estacional ingenuo, SARIMA aumenta el RMSE en 2,28 puntos del índice y el MAE en 1,76; el MAPE aumenta en 2,42 puntos porcentuales. Con las cifras redondeadas, eso equivale aproximadamente a 36,4 % más RMSE y 31,8 % más MAE. El cambio en MAPE debe distinguirse entre puntos porcentuales y cambio relativo.

El método seleccionado para servir de referencia al miniproyecto 2 es el estacional ingenuo. Entre los modelos SARIMA y SARIMAX ajustados, el SARIMA fue ligeramente mejor, pero no superó a la línea base. No se debe redactar una “mejora” inexistente para ajustarse al enunciado.

La diferencia entre los modelos complejos y la referencia puede relacionarse con cambios históricos, restricciones de la rejilla y estructura del modelo. Esas explicaciones son hipótesis plausibles; no se aisló cuantitativamente cuál produjo el resultado. La conclusión demostrada es la comparación de errores bajo este protocolo.

# 18 Dónde persisten errores de pronóstico

![Figura del informe](../figuras/ultimo_origen.png)

*Figura 7. Ejemplo de una ventana: entrenamiento hasta agosto de 2025 y evaluación de septiembre de 2025 a agosto de 2026. No reemplaza la evaluación de los 13 orígenes.*

Se conservaron los errores individuales de una reproducción del backtest para localizar meses problemáticos. Para el estacional ingenuo, los errores absolutos más altos por mes fueron diciembre de 2024 (17,024 puntos), septiembre de 2024 (14,776), diciembre de 2025 (9,987) y noviembre de 2024 (8,398).

En diciembre de 2024 el método sobreestima; en diciembre de 2025 subestima. Aunque reproduce la forma estacional, no anticipa completamente los cambios en la amplitud de esos picos. Se define error = observado − pronosticado: negativo indica sobreestimación y positivo subestimación.

Para SARIMA, los mayores errores absolutos medios por mes se concentran en mayo de 2025 (15,339), abril de 2025 (14,457), junio de 2025 (9,999) y agosto de 2026 (9,606). Los dos primeros presentan subestimación. SARIMAX muestra un patrón semejante, sin corregir sustancialmente esas dificultades.

Los promedios por fecha pueden incluir diferentes horizontes y números de evaluaciones: septiembre de 2024 aparece una vez, diciembre de 2024 cuatro y diciembre de 2025 nueve. No se deben comparar como tamaños muestrales iguales. En la línea base estacional las predicciones repetidas para un mismo mes coinciden con el mismo valor del año anterior; en SARIMA pueden variar según el origen.

# 19 Trazabilidad de funciones y productos

| **Función**     | **Qué realiza**                                      | **Producto**                                           |
|-----------------|------------------------------------------------------|--------------------------------------------------------|
| preparar        | Verifica faltantes y conserva valores.               | Serie sin cambios en ventas.                           |
| graficar_serie  | Representa la serie original.                        | figuras/serie.png                                      |
| descomponer     | Ajusta STL robusta.                                  | figuras/stl.png                                        |
| estacionariedad | ADF, diferencias y ACF/PACF.                         | adf.csv y figuras de diagnóstico.                      |
| elegir_sarima   | 16 ajustes, AIC, residuos y Ljung-Box.               | rejilla_sarima.csv, ljung_box_sarima.csv, residuos.png |
| modelo_sarima   | Crea una función que ajusta y pronostica por origen. | Pronósticos del SARIMA.                                |
| exogenas        | Calendario mensual histórico y futuro.               | exogenas.csv                                           |
| modelo_sarimax  | Ajusta por origen con calendario alineado.           | Pronósticos del SARIMAX.                               |
| fila y main     | Evalúan, ordenan y exportan.                         | resultados/metricas.csv                                |

## Problema de programación resuelto

Durante la integración apareció TypeError: cannot unpack non-iterable NoneType object al asignar orden, estacional = elegir_sarima(...). Esto indica que la función ejecutada no devolvió una pareja de valores. Se revisaron la sangría de def, la presencia del return y posibles definiciones duplicadas; después se confirmó la ejecución de los 16 ajustes. La evidencia compartida no permite atribuir exclusivamente el fallo a una sola causa interna.

Los avisos “pendiente” eran parte del diseño del guion con NotImplementedError y se fueron desplazando a la siguiente función sin implementar. La última ejecución compartida muestra los cuatro modelos sin avisos pendientes, lo que confirma la ejecución del recorrido implementado, no una validación de todos los supuestos estadísticos.

## Limitaciones que deben declararse

- ADF no rechaza raíz unitaria; d=D=1 es provisional y el MA estacional está cerca de la frontera.

- Selección de diferencias y órdenes con toda la serie antes del backtest.

- Rejilla de baja complejidad y evidencia de autocorrelación residual.

- Evaluación reciente, ventanas superpuestas y ausencia de una prueba formal de diferencias predictivas.

- Solo una exógena agregada; no se estudian mecanismos causales ni intervalos de pronóstico.

- Versiones exactas del entorno original y estado final de integración en main requieren comprobación del grupo.

# Parte II Informe para el miniproyecto

Las secciones siguientes corresponden a la estructura obligatoria de docs/informe.md. El archivo Markdown del paquete complementario contiene esta versión con fórmulas en LaTeX e imágenes con rutas relativas. Las cifras complementarias se identifican como reproducción con el mismo Excel y procedimiento.

# 1. La serie

Analizamos el índice mensual nacional de ventas reales de prendas de vestir y textiles de la Encuesta Mensual de Comercio (EMC) del DANE. La fuente es el anexo anex-EMC-ComercioMinorista-ago2026.xlsx, hoja 2.2, columna 4. Prendas de vestir y textiles. La hoja declara base 2019 = 100 y carácter provisional mediante la marca p. La serie comprende 92 observaciones de enero de 2019 a agosto de 2026, con frecuencia mensual y fechas de inicio de mes (MS). No se trata de cantidades de prendas ni de ingresos en pesos.

La elección permite estudiar un patrón anual marcado, cambios de nivel y una caída excepcional en 2020. El propósito fue comprobar si modelos SARIMA y SARIMAX mejoraban la predicción de referencias simples.

Fuente oficial: DANE EMC históricos (https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/encuesta-mensual-de-comercio-emc/encuesta-mensual-de-comercio-emc-historicos). El anexo de agosto de 2026 (https://www.dane.gov.co/files/operaciones/EMC/anex-EMC-ComercioMinorista-ago2026.xlsx) corresponde al archivo utilizado. Las condiciones generales de uso del DANE (https://www.dane.gov.co/index.php/en/terrminos-y-condiciones-dane) autorizan uso, transformación y análisis con atribución. Se conserva la cita: “Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co”. No se asigna por inferencia una licencia Creative Commons de otro producto.

![Figura del informe](../figuras/serie.png)

*Serie mensual del índice de ventas reales*

El script preparar_datos.py leyó el anexo, limpió encabezados, completó las etiquetas de año con ffill, convirtió los meses a números y construyó fechas. Completar el año no equivale a imputar ventas. Se comprobó ausencia de duplicados, de meses faltantes y de valores vacíos en el índice. El resultado se guardó en datos/prendas_vestir.csv.

Se conservaron todas las observaciones. Los picos de diciembre son recurrentes y no se eliminaron como errores. La caída de 2020 se mantuvo como parte de la historia, sin inferir una causa solamente de la gráfica. La decisión que acompaña a las métricas es: “Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020”.

# 2. Componentes

![Figura del informe](../figuras/stl.png)

*Descomposición STL robusta*

Se utilizó STL con period=12 y robust=True, bajo la representación aditiva:

$$y_t = T_t + S_t + R_t$$

La tendencia crece hasta aproximadamente 2022, disminuye hasta 2024 y luego presenta una recuperación parcial y estabilización. El ajuste robusto reduce la influencia de observaciones excepcionales al estimar los componentes; no cambia los valores originales. Por ello la caída abrupta de 2020 se concentra principalmente en el residuo.

El componente estacional promedio por mes calendario fue:

# 2 Componentes continuación

| **Mes**    | **Componente estacional promedio en puntos** |
|------------|----------------------------------------------|
| Enero      | -23,370                                      |
| Febrero    | -34,361                                      |
| Marzo      | -25,824                                      |
| Abril      | -27,034                                      |
| Mayo       | -13,861                                      |
| Junio      | -1,567                                       |
| Julio      | -11,822                                      |
| Agosto     | -17,789                                      |
| Septiembre | -15,743                                      |
| Octubre    | -12,115                                      |
| Noviembre  | 17,878                                       |
| Diciembre  | 167,232                                      |

Diciembre presenta el mayor aporte estacional, seguido por noviembre. El mínimo corresponde a febrero. Los valores son puntos respecto a la tendencia y no porcentajes; un componente negativo no significa ventas negativas. STL permite variaciones entre años: esta tabla resume promedios y no parámetros constantes. Enero a agosto cuentan con ocho observaciones por mes y septiembre a diciembre con siete.

El residuo de mayor magnitud absoluta se ubica en abril de 2020, con -65,108 puntos. La observación queda por debajo de la suma estimada de tendencia y estacionalidad. Este residuo de descomposición es diferente de un error de pronóstico fuera de muestra.

Los valores detallados y las figuras se completaron mediante reproducción con el mismo Excel y procedimiento. Las versiones utilizadas en esa verificación fueron statsmodels 0.15.0 y holidays 0.107.

# 3. Líneas base y backtest

Se mantuvo sin modificaciones comun.py. El backtest usa n_prueba=24 y h=12: la ventana evaluada es septiembre de 2024 a agosto de 2026 y se forman 13 orígenes con doce meses futuros observados disponibles.

El primer entrenamiento abarca enero de 2019 a agosto de 2024, con 68 meses, y evalúa septiembre de 2024 a agosto de 2025. El último termina en agosto de 2025, con 80 meses, y evalúa septiembre de 2025 a agosto de 2026. Es un esquema de entrenamiento expansivo y origen móvil. Hay 156 comparaciones por modelo, con superposición: no son 156 meses distintos ni errores independientes.

En cada origen, las funciones reciben solo las ventas hasta ese momento. SARIMA y SARIMAX reestiman sus parámetros con ese entrenamiento y la exógena futura se obtiene del calendario conocido. La selección previa de diferencias y órdenes sí utilizó toda la serie; esa es una limitación de la evaluación exploratoria y debe distinguirse del ajuste por origen.

Las métricas por origen, con horizonte H=12, son:

$$\mathrm{MAE}=\frac{1}{H}\sum_{j=1}^{H}|y_j-\hat y_j|$$

$$\mathrm{RMSE}=\sqrt{\frac{1}{H}\sum_{j=1}^{H}(y_j-\hat y_j)^2}$$

$$\mathrm{MAPE}=\frac{100}{H}\sum_{j=1}^{H}\left|\frac{y_j-\hat y_j}{y_j}\right|$$

Después se promedia cada métrica entre los 13 orígenes. El RMSE final es un promedio de RMSE por origen, no la raíz del error cuadrático medio de todos los errores agrupados. MAE y RMSE se expresan en puntos del índice. MAPE es porcentual y no equivale a una exactitud ni a un intervalo de confianza.

| **Línea base**     | **RMSE** | **MAE** | **MAPE (%)** |
|--------------------|----------|---------|--------------|
| Estacional ingenuo | 6,26     | 5,54    | 4,87         |
| Ingenuo            | 63,08    | 38,41   | 30,10        |

El ingenuo repite el último valor observado. El estacional ingenuo repite los valores del mismo mes del año anterior y gana en las tres métricas. Su ventaja es consistente con la utilidad del patrón anual en el periodo reciente. La caída de 2020 está dentro de los entrenamientos, pero no forma parte de la ventana de evaluación.

# 4. Estacionariedad e identificación

ADF contrasta como hipótesis nula la presencia de una raíz unitaria. En la serie original se usó regression="ct" y en las versiones diferenciadas regression="c", con rezagos seleccionados por AIC.

| **Versión**           | **d** | **D** | **Meses** | **Valor p** | **Rezagos ADF** |
|-----------------------|-------|-------|-----------|-------------|-----------------|
| Original              | 0     | 0     | 92        | 0,590762    | 12              |
| Diferencia regular    | 1     | 0     | 91        | 0,113224    | 11              |
| Diferencia estacional | 0     | 1     | 80        | 0,139772    | 12              |
| Ambas diferencias     | 1     | 1     | 79        | 0,100338    | 11              |

En ninguna versión se rechazó raíz unitaria al 5 %. No se interpreta el menor valor p como criterio suficiente para elegir diferencias. Se consideró también la persistencia de las autocorrelaciones y el comportamiento gráfico.

![Figura del informe](../figuras/diferencias.png)

*Comparación de versiones diferenciadas*

La diferencia regular conserva los picos anuales. La estacional reduce esos picos pero mantiene persistencia de corto plazo. Ambas diferencias reducen esa persistencia y producen fluctuaciones más centradas alrededor de cero. Se escogió provisionalmente d=1,D=1, sin afirmar estacionariedad confirmada. La transformación es:

$$ w_t=(1-B)(1-B^{12})y_t=y_t-y_{t-1}-y_{t-12}+y_{t-13} $$

![Figura del informe](../figuras/acf_pacf.png)

*ACF y PACF con ambas diferencias*

La verificación numérica identifica picos fuera de bandas aproximadas del 95 % en ACF para los rezagos 3, 9 y 12 y en PACF para 3, 9, 12, 24 y 36. Son referencias puntuales, no pruebas de causalidad ni una identificación automática de órdenes. La PACF se calculó con method="ywm".

No hay un corte sencillo que determine un único AR o MA. Se exploró una rejilla parsimoniosa p,q,P,Q∈{0,1}, que no representa directamente todos los rezagos destacados. El pico negativo estacional y el MA estimado cerca de -1 aconsejan revisar la posibilidad de diferenciación excesiva en análisis posteriores, sin considerarla demostrada.

# 5. Modelos clásicos

Se ajustaron 16 SARIMA manteniendo d=D=1, periodo 12 y ausencia de tendencia determinista (trend="n"). Todos convergieron. Se usó la serie original preparada: el modelo aplica las diferencias internamente.

| **Orden** | **Orden estacional** | **AIC** |
|-----------|----------------------|---------|
| (0,1,0)   | (1,1,1,12)           | 632,719 |
| (0,1,0)   | (0,1,1,12)           | 632,936 |
| (1,1,1)   | (0,1,1,12)           | 633,122 |
| (1,1,1)   | (1,1,1,12)           | 633,228 |
| (0,1,1)   | (1,1,1,12)           | 634,289 |
| (1,1,0)   | (1,1,1,12)           | 634,443 |
| (0,1,1)   | (0,1,1,12)           | 634,449 |
| (1,1,0)   | (0,1,1,12)           | 634,654 |
| (0,1,0)   | (1,1,0,12)           | 646,293 |
| (1,1,1)   | (1,1,0,12)           | 647,209 |
| (0,1,1)   | (1,1,0,12)           | 647,626 |
| (1,1,0)   | (1,1,0,12)           | 647,832 |
| (1,1,1)   | (0,1,0,12)           | 654,806 |
| (0,1,0)   | (0,1,0,12)           | 655,999 |
| (0,1,1)   | (0,1,0,12)           | 657,427 |
| (1,1,0)   | (0,1,0,12)           | 657,523 |

El mínimo de AIC fue 632,719 para SARIMA(0,1,0)(1,1,1)\_{12}. El segundo modelo presenta AIC 632,936: la diferencia de 0,217 es pequeña. Se conservó la selección automática del mínimo, pero no se afirma superioridad concluyente sobre la alternativa más sencilla.

Con B como operador de rezago, la ecuación estructural es:

$$ (1-\Phi B^{12})(1-B)(1-B^{12})y_t=(1+\Theta B^{12})\varepsilon_t $$

La reproducción del ajuste completo dio Φ≈0,181652, Θ≈-0,999776 y σ²≈125,856801, con AIC 632,718646, consistente con la salida redondeada del grupo. Por tanto:

$$ (1-0{,}181652B^{12})(1-B)(1-B^{12})y_t\approx(1-0{,}999776B^{12})\varepsilon_t $$

El coeficiente MA estacional muy cercano a -1 requiere cautela sobre invertibilidad y posible cancelación asociada a la diferencia estacional; no se diagnostica sobrediferenciación únicamente con ese valor.

![Figura del informe](../figuras/residuos.png)

*Residuos SARIMA y su ACF*

Se excluyeron los primeros 13 residuos o un tramo mayor si lo exigía la inicialización. Ljung-Box utiliza model_df=2, por los términos AR y MA estacionales.

| **Rezago** | **Estadístico reportado** | **Valor p reportado** |
|------------|---------------------------|-----------------------|
| 12         | 23,151039                 | 0,010203              |
| 24         | 34,360534                 | 0,045129              |

Se rechaza al 5 % la ausencia conjunta de autocorrelación hasta ambos rezagos. El diagnóstico no es plenamente satisfactorio. La reproducción de estos valores difiere únicamente en decimales menores. La gráfica presenta errores históricos más grandes en 2020-2022 y menor dispersión reciente. Entre los mayores residuos reproducidos están diciembre de 2020 (-45,762 puntos), diciembre de 2021 (+44,865), marzo de 2020 (-40,289) y enero de 2022 (-37,262). No se verificó formalmente normalidad ni varianza constante.

La exógena del SARIMAX fue el conteo mensual de fechas festivas nacionales de Colombia con holidays. Incluye festivos en fines de semana y no equivale a días hábiles. Se conoce de antemano por calendario y cubre enero de 2019 a agosto de 2027. Esta cobertura no implica que ya se haya generado un pronóstico final para 2026-2027.

Se mantuvieron los órdenes y se reestimaron los coeficientes con la exógena en cada entrenamiento. El RMSE pasó de 8,54 a 8,56, el MAE de 7,30 a 7,31 y el MAPE de 7,29 % a 7,30 %. No hubo mejora observada; tampoco se realizó una prueba formal que establezca equivalencia o diferencia estadística de precisión.

# 6. Tabla de métricas

| **Modelo**                          | **Decisión**                                                                                                                     | **RMSE** | **MAE** | **MAPE (%)** |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------|---------|--------------|
| Estacional ingenuo                  | Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020. | 6,26     | 5,54    | 4,87         |
| SARIMA(0,1,0)(1,1,1,12)             | Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020. | 8,54     | 7,30    | 7,29         |
| SARIMAX(0,1,0)(1,1,1,12) + exógenas | Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020. | 8,56     | 7,31    | 7,30         |
| Ingenuo                             | Sin huecos: no se imputa. Se conservan todas las observaciones, incluidos los picos estacionales y la caída excepcional de 2020. | 63,08    | 38,41   | 30,10        |

La tabla está ordenada por RMSE. Las métricas coinciden con la última ejecución compartida desde Codespaces y con la reproducción al redondear a dos decimales.

# 7. Conclusión

Entre SARIMA y SARIMAX, el SARIMA obtuvo menores errores; sin embargo, ninguno superó la mejor línea base. Frente al estacional ingenuo, SARIMA aumentó el RMSE en 2,28 puntos del índice y el MAE en 1,76 puntos; el MAPE aumentó en 2,42 puntos porcentuales. No se obtuvo una mejora sobre esa referencia.

El estacional ingenuo fue el mejor de los cuatro métodos, con RMSE 6,26, MAE 5,54 y MAPE 4,87 %. Esa es la referencia observada que el miniproyecto 2 debe superar bajo un protocolo comparable. El patrón anual reciente aporta más ventaja que las especificaciones clásicas evaluadas, sin que ello descarte otros modelos o variables.

La reproducción de errores por fecha ubica dificultades de la línea base estacional en diciembre de 2024 (error absoluto 17,024 puntos, sobreestimación), septiembre de 2024 (14,776, sobreestimación), diciembre de 2025 (9,987, subestimación) y noviembre de 2024 (8,398, sobreestimación). SARIMA presenta mayores errores absolutos medios por fecha en mayo de 2025 (15,339), abril de 2025 (14,457), junio de 2025 (9,999) y agosto de 2026 (9,606). En abril y mayo de 2025 subestima las observaciones.

Estos resúmenes tienen distintos números de evaluaciones por fecha y pueden mezclar horizontes. No son errores de meses independientes con igual representación. El gráfico siguiente muestra solo el último origen como ejemplo y no sustituye las métricas globales.

![Figura del informe](../figuras/ultimo_origen.png)

*Último origen de evaluación*

Las conclusiones se limitan al periodo reciente, con ventanas superpuestas, selección de estructura con toda la serie, una rejilla pequeña y autocorrelación residual. ADF no confirmó estacionariedad al 5 %. Para trabajos posteriores se propone revisar las diferencias, ampliar modelos con moderación y separar estrictamente la selección de la evaluación. No se modificó el backtest del docente ni se ocultó el resultado favorable a la línea base.

# Verificaciones de entrega y continuidad

- Ejecutar desde un entorno con dependencias instaladas: preparar_datos.py y miniproyecto.py deben terminar sin errores y mostrar los cuatro métodos.

- Conservar comun.py intacto y comprobar que la configuración activa apunta al CSV de prendas, no a Air Passengers.

- Revisar que docs/informe.md renderice las figuras con rutas ../figuras/ y las fórmulas LaTeX. Las imágenes del paquete fueron regeneradas; conviene conservar las que produce la versión final del repositorio si hay diferencias de estilo.

- Para que los nuevos detalles aparezcan también en la salida del guion, añadir las impresiones de estacionalidad, residuo máximo y coeficientes indicadas abajo; estos cálculos fueron verificados, pero no se afirma que el grupo ya haya añadido esas impresiones.

- Actualizar datos/README.md y README.md con fuente, condiciones de uso, instrucciones y versiones reales del entorno.

- Confirmar integrantes y cuentas, aceptación de invitaciones y evidencias de aportes. Verificar pull requests e integración en main antes de compartir la entrega definitiva.

- Registrar el avance con commit y sincronizar. Cada integrante debe abrir la rama integrada y ejecutar el código desde su propia cuenta, según las instrucciones del docente.

## Salidas complementarias de STL

Dentro de descomponer, después de resultado = STL(...).fit(), pueden añadirse estas instrucciones para que el guion imprima los valores utilizados en el informe:

mensual = resultado.seasonal.groupby(serie.index.month).mean()  
print(mensual.to_string())  
fecha = resultado.resid.abs().idxmax()  
print(fecha, resultado.resid.loc\[fecha\])

## Coeficientes del modelo elegido

Dentro de elegir_sarima, después de recuperar el ajuste seleccionado, puede imprimirse:

print(ajuste.params.to_string())

La tabla de meses con errores procede de conservar las predicciones individuales en la reproducción. El backtest del docente no devuelve ese detalle: solo métricas por origen. No se debe afirmar que errores_verificacion.csv era una salida original del guion. Se incluye en el paquete como evidencia complementaria de la verificación.

# Referencias y procedencia de los resultados

1\. Departamento Administrativo Nacional de Estadística. Encuesta Mensual de Comercio. Anexo comercio al por menor de agosto de 2026, hoja 2.2. Excel original aportado por el grupo, base 2019 = 100. Fecha de consulta de páginas: 30 de octubre de 2026.

https://www.dane.gov.co/files/operaciones/EMC/anex-EMC-ComercioMinorista-ago2026.xlsx

https://www.dane.gov.co/index.php/estadisticas-por-tema/comercio-interno/encuesta-mensual-de-comercio-emc/encuesta-mensual-de-comercio-emc-historicos

2\. DANE. Términos y condiciones generales de uso. Se utilizó para documentar la atribución, sin extender licencias de otros productos al anexo.

https://www.dane.gov.co/index.php/en/terrminos-y-condiciones-dane

3\. statsmodels. Documentación oficial de STL y acorr_ljungbox. Se utilizó como referencia de implementación para descomposición y diagnóstico.

https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.STL.html

https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html

4\. Código comun.py y funciones de miniproyecto.py compartidos por el grupo durante el desarrollo. La evaluación reproduce exactamente los valores predeterminados n_prueba=24 y h=12.

5\. Salidas de Codespaces: tabla ADF, rejilla AIC, Ljung-Box y métricas finales. Se preservaron sus cifras reportadas. Las figuras se regeneraron a partir del Excel original con la metodología descrita.

6\. Verificación complementaria: Python con statsmodels 0.15.0 y holidays 0.107. ADF coincide con los valores reportados; AIC y métricas coinciden al redondear. STL, coeficientes y errores por fecha se completaron en esta reproducción. Estos valores no constituyen una nueva búsqueda de modelos ni una modificación del repositorio.


[Informe_GitHub_2026.md](https://github.com/user-attachments/files/34202378/Informe_GitHub_2026.md)
