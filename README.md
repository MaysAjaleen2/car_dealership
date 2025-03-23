# Car Dealership Management System

A full-stack web app for managing a car dealership: inventory, customers, employees, appointments, services, sales, and invoicing. Built with **Flask** and **MySQL** as a database systems course project.

## Screenshots

| Home Page | Login |
|---|---|
| ![Home Page](https://github.com/user-attachments/assets/85a58b21-7450-4f21-9c21-85eccf1b97a7) | ![Login](https://github.com/user-attachments/assets/ab97f02d-4738-4025-ad54-b278deeddb42) |

| Appointments | Purchase |
|---|---|
| ![Appointments](https://github.com/user-attachments/assets/bc6be2b8-2812-47a6-8489-cd12840245da) | ![Purchase](https://github.com/user-attachments/assets/1ad631b4-8105-40f3-b4b2-836386372f77) |

## Features

- **Auth** — simple session-based login with separate Admin and User dashboards
- **Cars** — browse inventory, filter by year/make/price, add new cars with an image upload
- **Customers** — add, list, and delete customer records
- **Employees** — manage employees grouped by role, with phone/email, activate/deactivate/delete
- **Appointments** — book, search, sort, and view basic analytics (most-requested purpose, peak months)
- **Services** — add, update, delete service offerings
- **Sales** — record a sale, generate a printable invoice, update or delete a sale
- **Order Lines** — line items per sale (car + optional service + discount), with employees assignable to each line
- **Order Totals / Sales Details** — aggregate views across sales and their order lines

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (`mysql-connector-python`)
- **Frontend:** Jinja2 templates, vanilla HTML/CSS/JS (no frontend framework)

## Project Structure

```
app.py                              # Flask app: routes + queries
templates/                          # Jinja2 HTML templates
static/                             # Images, videos, (add CSS here if needed)
cars_db_dump.sql                    # Full schema + data dump of the working database
DATA BASE FINAL PHASE PROJECTSQL CODE.sql   # Original design-phase schema script
requirements.txt                    # Python dependencies
```

## Setup

### Prerequisites

- Python 3.10+
- MySQL Server 8.0+ running locally

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd "DATA BASE Final"
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Create the database

Import the schema + sample data dump into MySQL:

```bash
mysql -u root -p < cars_db_dump.sql
```

This creates a `Cars` database with all tables (`car`, `customer`, `employee`, `sale`, `order_line`, `order_line_service`, etc.) already populated with sample data.

### 3. Configure the database connection

By default `app.py` connects to `127.0.0.1` / user `root` / database `Cars`. Override any of these with environment variables instead of editing the file:

```bash
set DB_HOST=127.0.0.1
set DB_USER=root
set DB_PASSWORD=your_mysql_password
set DB_NAME=Cars
set FLASK_SECRET_KEY=some_random_string
```

(use `export` instead of `set` on macOS/Linux)

### 4. Run it

```bash
python app.py
```

Visit `http://127.0.0.1:5000`.

### Demo login credentials

| Role  | Email               | Password |
|-------|----------------------|----------|
| Admin | admin@example.com    | admin    |
| User  | user@example.com     | user     |

## Notes

- This is a course project, not a production deployment — it runs on Flask's built-in dev server (`debug=True`).
- `cars_db_dump.sql` reflects the actual working schema (including a couple of columns added after the original design script, like `Sale.Total_Amount` and `Order_Line.Final_Price`). Prefer it over the original SQL script when setting up fresh.