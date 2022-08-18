from os import getenv

def utility():
    def get_img(username):
        return f"{getenv('HostStorageFiles')}/img/{username}"
    return dict(get_img=get_img)