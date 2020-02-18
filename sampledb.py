# import app
#
# @app.cli.command("create_sampledb")
# def create_sampledb_cmd():
#     firstnames = ['Clarissa', 'Lucas', 'Jack', 'Lewis']
#     lastnames = ['Brown', 'Jones', 'Smith', 'Thomas']
#     usernames = ['BroCla', 'JonLuc', 'SmiJac', 'ThoLew']
#     pwd = 'test'
#     roles = ['Student', 'Teacher', 'Admin', 'Vendor']
#
#     for i in range(0, len(roles)):
#         role_name = Role(role=roles[i])
#         db.session.add(role_name)
#         db.session.commit()
#
#     r = db.session.query(Role).all()
#     for i in range(0, len(firstnames)):
#         user = User(firstname=firstnames[i], lastname=lastnames[i], username=usernames[i], password=pwd)
#         user.roles = [r[i]]
#         db.session.add(user)
#         db.session.commit()
#
#     for i in range(10):
#         coin = Coin()
#         db.session.add(coin)
#         db.session.commit()
#
# @app.cli.command("cleardb")
# def cleardb_cmd():
#     for table in db.metadata.sorted_tables:
#         db.session.execute(table.delete())
#     db.session.commit()
