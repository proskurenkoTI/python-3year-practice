import os
from translator import TypeScriptToPythonTranslator

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def translate_file(ts_path: str, py_path: str):
    with open(ts_path, "r", encoding="utf-8") as f:
        ts_code = f.read()

    translator = TypeScriptToPythonTranslator()
    result = translator.translate(ts_code)

    with open(py_path, "w", encoding="utf-8") as f:
        f.write(result.python_code)
    print(f"Translated {ts_path} → {py_path}")

if __name__ == "__main__":
    for ts_file in os.listdir(INPUT_DIR):
        if ts_file.endswith(".ts"):
            ts_path = os.path.join(INPUT_DIR, ts_file)
            py_file = ts_file.replace(".ts", ".py")
            py_path = os.path.join(OUTPUT_DIR, py_file)
            translate_file(ts_path, py_path)