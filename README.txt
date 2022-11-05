La presente carpeta corresponde a la tarea 2 parte 2 del curso CC3501: "Modelación y Computación 
Gráfica para Ingenieros", dentro de la cual se encuentran todos los archivos necesarios para
correr lo pedido en el pdf de la tarea.

En el archivo path, se encuentran dos funciones, una para encontrar el path hacia los assets definidos 
para cada casa y otra para encontrar el path hacia las instrucciones para la elaboración de cada figura.

En basic shapes se encuentra la clase encargada de hacer figuras básicas, además de 
poder operar con dichas figuras para mezclarlas, aplicarles transformaciones, etc, además tiene una serie
de funciones que permitieron facilitar el trabajo a la hora de hacer figuras medianamente complejas.

En constants están las constantes definidas para el tamaño de la ventana, la velocidad de la cámara, sensibilidad
del mouse y otras constantes. En controller está el controlador que se encarga de manejar la cámara para poder moverse libremente 
única y exclusivamente a través del mapa, recibiendo input tanto del teclado como del mouse, como si de un juego fps se tratase,
además de generar la vista y los 2 tipos distintos de proyecciones, ortogonal y en perspectiva.

En drawable_shapes está la primera superclase abstracta, AbstractShape, encargada de crear figuras medianamente complejas
a través de métodos bastante intutivos y la introducción al manejo de las texturas. Posteriormente, dentro del mismo archivo,
tenemos una subclase, AdvancedShape, la cual se encarga de crear figuras avanzadas usando un set de instrucciones
definido en un archivo .instruction en la carpeta instructions. Después, tenemos 3 subclases de AdvancedShape en drawable_houses.py,
las cuales sirven para crear los 3 modelos de casas distintas en la escena, además de un set de funciones para realizar operaciones
sobre dichas casas.

También tenemos otra subclase de AdvancedShape en drawable_light_shapes llamada AdvancedShapeWithLight, que es básicamente lo mismo
que AdvancedShape, sólo que ahora se introduce el manejo de luces en conjunto a una figura. Además de ello, se crea otra clase llamada
AdvancedMultiShapeWithLight, que corresponde a una versión de AdvancedShapeWithLight, que permite el uso de varias gpuShapes, esto con
el fin de aplicarle determinadas transformaciones a un set de basic shapes dentro de una figura compleja, para así simular animaciones,
como por ejemplo tenemos en la clase Car, la cual corresponde a un auto con luces y 5 gpuShapes, una para la carrocería y las otras 4
para las ruedas, que se mueven dependiendo el tiempo.

Pasando a drawable_terrain tenemos las clases de Road, Land y Poste, además de algunas funciones para operar sobre un set de postes.
Tanto Road como Land corresponden a subclases de AdvancedShape, mientras que Poste corresponde a una subclase de AdvancedShapeWithLight.

En el archivo curvas.py, tenemos el set de funciones que permitieron modelar curvas con spline, en particular, la curva correspondiente
al trayecto que debe seguir el auto dentro de la escena.

En day_cycle.py está la función encargada de simular el día y la noche usando un parámetro de tiempo.

En data_sender está una de las clases más importantes que permitió el uso de la iluminación, la clase Data_Sender fue la encargada
de permitir el intercambio de información eficiente entre este programa y el programa que realiza el manejo de los shaders de iluminación.

En easy_shaders están los shaders que permitieron generar figuras con texturas, una vista, proyección, modelo, transformaciones e 
iluminación, además de una función para asignarle textura de assets a una figura particular.

En transformations están las transformaciones, vistas y proyecciones usadas en los shaders, los cuales no fueron tantas, ya que
la mayoría de transformaciones se hicieron en la fase pre-gpushape. En gpu_shape hay una serie de funciones encargadas de crear
un gpushape de manera bastante sencilla.

Finalmente, en main es donde se juntan todas las cosas mencionadas anteriormente y se echa a correr la escena tal cual como es pedido.

Las siguientes teclas corresponden a las acciones posibles a través del input del teclado:
#WASD permiten el movimiento
#Esc permite cerrar ventana
#q permite ver las líneas de las figuras
#Espacio permite cambiar entre una perspectiva u otra.

Con respecto al punto creativo, cabe mencionar la creación de un auto medianamente detallado, con texturas e iluminación creado
a partir de el uso de diversos métodos definidos en la larga jerarquía de clases en esta carpeta. Además de un ciclo día y noche
más realista debido al cambio tenue del color del fondo para reforzar aún más el efecto del día y la noche.

#autor: Diego Zúñiga
#fecha de entrega: 26-06-2022