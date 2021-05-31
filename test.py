from tests.register_device import register
from tests.main import main

if __name__ == '__main__':
    check_registered = str(input("Have you already registered? (y/n) "))

    if check_registered == 'n':
        register()
    main()
