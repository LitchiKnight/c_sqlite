import subprocess
import os

DB_FILE = "mydb.db"

def run_script(cmd):
    p = subprocess.Popen(f".\db.exe {DB_FILE}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for c in cmd:
        p.stdin.write(c.encode("GBK"))
    out, err = p.communicate()
    return out.decode("GBK").split("\n")

def is_match(source, target):
    if not len(source) == len(target):
        return False
    for i in range(len(source)):
        if (not source[i] == target[i]):
            return False
    return True

def base_test():
    cmd = ["insert 1 bob foo@bat.com\n", "select\n", ".exit\n"]
    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output = run_script(cmd)
    result = ['db > Executed.', 'db > (1, bob, foo@bat.com)', 'Executed.', 'db > ']
    if is_match(output, result):
        print("base_test passed!")
    else:
        print("base_test failed!")
    

def table_full_test():
    cmd = []
    for i in range(1301):
        c = f"insert {i} user{i} person{i}@example.com\n"
        cmd.append(c)
    cmd.append(".exit\n")
    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output = run_script(cmd)
    if(output[-2] == "db > Error: Table full."):
        print("table_full_test passed!")
    else:
        print("table_full_test failed!")

def long_string_test():
    long_username = "a"*32
    long_email = "a"*255
    cmd = [f"insert 1 {long_username} {long_email}\n", "select\n", ".exit\n"]
    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output = run_script(cmd)
    result = ["db > Executed.", f"db > (1, {long_username}, {long_email})", "Executed.", "db > "]
    if is_match(output, result):
        print("long_string_test passed!")
    else:
        print("long_string_test failed!")

def overlong_string_test():
    long_username = "a"*33
    long_email = "a"*256
    cmd = [f"insert 1 {long_username} {long_email}\n", "select\n", ".exit\n"]
    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output = run_script(cmd)
    result = ["db > String is too long.", "db > Executed.", "db > "]
    if is_match(output, result):
        print("overlong_string_test passed!")
    else:
        print("overlong_string_test failed!")

def negtive_id_test():
    cmd = ["insert -1 bob foo@bar.com\n", "select\n", ".exit\n"]
    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output = run_script(cmd)
    result = ["db > ID must be positive.", "db > Executed.", "db > "]
    if is_match(output, result):
        print("negtive_id_test passed!")
    else:
        print("negtive_id_test failed!")  

def persistence_test():
    cmd_1st = ["insert 1 user1 person1@example.com\n", ".exit\n"]
    cmd_2nd = ["select\n", ".exit\n"]
    res_1st = ["db > Executed.", "db > "]
    res_2nd = ["db > (1, user1, person1@example.com)", "Executed.", "db > "]

    if os.path.exists(f"{DB_FILE}"):
        os.remove(f"{DB_FILE}")
    output_1st = run_script(cmd_1st)
    output_2nd = run_script(cmd_2nd)

    if is_match(output_1st, res_1st) and is_match(output_2nd, res_2nd):
        print("persistence_test passed!")
    else:
        print("persistence_test failed!")

base_test()
table_full_test()
long_string_test()
overlong_string_test()
negtive_id_test()
persistence_test()