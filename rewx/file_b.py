from file_a import extention_hook


def main_function(data):
    for a in data:
        print(extention_hook(a))



# main_function([
#     'should go to root',
#     2,
#     [3],
#     12.345  # want this new type to be handled by the user's registered function
# ])


