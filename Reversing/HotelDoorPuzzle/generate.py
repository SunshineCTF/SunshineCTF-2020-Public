import sys
import random

from jinja2 import Environment, PackageLoader, select_autoescape, Template, FileSystemLoader

CHANCE_MODIFY = .5
CHANCE_CHECK = 1 - CHANCE_MODIFY

TEMPLATE_FILE = 'template.c'
OUTPUT_FILE = 'output.c'
FLAG_FILE = 'flag.txt'

MODIFY_TEMPLATE = Template("""
flag[{{index}}] = flag[{{index}}] {{operator}} {{value}};
""")

CHECK_TEMPLATE = Template("""
if(flag[{{index}}] != '{{check_character}}')
{
    return 0;
}
""")


def all_nonzero(intlist):
    """ Checks if any items in a list are not zero
    
    Arguments:
        intlist {list[int]} -- list of ints
    
    Returns:
        bool -- Are there any 0s in intlist?
    """
    for item in intlist:
        if item == 0:
            return False
    return True

def setchar(instring, index, value):
    """instring[index] = value, because that's aparentally complicated
    """
    new = list(instring)
    new[index] = value
    return ''.join(new)

def modify_flag(modified_characters, current_flag, resulting_c):
    """Modifies the current_flag in some way and adds the code to complete the modification into resulting_c

    Side Effect: increments the character modified in modified_characters to match
    """
    operators = ['+','-']
    operator = operators[random.randint(0,1)]
    character_index = random.randint(0,len(current_flag)-1)
    value = random.randint(1,10)

    modified_characters[character_index]+=1

    # print(f"\tOperator: {operator}")
    if operator == '+':
        current_flag = setchar(current_flag, character_index, chr(ord(current_flag[character_index]) + value))
    elif operator == '-':
        current_flag = setchar(current_flag, character_index, chr(ord(current_flag[character_index]) - value))
    # elif operator == '*':
    #     current_flag[character_index] = current_flag[character_index] * value

    resulting_c.append(MODIFY_TEMPLATE.render(index=character_index, operator=operator, value=value))

    return resulting_c, current_flag

def check_flag(checked_characters, current_flag, resulting_c):
    """Generates the code for checking the current flag at index

    Args:
        checked_characters (list{int}): 0 if character not checked, 1 otherwise 
        current_flag (str): Current flag in progress 
        resulting_c (list{str}): List of C lines to output into the template
    """
    index = random.randint(0,len(current_flag)-1)
    if current_flag[index] in ['\\','\'','\n', '']:
        check_char = f'\\{current_flag[index]}'
    else:
        check_char = current_flag[index]

    checked_characters[index] = 1
    resulting_c = resulting_c.append(CHECK_TEMPLATE.render(index=index, check_character=check_char))

def generate_c(flag):
    """ Generate the appropriate C code to check the flag

    Args:
        flag (str): Flag
    """
    current_flag = flag

    modified_characters = [0 for x in flag]
    checked_characters = modified_characters
    resulting_c = []

    flag_length = len(flag)
    resulting_c.append(f"""
    if (strlen(flag) != {flag_length}) return 0;
    """)

    while (not all_nonzero(modified_characters) and not all_nonzero(checked_characters)):
        randchoice = random.randint(1,100)
        if randchoice < 100*CHANCE_MODIFY:
            # print("Modifying Flag")
            resulting_c, current_flag = modify_flag(modified_characters, current_flag, resulting_c)
        else:
            # print("Checking Flag")
            check_flag(checked_characters, current_flag, resulting_c)
    
    # Used to make sure that only the one flag matches
    for i in range(0,60):
        check_flag(checked_characters, current_flag, resulting_c)
    return resulting_c

if __name__ == "__main__":
    if len(sys.argv) != 1:
        resulting_c = generate_c(sys.argv[1])
    else:
        with open(FLAG_FILE,'r') as file:
            flag = file.readline()
            print(f"Generating with flag: {flag}")
            resulting_c = generate_c(flag)
    jinja_env = Environment(
        loader = FileSystemLoader('.')
    )
    output_template = jinja_env.get_template(TEMPLATE_FILE)
    output_file = output_template.render(check_code = resulting_c)
    with open(OUTPUT_FILE,'w') as file:
        file.write(output_file)
    print(f"Code Generated and output into {OUTPUT_FILE}")