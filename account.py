#!/usr/bin/env python3.6



from models import User
import argparse



parser = argparse.ArgumentParser(description='Account manager.')
parser.add_argument('-u','--user', help='user name', required=True)
parser.add_argument('-p','--passwd', help='user password', required=True)
parser.add_argument('-e','--edit', help='edit', action='store_true')
parser.add_argument('-n','--new-passwd', help='new user password')
parser.add_argument('-l','--list', help='list all users', action='store_true')
parser.add_argument('-d','--delete', help='delete user', action='store_true')



args = parser.parse_args()



##### NO ARGUMENTS #############################################################

if not args.list and not args.edit and not args.delete:
    loadedUser = User.load_by_('username', args.user)
    if not loadedUser:
        newUser = User()
        newUser.username = args.user
        newUser.set_password(args.passwd)
        newUser.save()
    else:
        raise Exception('User already exists!')



##### LIST ARGUMENT ############################################################

elif args.list and not args.edit and not args.delete:
    loadedUser = User.load_by_('username', args.user)
    if loadedUser and loadedUser.password_check(args.passwd):
        allUsers = User.load_all()
        print('\nAvailable Users:\n================')
        for user in allUsers:
            print(user)
        print('================\n')
    else:
        raise Exception('Wrong username or password!')



##### EDIT ARGUMENT ############################################################

elif not args.list and args.edit and not args.delete:
    loadedUser = User.load_by_('username', args.user)
    if loadedUser and loadedUser.password_check(args.passwd):
        if args.new_passwd:
            loadedUser.set_password(args.new_passwd)
            loadedUser.save()
            print('Password changed!')
        else:
            raise Exception('New password missing!')
    else:
        raise Exception('Wrong username or password!')



##### DELETE ARGUMENT ##########################################################

elif not args.list and not args.edit and args.delete:
    loadedUser = User.load_by_('username', args.user)
    if loadedUser and loadedUser.password_check(args.passwd):
        loadedUser.delete()
        print('User', loadedUser, 'deleted!')
    else:
        raise Exception('Wrong username or password!')



##### EVERYTHING ELSE ##########################################################

else:
    parser.print_help()
