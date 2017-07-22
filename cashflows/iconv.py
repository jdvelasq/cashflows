
import numpy

def iconv(nrate=None, erate=None, prate=None, pyr=1):
    """The function `iconv` computes the conversion among periodic, nominal
    and effective interest rates. Only an interest rate (periodic, nominal or
    effective) must be specified and the other two are computed. The periodic
    rate is the rate used in each compounding period. The effective rate is
    the equivalent rate that produces the same interest earnings that a periodic
    rate when there is P compounding periods in a year. The nominal rate is
    defined as the annual rate computed as P times the periodic rate.

    Args:
        nrate (float, list): nominal interest rate per year.
        erate (float, list): effective interest rate per year.
        prate (float, list): periodic rate
        pyr (int, list): number of compounding periods per year

    Returns:
        A tuple:
        * (**nrate**, **prate**): when **erate** is specified.
        * (**erate**, **prate**): when **nrate** is specified.
        * (**nrate**, **erate**): when **prate** is specified.


    **Examples**

    Effective interest rate to periodic and nominal interest rates.

    # example in code
    >>> iconv(erate=10, pyr=12) # doctest: +ELLIPSIS
    (9.56..., 0.79...)

    >>> iconv(erate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([9.68..., 9.60..., 9.56...], [3.22..., 1.60..., 0.79...])

    >>> iconv(erate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    ([9.56..., 11.38..., 13.17...], [0.79..., 0.94..., 1.09...])

    >>> iconv(erate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([9.68..., 11.44..., 13.17...], [3.22..., 1.90..., 1.09...])


    Nominal to effective and periodic rates.

    >>> iconv(nrate=10, pyr=12) # doctest: +ELLIPSIS
    (10.47..., 0.83...)

    >>> iconv(nrate=10, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([10.33..., 10.42..., 10.47...], [3.33..., 1.66..., 0.83...])

    >>> iconv(nrate=[10, 12, 14], pyr=12) # doctest: +ELLIPSIS
    ([10.47..., 12.68..., 14.93...], [0.83..., 1.0, 1.16...])

    >>> iconv(nrate=[10, 12, 14], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([10.33..., 12.61..., 14.93...], [3.33..., 2.0, 1.16...])

    Periodic to effective and nominal rates.

    >>> iconv(prate=1, pyr=12) # doctest: +ELLIPSIS
    (12, 12.68...)

    >>> iconv(prate=1, pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([3, 6, 12], [3.03..., 6.15..., 12.68...])

    >>> iconv(prate=[1, 2, 3], pyr=12) # doctest: +ELLIPSIS
    ([12, 24, 36], [12.68..., 26.82..., 42.57...])

    >>> iconv(prate=[1, 2, 3], pyr=[3, 6, 12]) # doctest: +ELLIPSIS
    ([3, 12, 36], [3.03..., 12.61..., 42.57...])



    """

    numnone = 0
    if nrate is None:
        numnone += 1
    if erate is None:
        numnone += 1
    if prate is None:
        numnone += 1
    if numnone != 2:
        raise ValueError('Two of the rates must be set to `None`')

    if isinstance(nrate, list) and isinstance(pyr, list) and len(nrate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(erate, list) and isinstance(pyr, list) and len(erate) != len(pyr):
        raise ValueError('List must have the same length')
    if isinstance(prate, list) and isinstance(pyr, list) and len(prate) != len(pyr):
        raise ValueError('List must have the same length')

    maxlen = 1
    if isinstance(nrate, list):
        maxlen = max(maxlen, len(nrate))
    if isinstance(erate, list):
        maxlen = max(maxlen, len(erate))
    if isinstance(prate, list):
        maxlen = max(maxlen, len(prate))
    if isinstance(pyr, list):
        maxlen = max(maxlen, len(pyr))

    if isinstance(pyr, (int, float)):
        pyr = [pyr] * maxlen
    pyr = numpy.array(pyr)

    if nrate is not None:
        if isinstance(nrate, (int, float)):
            nrate = [nrate] * maxlen
        nrate = numpy.array(nrate)
        prate = nrate / pyr
        erate = 100 * (numpy.power(1 + prate/100, pyr) - 1)
        prate = prate.tolist()
        erate = erate.tolist()
        if maxlen == 1:
            prate = prate[0]
            erate = erate[0]
        return (erate, prate)

    if erate is not None:
        if isinstance(erate, (int, float)):
            erate = [erate] * maxlen
        erate = numpy.array(erate)
        prate = 100 * (numpy.power(1 + erate / 100, 1 / pyr) - 1)
        nrate = pyr * prate
        prate = prate.tolist()
        nrate = nrate.tolist()
        if maxlen == 1:
            prate = prate[0]
            nrate = nrate[0]
        return (nrate, prate)

    if isinstance(prate, (int, float)):
        prate = [prate] * maxlen
    prate = numpy.array(prate)
    erate = 100 * (numpy.power(1 + prate / 100, pyr) - 1)
    nrate = pyr * prate
    erate = erate.tolist()
    nrate = nrate.tolist()
    if maxlen == 1:
        erate = erate[0]
        nrate = nrate[0]
    return (nrate, erate)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
