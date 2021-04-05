from imdb.conf import env_config


def get_config_object():
    class_ = env_config.Config
    return class_()
