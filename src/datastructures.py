from enum import Enum, auto
import time
import random

class Seat:
    def __init__(self) -> None:
        pass

class TableAttribute(Enum):
    BOOTH = auto()
    HIGH_TOP = auto()
    OUTDOOR = auto()

class Table:
    def __init__(self, id: int, seats: int, attributes: list[TableAttribute]=[]) -> None:
        self.id = id
        self.seats = seats
        self.attributes = attributes
        self.party = None

    def __str__(self) -> str:
        return f"Table {self.id} ({self.seats} top)"
    
    def __repr__(self) -> str:
        return str(self)
    
class Party:
    used_ids = set()

    def __init__(self, size: int) -> None:
        self.id = self.generate_unique_id()
        self.size = size
        self.queue_time = None
        self.seated_time = None
        self.table = None

    @classmethod
    def generate_unique_id(cls):
        while True:
            id = random.randint(1000000, 9999999)
            if id not in cls.used_ids:
                cls.used_ids.add(id)
                return id
            
    def __str__(self) -> str:
        return f"Party {self.id} ({self.size} people) (QueueTime: {self.queue_time})"
    
    def __repr__(self) -> str:
        return str(self)

class PartyQueue:
    def __init__(self) -> None:
        self.parties = []

    def add_party(self, party: Party):
        self.parties.append(party)

    def remove_party(self, party: Party):
        self.parties.remove(party)

    def __iter__(self):
        return iter(self.parties)
    
    def __next__(self):
        return next(self.parties)
    
    def __len__(self):
        return len(self.parties)
    
    def __getitem__(self, key):
        return self.parties[key]
    
    def __setitem__(self, key, value):
        self.parties[key] = value

    def __delitem__(self, key):
        del self.parties[key]

    def __contains__(self, item):
        return item in self.parties
    
    def __add__(self, other):
        return self.parties + other

class Restaurant:
    def __init__(self) -> None:
        self.tables = []
        self.queue = PartyQueue()

    def add_table(self, table: Table):
        if table.id in [t.id for t in self.tables]:
            raise ValueError(f"Table ID {table.id} already exists")
        self.tables.append(table)

    def remove_table(self, table: Table):
        self.tables.remove(table)

    def enqueue(self, party: Party) -> None:
        party.queue_time = time.time()
        self.queue.add_party(party)

    def dequeue(self, party: Party) -> None:
        self.queue.remove_party(party)

    def seat_party(self, party: Party, table: Table) -> None:
        party.seated_time = time.time()
        party.table = table
        table.party = party
        self.queue.remove_party(party)
