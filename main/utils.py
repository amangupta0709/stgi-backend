import json
import re


class GeneratorUtil:
    def generate(self, input_json, csv_file):
        self.output_str = """
import json
\n
"""

        self.output_str += f"""
json_data = %s
source_json = dotdict(json_data)

target_json = {{}}

\n
"""
        file = csv_file.read().decode("utf-8").strip().split("\n")
        for line in file[1:]:
            line = line.rstrip()
            data = [i.strip() for i in line.split(",", 3)]

            target_key = data[1]
            source_operation = data[2]
            if data[3] == "-":
                enum_dict = "{}"
            else:
                enum_dict = data[3].replace('","', ",")
                self.output_str += f"enums = {enum_dict}\n"
            json_enum_dict = json.loads(enum_dict)
            target_keys = target_key.split(".")
            idxs = [i for i, val in enumerate(target_keys) if val == "item"]
            a = 0

            lhs_str = "target_json"
            last_val_type = "dict"
            for idx in range(len(target_keys)):
                if target_keys[idx] == "item":
                    continue
                if last_val_type == "dict":
                    lhs_str += f"['{target_keys[idx]}']"
                elif last_val_type == "list":
                    lhs_str += f"[0]['{target_keys[idx]}']"
                if idx < len(target_keys) - 1:
                    if a < len(idxs) and idx + 1 == idxs[a]:
                        self.output_str += lhs_str + " = [{}]\n"
                        a += 1
                        last_val_type = "list"
                    else:
                        self.output_str += lhs_str + " = {}\n"
                        last_val_type = "dict"

            self.output_str += (
                f"{lhs_str} = {self.do_operation(source_operation,json_enum_dict)}\n"
            )

        self.output_str += f"print(target_json)\n"
        return self.output_str

    def do_operation(self, source_operation, enum_dict):
        ret_str = ""
        source_operation = (
            source_operation.replace("IF", "if")
            .replace("ELSEIF", "elif")
            .replace("ELSE", "else")
            .replace("ENUM", "enums")
            .replace("(", " ")
            .replace(")", "")
        )

        ret_str += source_operation
        # if source_operation.find("+") != -1:
        #     operands = [
        #         self.do_operation(i.strip(), enum_dict)
        #         for i in source_operation.split("+")
        #     ]
        #     ret_str += f"{operands[0]}"
        #     for op in operands[1:]:
        #         ret_str += f" + {op}"

        # if source_operation[:4] == "ENUM":
        #     # print(f"source_json{source_operation[5:-1]}")
        #     new_data = enum_dict
        #     ret_str += f"enums[source_json{source_operation[5:-1]}]"

        # elif source_operation[:2] == "IF":
        #     result = re.search("IF(.*)", source_operation)
        #     print(result.group(1))

        # elif source_operation[0] == ".":
        #     return f"source_json{source_operation.strip()}"

        # else:
        #     return source_operation.strip()

        # if(source[0]=='.')

        return ret_str


# obj = GeneratorUtil()
# obj.generate()

# print(obj.output_str)
