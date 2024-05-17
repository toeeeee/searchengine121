import parse

def run():
    user_path = input( "Please enter the path to your folder of domain folders (ANALYST or DEV): ")
    parse.build_index( user_path )

if __name__ == '__main__':
    run()
