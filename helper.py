def convert_float_to_percentage(n):
    return "{}%".format("{0:.3f}".format(float(n) * 100).rstrip('0'))
