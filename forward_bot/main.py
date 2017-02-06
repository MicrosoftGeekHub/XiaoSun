import itchat
from itchat.content import *
import logging
import pymongo

logging.basicConfig(format = '[%(asctime)s - %(levelname)s] %(message)s', level = logging.DEBUG)

@itchat.msg_register(TEXT, isGroupChat = True)
def on_group_message(msg):
    '''
    This function is triggered when a group message received
    '''
    if msg['FromUserName'] == from_group:
        logging.info(f'Get message from group {from_groupname}')
        text = msg['Text']
        username = msg['ActualNickName']
        create_time = msg['CreateTime']

        # Save the message into database
        record = dict(
            group_name = from_groupname,
            username = username,
            create_time = create_time,
            text = text)
        db.message.insert(record)

        # Forward into to_group
        new_text = f'{from_groupname}: {text}'
        itchat.send(new_text, to_group)

def get_group_id(group_name):
    '''
    Get group id by its name. Assuming that itchat is alread logged in
    '''
    search_result = itchat.search_chatrooms(group_name)
    if search_result == None or search_result == []:
        raise RuntimeError(f'Unable to find group {group_name}')
    return search_result[0]['UserName']

from_groupname = 'PaperWeekly交流四群'
to_groupname = '神侠 Geek 家'
from_group = None
to_group = None
def initialize_groups():
    '''
    Initialize the from group and 
    '''
    global from_group, to_group

    from_group = get_group_id(from_groupname)
    to_group = get_group_id(to_groupname)

def main():
    global db

    conn = pymongo.MongoClient()
    db = conn.forward_bot
    itchat.auto_login(hotReload = True)
    initialize_groups()
    itchat.run()

if __name__ == '__main__':
    main()
