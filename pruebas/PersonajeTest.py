from controlador.biografia.BiografiaController import BiografiaController

controller = BiografiaController()
personaje = controller.get_personaje()

print("=== DATOS DEL PERSONAJE ===")
print(f"Nombre completo: {personaje.nombre_completo}")
print(f"Fecha de nacimiento: {personaje.fecha_nacimiento}")
print(f"Lugar de nacimiento: {personaje.lugar_nacimiento}")
print(f"Profesión: {personaje.profesion}")
