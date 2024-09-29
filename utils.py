import json

from config import DATA_DIR


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
    
def construct_lis_prompt(template_filename: str) -> str:
    template = read_file(f'{DATA_DIR}/{template_filename}')
    facts = json.loads(read_file(f'{DATA_DIR}/facts.json'))
    beliefs = json.loads(read_file(f'{DATA_DIR}/beliefs.json'))
    personality = json.loads(read_file(f'{DATA_DIR}/personality.json'))
    return template.format(
        FACTS=';\n'.join(['- ' + f for f in facts]),
        BELIEFS='\n'.join([f'{b["strength"]} Belief #{b["id"]}. {b["belief"]} {b["reason"]}' for b in beliefs]),
        PERSONALITY=';\n'.join(['- ' + p for p in personality])
    )