
def _vars2list(params):
    """ Converts the variables on lists of the same length
    """
    length = 1
    for param in params:
        if isinstance(param, list):
            length = max(length, len(param))
    if length > 1:
        for param in params:
            if isinstance(param, list) and len(param) != length:
                raise Exception('Lists in parameters must the same length')
    result = []
    for param in params:
        if isinstance(param, list):
            result.append(param)
        else:
            result.append([param] * length)
    return result




if __name__ == "__main__":
    import doctest
    doctest.testmod()
