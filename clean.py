import os
import re

def clean_asm_files(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".s"):
            filepath = os.path.join(dir, filename)
            with open(filepath, "r") as f:
                content = f.read()
            # Remove first 7 lines
            content = content.splitlines()[7:]
            content = "\n".join(content)
            content = content[:content.rfind("main PROC")].strip()
            with open(os.path.join("cleaned", filename), "w") as f:
                f.write(content)

from generate_dataset import compile_cpp_to_asm
def regen_asm(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".cpp"):
            asm_filename = filename[:-4] + ".s"
            compile_cpp_to_asm(os.path.join(dir, filename), os.path.join(dir, asm_filename))

if __name__ == "__main__":
    # regen_asm("data")
    clean_asm_files("data")

