registry = {}

def register(model, fields):
    registry[str(model)] = (model, fields)

def search_for_string(search_string):
    search_string = search_string.lower()
    matches = []
    for key in registry:
        model, fields = registry[key]
        for object in model.objects.all():
            for field in fields:
                try:
                    searchee = getattr(object, field)
                except AttributeError:
                    pass
                if search_string in [s.lower() for s in searchee.split()]:
                    matches.append(object)
    return matches
