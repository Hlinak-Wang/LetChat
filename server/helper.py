def authorise(function):
    def wrapper(*args):
        if len(args) >= 2:
            data = args[0]
            token = args[1]
            user = data.get_user('token', token)
            if user is not None:
                new_args = list(args)
                new_args[1] = user
                args = tuple(new_args)
                return function(*args)
            else:
                return {'ValueError': 'token not valid'}

    return wrapper
