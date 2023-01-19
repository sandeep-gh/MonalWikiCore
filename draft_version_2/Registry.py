from typing import Any, NamedTuple
from operator import attrgetter
class RegistryBase:
    PRIORITY_REALLY_FIRST = -20
    PRIORITY_FIRST = -10
    PRIORITY_MIDDLE = 0
    PRIORITY_LAST = 10
    PRIORITY_REALLY_LAST = 20

    class Entry(NamedTuple):
         factory: Any
         priority: Any
         def __call__(self, *args, **kw):
             return self.factory(*args, **kw)
         def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self.priority < other.priority
            return NotImplemented

    def __init__(self):
        self._entries = []

    def __repr__(self):
        return '<{0}: {1!r}>'.format(self.__class__.__name__, self._entries)

    def get(self, *args, **kw):
        """
        Lookup a matching module

        Each registered factory is called with the given arguments and
        the first matching wins.
        """
        for entry in self._entries:
            conv = entry(*args, **kw)
            if conv is not None:
                return conv

    def _register(self, entry):
        if entry not in self._entries:
            entries = self._entries[:]
            for i in range(len(entries)):
                if entry < entries[i]:
                    entries.insert(i, entry)
                    break
            else:
                entries.append(entry)
            self._entries = entries

    def unregister(self, factory):
        """
        Unregister a factory

        :param factory: Factory to unregister
        """
        old_entries = self._entries
        entries = [i for i in old_entries if i.factory is not factory]
        if len(old_entries) == len(entries):
            # TODO: Is this necessary?
            raise ValueError
        self._entries = entries

        
class RegistryItem(RegistryBase):
    class Entry(NamedTuple):
        factory: Any
        itemtype: Any 
        display_name: Any 
        description: Any 
        order: Any 
        def __call__(self, itemtype, *args, **kw):
            if self.itemtype == itemtype:
                return self.factory(*args, **kw)

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                return self.itemtype < other.itemtype
            return NotImplemented

    def __init__(self):
        super(RegistryItem, self).__init__()
        self.shown_entries = []

    def register(self, e, shown):
        """
        Register a factory

        :param factory: Factory to register. Callable, must return an object.
        """
        if shown:
            self.shown_entries.append(e)
            self.shown_entries.sort(key=attrgetter('order'))
        return self._register(e)


    
