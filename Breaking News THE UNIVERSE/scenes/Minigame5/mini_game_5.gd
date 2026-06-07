extends Minigame

# Cuánto movimiento de ratón se necesita para completar el rallado
var rallado_necesario = 400.0
var rallado_actual = 0.0

# Para detectar el movimiento rápido del mouse
var esta_presionado = false
var ultima_pos_mouse = Vector2.ZERO

func _ready():
	$Label.text = "Ralla la luna para el spaguetti galáctico\nHaz click en el planeta y mueve el mouse arriba y abajo rápido"
	$ProgressBar.max_value = rallado_necesario
	$ProgressBar.value = 0

func _process(delta):
	if esta_presionado:
		var pos_actual = get_viewport().get_mouse_position()
		var movimiento = abs(pos_actual.y - ultima_pos_mouse.y)
		
		# Solo cuenta si el movimiento es rápido (más de 5 pixels)
		if movimiento > 5:
			rallado_actual += movimiento
			$ProgressBar.value = rallado_actual
			
			if rallado_actual >= rallado_necesario:
				nivel_superado()
		
		ultima_pos_mouse = pos_actual

func _on_planeta_gui_input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			esta_presionado = event.pressed
			ultima_pos_mouse = get_viewport().get_mouse_position()

func nivel_superado():
	esta_presionado = false
	$Label.text = "Spaguetti galáctico listo!"
	completed.emit()

func nivel_fallido():
	esta_presionado = false
	$Label.text = "Fallaste!"
	lost.emit()
