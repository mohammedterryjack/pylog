data = {
    "married_to/2": [
        [
            "dery",
            "rouhy"
        ],
        [
            "garry",
            "bob"
        ],
        [
            "faizan",
            "shenny"
        ]
    ],
    "human/1": [
        "dery",
        "rouhy",
        "fahtima",
        "garry",
        "bob",
        "faizan",
        "shenny"
    ],
    "female/1": [
        "rouhy",
        "fahtima",
        "shenny"
    ]
}

def example_program():
	for married_to_0,married_to_1 in data['married_to/2']:
		X=married_to_0
		Y=married_to_1
		for human_0 in data['human/1']:
			if X==human_0:
				for female_0 in data['female/1']:
					if Y==female_0:
						yield X,Y
print(list(example_program()))
    