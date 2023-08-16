from os import getenv

def utility():
    DEFAULT_FT = getenv("DEFAULT_FT")
    def get_img(hash_):
        return f"{getenv('HostStorageFiles')}/img/yisus/{hash_}"
    return dict(get_img=get_img, DEFAULT_FT=DEFAULT_FT)