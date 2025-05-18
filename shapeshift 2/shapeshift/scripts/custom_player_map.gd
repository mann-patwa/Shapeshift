extends Node2D

const PLATFORM_SCENE = preload("res://scenes/wall.tscn")
const COIN_SCENE = preload("res://scenes/custom_coin.tscn")
const PLAYER_SCENE = preload("res://scenes/player.tscn")

var player_instance = null

func _ready():
	load_level("res://assets/json_maps/map.json")

func load_level(json_path):
	var json_file = FileAccess.open(json_path, FileAccess.READ)
	if json_file == null:
		push_error("Failed to load JSON file: " + json_path)
		return
	
	var json_data = json_file.get_as_text()
	json_file.close()
	
	var parsed = JSON.parse_string(json_data)
	if not parsed is Array:
		push_error("Invalid level data format: Expected an array")
		return
	
	for item in parsed:
		if not item.has("type"):
			push_warning("Skipping item with missing 'type' field")
			continue
		match item["type"].to_lower():
			"platform":
				create_platform(item)
			"coin":
				create_coin(item)
			"spawn":
				create_spawn(item)
			"exit":
				create_exit(item)
			_:
				push_warning("Unknown item type: " + item["type"])

func create_platform(data):
	if not data.has_all(["cx", "cy", "width", "height"]):
		push_error("Platform data missing required fields")
		return
	if data["width"] <= 0 or data["height"] <= 0:
		push_error("Invalid platform dimensions")
		return

	var platform = PLATFORM_SCENE.instantiate()
	platform.position = Vector2(data["cx"], data["cy"])
	
	var static_body = platform.get_node_or_null("StaticBody2D")
	if not static_body:
		push_error("Platform scene missing StaticBody2D node")
		return
	
	static_body.collision_layer = 1
	static_body.collision_mask = 0
	
	var collision = static_body.get_node_or_null("CollisionShape2D")
	if not collision:
		collision = CollisionShape2D.new()
		static_body.add_child(collision)
		collision.owner = platform
	
	var shape = collision.shape
	if not shape or not (shape is RectangleShape2D):
		shape = RectangleShape2D.new()
		collision.shape = shape
	
	var platform_size = Vector2(data["width"], data["height"])
	shape.size = platform_size
	collision.position = Vector2(0, 0)
	collision.disabled = false
	
	var sprite = platform.get_node_or_null("Sprite2D")
	if sprite:
		sprite.region_enabled = true
		

		if sprite.texture:
			sprite.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
			var tile_size = sprite.texture.get_size()
			if tile_size != Vector2.ZERO:
				sprite.region_rect = Rect2(Vector2.ZERO, platform_size)
			else:
				push_warning("Sprite texture size is zero, cannot compute region tiling")
		else:
			push_warning("Sprite texture is missing")

		sprite.centered = true
		sprite.position = Vector2(0, 0)

		print("Platform sprite at ", platform.position, " tiled to size: ", platform_size)
	else:
		push_warning("Platform scene missing Sprite2D node")
	
	add_child(platform)
	call_deferred("validate_collision", platform, shape, platform_size)

func validate_collision(platform, shape, expected_size):
	var static_body = platform.get_node("StaticBody2D")
	var collision = static_body.get_node("CollisionShape2D")
	if collision and collision.shape and not collision.disabled:
		var actual_size = collision.shape.size
		if actual_size == expected_size:
			print("Platform at ", platform.position, " has collision shape: size=", actual_size)
		else:
			push_error("Platform at ", platform.position, " collision size mismatch")
	else:
		push_error("Platform at ", platform.position, " has invalid collision setup")

func create_coin(data):
	if not data.has_all(["cx", "cy", "width", "height"]):
		push_error("Coin data missing required fields")
		return
	
	var coin = COIN_SCENE.instantiate()
	coin.position = Vector2(data["cx"], data["cy"])
	
	var animated_sprite = coin.get_node_or_null("AnimatedSprite2D")
	if animated_sprite and animated_sprite.sprite_frames:
		var frame_size = animated_sprite.sprite_frames.get_frame_texture("spin", 0).get_size()
		var scale_x = data["width"] / frame_size.x
		var scale_y = data["height"] / frame_size.y
		animated_sprite.scale = Vector2(scale_x, scale_y)
	else:
		push_warning("AnimatedSprite2D node or sprite frames missing")
	
	var collision = coin.get_node_or_null("CollisionShape2D")
	if collision and collision.shape is CircleShape2D:
		var radius = min(data["width"], data["height"]) / 2.0
		collision.shape.radius = radius
	else:
		push_warning("Coin scene missing or invalid CollisionShape2D")
	
	coin.collision_layer = 2
	coin.collision_mask = 2
	
	add_child(coin)

func create_spawn(data):
	if not data.has_all(["cx", "cy"]):
		push_error("Spawn data missing required fields")
		return

	if not player_instance:
		player_instance = get_node_or_null("Player")  # Ensure your Player node is named "Player"

	if not player_instance:
		push_error("Player node not found in the scene tree. Make sure it exists and is named correctly.")
		return

	player_instance.position = Vector2(data["cx"], data["cy"])
	print("Moved existing player to: ", player_instance.position)

func create_exit(data):
	if not data.has_all(["cx", "cy", "width", "height"]):
		push_error("Exit data missing required fields")
		return
	
	var exit_area = Area2D.new()
	exit_area.position = Vector2(data["cx"], data["cy"])
	exit_area.name = "Exit"

	var collision = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(data["width"], data["height"])
	collision.shape = shape
	collision.position = Vector2(0, 0)
	
	exit_area.add_child(collision)
	collision.owner = exit_area

	var sprite = Sprite2D.new()
	var tex = preload("res://assets/sprites/red-flag.png")
	if tex:
		sprite.texture = tex
		sprite.scale = Vector2(data["width"], data["height"]) / tex.get_size()
		sprite.centered = true
		exit_area.add_child(sprite)

	exit_area.connect("body_entered", Callable(self, "_on_exit_entered"))
	exit_area.collision_layer = 4
	exit_area.collision_mask = 2
	
	add_child(exit_area)
	print("Exit created at: ", exit_area.position)

func _on_exit_entered(body):
	if body.name == "Player":
		var hud = %HUD
		
	if body.name == "Player":
		print("Player reached exit. Returning to main menu...")
		get_tree().change_scene_to_file("res://scenes/mainmenu.tscn")
