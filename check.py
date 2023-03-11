import os

from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

if __name__ == '__main__':
    print(os.environ.get('DEBUG'))
    print(os.environ.get('SECRET_KEY'))
