from file_b import extention_hook, main_function
import file_bb

@extention_hook.register(float)
def fn(a):
    return "hello from file_b's float handler!"



if __name__ == '__main__':
    main_function([
        'should go to root',
        2,
        [3],
        12.345  # want this new type to be handled by the user's registered function
    ])