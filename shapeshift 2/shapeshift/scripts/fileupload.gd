extends Button

# Path where files will be saved
@export_dir var save_directory: String = "user://uploads/"

# Reference to the FileDialog node
var file_dialog: FileDialog

func _ready():
	# Connect the button's pressed signal to our function
	pressed.connect(_on_UploadButton_pressed)
	
	# Create the FileDialog
	file_dialog = FileDialog.new()
	add_child(file_dialog)
	
	# Configure the FileDialog
	file_dialog.title = "Select Files to Upload"
	file_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILES
	file_dialog.access = FileDialog.ACCESS_FILESYSTEM
	file_dialog.min_size = Vector2(500, 400)
	file_dialog.exclusive = true
	
	# Connect the file_selected signal
	file_dialog.files_selected.connect(_on_files_selected)
	
	# Create save directory if it doesn't exist
	var dir = DirAccess.open("user://")
	if not dir.dir_exists(save_directory):
		dir.make_dir_recursive(save_directory)

func _on_UploadButton_pressed() -> void:
	# Show the file dialog when button is pressed
	file_dialog.popup_centered()

func _on_files_selected(paths: PackedStringArray) -> void:
	# Process each selected file
	for path in paths:
		copy_file(path)
		
func copy_file(source_path: String) -> void:
	# Extract the filename from the path
	var filename = source_path.get_file()
	var destination_path = save_directory + filename
	
	# Copy the file
	var err = DirAccess.copy_absolute(source_path, destination_path)
	
	if err == OK:
		print("File saved successfully: " + destination_path)
	else:
		print("Error saving file: " + str(err))
