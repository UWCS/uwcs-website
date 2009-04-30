registry = {}

def register(model, fields, order='pk', filter=False, results=5):
    registry[str(model)] = (model, fields, results, order, filter)

def search_for_string(search_string):
    search_string = search_string.lower()
    matches = []
    for key in registry:
        model, fields, results, order, filter_by = registry[key]
        # partial application didn't seem sane in python ... so:
        if filter_by:
            objects = model.objects.filter(filter_by)
        else:
            objects = model.objects.all()
        for object in objects.order_by(order)[:results]:
            for field in fields:
                try:
                    searchee = getattr(object, field)
                except AttributeError:
                    pass
                if callable(searchee):
                    searchee = searchee()
                if search_string in searchee.lower():
                    matches.append(object)
    return matches
