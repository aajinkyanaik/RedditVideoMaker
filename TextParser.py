import os.path, pathlib
import os
import time

def ManualParser(text, filename="Temp.txt"):
    with open(f"{os.path.dirname(__file__)}/{filename}", "w") as f:
        f.write(text)
        Filename = f.name
        print(f"File located at: {Filename}")
        f.flush()
    os.system(f"code -r --wait {Filename}")
    with open(f"{os.path.dirname(__file__)}/{filename}", "r") as f:
        Output = f.read()
    #pathlib.Path(f"{os.path.dirname(__file__)}/Temp.txt").unlink()
    return Output


if __name__ == "__main__":
    print(f"The output is:\n{ManualParser("This text would show up in Temp.txt.\n")}")