import raylibpy

__craft__ = {
    i: getattr(raylibpy, i)
    for i in dir(raylibpy)
    if not i.startswith("__") and not i.endswith("__")
}
