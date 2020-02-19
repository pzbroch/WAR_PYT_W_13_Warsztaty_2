#!/usr/bin/env python3.6



from models import User,Message
import argparse



parser = argparse.ArgumentParser(description='Account manager.')
parser.add_argument('-u','--user', help='user name', required=True)
parser.add_argument('-p','--passwd', help='user password', required=True)
parser.add_argument('-s','--send', help='send message')
parser.add_argument('-t','--to', help='to user')
parser.add_argument('-l','--list', help='list all messages', action='store_true')



args = parser.parse_args()



##### LIST ARGUMENT ############################################################

if args.list and not args.send:
    loadedUser = User.load_by_('username', args.user)
    if loadedUser and loadedUser.password_check(args.passwd):
        userMessages = Message.load_by_('to_id',loadedUser.id)
        print('\nUser Messages:\n==============')
        for userMessage in userMessages:
            fromUser = User.load_by_('id',userMessage.from_id)
            print()
            print('Date:', userMessage.creation_date)
            print('From:', fromUser)
            print('Message:', userMessage.text)
    else:
        raise Exception('Wrong username or password!')



##### SEND ARGUMENT ############################################################

elif not args.list and args.send:
    loadedUser = User.load_by_('username', args.user)
    if loadedUser and loadedUser.password_check(args.passwd):
        if args.to:
            destUser = User.load_by_('username', args.to)
            if destUser:
                newMessage = Message()
                newMessage.from_id = loadedUser.id
                newMessage.to_id = destUser.id
                newMessage.text = args.send
                newMessage.save()
            else:
                raise Exception('No such destination user!')
        else:
            raise Exception('You need to provide destination user (-t argument)')
    else:
        raise Exception('Wrong username or password!')



##### EVERYTHING ELSE ##########################################################

else:
    parser.print_help()
