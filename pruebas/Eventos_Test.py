from controlador.biografia.BiografiaController import BiografiaController

# Crear instancia del controlador
controller = BiografiaController()

# Buscar un evento específico por su ID (por ejemplo, "evento3")
evento = controller.buscar_evento_por_id("evento1")

print("=== RELATO HISTÓRICO ===")
if evento:
    print(f"ID: {evento.id_evento}")
    print(f"Texto: {evento.texto}")
else:
    print("❌ Evento no encontrado.")
