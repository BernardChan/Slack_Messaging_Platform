# Tests for user_profile() function in user.py
# Dependencies:
    # workspace_reset()
    # auth_register()
    
import pytest

from interface_functions.auth import auth_register
from interface_functions.user import user_profile
from error import InputError, AccessError
from interface_functions.workspace_reset import workspace_reset

# Pytest fixture to regiser a new test user
@pytest.fixture
def get_new_user():
    workspace_reset()
    data = auth_register("test.user@test.com", "password123", "fname", "lname")
    return data["token"], data["u_id"]

# Helper function to assert that user_profile was succesful
def assert_profile_success(user_token, user_id, fname, lname, email, handle):
    # Call the profile to be tested and assert all info is correct
    user = user_profile(user_token, user_id)
    assert(user["u_id"] == user_id)
    assert(user["name_first"] == fname)
    assert(user["name_last"] == lname)
    assert(user["email"] == email)
    assert(user["handle_str"] == handle)

# Test successful call of user_profile by the same user
def test_profile_success():
    workspace_reset()
    member = auth_register("test.user@test.com", "password123", "fname", "lname")
    assert_profile_success(member["token"], member["u_id"], "fname", "lname", "test.user@test.com", "fname.lname")

# Test successful call of user_profile by a different user
def test_profile_separate_user_success():
    workspace_reset()
    member1 = auth_register("test.user@test.com", "password123", "fname", "lname")
    member2 = auth_register("test2.user2@yer.com", "123password", "Harry", "Potter")
    member3 = auth_register("test3.user3@hi.com", "456password", "Ron", "Weasley")
    # Get member2's profile using member 1's token
    assert_profile_success(member1["token"], member2["u_id"], "Harry", "Potter", "test2.user2@yer.com", "harry.potter")
    # Get member3's profile using member 1's token
    assert_profile_success(member1["token"], member3["u_id"], "Ron", "Weasley", "test3.user3@hi.com", "ron.weasley")
    # Get member1's profile using member 3's token
    assert_profile_success(member3["token"], member1["u_id"], "fname", "lname", "test.user@test.com", "fname.lname")
    

# Input error if invalid user id
def test_profile_input_error(get_new_user):
    workspace_reset()
    user_token, user_id = get_new_user
    
    with pytest.raises(InputError):
        user = user_profile(user_token, "INVALIDUID")

# Access error if invalid token
def test_profile_access_error(get_new_user):
    workspace_reset()
    user_token, user_id = get_new_user
    
    with pytest.raises(AccessError):
        user = user_profile("INVALIDTOKEN", user_id)
        
# Both access and input error if invalid token and user id
def test_profile_input_and_access_error():
    workspace_reset()
    with pytest.raises( (AccessError, InputError) ):
         user = user_profile("INVALIDTOKEN", "INVALIDUID")
    

