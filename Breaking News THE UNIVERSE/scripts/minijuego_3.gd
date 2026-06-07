extends Minigame

const sfx_impact = preload("res://sounds/minigame_3/impacto_de_roca/impacto_de_roca.mp3")
const sfx_win = preload("res://sounds/minigame_3/foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_3/foleys/perdiste.mp3")

var colores = ["Rojo", "Azul", "Verde", "Amarillo", "Morado"]
var orden_correcto = []
var orden_jugador = []
var longitud_secuencia = 3
var texturas_originales = {}
var texturas_rotas = {}

func _ready():
	generar_secuencia()
	actualizar_instruccion()
	for color in colores:
		var planeta = get_node(color)
		texturas_originales[color] = planeta.texture_normal
		texturas_rotas[color] = planeta.texture_pressed
		
	var game_manager = get_parent()
	if game_manager and game_manager.has_node("GameTimer"):
		var game_timer = game_manager.get_node("GameTimer")
		game_timer.minigame_timed_out.connect(_on_timeout)

func generar_secuencia():
	var mezclados = colores.duplicate()
	mezclados.shuffle()
	orden_correcto = mezclados.slice(0, longitud_secuencia)
	print("Orden correcto: ", orden_correcto)

func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func actualizar_instruccion():
	var siguiente = orden_correcto[orden_jugador.size()]
	$Label.text = "Explota el planeta: " + siguiente

func cable_cortado(color: String):
	if orden_jugador.size() >= orden_correcto.size():
		return
	
	play_sound(sfx_impact, -15.0)
	
	var siguiente_esperado = orden_correcto[orden_jugador.size()]
	
	if color == siguiente_esperado:
		orden_jugador.append(color)
		var planeta = get_node(color)
		planeta.texture_normal = texturas_rotas[color]
		planeta.disabled = true
		
		if orden_jugador.size() == orden_correcto.size():
			nivel_superado()
		else:
			actualizar_instruccion()
	else:
		var planeta = get_node(color)
		planeta.button_pressed = false
		nivel_fallido()

func nivel_superado():
	$Label.text = "NIVEL SUPERADO!"
	for color in colores:
		get_node(color).disabled = true
	play_sound(sfx_win, -2.0)
	completed.emit()

func _on_timeout() -> void:
	play_sound(sfx_lose, -2.0)

func nivel_fallido():
	$Label.text = "No Conseguido, Reiniciando..."
	for color in colores:
		var planeta = get_node(color)
		planeta.disabled = false
		planeta.button_pressed = false
		planeta.texture_normal = texturas_originales[color]
	await get_tree().create_timer(2.0).timeout
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
