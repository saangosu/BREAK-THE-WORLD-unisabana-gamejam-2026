import re

# Revert eggs_minigame.gd
gd_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scripts\eggs\eggs_minigame.gd"
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

gd_content = gd_content.replace("@onready var egg_3 = $Egg3\n@onready var egg_4 = $Egg4", "@onready var egg_3 = $Egg3")
gd_content = gd_content.replace("const winning_goal = 4", "const winning_goal = 3")
gd_content = gd_content.replace("eggs.insert(2, egg_3)\n\teggs.insert(3, egg_4)", "eggs.insert(2, egg_3)")

score_logic_new = """	if level_score == 1:
		bowl_sprite.texture = tex_1_4
	elif level_score == 2:
		bowl_sprite.texture = tex_medio
	elif level_score == 3:
		bowl_sprite.texture = tex_medio # Keep it at half
	elif level_score == 4:
		bowl_sprite.texture = tex_lleno"""

score_logic_old = """	if level_score == 1:
		bowl_sprite.texture = tex_1_4
	elif level_score == 2:
		bowl_sprite.texture = tex_medio
	elif level_score == 3:
		bowl_sprite.texture = tex_lleno"""

gd_content = gd_content.replace(score_logic_new, score_logic_old)

with open(gd_path, "w", encoding="utf-8") as f:
    f.write(gd_content)

# Revert eggs.tscn
tscn_path = r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\scenes\eggs\eggs.tscn"
with open(tscn_path, "r", encoding="utf-8") as f:
    tscn_content = f.read()

# Strip Egg4 block
egg4_index = tscn_content.find('\n[node name="Egg4"')
if egg4_index != -1:
    tscn_content = tscn_content[:egg4_index]
    with open(tscn_path, "w", encoding="utf-8") as f:
        f.write(tscn_content)
    print("Reverted Egg4 in scene and script")
else:
    print("Could not find Egg4 block in scene")
