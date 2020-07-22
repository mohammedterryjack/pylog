# pylog
converts prolog into python

PyLog
==========



Backtracking = Nested Loops
-----------
Unification = shared variables in conditionals
-----------
PROLOG
example_program :-
	human(X),
	female(X).

-> 
PYTHON
for human in HUMAN:
	X = human
	for female in FEMALE:
		if female == X:
			yield X


++++++++++++++++++++++++++++++++

PROLOG
example_program :- 
	write("heading"),
	human(X),
	write(X),
	fail.

->
PYTHON
def example_program() -> dict:
	print("heading")
	for human_ in HUMAN
		X = human_
		print(X)
		yield X

++++++++++++++++++++++++++++++++
PROLOG
example_program :-
	man("bob"),
	married_to("bob",X),
	girl(X).
	

-> 
PYTHON
for man in MAN:
	if man == "bob":
		for person_a,person_b in MARRIED_TO:
			X = person_b
			if person_a == "bob":
				for girl in GIRL:
					if girl == X:
						yield X

++++++++++++++++++++++++++++++++
a :- b(X),c(Y),d(Z).
->
[a,b(X)c(Y)d(Z)]
->
[a]
[b(X),c(Y),d(Z)]
->
b(X)
-> 
variable_condition = lambda X,var: "{X}={var}" if {X} in seen else "if {X} == {var}:"

for b_ in b:
	{variable_condition}
	{NEXT}

if []:
	NEXT = yield
++++++++++++++++++++++++++++++++

bla :-   --> def bla(): OR lambda:
bla() -> (bla_ for bla_ in BLA)
fail -> yield
("heading") -> if bla_ == "heading"
(X) -> X = bla_  #if its first time seeing X
(X) -> if bla_ == X #if its not first time seeing X
write() -> print()
++++++++++++++++++++++++++++++++
