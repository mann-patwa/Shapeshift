extends Node

var score = 0
@onready var coin_label = $"../HUD/CoinsLabel"
func add_point():
	score+=1
	coin_label.text = "COINS: "+str(score)
