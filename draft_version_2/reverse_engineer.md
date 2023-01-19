# Step 1: create instance
make wiki_local
copies wikiconfig.py
also logcfg. 

# Step 2: index-create -s -i
two options : -s: create_index, -i: create_storage 
calls indexingmiddleware.create
calls get_storage
for idx in  INDEXES :
 calls create_index 
 
## get_storage 
All it does is call FileStorage(index_dir) 
this is mega stupid code 
refer to meilesearch-#11

## create_index
for name in INDEXES:
   storage.create_index(self.schemas[name], indexname=name)
            

# new thread
## what about namespaces, backends
In wikiconfig.py --> create namespace_mapping, backend_mapping
used by routing.Backend 
namespace_mapping, 

### namespace_mapping
```
[('userprofiles', 'userprofiles'), 
 ('help-common', 'help-common'), 
 ('help-en', 'help-en'), 
 ('users', 'users'), 
 ('', 'default')]
```
### backend_mapping
```json
{
'default': <moin.storage.backends.stores.MutableBackend object at 0x10316d1490>, 
'users': <moin.storage.backends.stores.MutableBackend object at 0x10316ecbd0>, 
'userprofiles': <moin.storage.backends.stores.MutableBackend object at 0x10316ecd50>, 
'help-common': <moin.storage.backends.stores.MutableBackend object at 0x10316eced0>, 
'help-en': <moin.storage.backends.stores.MutableBackend object at 0x10316ed050>}
```
### acl_mapping
```
[
('userprofiles', {'before': 'All:', 'default': '', 'after': '', 'hierarchic': False}), 
('help-common', {'before': 'SuperUser:read,write,create,destroy,admin', 'default': 'All:read,write,create,destroy', 'after': '', 'hierarchic': True}), 
('help-en', {'before': 'SuperUser:read,write,create,destroy,admin', 'default': 'All:read,write,create,destroy', 'after': '', 'hierarchic': False}), 
('users', {'before': 'SuperUser:read,write,create,destroy,admin', 'default': 'All:read,write,create', 'after': '', 'hierarchic': False}), 
('', {'before': 'SuperUser:read,write,create,destroy,admin', 'default': 'All:read,write,create', 'after': '', 'hierarchic': False})
]
```


# mielesearch 
## 1. create a meilesearch db instance
```
./meilisearch --db-path ./meilifiles --http-addr '127.0.0.1:7700'
```

## 2. create indexes (we don't care for schema) 
make sure to provide primary key 

```
for name in INDEXES:
  client.create_index(name, {'primaryKey': 'id'})
```



