from flask_script import Manager

from app.models import db, Role, User, Coin
from app import create_app

manager = Manager(create_app())

@manager.command
def reset_basedb():
    """ Reset database back to base with all roles and only admin, costa and canteen users """

    db.drop_all()
    db.create_all()

    roles = ['Admin', 'Teacher', 'Student', 'Vendor']
    for i in range(0, len(roles)):
        role = Role(name=roles[i])
        db.session.add(role)
        db.session.commit()

    admin_role = Role.query.filter_by(name='Admin').first()
    admin = User(firstname='Admin', lastname='Admin', username='Admin', password='admin')
    admin.roles.append(admin_role)
    db.session.add(admin)
    db.session.commit()

    vendor_role = Role.query.filter_by(name='Vendor').first()
    costa = User(firstname='Costa', lastname='Costa', username='Costa', password='costa')
    canteen = User(firstname='Canteen', lastname='Canteen', username='Canteen', password='canteen')
    costa.roles.append(vendor_role)
    canteen.roles.append(vendor_role)
    db.session.add(costa)
    db.session.add(canteen)
    db.session.commit()

    for i in range(10):
        coin = Coin(owner_id=admin.id)
        db.session.add(coin)
        db.session.commit()

@manager.command
def add_sampledb():
    pass


if __name__ == "__main__":
    manager.run()
