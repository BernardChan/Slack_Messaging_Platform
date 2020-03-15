import message
import helper_functions.channel_helpers as ch
import channel
from error import InputError, AccessError

def test_message_send():
    
    channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
    channel_messages_list = channel_messages["messages"]
    m_id = channel_messages_list[0]["message_id"]
    
    assert message.message_send(ch.chan_owner_token, ch.channel_id, message) == m_id
    
def send_input_error():    
    if len(message) > 1000:
        raise(InputError)
  

    
    
    
    
 