T1 - Checkins
=============

[T1](Enunciado Tarea 1)

Sencilla aplicación web que provee información sobre checkins de foursquare. Despliega un muestreo de los checkins en un mapa interactivo en el cual se pueden ver imágenes de los lugares en cuestión, y permite ver, en otro mapa, las rutas recorridas por usuarios, además de marcar a sus amigos.

## Instalación

### Inicializando el sitio

Para usar la página web se recomienda no ejecutar simplemente los archivos .html sino que partir un servidor en localhost, para no tener conflictos con los archivos json abiertos localmente. Para esto, en un sistema linux con python, dirigirse al directorio donde esté el sitio y ejecutar en el shell la siguiente instrucción:

```python
python3 -m http.server
```

Una vez ejecutada se puede acceder a la página yendo a [http://localhost:8000/home.html](http://localhost:8000/home.html)

## Uso

Una vez dentro del sitio, podemos acceder a dos pestañas que otorgan distintas funcionalidades

### Primera pestaña: Información

En la primera pestaña visible se pueden ver datos obtenidos de los checkins del archivo raw_data/foursquare_checkins.csv (incluido en .gitignore por pesar mas de 100mb) obtenido al ejecutar en python 3 el archivo [data.py](data.py).

Junto a lo anterior hay un mapa que despliega todos los checkins de un muestreo aleatorio de 500 obtenido también con el mismo script. Para mejorar la visualización del mapa se ha utilizado un plugin para Leaflet que agrupa marcadores de ubicaciones según proximidad y el zoom al que se visualice:

[Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)

Cuando se hace click en un círculo que agrupa varios pines, este despliega circulos menores, o cuando están lo suficientemente separados, despliega derechamente los marcadores. Se ha añadido la funcionalidad de que al hacer click sobre un marcador este despliegue, de estar disponible, una imagen de las proximidades de la ubicación, obtenida de la utilización de la API de MediaWiki:

[MediaWiki](https://www.mediawiki.org/wiki/API)

Se prefiere la API anterior en desmedro de otras como Flickr, porque es más posible que provea imágenes relativas al lugar y descriptivas, ya que son usadas para entregar información más que para el uso personal y poco descriptivo de la ubicación que se les da a las imágenes de Flickr.

### Segunda pestaña: Búsqueda

En la segunda pestaña se pueden ver los checkins de usuarios específicos, obtenidos de un archivo json. Este archivo se encuentra en [processed_data/input3.json](processed_data/input3.json) y es abierto localmente porque el servidor [doge.ing.puc.cl](http://doge.ing.puc.cl/iic1005/input3.json) presenta complicaciones para obtener los archivos desde ahí como se explicará más adelante en [Explicación-JSONP](#explicación-jsonp).

Para desplegar los checkins, existe un formulario simple que permite elegir en un dropdown los usuarios, decidir si mostrar o no los amigos y las rutas, y finalmente, de modo opcional, filtrar por fecha los checkins a mostrar. El formulario tiene validación de campos, y solo permite ingresar fechas de formato "mm/yyyy". Se pueden escribir las fechas con ese formato o se puede utilizar el plugin incluido para que sea sencillo ingresarlas. El plugin usado es el Monthpicker basado en jquery-ui:

[MonthPicker](https://github.com/KidSysco/jquery-ui-month-picker)

Una vez que se ingresan los datos correctamente se despliegan los checkins pedidos, siendo azules los checkins del usuario, y de haber activado la opción "mostrar amigos", verde los checkins de sus amigos. El mapa se adapta a la zona donde están los checkins del usuario de modo que quede centrado y con un zoom adecuado. Si se activa la opción "mostrar recorridos" los checkins estarán unidos por rutas (rojas), y estas rutas son recorridas por una punta de flecha (azul), que va en orden cronológico avanzando dinámicamente por el camino que hizo el usuario. Para esto se utilizó parte del código del siguiente plugin:

[Leaflet.PolylineDecorator](https://github.com/bbecquet/Leaflet.PolylineDecorator)

## Notas

### Compatibilidad

La totalidad de las funciones del sitio fueron probadas en el navegador Google Chrome versión 41.0.2272.101 (64-bit), corriendo en Ubuntu.


### Semantic UI

Para el diseño y ciertas características de la página se utiliza el buenísimo framework de Semantic UI, usando muchos elementos suyos:

[Semantic UI](http://semantic-ui.com/)


### Explicación-JSONP

Muchos servidores presentan errores para la obtención de archivos json por métodos convencionales, usando las funciones disponibles de jQuery como getJSON o ajax:

```javascript
$.getJSON('http://doge.ing.puc.cl/iic1005/input3.json?callback=?', function(data) {});

$.ajax({
    url: 'http://doge.ing.puc.cl/iic1005/input3.json',
    type: 'GET',
    dataType: "jsonp",
    success: function(data){}
  });
```

Las complicaciones radican en que al intentar obtener json sin una función de callback desde un servidor, este responderá con el json o con un error debido a "Access-Control-Allow-Origin". En este caso el servidor responde con un error del tipo antes señalado, por lo que lo natural es pedir el json nuevamente, pero ahora con una función en el callback. Esto automáticamente hace que el request de json sea de tipo jsonp, y el servidor entrega el archivo sin problemas. Esto solucionaría el problema si el servidor tuviese una respuesta adecuada a los request de jsonp, porque si bien ambos formatos usan los mismos diccionarios, json entrega un archivo con contenido de tipo:

```JSON
{"name": "value"}
```

Mientras que un request de jsonp es a través de una url semejante a "http://url/path/to/API&callback=jQuery111206021413174457848_1428206897928&_=1428206897948" generando un archivo con una especie de función que contiene el mismo contenido:

```JSON
jQuery111206021413174457848_1428206897928({"name": "value"})
```

Si el servidor no devuelve algo con el formato explicado anteriormente, los request de jsonp resultarán en un error y no será posible traer contenido desde ahí. Para mas información sobre este error:

1) [stackoverflow](http://stackoverflow.com/questions/7936610/json-uncaught-syntaxerror-unexpected-token)

2) [stackoverflow](http://stackoverflow.com/questions/26196820/uncaught-syntaxerror-unexpected-token-when-parse-jsonp)