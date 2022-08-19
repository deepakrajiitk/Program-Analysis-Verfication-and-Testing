pendown
if (:a > :b)[
    if(:a > :c)[
        forward :a
    ]
]
if (:b > :a)[
    if(:b > :c)[
        forward :b
    ]
]
if (:c > :a)[
    if(:c > :b)[
        forward :a
    ]
]