from pony.orm import db_session, select, commit
from models import User, Address


class UserRepo:
    def __init__(self):
        self.model = User

    @db_session
    def update_name_by_id(self, id, name):
        user = self.get_by_id(id)
        user.name = name

    @db_session
    def create(self, age, name, address):
        self.model(age=age, name=name, address=address)


    @db_session
    def delete_by_id(self, id):
        user = self.get_by_id(id)
        user.delete()

    @db_session
    def get_by_id(self, id):
        user = self.model.get(lambda u: u.id == id)
        return user

    @db_session
    def get_all(self):
        users = User.select(lambda u: u).prefetch(Address).page(1).to_list()
        return users

    @db_session
    def get_all_by_name(self, name):
        users = self.model.select(lambda u: u.name == name).prefetch(Address).page(1).to_list()
        return users

    @db_session
    def get_all_by_name_using_cycle(self, name):
        users = select(u for u in self.model if u.name == name).prefetch(Address).page(1).to_list()
        return users

    @db_session
    def get_all_by_name_and_sql(self, name):
        users = self.model.select_by_sql(f"SELECT * FROM users WHERE name = '{name}'")
        return users


class AddressRepo:
    def __init__(self):
        self.model = Address


    @db_session
    def get_by_id(self, id):
        user = self.model.get(lambda a: a.address_id == id)
        return user

    @db_session
    def select_all(self):
        address = select(role for role in self.model).page(1).to_list()
        return address


if __name__ == '__main__':
    repo = UserRepo()
    repo_address = AddressRepo()
    user = repo.get_by_id(4)
    # print(user.address)
    users = repo.get_all()
    print(users[0].address)
    print(users)
    users_by_name = repo.get_all_by_name("Lesha")
    print(users_by_name)
    users_by_name_sql = repo.get_all_by_name_using_cycle("Lesha")
    print(users_by_name_sql)
    users_by_name_sql = repo.get_all_by_name_and_sql("Lesha")
    print(users_by_name_sql)
    # repo.update_name_by_id(5, "NewName")
    print(users_by_name)
    users_by_name_sql = repo.get_all_by_name_using_cycle("NewName")
    print(users_by_name_sql)
    # repo.delete_by_id(5)
    users_by_name_sql = repo.get_all_by_name_using_cycle("NewName")
    print(users_by_name_sql)
    repo.create(1, "asd", 7)