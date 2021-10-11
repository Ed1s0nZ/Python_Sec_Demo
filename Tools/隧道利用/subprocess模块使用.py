import subprocess
'''
command = "whoami"
out = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
# print(out)
print(out.decode())
'''


def run_command():
    while True:
        try:
            command = input("shell_>")
            out =subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            print(out.decode())
        except:
            print("False to execute the command !")
