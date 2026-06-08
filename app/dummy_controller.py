class DummyController:

    def __getattr__(self, name):

        def wrapper(*args, **kwargs):
            print(f"{name} called")

        return wrapper