import csv

from flask_script import Manager

from app.models import db, Role, User, Coin
from app import create_app

manager = Manager(create_app())

@manager.command
def reset_basedb():
    """ Reset database back to base with all roles and only admin, costa and canteen users """

    # Clears db of all data and tables
    db.drop_all()
    db.create_all()

    # Adds the four roles to the db
    roles = ['Admin', 'Teacher', 'Student', 'Vendor']
    for i in range(0, len(roles)):
        role = Role(name=roles[i])
        db.session.add(role)
        db.session.commit()

    # adds admin user to db
    admin_role = Role.query.filter_by(name='Admin').first()
    admin = User(firstname='Admin', lastname='Admin', username='Admin', password='admin')
    admin.roles.append(admin_role)
    db.session.add(admin)
    db.session.commit()

    # adds costa and canteen users with 'vendor' role to db
    vendor_role = Role.query.filter_by(name='Vendor').first()
    costa = User(firstname='Costa', lastname='Costa', username='Costa', password='costa')
    canteen = User(firstname='Canteen', lastname='Canteen', username='Canteen', password='canteen')
    costa.roles.append(vendor_role)
    canteen.roles.append(vendor_role)
    db.session.add(costa)
    db.session.add(canteen)
    db.session.commit()

    # adds 20 coins with owner as admin to db
    for i in range(20):
        coin = Coin(owner_id=admin.id)
        db.session.add(coin)
        db.session.commit()


@manager.command
def load_data(csvfile):
    """ Loads sample user data from csv file into database"""

    firstnames = []
    lastnames = []
    usernames = []
    roles = []
    passwords = []

    # read csv file with user data
    with open(csvfile) as f:
        csv_reader = csv.reader(f, delimiter=',')
        count = 0
        for row in csv_reader:
            if count == 0: # ignores headers
                pass
            else:
                firstnames.append(row[0])
                lastnames.append(row[1])
                usernames.append(row[2])
                roles.append(row[3])
                passwords.append(row[4])
            count += 1

    # adds every user in csv file to db
    for i in range(len(firstnames)):
        role = Role.query.filter_by(name=roles[i]).first()
        user = User(firstname=firstnames[i], lastname=lastnames[i], username=usernames[i], password=passwords[i])
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()


if __name__ == "__main__":
    manager.run()
