def announce(f):
    def wrapper():
        print("about to run:")
        f()
        print("done")
    return wrapper


@announce
def hello():
    print("py world")


hello()