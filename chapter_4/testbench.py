import subprocess

def run_script(commands):
    p = subprocess.Popen(".\db.exe", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for c in commands:
        p.stdin.write(c.encode("GBK"))
    out, err = p.communicate()
    return out.decode("GBK").split("\n")

def base_test():
    commands = ["insert 1 bob foo@bat.com\n", "select\n", ".exit\n"]
    result = run_script(commands)
    pattens = ['db > Executed.', 'db > (1, bob, foo@bat.com)', 'Executed.', 'db > ']
    for i in range(len(result)):
        if (not pattens[i] == result[i]):
            print(f"base_test failed, mismatch: {pattens[i]}, {result[i]}")
            return
    print("base_test passed!")

def table_full_test():
    commands = []
    for i in range(1301):
        c = f"insert {i} user{i} person{i}@example.com\n"
        commands.append(c)
    commands.append(".exit\n")
    result = run_script(commands)
    if(result[-2] == "db > Error: Table full."):
        print("table_full_test passed!")
    else:
        print("table_full_test failed!")

def long_string_test():
    long_username = "a"*32
    long_email = "a"*255
    commands = [f"insert 1 {long_username} {long_email}\n", "select\n", ".exit\n"]
    result = run_script(commands)
    pattens = ["db > Executed.", f"db > (1, {long_username}, {long_email})", "Executed.", "db > "]
    for i in range(len(result)):
        if (not result[i] == pattens[i]):
            print(f"long_string_test failed, mismatch: {result[i]}, {pattens[i]}")
            return
    print("long_string_test passed!")

def overlong_string_test():
    long_username = "a"*33
    long_email = "a"*256
    commands = [f"insert 1 {long_username} {long_email}\n", "select\n", ".exit\n"]
    result = run_script(commands)
    pattens = ["db > String is too long.", "db > Executed.", "db > "]
    for i in range(len(result)):
        if (not result[i] == pattens[i]):
            print(f"overlong_string_test failed, mismatch: {result[i]}, {pattens[i]}")
            return
    print("overlong_string_test passed!")

def negtive_id_test():
    commands = ["insert -1 bob foo@bar.com\n", "select\n", ".exit\n"]
    result = run_script(commands)
    pattens = ["db > ID must be positive.", "db > Executed.", "db > "]
    for i in range(len(result)):
        if (not result[i] == pattens[i]):
            print(f"negtive_id_test failed, mismatch: {result[i]}, {pattens[i]}")
            return
    print("negtive_id_test passed!")    

base_test()
table_full_test()
long_string_test()
overlong_string_test()
negtive_id_test()