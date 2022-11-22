# Trabajo Práctico 2 - SDN

## Inicializacion

Se debe comenzar por iniciar el controlador para que POX aplique las reglas del firewall a los switches de la topologia.

Luego, se inicializa la topologia en la cual se debe especificar la cantidad de switches que se desean utilizar.

Todo esto se puede lograr ejecutando el script provisto `run.sh <switches_amount>` cuyo parametro establece la cantidad de switches a utilizar y se encarga de inicializar el controlador y la topologia.

---

## Ejecucion

Una vez inicializada la topologia, se puede proceder a ejecutar las pruebas para validar el funcionamiento del firewall.

A continuacion, se especifica como ejecutar cada una de las reglas por defecto dadas en la consigna.

### Regla 1
> Se deben descartar todos los mensajes cuyo puerto destino sea 80

En la terminal que ejecuta `mininet`, ejecutar `xterm` para abrir las terminales de los hosts.
```bash
mininet> xterm h1 h2
```

En la terminal de `h1`, ejecutar:
```bash
iperf -s -p 80
```

En la terminal de `h2`, ejecutar:
```bash
iperf -c 10.0.0.1 -p 80
```

De esta forma se podra observar que el mensaje es descartado por el firewall al intentar ejecutarse el flujo generado por `iperf`.


### Regla 2

> Se deben descartar todos los mensajes que provengan del host 1, tengan como puerto destino el 5001, y esten utilizando el protocolo UDP.

De la misma forma que en la regla anterior, se debe abrir una terminal para cada host siendo necesario que un host sea el 1, 

```bash
mininet> xterm h1 h2
```

y ejecutar `iperf` en el host 1 e `iperf` en el host 2, pero esta vez especificando el puerto 5001 y el protocolo UDP.

En la terminal de `h2`, ejecutar:
```bash
iperf -s -p 5001 -u
```

En la terminal de `h1`, ejecutar:
```bash
iperf -c 10.0.0.2 -p 5001 -u
```

### Regla 3

> Se debe elegir dos hosts cualquiera, y los mismos no deben poder comunicarse de ninguna forma.

Para probar esta regla solo es necesario ejecutar en la terminal de `mininet` el siguiente comando:

```bash
mininet> pingall
```

De esta forma se podra observar que los hosts elegidos (en este caso, estableciendo los parametros para elegir h2 y h4) no pueden comunicarse entre si.

```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 
h2 -> h1 h3 X 
h3 -> h1 h2 h4 
h4 -> h1 X h3 
*** Results: 16% dropped (10/12 received)
```