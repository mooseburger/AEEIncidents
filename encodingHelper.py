def encodedDict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        out_dict[k] = encodedString(v)
    return out_dict

def encodedString(word):
    if isinstance(word, unicode):
        word = word.encode('utf8')
    elif isinstance(word, str):
        # Must be encoded in UTF-8
        word = word.decode('utf8')
    return word
