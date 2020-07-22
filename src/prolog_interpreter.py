def parse_prolog(prolog_filename:str) -> str:
    """ convert prolog syntax into python syntax for executing"""
    pass 

PROLOG_RULE_DEFINER = ":-"
PROLOG_RULE_END = "."
PROLOG_RULE_SEPARATOR = ";"
PROLOG_PREDICATE_SEPARATOR = ","
PROLOG_PREDICATE_START = "("
PROLOG_PREDICATE_END = ")"
INDENT = "\t"

def convert_prolog_rule(prolog_rule:str) -> str:
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
        python_code += f"{INDENT*INDENT_LEVEL}for {','.join(variables)} in {list_name}:\n"
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

FILENAME = "example"
PATH_IN = f"prolog_programs/{FILENAME}.pl"
PATH_OUT = f"converted_programs/{FILENAME}.py"

with open(PATH_IN) as prolog_file:
    prolog_code = prolog_file.read()

python_code = convert_prolog_rule(prolog_code)

additional_script = """

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

"""

with open(PATH_OUT,"w") as f:
    f.write(python_code + additional_script)