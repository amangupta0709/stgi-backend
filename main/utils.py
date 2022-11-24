import pandas as pd
import json


class GeneratorUtil:
    def generate(self):
        self.output_str = """
import json

class dotdict(dict):

    def __getattr__(*args):
        val = dict.get(*args)
        return dotdict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
\n
"""

        self.output_str += """
with open("json-transformation/data/sample_1/source.json") as json_file:
    source_json = dotdict(json.load(json_file))

target_json = {}
\n
"""
        with open("media/mapping.csv") as file:
            next(file)
            for line in file:
                line = line.rstrip()
                data = [i.strip() for i in line.split(",", 3)]
                # print(data)

                target_key = data[1]
                source_operation = data[2]
                if data[3] == "-":
                    enum_dict = "{}"
                else:
                    enum_dict = data[3].replace('","', ",")
                    self.output_str += f"enums = {enum_dict}\n"

                json_enum_dict = json.loads(enum_dict)
                self.output_str += f"target_json['{target_key}'] = {self.do_operation(source_operation,json_enum_dict)}\n"

    def do_operation(self, source_operation, enum_dict):
        ret_str = ""
        if source_operation.find("+") != -1:
            operands = [
                self.do_operation(i.strip(), enum_dict)
                for i in source_operation.split("+")
            ]
            ret_str += f"{operands[0]}"
            for op in operands[1:]:
                ret_str += f" + {op}"

        elif source_operation[:4] == "ENUM":
            # print(f"source_json{source_operation[5:-1]}")
            new_data = enum_dict
            ret_str += f"enums[source_json{source_operation[5:-1]}]\n"

        else:
            return f"source_json{source_operation.strip()}"

            # if(source[0]=='.')

        return ret_str


obj = GeneratorUtil()
obj.generate()

print(obj.output_str)
