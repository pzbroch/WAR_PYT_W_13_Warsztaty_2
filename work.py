from models import User
#####
# Arg parse odczytuje z cli
username = 'jo'
passwd = 'jo_pass'
message_text = 'jakis tekst'
message_to = 'jim'

# jo = User()
# jo.username = 'Jo'
# jo.email = 'jo@host.com'
# jo.save()

user = User.load_by_username(username)

if user.check_password(passwd):
    # for message in user.get_all_message():
    #     print(message)
    #
    user_to = User.load_by_username(message_to)
    mesg = Message()
