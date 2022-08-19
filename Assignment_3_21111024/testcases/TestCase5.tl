:a = 3
:b = 2
if :b<:a[
    forward :b
]
else[
    forward :a
]
repeat 3[
forward :a+:b
]
left :b
forward :a 