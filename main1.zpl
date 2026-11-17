# Codigo del trabajo practico 2 de ACN.

# Grupo: Felipe Vilaseca Navajas y Manuel Ferrario

# 1 -> Plantear modelo de programación lineal:

# ------ (1) Definción de variables:

# Lista de meses
set T := { 1 .. 24 };

# Productos que hay que producir en la fabrica
set P := { "A", "B", "C", "D", "E" };

# Demanda por mes (1 = Ene/27 ... 24 = Dic/28) y producto
param d[T * P] := read "demanda.csv" as "<1n, 2s> 3n" skip 1;

# Variable de producción por <t,p>
var x[T * P];

# Costo de producir cualquier producto
param costo := 370;

# Variable de stock
var s[{0 .. 24} * P] >= 0; # El stock necesita un valor en t = 0.

# Variable para lotes de 10
var y[T * P] integer >= 0 <= 12;  

# ------ (2) Función Objetivo:

minimize costo_produccion: sum <t,p> in T * P: costo * x[t,p];

# ------ (3) Restricciones:

subto prod_max_producto: forall <t,p> in T * P: 0 <= x[t,p] <= 120;

subto lotes_10: forall <t,p> in T * P: x[t,p] == 10 * y[t,p];

subto stock_inicial: forall <p> in P: s[0,p] == 0;

subto stock: forall <t,p> in T * P: s[t,p] == s[t-1,p] + x[t,p] - d[t,p];

subto max_stock: forall <t> in T: sum <p> in P: s[t,p] <= 900;

