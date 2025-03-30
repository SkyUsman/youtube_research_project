# Import the initalizion of the app.
from app import create_app

# Create the app.
app = create_app()

# Entry point to running the app.
if __name__ == '__main__':
  app.run()