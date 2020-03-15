import message
import helper_functions.channel_helpers as ch
import channel

def test_message_remove():
    
    channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
    channel_messages_list = channel_messages["messages"]
    
    m_id = channel_messages_list[0]["message_id"]    
    mess = channel_messages_list[0]["message"]
    
    message.message_remove(ch.chan_owner_token, m_id)
    
    new_channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
    new_list = new_channel_messages["messages"]
    assert mess not in new_list

 
"""    
def test_message_send_access_error():
    assert(not ch.is_member(ch.member_id, True))

    # User is not part of the channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(ch.member_id, ch.channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", ch.channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_message_send_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(ch.chan_owner_id, -100000)
"""
    

    