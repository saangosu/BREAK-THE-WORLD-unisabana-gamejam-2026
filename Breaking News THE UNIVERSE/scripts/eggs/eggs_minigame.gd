extends Minigame
class_name EggsLevel

# OnReadies
@onready var egg_1 = $Egg1
@onready var egg_2 = $Egg2
@onready var egg_3 = $Egg3

# constants
const winning_goal = 3

const sfx_viscosity = preload("res://sounds/minigame_1/tazon/viscosidad.mp3")
const sfx_win = preload("res://sounds/minigame_1/Foleys/gano.mp3")
const sfx_lose = preload("res://sounds/minigame_1/Foleys/perdiste.mp3")

# variables
var level_score = 0
var eggs : Array = []

var game_over = false
var status_label: Label

@onready var bowl_sprite = $Bowl
const tex_vacio = preload("res://assets/sprites/minigame_1/tazon/tazon_vacio.png")
const tex_1_4 = preload("res://assets/sprites/minigame_1/tazon/tazon_1_4.png")
const tex_medio = preload("res://assets/sprites/minigame_1/tazon/tazon_medio.png")
const tex_lleno = preload("res://assets/sprites/minigame_1/tazon/tazon_lleno.png")

# built in
func _ready() -> void:
	setup_ui()
	eggs.insert(0, egg_1)
	eggs.insert(1, egg_2)
	eggs.insert(2, egg_3)
	for egg in eggs.size():
		eggs[egg].cracked.connect(increase_score)
		eggs[egg].selected.connect(egg_selected)
	
	# -- No sé qué les dijo la IA, pero esto rompe la música xD
	#if BGM_player and BGM_player.stream is AudioStreamWAV:
		#BGM_player.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	
	# Connect to game timer timeout for lose SFX
	var game_manager = get_parent()
	if game_manager and game_manager.has_node("GameTimer"):
		var game_timer = game_manager.get_node("GameTimer")
		game_timer.minigame_timed_out.connect(_on_timeout)

func setup_ui():
	var canvas = CanvasLayer.new()
	add_child(canvas)
	
	status_label = Label.new()
	status_label.position = Vector2(0, 500)
	status_label.size = Vector2(1920, 200)
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_label.add_theme_font_size_override("font_size", 100)
	status_label.text = ""
	canvas.add_child(status_label)

# functions
func play_sound(stream: AudioStream, volume: float = 0.0) -> void:
	if stream == null: return
	var asp = AudioStreamPlayer.new()
	asp.stream = stream
	asp.volume_db = volume
	get_tree().current_scene.add_child(asp)
	asp.play()
	asp.finished.connect(asp.queue_free)

func egg_selected(selected : bool, selected_egg : String) -> void:
	for egg in eggs.size():
		if is_instance_valid(eggs[egg]):
			eggs[egg].switch_can_select(!selected, selected_egg)

func increase_score() -> void:
	$FeedbackArrow.visible = false
	play_sound(sfx_viscosity, -4.0)
	emit_signal("point_scored")
	level_score += 1
	
	if level_score == 1:
		bowl_sprite.texture = tex_1_4
	elif level_score == 2:
		bowl_sprite.texture = tex_medio
	elif level_score == 3:
		bowl_sprite.texture = tex_lleno
		
	print('new score: ', level_score)
	if level_score == winning_goal:
		win_game("¡NIVEL COMPLETADO!")

func win_game(reason: String):
	if game_over: return
	game_over = true
	status_label.text = reason
	status_label.modulate = Color(0, 1, 0) # Verde
	

	$Music.stream = load("res://sounds/minigame_1/Foleys/gano.mp3")
	$Music.volume_db = 9
	$Music.play()
	
	await get_tree().create_timer(2.0).timeout
	emit_signal("completed")

func _on_timeout() -> void:
	if not game_over:
		play_sound(sfx_lose, -2.0)
