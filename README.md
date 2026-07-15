# SplitEase — Expense Splitting REST API

A backend REST API for splitting shared expenses among groups, built with Python and Flask.

## Features
- JWT-based user authentication (signup, login, protected routes)
- Create groups and add members
- Add shared expenses with equal split logic
- Automatic balance calculation per user
- Greedy debt settlement algorithm that minimizes the number of transactions needed to settle all debts
- Input validation with Marshmallow
- Unit tests for the settlement algorithm with pytest

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL with SQLAlchemy ORM
- **Auth:** JWT (flask-jwt-extended), bcrypt password hashing
- **Validation:** Marshmallow
- **Testing:** pytest

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/signup | Register a new user |
| POST | /auth/login | Login and receive JWT token |
| GET | /auth/me | Get current logged-in user (protected) |

### Groups
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /groups | Create a new group |
| GET | /groups | List all groups you belong to |
| POST | /groups/<id>/members | Add a member to a group |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /groups/<id>/expenses | Add an expense to a group |
| GET | /groups/<id>/expenses | List all expenses in a group |
| GET | /groups/<id>/balances | Get balances and settlement transactions |

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/yazhinicodes/splitease.git
cd splitease

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up .env file with your database credentials
# See .env.example for required variables

# Run the app
python run.py
```

## Running Tests
```bash
pytest tests -v
```

## Settlement Algorithm
The balance calculation uses a greedy algorithm to minimize the number of transactions needed to settle all debts within a group. Given each person's net balance, it repeatedly matches the largest creditor with the largest debtor until all balances reach zero.