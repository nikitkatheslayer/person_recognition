user_commands = {}
user_paths = {}

def set_command(user, command):
    user_commands[user] = command

def get_last_command(user):
    return user_commands.get(user)


def set_user_path(user, path):
    user_paths[user] = path

def get_last_user_path(user):
    return user_paths.get(user)

