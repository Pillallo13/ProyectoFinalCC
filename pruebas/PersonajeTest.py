from controlador.biografia.BiografiaController import BiografiaController

# Crear una instancia del controlador
controller = BiografiaController()

# Obtener el personaje y mostrar sus datos
personaje = controller.get_personaje()

print("=== DATOS DEL PERSONAJE ===")
print(f"Nombre completo: {personaje.nombre_completo}")
print(f"Fecha de nacimiento: {personaje.fecha_nacimiento}")
print(f"Lugar de nacimiento: {personaje.lugar_nacimiento}")
print(f"Profesión: {personaje.profesion}")

# Mostrar el nombre del jugador desde el controlador
print(controller.obtener_nombre_jugador())
