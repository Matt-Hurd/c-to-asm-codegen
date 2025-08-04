'''
The goal of this file is to generate a dataset of ASM to C++ mappings. To achieve this, we'll utilize deepseek
to generate a series of C++ programs that cover all of the functionality of the compiler. We'll feed these
examples into the compiler, and use the produced ASM for the mapping.
'''

# def query_deepseek(prompt: list[dict], model: str = "deepseek-chat", max_tokens: int = 150, response_format: dict = openai.NOT_GIVEN) -> str:
from api import query_deepseek

def compile_cpp_to_asm(cpp_filename: str, asm_filename: str):
    """
    Compile a C++ program to ASM and save the output.
    Compiler example: armcpp -O2 -S -o{out filename}.s {in filename}
    """
    import subprocess
    try:
        subprocess.run(["armcpp", "-Wi", "-Wp", "-Wb", "-Ono_autoinline", "-O2", "-Otime", "-S", "-g", "-apcs", "/interwork", "-o", asm_filename, cpp_filename], check=True)
        print(f"Successfully compiled {cpp_filename} to {asm_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile {cpp_filename}: {e}")

def get_list_of_features() -> list[str]:
    """
    Queries DeepSeek with PROMPT_1 to get a list of features needed for training.
    """
    from prompts import PROMPT_1
    response = query_deepseek([
        {"role": "system", "content": "You are an expert C++ developer."},
        {"role": "user", "content": PROMPT_1}
    ])
    return [line.strip() for line in response.splitlines() if line.strip()]

def get_cpp_for_feature(feature: str) -> str:
    """
    Queries DeepSeek with feature inserted into PROMPT_2 to generate a c++ program.
    """
    print(feature)
    from prompts import PROMPT_2
    response = query_deepseek([
        {"role": "system", "content": "You are an expert C++ developer."},
        {"role": "user", "content": PROMPT_2.format(feature)}
    ])
    if response.startswith('```cpp'):
        response = response[7:-4]
    return response

def generate_dataset():
    """
    Generate a dataset of ASM to C++ mappings.
    Temporarily just generating .cpp/.s file pairs.
    """
    import os
    # features = get_list_of_features()
    with open("features.txt", "r") as f:
        features = [line.strip() for line in f.readlines() if line.strip()]
    for i, feature in enumerate(features):
        if i < 1017:
            continue
        cpp_filename = f"data/feature_{i}.cpp"
        asm_filename = f"data/feature_{i}.s"
        cpp_code = get_cpp_for_feature(feature)
        with open(cpp_filename, "w") as f:
            f.write(cpp_code)
        compile_cpp_to_asm(cpp_filename, asm_filename)
    print("Dataset generation complete.")

if __name__ == "__main__":
    generate_dataset()