repeat 8 [
	penup
	goto (0, 0)
	pendown
	repeat 6 [
		if (:vara != :varb) [
			if ( :vara > :varb) [ right :vara ]
			else [ left :varb ]
		]
		else [
		 if ((:vara <= :varc) || (:varb <= :varc)) [
			:vara = :varc / :vara
			:varb = :varb / :varc
			:varc = :varb
		 ]
		]
		forward :vara
		right :varb
		forward :varc
		left :varc
	]
	left 45
]
penup
forward 500