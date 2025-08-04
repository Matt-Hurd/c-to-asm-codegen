import os
import json

def generate_examples(dir='cleaned', fileext='jsonl'):
    examples = []
    for filename in os.listdir(dir):
        if filename.endswith(".s"):
            filepath = os.path.join(dir, filename)
            with open(filepath, "r") as f:
                asm = f.read()
            if len(asm) < 10:
                continue
            with open(os.path.join("data", filename[:-2] + ".cpp")) as f:
                cpp = f.readlines()
                start = 0
                i = 0
                end = 0
                for line in cpp:
                    if "#include" in line:
                        start = i + 1
                    if "main" in line:
                        end = i
                    i += 1
                cpp = "".join(cpp[start:end])
            examples.append(
                {
                    "systemInstruction": {
                        "role": "",
                        "text": "You are a disassembler that translates assembly code to C++ code. " +
                            "You are built specifically to convert code that was compiled with the Arm Developer Suite v1.2 compiler. " +
                            "All input that you receive will be asembly code that was compiled with the following command: " +
                            "armcpp -Wi -Wp -Wb -O2 -Otime -S -g -apcs '/interwork'"
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": "```asm\n" + asm + "\n```"}]
                        },
                        {
                            "role": "model",
                            "parts": [{"text": '```cpp\n' + cpp + "```"}]}
                    ]
                })
    
    if fileext == 'jsonl':
        # Save to jsonl
        with open("data.jsonl", "w") as f:
            for example in examples:
                json.dump(example, f)
                f.write("\n")
    elif fileext == 'alpaca':
        new_examples = []
        for example in examples:
            new_example = {
                "instruction": example["systemInstruction"]["text"] + "\n" + example["contents"][0]["parts"][0]["text"],
                "output": example["contents"][1]["parts"][0]["text"]
            }
            new_examples.append(new_example)
        with open("data.alpaca.json", "w") as f:
            json.dump(new_examples, f, indent=4)
    else:
        print("Unsupported file extension")
    
if __name__ == "__main__":
    generate_examples(fileext='alpaca')