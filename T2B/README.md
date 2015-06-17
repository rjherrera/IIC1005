T2B - Turing
============

[Enunciado Tarea 2B](T2B.pdf)

[turing](turing.txt)

El link es [martinugarte.com -> code:oyycxawfsz](http://martinugarte.com/turingmachine/shared/oyycxawfsz), pero se incluye igualmente el código de la máquina en el repositorio.

### Acerca del código

Acepta palabras que cumplan con

```
L = { aⁱbʲcᵏ | j = i − 2k }
```

De modo que solo permite que el orden sea de la 'a' a la 'b' y luego a la 'c', sin permitir palabras como 'aabca', que si bien cumplen con la cantidad de cada letra, tienen una 'a' después de letras "mayores".