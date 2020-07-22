def example_program():
	for married_to_0,married_to_1 in married_to:
		X=married_to_0
		Y=married_to_1
		for human_0 in human:
			if X==human_0:
				for female_0 in female:
					if Y==female_0:
						yield Y,X

married_to = [
    ("dery","rouhy"),
    ("garry","bob"),
    ("faizan","shenny")
]
human = [
	"dery",
	"rouhy",
	"fahtima",
    "garry",
    "bob",
    "faizan",
    "shenny"
]
female = [
	"rouhy",
	"fahtima",
    "shenny"
]
print(list(example_program()))

