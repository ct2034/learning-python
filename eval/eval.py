import random

def get_undefined(code: str, vars: dict = None):
    try: 
        eval(code, {}, vars)
    except NameError as e:
        return e.args[0].split("'")[1]
    return None


if __name__ == '__main__':
    my_code = "x - y - 6"
    vars = {}
    while undefined_var := get_undefined(my_code, vars):
        print(f"Undefined variable: {undefined_var}")
        vars[undefined_var] = random.randint(0, 100)

    print(f"Final code: {my_code}, {vars}")
    print(f"Final result: {eval(my_code, {}, vars)}")