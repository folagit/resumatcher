import os
print os.environ["PATH"]
os.environ["MY_VAR"] = "99999"
os.system("bash")
