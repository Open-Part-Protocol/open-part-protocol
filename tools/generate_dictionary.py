#!/usr/bin/env python3
"""Generate the serialized field dictionary from the authoritative common schema."""
import argparse
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def describe(value):
    if '$ref' in value: return value['$ref'].split('/')[-1]
    if 'const' in value: return '`'+str(value['const'])+'`'
    if 'enum' in value: return ' / '.join('`'+str(x)+'`' for x in value['enum'])
    if value.get('type')=='array':
        suffix='; '+str(value['minItems'])+'–'+str(value['maxItems'])+' entries' if 'maxItems' in value else ''
        return 'array of '+describe(value['items'])+suffix
    if value.get('type')=='object': return 'inline object; see schema'
    if value.get('format'): return value.get('type','value')+' ('+value['format']+')'
    if value.get('pattern'): return 'string; controlled grammar in schema'
    return value.get('type','conditional type; see schema')

def render():
    common=json.loads((ROOT/'schemas/v0/common.schema.json').read_text())
    lines=['# V0 serialized field dictionary','','Generated from [common.schema.json](../../../schemas/v0/common.schema.json). Do not edit this dictionary by hand; run `tools/generate_dictionary.py`.','','This lists every serialized field in the V0 types. **Required** means unconditionally required; conditional requirements and interpretation rules remain in the schema and [specification](README.md). Array entries can have inline object fields whose complete constraints are in the schema.','','Quantity, range, transform, requirement, and identity semantics are described in [common types](common-types.md), [requirements](requirements.md), [design](design.md), and [as-built](as-built.md).','']
    for name,value in common['$defs'].items():
        lines.extend(['## '+name,''])
        if 'properties' not in value:
            lines.extend([describe(value)+'.','']);continue
        lines.extend(['| Field | Required | Serialized type |','| --- | --- | --- |'])
        for field,typ in value['properties'].items():
            lines.append('| `'+field+'` | '+('yes' if field in value.get('required',[]) else 'no / conditional')+' | '+describe(typ)+' |')
        if any(key in value for key in ['allOf','anyOf','oneOf','dependentRequired','not']):
            lines.extend(['','Conditional/cross-field structural constraints apply; inspect this type in the common schema.'])
        lines.append('')
    return '\n'.join(lines)+'\n'

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    path=ROOT/'docs/spec/v0/data-dictionary.md';content=render()
    if args.check:
        if not path.is_file() or path.read_text()!=content:
            print('Serialized field dictionary is stale',file=sys.stderr);return 1
    else:path.write_text(content)
    return 0

if __name__=='__main__':sys.exit(main())
