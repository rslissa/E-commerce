def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    print(f"Presenti nel primo ma non nel secondo {added}")
    removed = d2_keys - d1_keys
    print(f"presenti nel secondo ma non nel primo {removed}")
    modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    print(f"modified {modified}")
    same = set(o for o in shared_keys if d1[o] == d2[o])
    print(f"same {same}")
    return added, removed, modified, same



if __name__ == '__main__':
    x = dict(a=1, b=2, c=4)
    y = dict(a=2, b=2, d=4)
    dict_compare(x,y)

