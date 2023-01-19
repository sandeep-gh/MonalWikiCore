from constant_keys import NAMESPACE_DEFAULT, NAMESPACE_USERPROFILES, NAMESPACE_USERS

namespaces = {
        # maps namespace name -> backend name
        # these 3 standard namespaces are required, these have separate backends
        NAMESPACE_DEFAULT: 'default',
        NAMESPACE_USERS: 'users',
        NAMESPACE_USERPROFILES: 'userprofiles',
        # namespaces for editor help files are optional, if unwanted delete here and in backends and acls
        'help-common': 'help-common',  # contains media files used by other language helps
        'help-en': 'help-en',  # replace this with help-de, help-ru, etc.
        # define custom namespaces if desired, trailing / below causes foo to be stored in default backend
        # 'foo/': 'default',
        # custom namespace with a separate backend - note absence of trailing /
        # 'bar': 'bar',
    }


# we need the longest mountpoints first, shortest last (-> '' is very last)
namespace_mapping =  sorted(namespaces.items(), key=lambda x: len(x[0]), reverse=True)  
namespaces = {namespace.rstrip('/') for namespace, _ in namespace_mapping}
class FieldNotUniqueError(ValueError):
    """
    The Field is not a UFIELD(unique Field).
    Non unique fields can refer to more than one item.
    """
