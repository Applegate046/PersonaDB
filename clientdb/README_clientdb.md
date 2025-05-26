# User Database Project

This project is designed to create and manage a simple SQLite database for storing user information. The database includes a table named `users` with the following structure:

- **phone**: TEXT, primary key
- **name**: TEXT
- **flags**: TEXT (nullable JSON)

## Project Structure

```
userdb-project
├── src
│   ├── Random.py        # Contains code to create the SQLite database and users table
│   └── db
│       └── __init__.py  # Initializes the database connection and related functions
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository** (if applicable):
   ```
   git clone <repository-url>
   cd userdb-project
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the database setup**:
   Execute the `Random.py` script to create the `users.db` database and the `users` table:
   ```
   python src/Random.py
   ```

## Usage

After setting up the database, you can use the functions defined in `src/db/__init__.py` to interact with the `users` table, such as adding, retrieving, or updating user records.

## License

This project is licensed under the MIT License - see the LICENSE file for details.