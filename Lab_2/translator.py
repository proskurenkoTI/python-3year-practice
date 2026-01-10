
import re
from dataclasses import dataclass
from typing import List, Any


@dataclass
class TranslationResult:
    python_code: str


class TypeScriptToPythonTranslator:
    TYPE_MAP = {
        "number": "float",
        "string": "str",
        "boolean": "bool",
        "void": "None"
    }

    def translate(self, ts_code: str) -> TranslationResult:
        python_lines: List[str] = []

        blocks = ts_code.split("\n\n")
        for block in blocks:
            block = block.strip()

            if block.startswith("interface"):
                python_lines.append(self._translate_interface(block))
            elif block.startswith("function"):
                python_lines.append(self._translate_function(block))
            elif "=>" in block:
                python_lines.append(self._translate_arrow_function(block))
            elif re.match(r"(const|let) \w+\s*=\s*\[", block):
                python_lines.append(self._translate_array(block))
            else:
                python_lines.append(f"# Unsupported construct:\n# {block}")

        return TranslationResult("\n\n".join(python_lines))

    def _translate_array(self, block: str) -> str:
        block = re.sub(r"\b(const|let)\b", "", block)
        block = block.replace("true", "True").replace("false", "False")
        block = block.lstrip()
        block = block.rstrip(";")
        return block

    def _translate_interface(self, block: str) -> str:
        name_match = re.search(r"interface (\w+)", block)
        if not name_match:
            return f"# Invalid interface:\n# {block}"
        name = name_match.group(1)
        fields = re.findall(r"(\w+): (\w+);", block)

        lines = ["@dataclass", f"class {name}:"]
        if not fields:
            lines.append("    pass")
        else:
            for field, ts_type in fields:
                py_type = self.TYPE_MAP.get(ts_type, ts_type)
                lines.append(f"    {field}: {py_type}")

        return "\n".join(lines)

    def _translate_function(self, block: str) -> str:
        header = re.search(r"function (\w+)\((.*?)\): (\w+)", block, re.S)
        if not header:
            return f"# Invalid function:\n# {block}"
        name, args, ret_type = header.groups()
        ret_py = self.TYPE_MAP.get(ret_type, ret_type)

        args_py = []
        for arg in args.split(","):
            arg = arg.strip()
            if arg:
                n, t = arg.split(":")
                args_py.append(f"{n.strip()}: {self.TYPE_MAP.get(t.strip(), t.strip())}")

        body_match = re.search(r"\{(.*)\}", block, re.S)
        if body_match:
            body = body_match.group(1).strip()
            body_py = self._indent_body(self._translate_ts_body(body))
        else:
            body_py = "    pass"

        return f"def {name}({', '.join(args_py)}) -> {ret_py}:\n{body_py}"

    def _translate_arrow_function(self, block: str) -> str:
        block = block.strip()

        match = re.match(r"const (\w+)\s*=\s*\((\w+): (\w+)\)\s*:\s*(\w+)\s*=>\s*\{(.*)\}", block, re.S)
        if match:
            name, arg, arg_type, ret_type, body = match.groups()
            ret_py = self.TYPE_MAP.get(ret_type, ret_type)
            body_py = self._indent_body(self._translate_ts_body(body))
            return f"def {name}({arg}: {self.TYPE_MAP.get(arg_type, arg_type)}) -> {ret_py}:\n{body_py}"

        match = re.match(r"const (\w+)\s*=\s*\((\w+): (\w+)\)\s*:\s*(\w+)\s*=>\s*(.+);", block)
        if match:
            name, arg, arg_type, ret_type, expr = match.groups()
            expr = self._translate_ts_body(expr, single_line=True)
            return f"{name} = lambda {arg}: {expr}  # type: ({self.TYPE_MAP.get(arg_type,arg_type)}) -> {self.TYPE_MAP.get(ret_type,ret_type)}"

        return f"# Unsupported arrow function:\n# {block}"

    def _translate_ts_body(self, body: str, single_line=False) -> str:

        body = body.replace("true", "True").replace("false", "False")
        body = re.sub(r"!\s*", "not ", body)
        body = re.sub(r"console\.log", "print", body)
        body = re.sub(r"`([^`]*)\${(.*?)}([^`]*)`", r'f"\1{\2}\3"', body)
        spread_match = re.match(r"return\s*\{\s*\.\.\.(\w+),\s*(\w+)\s*:\s*(.*)\s*\}", body.strip())
        if spread_match:
            obj, field, value = spread_match.groups()
            body = f"{obj}.{field} = {value}\nreturn {obj}"
        body = re.sub(r"\b(const|let)\b", "", body)
        if single_line:
            m = re.match(r"\{(.*)\}", body.strip())
            if m:
                items = [x.strip() for x in m.group(1).split(",") if x.strip()]
                body = "{" + ", ".join([f'"{x.split(":")[0].strip()}": {x.split(":")[1].strip()}' if ":" in x else f'"{x}": {x}' for x in items]) + "}"
        return body

    def _indent_body(self, body: str) -> str:
        """Добавляет ровно 4 пробела к каждой строке и убирает лишние ;"""
        lines = [line.rstrip().rstrip(";") for line in body.splitlines() if line.strip()]
        return "\n".join("    " + line.strip() for line in lines)