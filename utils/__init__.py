def get_instance_vals(instance):
    vals = dict()
    for key in dir(instance):
        if not key.startswith('_') and not callable(getattr(instance, key)):
            try:
                if len(getattr(instance, key)) > 0:
                    vals.update({key: getattr(instance, key)})
            except TypeError:
                if getattr(instance, key):
                    vals.update({key: getattr(instance, key)})
    return vals