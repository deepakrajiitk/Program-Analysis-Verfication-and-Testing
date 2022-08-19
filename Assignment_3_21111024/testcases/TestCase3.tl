pendown
:dir = 45
repeat 11 [
	:move = 20
	repeat 4 [
		repeat 2 [
			repeat 4 [
				forward :move
				right :dir
			]
		]
		:move = :move + 5 	
	]
	left 20
	forward 150
]
forward 20
penup