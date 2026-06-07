extends Minigame

@onready var moon = $Moon
@onready var progress_bar = $ProgressBar
@onready var particles = $CheeseParticles

var is_grating = false
var progress = 0.0
var required_distance = 10000.0 # lowered distance slightly for testing

var is_game_over = false

var grater_left_bound = 800.0
var grater_right_bound = 1120.0

var initial_scale = 0.25

func _ready():
    progress_bar.max_value = 100
    progress_bar.value = 0
    moon.scale = Vector2(initial_scale, initial_scale)
    moon.position = Vector2(960, 540)
    
    var gm = get_parent()
    var time_limit = 10.0
    if gm and "current_time" in gm:
        time_limit = gm.current_time
        
    var timer = get_tree().create_timer(time_limit - 0.1)
    timer.timeout.connect(_on_timeout)

func _on_timeout():
    if not is_game_over:
        is_game_over = true
        emit_signal("lost")

func _input(event):
    if is_game_over: return
    
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            is_grating = true
        else:
            is_grating = false
            particles.emitting = false
            
    if is_grating and event is InputEventMouseMotion:
        moon.position += event.relative
        moon.position.y = clamp(moon.position.y, 140, 940)
        
        # Check walls
        if moon.position.x < grater_left_bound or moon.position.x > grater_right_bound:
            _hit_wall()
            return
            
        particles.position = moon.position + Vector2(0, 50)
        
        if abs(event.relative.y) > 0:
            particles.emitting = true
            progress += abs(event.relative.y)
            var pct = min((progress / required_distance) * 100.0, 100.0)
            progress_bar.value = pct
            
            # Make moon thinner
            moon.scale.x = lerp(initial_scale, 0.02, progress / required_distance)
            
            if pct >= 100.0:
                _win()
        else:
            particles.emitting = false

func _hit_wall():
    is_grating = false
    particles.emitting = false
    moon.position.x = 960
    emit_signal("life_lost")

func _win():
    is_game_over = true
    particles.emitting = false
    var tween = create_tween()
    tween.tween_property(moon, "scale", Vector2(0, 0), 0.2)
    await tween.finished
    emit_signal("point_scored")
    emit_signal("completed")
