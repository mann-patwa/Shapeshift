extends CharacterBody2D

const SPEED = 400
const JUMP_VELOCITY = -700
const DASH_SPEED = 500.0
const DASH_TIME = 0.2

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var jump_count = 0
var is_dashing = false
var can_dash = true
var dash_time_left = 0.0
var dash_direction = 0

@onready var animated_sprite = $AnimatedSprite2D

func _physics_process(delta):
	# Apply gravity when not on floor
	if not is_on_floor():
		velocity.y += gravity * delta
	
	# Handle dash
	if is_dashing:
		velocity.x = DASH_SPEED * dash_direction
		dash_time_left -= delta
		if dash_time_left <= 0:
			is_dashing = false
	else:
		# Handle movement
		var direction = Input.get_axis("move_left", "move_right")
		if direction:
			velocity.x = direction * SPEED
		else:
			velocity.x = move_toward(velocity.x, 0, SPEED)
		
		# Flip sprite based on direction
		if direction > 0:
			animated_sprite.flip_h = false
		elif direction < 0:
			animated_sprite.flip_h = true
		
		# Handle dash input
		if Input.is_action_just_pressed("dash") and can_dash and not is_dashing:
			is_dashing = true
			can_dash = false
			dash_time_left = DASH_TIME
			dash_direction = direction if direction != 0 else (1 if animated_sprite.flip_h else -1)
	
	# Handle jump
	if Input.is_action_just_pressed("jump") and jump_count == 1:
		velocity.y = JUMP_VELOCITY + 200  # Slightly weaker double jump
		jump_count = 2
	elif Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY
		jump_count = 1
	
	# Reset jump and dash counts when on floor
	if is_on_floor():
		jump_count = 0
		if not is_dashing:
			can_dash = true
	
	# Update animations
	if is_dashing:
		animated_sprite.play("run")  # Use run animation for dash
	else:
		if is_on_floor():
			if abs(velocity.x) > 1:
				animated_sprite.play("run")
			else:
				animated_sprite.play("idle")
		else:
			animated_sprite.play("jump")
	
	move_and_slide()
