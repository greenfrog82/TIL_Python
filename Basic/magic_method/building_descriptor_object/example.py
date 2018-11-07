class Meter(object):
    '''Descriptor for a meter'''
    def __init__(self, value=0.0):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    '''Descriptor for a foot'''
    def __get__(self, instance, owner):
        return instance.meter * 3.208

    def __set__(self, instance, value):
        instance.meter = value / 3.208


class Distance(object):
    meter = Meter()
    foot = Foot()