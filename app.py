from Backend import create_app
import os

environment = os.environ.get('LOAD_ENV') 
app = create_app(environment)

if __name__ == '__main__':
    app.run()