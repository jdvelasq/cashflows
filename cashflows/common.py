
import pandas as pd

def getpyr(x):
    """ returns the frequency as a number of periods per year"""

    if not isinstance(x, pd.Series):
        msg = 'Pandas Series object expected:  ' + x.__repr__()
        raise ValueError(msg)

    if x.axes[0].freq not in ['A', 'BA', 'Q', 'BQ', 'M', 'BM', 'CBM', 'SM', '6M', '6BM', '6CBM']:
        msg = 'Invalid freq value:  ' + freq.__repr__()
        raise ValueError(msg)

    if x.axes[0].freq in ['A', 'BA']:
        return 1
    if x.axes[0].freq in ['6M', '6BM', '6CBM']:
        return 2
    if x.axes[0].freq in ['Q', 'BQ']:
        return 4
    if x.axes[0].freq in ['M', 'BM', 'CBM']:
        return 12
    return 24 # 'freq = "SM"'



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
