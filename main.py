"""Data Contract Compatibility Checker. Synthetic portfolio demonstration."""
def run(data):
    old,new = data['old'],data['new']
    issues = []
    for field,spec in old.items():
        if field not in new:
            issues.append({'field':field,'issue':'field_removed'})
        elif spec['type'] != new[field]['type']:
            issues.append({'field':field,'issue':'type_changed'})
        elif spec.get('required',False) and not new[field].get('required',False):
            issues.append({'field':field,'issue':'required_became_optional'})
    for field,spec in new.items():
        if field not in old and spec.get('required',False):
            issues.append({'field':field,'issue':'new_required_field'})
    return {'compatible':not issues,'issues':issues,
            'policy':'existing consumers and producers; additive optional fields allowed'}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
