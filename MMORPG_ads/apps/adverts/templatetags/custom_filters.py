import string
from django import template

register = template.Library()

unaccepted_words = ['radish', 'bullshit']


@register.filter()
def censoring_filter(value: str):
    """
    Replaces all forbidden words from text passed in value-param
    :param value: str - text for replacement
    :return: text passed in value-parameter with replaced forbidden words
    :rtype: str
    """
    result = value
    for w in unaccepted_words:
        pos = result.upper().find(w.upper())
        l: int = len(w)
        res = []
        prev_pos = 0
        while pos > -1:
            l_chr = result[pos - 1]
            r_chr = result[pos + l]
            detected = {l_chr, r_chr}.issubset(string.punctuation + ' ')
            if detected:
                res.append(result[prev_pos:pos])
                res.append(result[pos] + '*'*(l-1))
            else:
                res.append(result[prev_pos:pos + l])
            prev_pos = pos + l
            pos = value.upper().find(w.upper(), pos + l)
        if prev_pos > 0:
            res.append(result[prev_pos:])
        res = ''.join(res)
        result = res if res else result

    return result
