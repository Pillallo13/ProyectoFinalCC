import json
from controlador.ArbolController import ArbolController

with open("../modelo/datos/campanna/redPoliticaCampana.json", encoding="utf-8") as f:
    datos = json.load(f)

arbol_ctrl = ArbolController(datos)
arbol_ctrl.mostrar_arbol()

print("\nHijos del Alcalde:")
print(arbol_ctrl.obtener_hijos("Alcalde Mermelada"))

print("\nPadre del Inspector Mañoso:")
print(arbol_ctrl.obtener_padre("Inspector Mañoso"))

print("\nProfundidad del Inspector Mañoso:")
print(arbol_ctrl.obtener_profundidad("Inspector Mañoso"))

print("\nAtributos de ID JSON 6:")
print(arbol_ctrl.obtener_atributos(6))
