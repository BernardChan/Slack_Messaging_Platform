"""
File for functions relating to channels in Slackr
"""

# pylint: disable=W0105, W0622
from error import InputError
import database_files.database_retrieval as db
from database_files.database_retrieval import get_user_channels_by_key
from database_files.database_retrieval import get_channels
from helper_functions.interface_function_helpers import is_valid_token
import helper_functions.interface_function_helpers as help


def channels_list(token):
    """
    Provides a list of all channels and their details that the user is part of
    :param token: authorised user's identifier
    """
    # Raise an access error if not a valid token
    is_valid_token(token)
    # Get the list of all channels the user is part of
    channels = get_user_channels_by_key("token", token)
    # return the list
    return {"channels": channels}


def channels_listall(token):
    """
    Provides a list of all channels and their details
    :param token: authorised user's identifier
    """
    # Raise an access error if not a valid token
    is_valid_token(token)
    # Get the list of all channels the user is part of
    channels = get_channels()
    print(f"listall gave channel_id {channels}")
    # return the list
    return {"channels": channels}


def channels_create(token, name, is_public):
    """
    Creates a new channel
    :param token: authorised user's identifier
    :param name: string for the name of a channel
    :param is_public: boolean for whether the channel is public or not
    :return: returns a dictionary with the created channel's id
    """

    is_valid_token(token)
    if len(name) > 20:
        raise InputError("Channel name cannot be more than 20 characters long")

    channels = db.get_channels()
    user = db.get_users_by_key("token", token)[0]
    channel_id = help.get_unique_id()

    channels.append(
        {
            "channel_id": channel_id,
            "name": name,
            "owner_members": [user],
            "members": [user],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": is_public,
            "hangman": {
                "mistake": 0,
                "guessed": [" "],
                "hangmanWord": "word",
                "guess": "",
                "active": False
            }
        }
    )

    return {"channel_id": channel_id}
