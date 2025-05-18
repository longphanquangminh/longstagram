import os
from app import create_app

# Initialize Flask app and secret key for JWT
app = create_app()

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))