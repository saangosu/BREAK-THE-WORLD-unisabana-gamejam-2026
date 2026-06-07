import re

# Update eggs_minigame.gd
gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\eggs\eggs_minigame.gd"
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

gd_content = gd_content.replace("@onready var egg_3 = $Egg3", "@onready var egg_3 = $Egg3\n@onready var egg_4 = $Egg4")
gd_content = gd_content.replace("const winning_goal = 3", "const winning_goal = 4")
gd_content = gd_content.replace("eggs.insert(2, egg_3)", "eggs.insert(2, egg_3)\n\teggs.insert(3, egg_4)")

# Update score logic
score_logic_old = """	if level_score == 1:
		bowl_sprite.texture = tex_1_4
	elif level_score == 2:
		bowl_sprite.texture = tex_medio
	elif level_score == 3:
		bowl_sprite.texture = tex_lleno"""

score_logic_new = """	if level_score == 1:
		bowl_sprite.texture = tex_1_4
	elif level_score == 2:
		bowl_sprite.texture = tex_medio
	elif level_score == 3:
		bowl_sprite.texture = tex_medio # Keep it at half
	elif level_score == 4:
		bowl_sprite.texture = tex_lleno"""

gd_content = gd_content.replace(score_logic_old, score_logic_new)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_content)

# Update eggs.tscn
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\eggs\eggs.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn_content = f.read()

# Extract Egg1 block
egg1_pattern = r'(\[node name="Egg1" type="RigidBody2D" parent="\." unique_id=\d+\].*?)(?=\[node name="Egg2")'
egg1_match = re.search(egg1_pattern, tscn_content, re.DOTALL)

if egg1_match:
    egg1_block = egg1_match.group(1)
    # Create Egg4 block by modifying Egg1 block
    import random
    
    # Replace names and IDs
    egg4_block = egg1_block.replace('name="Egg1"', 'name="Egg4"')
    egg4_block = egg4_block.replace('parent="Egg1', 'parent="Egg4')
    
    # Generate new unique IDs
    for match in re.finditer(r'unique_id=(\d+)', egg4_block):
        old_id = match.group(1)
        new_id = str(random.randint(100000000, 999999999))
        egg4_block = egg4_block.replace(f'unique_id={old_id}', f'unique_id={new_id}')
        
    # Change position
    egg4_block = re.sub(r'position = Vector2\(\d+, \d+\)', 'position = Vector2(250, 750)', egg4_block, count=1)
    
    # Change color
    egg4_block = re.sub(r'modulate = Color\([\d\., ]+\)', 'modulate = Color(0.4, 0.8, 0.4, 1)', egg4_block, count=1)
    
    # Append Egg4 to the end of the file
    tscn_content += "\n" + egg4_block
    
    with open(tscn_path, "w", encoding="utf-8") as f:
        f.write(tscn_content)
    print("Added Egg4 to scene and script")
else:
    print("Could not find Egg1 block")
