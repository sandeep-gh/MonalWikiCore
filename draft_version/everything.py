from .storage imporrt init_storage
from .systemdesign import StorageType
from addict import Dict

runtime = Dict()

# Test drive
runtime.storage.set_item, runtime.storage.get_item = init_storage(StorageType.fs)


