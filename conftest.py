# conftest.py
def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure test classes run in a given order."""
    function_order = ["test_login","test_register", "test_get_all_messages", "test_add_message_for_loggedin_user","test_vote_for_message","test_delete_user_message","test_get_all_user_messages","test_logout"]
    function_mapping = {item: item.name.split("[")[0]
    if "]" not in function_order[0]
    else item.name
                        for item in items}

    sorted_items = items.copy()
    for func_ in function_order:
        sorted_items = [it for it in sorted_items if function_mapping[it] != func_] + [it for it in sorted_items if
                                                                                       function_mapping[it] == func_]
    items[:] = sorted_items