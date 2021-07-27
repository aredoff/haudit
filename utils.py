def bytes_sizeof_fmt(num, factor=1024.0, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < factor:
            return "%3.1f%s" % (num, unit ), suffix
        num /= factor
    return "%.1f%s" % (num, 'Yi'), suffix