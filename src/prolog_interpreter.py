from json import dumps

PROLOG_RULE_DEFINER = ":-"
PROLOG_RULE_END = "."
PROLOG_RULE_SEPARATOR = ";"
PROLOG_PREDICATE_SEPARATOR = ","
PROLOG_PREDICATE_START = "("
PROLOG_PREDICATE_END = ")"
INDENT = "\t"

def convert_data(data:dict) -> str:
    return f"data = {dumps(data,indent=4)}\n\n"

def convert_prolog_predicate(prolog_predicate:str,data:dict) -> None:
    """
    e.g.1)
        relation(someone,someone_else).

        ->
        data["relation/2"].append(("someone","someone_else"))
    """
    prolog_predicate = prolog_predicate.strip()
    assert(prolog_predicate.endswith(PROLOG_PREDICATE_END + PROLOG_RULE_END))
    assert(prolog_predicate.count(PROLOG_PREDICATE_START) == prolog_predicate.count(PROLOG_PREDICATE_END) == 1)

    relation,variables = prolog_predicate.rstrip(PROLOG_PREDICATE_END + PROLOG_RULE_END).split(PROLOG_PREDICATE_START)
    variables = variables.split(PROLOG_PREDICATE_SEPARATOR)
    N = len(variables)
    if N == 1:
        variables = variables[0]
    key = f"{relation}/{N}"
    if key in data:
        data[key].append(variables)
    else:
        data[key] = [variables]


def convert_prolog_rule(prolog_rule:str) -> str:
    """
    e.g.1)
        example_program :-
            human(X),
            female(X).

        -> 
        def example_program():
            for human in data["human/1"]:
                X = human
                for female in data["female/1"]:
                    if female == X:
                        yield X

    e.g.2)
        example_program :-
            man("bob"),
            married_to("bob",X),
            girl(X).
            

        -> 
        def example_program():
            for man in MAN:
                if man == "bob":
                    for person_a,person_b in data["married_to/2"]:
                        X = person_b
                        if person_a == "bob":
                            for girl in data["girl/1"]:
                                if girl == X:
                                    yield X
    """
    INDENT_LEVEL = 0
    seen_conditionals = set()
    prolog_rule = prolog_rule.strip()

    assert(prolog_rule.count(PROLOG_RULE_DEFINER)==1)
    assert(prolog_rule.endswith(PROLOG_RULE_END))
    function_name,function_body = prolog_rule.split(PROLOG_RULE_DEFINER)
    
    function_name = function_name.strip()
    python_code = f"def {function_name}():\n"
    INDENT_LEVEL += 1

    function_body = function_body.rstrip(PROLOG_RULE_END).split(PROLOG_RULE_SEPARATOR)
    for part in function_body:
        part = part.strip()
        assert(PROLOG_PREDICATE_START in part)
        assert(part.endswith(PROLOG_PREDICATE_END))
        list_name,list_conditionals_ = part.rstrip(PROLOG_PREDICATE_END).split(PROLOG_PREDICATE_START)
        list_conditionals = list_conditionals_.split(PROLOG_PREDICATE_SEPARATOR)
        
        variables = list(
            map(
                lambda index: f"{list_name}_{index}",
                range(len(list_conditionals))
            )
        )
        python_code += f"{INDENT*INDENT_LEVEL}for {','.join(variables)} in data['{list_name}/{len(variables)}']:\n"
        INDENT_LEVEL += 1

        for list_conditional,variable in zip(list_conditionals,variables):
            if list_conditional in seen_conditionals:
                python_code += f"{INDENT*INDENT_LEVEL}if {list_conditional}=={variable}:\n"
                INDENT_LEVEL += 1
            else:
                python_code += f"{INDENT*INDENT_LEVEL}{list_conditional}={variable}\n"
                seen_conditionals.add(list_conditional)

    python_code += f"{INDENT*INDENT_LEVEL}yield {','.join(seen_conditionals)}"
    return python_code

def convert_prolog_program_to_python(prolog_filename:str) -> str:
    """ convert prolog syntax into python syntax for executing"""
    PATH_IN = f"prolog_programs/{prolog_filename}.pl"
    PATH_OUT = f"converted_programs/{prolog_filename}.py"

    with open(PATH_IN) as prolog_file:
        prolog_code = prolog_file.read()

    data = {}

    prolog_predicates = """married_to(dery,rouhy).
    married_to(garry,bob).
    married_to(faizan,shenny).
    human(dery).
    human(rouhy).
    human(fahtima).
    human(garry).
    human(bob).
    human(faizan).
    human(shenny).
    female(rouhy).
    female(fahtima).
    female(shenny).""".split("\n")
    
    for predicate in prolog_predicates:
        convert_prolog_predicate(predicate,data)
    data_code = convert_data(data)
    prolog_rule_code = convert_prolog_rule(prolog_code)
    execute_command = """
print(list(example_program()))
    """
    python_code = data_code + prolog_rule_code + execute_command

    with open(PATH_OUT,"w") as f:
        f.write(python_code)


convert_prolog_program_to_python("example")