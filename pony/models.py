from pony.orm import Database, PrimaryKey, Required, Set

db = Database()
db.bind(provider='postgres', user='postgres', password='admin', host='127.0.0.1', database='group2006')


class Address(db.Entity):
    _table_ = 'addresses'
    address_id = PrimaryKey(int, auto=True)
    city = Required(str, 100)
    country = Required(str, 100)
    users = Set("User")

    def __str__(self):
        return f"{self.address_id}-{self.country}-{self.city}"

    def __repr__(self):
        return f"{self.address_id}-{self.country}-{self.city}"

class User(db.Entity):
    _table_ = "users"
    id = PrimaryKey(int, auto=True)
    age = Required(int)
    name = Required(str, 100)
    address = Required(Address, column='address_id')

    def __str__(self):
        return f"{self.id}-{self.name}"

    def __repr__(self):
        return f"{self.id}-{self.name}"

db.generate_mapping(create_tables=True)

