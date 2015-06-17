T1B - Crontab
=============

[Enunciado Tarea 1B](T1B.pdf)

[Archivo script.py](script.py)

### Configurando el cron

Para usar el cron del sistema debemos en el terminal escribir

```python
crontab -e
```

Si es la primera vez que modificamos algo, nos hará elegir el editor de texto. Para los siguientes pasos se usa "vim".

Una vez abierto el crontab en modo edición de texto, debemos ir al fondo del documento y crear la nueva tarea. Para que esta se ejecute a las 7 de la mañana todos los días el comando debe ser señalado de este modo:

```
0 7 * * * python3 /path/to/script.py
```

Donde los primeros números indican minutos y horas, es decir a las 7 horas con 0 minutos, luego los asteriscos siguientes indican, a grandes rasgos, que el script será ejecutado todos los días del mes. Después se señala el comando, primero señalando con que se ejecuta, en este caso python3 y, separada con un espacio, se indica la ruta absoluta al script, por ejemplo "/home/username/desktop/script.py".

* Probado en ubuntu 14.04

### Detalles del script

El script obtiene de la API de Yahoo el pronóstico para Santiago, y lo transforma en un string sencillo para luego abrir una conexión SMTP con el mail del usuario, y así poder enviar el mail. En la línea 22, basta cambiar la dirección del destinatario para recibir el mail donde se desee.