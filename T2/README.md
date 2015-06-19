T2 - SQL Mining
===============

[Enunciado Tarea 2](T2.pdf)

Workflow Tarea 3
-----------------
#####OS: Mac OS X, Ubuntu 14.04
#####Python: 3.4.1, 3.4.3
#####Lib: Anaconda, MySQLclient


#### Raimundo Herrera, Benjamín Assael

Introducción
-------------
Este archivo tiene como finalidad describir el correcto funcionamiento de la tarea. Es necesario ejecutar los pasos descritos a continuación en orden para el correcto entendimiento del código.

Pasos de Ejecución
-------------------
1.  El archivo [general_information.py](general_information.py) genera el primer reconocimiento a la base de datos. Éste imprime todos los datos necesarios para conocer a grandes rasgos el contenido del dataset.

2.  Una vez conocido el dataset, es necesario ejecutar el archivo [dataset_generator.py](dataset_generator.py). Este archivo genera un csv con todos los datos necesarios por usuario para realizar la mineria de datos. El tiempo estimado de ejecución es de 6:30 minutos.

3.  Una vez que el dataset esta listo, el archivo [logistic_regression.py](logistic_regression.py) se encarga de hacer la regresión logística. Este archivo genera todas las métricas necesarias para hacer un análisis cuantitativo.  También se generan las métricas de evaluación del clasificador Decision Trees para luego realizar una comparación con los datos de la regresión logística.

4.  El archivo [roc_curve.py](roc_curve.py) genera un gráfico con los promedios de las cuatro regresiones logisticas realizadas.  El código de los gráficos se hizo en base al código de ejemplo de la página de scikit-learn acerca de las curvas roc con cross validation: [Scikit-learn ROC plots](http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html#example-model-selection-plot-roc-crossval-py).

5. 	En el archivo [std_mean_analysis.py](std_mean_analysis.py) se encuentra el desarrollo del promedio y desviación estandar por cada feature del dataset.

6.  En el archivo [report.pdf](report.pdf) se encuentra todo el análisis cuantitativo de los datos conseguidos y las conclusiones de la tarea.
