extends Node2D

# Los 5 colores posibles
var colores = ["Rojo", "Azul", "Verde", "Amarillo", "Morado"]

# El orden que el jugador debe seguir (se genera aleatorio)
var orden_correcto = []

# Lo que el jugador lleva cortado hasta ahora
var orden_jugador = []

# Cuántos cables hay en la secuencia (puedes cambiar esto)
var longitud_secuencia = 3

func _ready():
	generar_secuencia()
	actualizar_instruccion()

func generar_secuencia():
	# Mezcla los colores y toma los primeros N
	var mezclados = colores.duplicate()
	mezclados.shuffle()
	orden_correcto = mezclados.slice(0, longitud_secuencia)
	print("Orden correcto: ", orden_correcto)  # Para que lo veas en consola mientras pruebas

func actualizar_instruccion():
	# Busca el Label y actualiza el texto
	var label = $Label
	var siguiente = orden_correcto[orden_jugador.size()]
	label.text = "✂ Corta el cable: " + siguiente

func cable_cortado(color: String):
	var siguiente_esperado = orden_correcto[orden_jugador.size()]
	
	if color == siguiente_esperado:
		orden_jugador.append(color)
		print("✅ Correcto! Cortaste: ", color)
		
		if orden_jugador.size() == orden_correcto.size():
			nivel_superado()
		else:
			actualizar_instruccion()
	else:
		print("❌ Incorrecto! Debías cortar: ", siguiente_esperado)
		nivel_fallido()

func nivel_superado():
	$Label.text = "🎉 ¡NIVEL SUPERADO!"
	# Aquí luego puedes cambiar de escena o mostrar pantalla de victoria

func nivel_fallido():
	$Label.text = "💥 ¡FALLASTE! Reiniciando..."
	await get_tree().create_timer(2.0).timeout
	# Reinicia la secuencia
	orden_jugador = []
	generar_secuencia()
	actualizar_instruccion()

func _on_rojo_pressed() -> void:
	cable_cortado("Rojo")


func _on_azul_pressed() -> void:
	cable_cortado("Azul")


func _on_verde_pressed() -> void:
	cable_cortado("Verde")


func _on_amarillo_pressed() -> void:
	cable_cortado("Amarillo")


func _on_morado_pressed() -> void:
	cable_cortado("Morado")
