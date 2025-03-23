from flask import flash
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import mysql.connector
import os


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', '123')


# Database connection configuration
# Override any of these with environment variables (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
# instead of editing this file directly.
db_config = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'cars123'),
    'database': os.environ.get('DB_NAME', 'Cars')
}
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connection successful")
except mysql.connector.Error as err:
    print(f"Connection failed: {err}")
finally:
    if connection.is_connected():
        connection.close()

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(autocommit=True, **db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def fetch_all(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or [])
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    role = session.get('role', None)  # Retrieve role from session
    return render_template('home.html', role=role)  # Pass role to template


@app.route('/Appointment')
def Appointment():
        return render_template('Appointment.html')

   ## ------------------------------------------------- LOGIn  ------------------------------------ ##

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check credentials for Admin
        if email == "admin@example.com" and password == "admin":
            session['role'] = 'Admin'  # Save role in session
            flash("Logged in as Admin", "success")
            return redirect(url_for('admin_dashboard'))  # Redirect to Admin Dashboard
        # Check credentials for User
        elif email == "user@example.com" and password == "user":
            session['role'] = 'User'  # Save role in session
            flash("Logged in as User", "success")
            return redirect(url_for('user_dashboard'))  # Redirect to User Dashboard
        else:
            flash("Invalid credentials, please try again.", "error")

    return render_template('login.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('role') == 'Admin':
        return render_template('admin_dashboard.html')
    flash("Unauthorized access!", "error")
    return redirect(url_for('home'))


@app.route('/user-dashboard')
def user_dashboard():
    if session.get('role') == 'User':
        return render_template('user_dashboard.html')
    flash("Unauthorized access!", "error")
    return redirect(url_for('home'))


    ## ------------------------------------------------- Employees ------------------------------------ ##


@app.route('/employees')
def show_employees():
    """
    Main page: Lists employees grouped by EmRole,
    also includes forms for Add and Search inline.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch employees + phone + email, group by Emp_ID
    query = """
    SELECT e.Emp_ID,
           e.EmName AS Name,
           e.EmRole,
           e.Salalry,
           e.Statuss,
           GROUP_CONCAT(DISTINCT ep.Phone SEPARATOR ', ') AS Phones,
           GROUP_CONCAT(DISTINCT ee.Email SEPARATOR ', ') AS Emails
      FROM Employee e
      JOIN Employee_Phone ep ON e.Emp_ID = ep.Emp_ID
      JOIN Employee_Email ee ON e.Emp_ID = ee.Emp_ID
     GROUP BY e.Emp_ID
     ORDER BY e.EmRole, e.EmName;
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group employees by EmRole
    roles = {}
    for emp in employees:
        role = emp['EmRole']
        if role not in roles:
            roles[role] = []
        roles[role].append({
            'Emp_ID': emp['Emp_ID'],
            'Name': emp['Name'],
            'EmRole': emp['EmRole'],
            'Salalry': emp['Salalry'],
            'Emails': emp['Emails'],  # Emails concatenated or 'No Email'
            'Phones': emp['Phones'],  # Phones concatenated or 'No Phone'
            'Status': 'Active' if emp['Statuss'] == 1 else 'Inactive'
        })

    return render_template('employee.html', roles=roles)


# ----------------------- ADD -----------------------
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_id = request.form['emp_id']  # from the form
        name = request.form['name']
        role = request.form['role']
        salary = request.form['salary']
        phone = request.form['phone']
        email = request.form['email']

        # Basic validation
        if not (emp_id and name and role and salary and phone and email):
            return "All fields are required, including Emp_ID!", 400

        # Convert emp_id to int if you like
        try:
            emp_id_int = int(emp_id)
        except ValueError:
            return "Emp_ID must be an integer.", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into Employee (5 columns)
            # We set Statuss=1 inline for default "Active" status
            sql_emp = """
                INSERT INTO Employee (Emp_ID, EmName, EmRole, Salalry, Statuss)
                VALUES (%s, %s, %s, %s, 1)
            """
            cursor.execute(sql_emp, (emp_id_int, name, role, salary))

            # You used 'lastrowid' before, but we already know the ID: emp_id_int
            new_id = emp_id_int

            # Insert phone
            sql_phone = """
                INSERT INTO Employee_Phone (Phone_ID, Emp_ID, Phone)
                VALUES (NULL, %s, %s)
            """
            cursor.execute(sql_phone, (new_id, phone))

            # Insert email
            sql_email = """
                INSERT INTO Employee_Email (Email_ID, Emp_ID, Email)
                VALUES (NULL, %s, %s)
            """
            cursor.execute(sql_email, (new_id, email))

            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Error inserting new employee: {e}", 500
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('show_employees'))
    else:
        # If GET, we just redirect back or show a form in-page
        return redirect(url_for('show_employees'))


# ----------------------- UPDATE -----------------------
@app.route('/update-employee/<int:emp_id>', methods=['GET', 'POST'])
def update_employee(emp_id):
    if request.method == 'POST':
        upd_name   = request.form['upd_name']
        upd_role   = request.form['upd_role']
        upd_salary = request.form['upd_salary']
        upd_phone  = request.form['upd_phone']
        upd_email  = request.form['upd_email']

        # Validate
        if not (upd_name and upd_role and upd_salary and upd_phone and upd_email):
            return "All fields are required!", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Update Employee
            sql_emp = """
                UPDATE Employee
                   SET EmName=%s,
                       EmRole=%s,
                       Salalry=%s
                 WHERE Emp_ID=%s
            """
            cursor.execute(sql_emp, (upd_name, upd_role, upd_salary, emp_id))

            # Update phone
            sql_phone = """
                UPDATE Employee_Phone
                   SET Phone=%s
                 WHERE Emp_ID=%s
            """
            cursor.execute(sql_phone, (upd_phone, emp_id))

            # Update email
            sql_email = """
                UPDATE Employee_Email
                   SET Email=%s
                 WHERE Emp_ID=%s
            """
            cursor.execute(sql_email, (upd_email, emp_id))

            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Error updating employee: {e}", 500
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('show_employees'))
    else:
        # If GET, just redirect or handle differently
        return redirect(url_for('show_employees'))

# ----------------------- DEACTIVATE -----------------------
@app.route('/deactivate-employee/<int:emp_id>', methods=['POST', 'GET'])
def deactivate_employee(emp_id):
    """
    Deactivates a specific employee by setting their status to 0.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Update the status of only the employee with the provided Emp_ID
        cursor.execute("UPDATE Employee SET Statuss=0 WHERE Emp_ID=%s", (emp_id,))
        conn.commit()
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Error deactivating employee {emp_id}: {e}")
    finally:
        cursor.close()
        conn.close()

    # Redirect to the employee management page
    return redirect(url_for('show_employees'))


# ----------------------- ACTIVATE -----------------------
@app.route('/activate-employee/<int:emp_id>', methods=['POST', 'GET'])
def activate_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Employee SET Statuss=1 WHERE Emp_ID=%s", (emp_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error activating: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('show_employees'))


# ----------------------- DELETE -----------------------
@app.route('/delete-employee/<int:emp_id>', methods=['POST', 'GET'])
def delete_employee(emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Employee_Phone WHERE Emp_ID=%s", (emp_id,))
        cursor.execute("DELETE FROM Employee_Email WHERE Emp_ID=%s", (emp_id,))
        cursor.execute("DELETE FROM Employee WHERE Emp_ID=%s", (emp_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error deleting: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('show_employees'))


# ----------------------- SEARCH -----------------------
@app.route('/search-employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == 'POST':
        query_txt = request.form.get('search_query', '').strip()
        if not query_txt:
            return redirect(url_for('show_employees'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
          SELECT e.Emp_ID,
                 e.EmName AS Name,
                 e.EmRole,
                 e.Salalry,
                 e.Statuss,
                 ep.Phone,
                 ee.Email
            FROM Employee e
       LEFT JOIN Employee_Phone ep ON e.Emp_ID = ep.Emp_ID
       LEFT JOIN Employee_Email ee ON e.Emp_ID = ee.Emp_ID
           WHERE e.EmName LIKE %s OR e.EmRole LIKE %s
        ORDER BY e.EmRole, e.EmName;
        """
        like_str = f"%{query_txt}%"
        cursor.execute(sql, (like_str, like_str))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Group by EmRole
        roles = {}
        for emp in results:
            role = emp['EmRole']
            if role not in roles:
                roles[role] = []
            roles[role].append({
                'Emp_ID': emp['Emp_ID'],
                'Name': emp['Name'],
                'EmRole': emp['EmRole'],
                'Salalry': emp['Salalry'],
                'Email': emp['Email'],
                'Phone': emp['Phone'],
                'Status': 'Active' if emp['Statuss'] == 1 else 'Inactive'
            })

        return render_template('employee.html', roles=roles, search_term=query_txt)
    else:
        return redirect(url_for('show_employees'))
    ## ------------------------------------------------- APPOINTMENTS ------------------------------------ ##
    # ----------------------- SHOW APPOINTMENTS -----------------------

@app.route('/appointments')
def view_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get search and sort parameters
    search_term = request.args.get('search_term', '')
    sort_by = request.args.get('sort_by', 'Date')  # Default to sorting by Date
    sort_order = request.args.get('sort_order', 'ASC')  # Default to ascending order

    # Build query dynamically based on search and sort
    query = """
        SELECT a.Appoint_ID, a.Date, a.Time, a.Purpose, 
               c.Model AS Car_Model, cus.Name AS Customer_Name
        FROM Appointment a
        LEFT JOIN Car c ON a.Car_ID = c.Car_ID
        LEFT JOIN Customer cus ON a.Customer_ID = cus.Customer_ID
    """

    # Apply search filters
    if search_term:
        query += " WHERE a.Purpose LIKE %s OR a.Date LIKE %s"
        params = ('%' + search_term + '%', '%' + search_term + '%')
    else:
        params = ()

    # Apply sorting
    query += f" ORDER BY {sort_by} {sort_order}"

    cursor.execute(query, params)
    appointments = cursor.fetchall()

    # Fetch dropdown data for the form
    cursor.execute("SELECT Car_ID, Model FROM Car")
    cars = cursor.fetchall()
    cursor.execute("SELECT Customer_ID, Name FROM Customer")
    customers = cursor.fetchall()
    cursor.execute("SELECT TypeSer, Price FROM Service")
    services = cursor.fetchall()

    conn.close()

    return render_template(
        'Appointment.html',
        appointments=appointments,
        cars=cars,
        customers=customers,
        services=services,
        search_term=search_term,
        sort_by=sort_by,
        sort_order=sort_order
    )


# Updated add_appointment route
@app.route('/add-appointment', methods=['POST'])
def add_appointment():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Retrieve form data
    date = request.form.get('date')
    time = request.form.get('time')
    purpose = request.form.get('purpose')
    car_id = request.form.get('car_id') or None  # Optional
    customer_id = request.form.get('customer_id')

    if not date or not time or not purpose or not customer_id:
        flash("All fields are required except Car ID!", "error")
        return redirect(url_for('view_appointments'))

    # Insert into database
    query = """
        INSERT INTO Appointment (Date, Time, Purpose, Car_ID, Customer_ID)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (date, time, purpose, car_id, customer_id))
    conn.commit()

    flash('Appointment added successfully!', 'success')
    conn.close()
    return redirect(url_for('view_appointments'))


#--------------Update

@app.route('/update-appointment/<int:appoint_id>', methods=['POST'])
def update_appointment(appoint_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get form data
    date = request.form['date']
    time = request.form['time']
    purpose = request.form['purpose']
    car_id = request.form.get('car_id') or None
    customer_id = request.form['customer_id']

    # Validate required fields
    if not (date and time and purpose and customer_id):
        flash("All fields except Car ID are required!", "error")
        return redirect(url_for('Appointment'))

    # Update the database
    query = """
        UPDATE Appointment
        SET Date = %s, Time = %s, Purpose = %s, Car_ID = %s, Customer_ID = %s
        WHERE Appoint_ID = %s
    """
    cursor.execute(query, (date, time, purpose, car_id, customer_id, appoint_id))
    conn.commit()

    conn.close()
    flash("Appointment updated successfully!", "success")
    return redirect(url_for('Appointment'))



@app.route('/search-appointments', methods=['GET'])
def search_appointments():
    search_term = request.args.get('search_term', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT a.Appoint_ID, a.Date, a.Time, a.Purpose, 
               c.Model AS Car_Model, cus.Name AS Customer_Name
        FROM Appointment a
        LEFT JOIN Car c ON a.Car_ID = c.Car_ID
        LEFT JOIN Customer cus ON a.Customer_ID = cus.Customer_ID
        WHERE a.Purpose LIKE %s OR a.Date LIKE %s
    """
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    appointments = cursor.fetchall()

    conn.close()
    return render_template('Appointment.html', appointments=appointments, search_term=search_term)

@app.route('/delete-appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the appointment from the database
    cursor.execute("DELETE FROM Appointment WHERE Appoint_ID = %s", (appointment_id,))
    conn.commit()
    conn.close()

    flash("Appointment deleted successfully!", "success")
    return redirect(url_for('Appointment'))

@app.route('/analytics/appointments', methods=['GET'])
def appointment_analytics():
    """Provides analytics for appointments."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch analytics: Most reserved purposes and peak reservation times
    most_reserved_query = """
    SELECT Purpose, COUNT(*) AS Count
      FROM Appointment
     GROUP BY Purpose
     ORDER BY Count DESC
     LIMIT 5;
    """
    peak_times_query = """
    SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, COUNT(*) AS Count
      FROM Appointment
     GROUP BY Year, Month
     ORDER BY Count DESC
     LIMIT 5;
    """
    cursor.execute(most_reserved_query)
    most_reserved = cursor.fetchall()

    cursor.execute(peak_times_query)
    peak_times = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "most_reserved": most_reserved,
        "peak_times": peak_times
    }

    ## ------------------------------------------------- Cars ------------------------------------ ##

@app.route('/cars')
def cars():
    """Display cars collection."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM Car"  # Simplified query for debugging
    cursor.execute(query)
    cars = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('cars.html', cars=cars)

   # return render_template('cars.html')



@app.route('/our-cars', methods=['GET', 'POST'])
def our_cars():
    year = request.args.get('year')
    make = request.args.get('make')
    price = request.args.get('price')

    query = "SELECT * FROM Car WHERE 1=1"
    params = []

    if year:
        query += " AND Year = %s"
        params.append(year)
    if make:
        query += " AND Make LIKE %s"
        params.append(f"%{make}%")
    if price:
        query += " AND Price <= %s"
        params.append(price)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(query, params)
    cars = cursor.fetchall()

    # Log the filter to the database
    log_query = """
    INSERT INTO Filter_Log (Filtered_By, Year_Filter, Make_Filter, Price_Filter)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(log_query, ('Web User', year, make, price))
    connection.commit()

    cursor.close()
    connection.close()

    return render_template('cars.html', cars=cars)

@app.route('/add-car', methods=['GET', 'POST'])
def add_car():
        if request.method == 'POST':
            model = request.form['model']
            make = request.form['make']
            year = request.form['year']
            price = request.form['price']
            color = request.form['color']
            status = request.form['status']
            image = request.files['image']
            image_filename = image.filename

            image.save(f"static/images/{image_filename}")

            connection = get_db_connection()
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO Car (Model, Make, Year, Price, Color, Status, Image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (model, make, year, price, color, status, image_filename))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('our_cars'))
        return render_template('cars.html')

    ## ------------------------------------------------- Customer ------------------------------------ ##
@app.route('/customer', methods=['GET', 'POST'])
def customer():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')

        insert_query = "INSERT INTO Customer (Name, Address, Phone, Email) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, address, phone, email))
        connection.commit()

    query = "SELECT * FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('customer.html', customers=customers)

@app.route('/delete-customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM Customer WHERE Customer_ID = %s"
    cursor.execute(delete_query, (customer_id,))
    connection.commit()

    cursor.close()
    connection.close()
    return redirect(url_for('customer'))

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
        """View and add customers."""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            name = request.form['name']
            address = request.form['address']
            phone = request.form['phone']
            email = request.form['email']

            try:
                query = "INSERT INTO Customer (Name, Address, Phone, Email) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (name, address, phone, email))
                conn.commit()
            except Exception as e:
                conn.rollback()
                return f"Error adding customer: {e}", 500
            finally:
                cursor.close()
                conn.close()
                return redirect(url_for('manage_customers'))

        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('customer.html', customers=customers)
    ## ------------------------------------------------- Contact ------------------------------------ ##

@app.route('/contact')
def contact():
    return render_template('contact.html')
    ## ------------------------------------------------- Logout ------------------------------------ ##

@app.route('/logout')
def logout():
    session.clear()  # Clear session
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

    ## ------------------------------------------------- Services ------------------------------------ ##

@app.route('/services')
def view_services():
    db = get_db_connection()
    cursor = db.cursor()

    # Fetch all services
    query = "SELECT * FROM Service"
    cursor.execute(query)
    services = cursor.fetchall()

    # Close the connection
    cursor.close()
    db.close()
    return render_template('services.html', services=services)

@app.route('/add-service', methods=['GET', 'POST'])
def add_service():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Capture form data
        type_ser = request.form['type_ser']  # Service type
        date = request.form['date']         # Service date
        price = request.form['price']       # Service price
        employee_id = request.form['employee_id']  # Selected employee

        # Insert the new service into the database
        query = """
            INSERT INTO Service (TypeSer, Date, Price, Employee_ID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (type_ser, date, price, employee_id))
        conn.commit()

        flash('Service added successfully!', 'success')
        return redirect(url_for('view_services'))

    # Fetch all employees to populate the dropdown
    cursor.execute("SELECT Emp_ID, Emrole, EmName FROM Employee")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('add_service.html', employees=employees)

@app.route('/delete-service/<int:service_id>', methods=['GET'])
def delete_service(service_id):
        db = get_db_connection()
        cursor = db.cursor()

        try:
            query = "DELETE FROM Service WHERE Service_ID = %s"
            cursor.execute(query, (service_id,))
            db.commit()
        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred: {e}"
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('view_services'))

@app.route('/update-service/<int:service_id>', methods=['GET', 'POST'])
def update_service(service_id):
        db = get_db_connection()
        cursor = db.cursor()

        if request.method == 'POST':
            service_type = request.form['type']
            date = request.form['date']
            price = float(request.form['price'])
            employee_id = int(request.form['employee_id'])

            try:
                query = """
                    UPDATE Service
                    SET TypeSer = %s, Date = %s, Price = %s, Employee_ID = %s
                    WHERE Service_ID = %s
                """
                cursor.execute(query, (service_type, date, price, employee_id, service_id))
                db.commit()
            except Exception as e:
                print(f"Error: {e}")
                return f"An error occurred: {e}"
            finally:
                cursor.close()
                db.close()

            return redirect(url_for('view_services'))

        # Fetch existing data for pre-filling the update form
        try:
            query = "SELECT * FROM Service WHERE Service_ID = %s"
            cursor.execute(query, (service_id,))
            service = cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred: {e}"
        finally:
            cursor.close()
            db.close()

        return render_template('update_services.html', service=service)

    # SALES ROUTES
        return render_template('services.html', services=services)

#---------------------------------------------- SALES -------------------------------------#
# ----------------- View Sales -----------------
@app.route('/sales', methods=['GET'])
def view_sales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all sales data
    cursor.execute("""
        SELECT S.Sale_ID, S.Date, S.Quantity, S.Total_Amount, C.Name AS Customer_Name, S.Payment_Method
        FROM Sale S
        JOIN Customer C ON S.Customer_ID = C.Customer_ID
    """)
    sales = cursor.fetchall()

    # Fetch all cars data
    cursor.execute("SELECT * FROM Car WHERE Status = 'Available'")
    cars = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('sales.html', sales=sales, cars=cars)

# ----------------- Add a Sale -----------------
# ----------------- Add a Sale -----------------
@app.route('/add-sale', methods=['GET', 'POST'])
def add_sale():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        date = request.form['date']
        quantity = int(request.form['quantity'])
        total_amount = float(request.form['total_amount'])
        customer_id = int(request.form['customer_id'])
        car_id = int(request.form['car_id'])
        payment_method = request.form['payment_method']

        # Insert sale into the Sale table
        query = """
            INSERT INTO Sale (Date, Total_Amount, Customer_ID, Payment_Method)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (date, total_amount, customer_id, payment_method))

        # Retrieve the last inserted Sale_ID
        sale_id = cursor.lastrowid

        # Update car status
        update_car_status = """
            UPDATE Car SET Status = 'Sold' WHERE Car_ID = %s
        """
        cursor.execute(update_car_status, (car_id,))

        # Insert into Order_Line (if necessary for your logic)
        order_line_query = """
            INSERT INTO Order_Line (Sale_ID, Car_ID, Real_Price, Discount_Percentage)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(order_line_query, (sale_id, car_id, total_amount, 0))

        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the pill.html page with the Sale_ID
        return redirect(url_for('view_pill', sale_id=sale_id))

    # Handle GET requests (populate dropdowns, etc.)
    car_id = request.args.get('car_id')
    car_details = None

    if car_id:
        cursor.execute("SELECT Car_ID, Model, Price FROM Car WHERE Car_ID = %s", (car_id,))
        car_details = cursor.fetchone()

    cursor.execute("SELECT Customer_ID, Name FROM Customer")
    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('add_sale.html', customers=customers, car_details=car_details)


# -------------------------------------------buy


@app.route('/pill/<int:sale_id>')
def view_pill(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch the Sale details
    sale_query = """
        SELECT s.Sale_ID, s.Date, s.Total_Amount, s.Customer_ID, s.Payment_Method,
               c.Name AS Customer_Name, c.Phone AS Customer_Phone,
               c.Address AS Customer_Address, c.Email AS Customer_Email
        FROM Sale s
        JOIN Customer c ON s.Customer_ID = c.Customer_ID
        WHERE s.Sale_ID = %s
    """
    cursor.execute(sale_query, (sale_id,))
    sale = cursor.fetchone()

    if not sale:
        return f"No sale found with ID {sale_id}", 404

    # Fetch related order line details
    order_line_query = """
        SELECT ol.Real_Price, ol.Discount_Percentage, ol.Final_Price, c.Model AS Car_Model
        FROM Order_Line ol
        JOIN Car c ON ol.Car_ID = c.Car_ID
        WHERE ol.Sale_ID = %s
    """
    cursor.execute(order_line_query, (sale_id,))
    order_lines = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pill.html', sale=sale, order_lines=order_lines)

# ----------------- Update Sale -----------------
@app.route('/update-sale/<int:sale_id>', methods=['GET', 'POST'])
def update_sale(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Retrieve form data
        date = request.form['date']
        quantity = int(request.form['quantity'])
        total_amount = float(request.form['total_amount'])
        customer_id = int(request.form['customer_id'])
        payment_method = request.form['payment_method']

        # Update the sale in the database
        query = """
            UPDATE Sale 
            SET Date = %s, Quantity = %s, Total_Amount = %s, Customer_ID = %s, Payment_Method = %s
            WHERE Sale_ID = %s
        """
        cursor.execute(query, (date, quantity, total_amount, customer_id, payment_method, sale_id))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect back to the Sales Management page
        flash('Sale updated successfully!', 'success')
        return redirect(url_for('view_sales'))

    # Fetch the sale to update
    query = "SELECT * FROM Sale WHERE Sale_ID = %s"
    cursor.execute(query, (sale_id,))
    sale = cursor.fetchone()

    # Fetch all customers for the dropdown
    cursor.execute("SELECT Customer_ID, Name FROM Customer")
    customers = cursor.fetchall()

    # Fetch all available cars with prices
    cursor.execute("SELECT Car_ID, Model, Price FROM Car WHERE Status = 'Available'")
    cars = cursor.fetchall()

    cursor.close()
    conn.close()

    # Render the Update Sale form with the selected sale's data
    return render_template('update_sale.html', sale=sale, customers=customers, cars=cars)

# ----------------- Delete Sale -----------------
@app.route('/delete-sale/<int:sale_id>', methods=['POST'])
def delete_sale(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Step 1: Retrieve Car_IDs linked to this sale
        query_get_cars = "SELECT DISTINCT Car_ID FROM order_line WHERE Sale_ID = %s AND Car_ID IS NOT NULL"
        cursor.execute(query_get_cars, (sale_id,))
        cars = cursor.fetchall()

        # Step 2: Delete the sale (this cascades to order_line due to ON DELETE CASCADE)
        query_delete_sale = "DELETE FROM sale WHERE Sale_ID = %s"
        cursor.execute(query_delete_sale, (sale_id,))

        # Step 3: Update the status of the cars to 'Available'
        if cars:
            for car in cars:
                query_update_car_status = "UPDATE car SET Status = 'Available' WHERE Car_ID = %s"
                cursor.execute(query_update_car_status, (car['Car_ID'],))

        # Commit changes
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error during deletion:", str(e))

    finally:
        cursor.close()
        conn.close()

    # Redirect back to sales page
    return redirect(url_for('view_sales'))



#--------------------------------------------------------Order_Line

#show
# View all order lines along with employee responsibilities
@app.route('/order-lines', methods=['GET'])
def view_order_lines():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch order lines and their associated employee responsibilities
    cursor.execute("""
        SELECT OL.Order_Line_ID, OL.Sale_ID, OL.Car_ID, OL.Real_Price,
               OL.Discount_Percentage, OL.Final_Price, S.Date AS Sale_Date,
               C.Model AS Car_Model,
               GROUP_CONCAT(DISTINCT SR.TypeSer SEPARATOR ', ') AS Service_Name,
               GROUP_CONCAT(DISTINCT CONCAT(E.EmName, ' (', E.EmRole, ')') SEPARATOR ', ') AS Employees
        FROM Order_Line OL
        LEFT JOIN Sale S ON OL.Sale_ID = S.Sale_ID
        LEFT JOIN Car C ON OL.Car_ID = C.Car_ID
        LEFT JOIN order_line_service OLS ON OL.Order_Line_ID = OLS.Order_Line_ID
        LEFT JOIN Service SR ON OLS.Service_ID = SR.Service_ID
        LEFT JOIN Order_Line_Employee OLE ON OL.Order_Line_ID = OLE.Order_Line_ID
        LEFT JOIN Employee E ON OLE.Employee_ID = E.Emp_ID
        GROUP BY OL.Order_Line_ID
    """)
    order_lines = cursor.fetchall()

    # Fetch related data for the inline "Add Order Line" form's dropdowns
    cursor.execute("SELECT Sale_ID, Date FROM Sale")
    sales = cursor.fetchall()
    cursor.execute("SELECT Car_ID, Model FROM Car")
    cars = cursor.fetchall()
    cursor.execute("SELECT Service_ID, TypeSer FROM Service")
    services = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('order_line.html', order_lines=order_lines, sales=sales, cars=cars, services=services)


# Add a new order line
@app.route('/add-order-line', methods=['GET', 'POST'])
def add_order_line():
    if request.method == 'POST':
        sale_id = request.form['sale_id']
        car_id = request.form.get('car_id')
        service_id = request.form.get('service_id')
        real_price = request.form['real_price']
        discount_percentage = request.form['discount_percentage']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert into the order line table
        cursor.execute("""
            INSERT INTO Order_Line (Sale_ID, Car_ID, Real_Price, Discount_Percentage)
            VALUES (%s, %s, %s, %s)
        """, (sale_id, car_id, real_price, discount_percentage))
        order_line_id = cursor.lastrowid

        # Link the selected service via the Order_Line <-> Service junction table
        if service_id:
            cursor.execute("""
                INSERT INTO order_line_service (Order_Line_ID, Service_ID)
                VALUES (%s, %s)
            """, (order_line_id, service_id))

        conn.commit()

        cursor.close()
        conn.close()
        flash('Order Line added successfully!', 'success')
        return redirect(url_for('view_order_lines'))

    # Fetch related data for dropdowns
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Sale_ID, Date FROM Sale")
    sales = cursor.fetchall()
    cursor.execute("SELECT Car_ID, Model FROM Car")
    cars = cursor.fetchall()
    cursor.execute("SELECT Service_ID, TypeSer FROM Service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_order_line.html', sales=sales, cars=cars, services=services)


# Assign an employee to an order line
@app.route('/add-order-line-employee', methods=['GET', 'POST'])
def add_order_line_employee():
    if request.method == 'POST':
        order_line_id = request.form['order_line_id']
        emp_id = request.form['emp_id']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert into the order line employee table
        cursor.execute("""
            INSERT INTO Order_Line_Employee (Order_Line_ID, Emp_ID, Role) 
            VALUES (%s, %s, %s)
        """, (order_line_id, emp_id, role))
        conn.commit()

        cursor.close()
        conn.close()
        flash('Employee assigned to Order Line successfully!', 'success')
        return redirect(url_for('add_order_line_employee'))

    # Fetch related data for dropdowns
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Order_Line_ID FROM Order_Line")
    order_lines = cursor.fetchall()
    cursor.execute("SELECT Emp_ID, EmName FROM Employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_order_line_employee.html', order_lines=order_lines, employees=employees)


# Update an order line
@app.route('/update-order-line/<int:order_line_id>', methods=['GET', 'POST'])
def update_order_line(order_line_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        sale_id = request.form['sale_id']
        car_id = request.form.get('car_id')
        service_id = request.form.get('service_id')
        real_price = request.form['real_price']
        discount_percentage = request.form['discount_percentage']

        # Update order line details
        cursor.execute("""
            UPDATE Order_Line
            SET Sale_ID = %s, Car_ID = %s, Real_Price = %s, Discount_Percentage = %s
            WHERE Order_Line_ID = %s
        """, (sale_id, car_id, real_price, discount_percentage, order_line_id))

        # Re-link the selected service via the Order_Line <-> Service junction table
        cursor.execute("DELETE FROM order_line_service WHERE Order_Line_ID = %s", (order_line_id,))
        if service_id:
            cursor.execute("""
                INSERT INTO order_line_service (Order_Line_ID, Service_ID)
                VALUES (%s, %s)
            """, (order_line_id, service_id))

        conn.commit()

        cursor.close()
        conn.close()
        flash('Order Line updated successfully!', 'success')
        return redirect(url_for('view_order_lines'))

    # Fetch existing order line data
    cursor.execute("""
        SELECT OL.*, OLS.Service_ID
        FROM Order_Line OL
        LEFT JOIN order_line_service OLS ON OL.Order_Line_ID = OLS.Order_Line_ID
        WHERE OL.Order_Line_ID = %s
    """, (order_line_id,))
    order_line = cursor.fetchone()

    # Fetch related data for dropdowns
    cursor.execute("SELECT Sale_ID, Date FROM Sale")
    sales = cursor.fetchall()
    cursor.execute("SELECT Car_ID, Model FROM Car")
    cars = cursor.fetchall()
    cursor.execute("SELECT Service_ID, TypeSer FROM Service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('update_order_line.html', order_line=order_line, sales=sales, cars=cars, services=services)


# Delete an order line
@app.route('/delete-order-line/<int:order_line_id>', methods=['POST'])
def delete_order_line(order_line_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete order line
    cursor.execute("DELETE FROM Order_Line WHERE Order_Line_ID = %s", (order_line_id,))
    conn.commit()

    cursor.close()
    conn.close()
    flash('Order Line deleted successfully!', 'success')
    return redirect(url_for('view_order_lines'))


# Delete an employee from an order line
@app.route('/delete-order-line-employee/<int:order_line_id>/<int:emp_id>', methods=['POST'])
def delete_order_line_employee(order_line_id, emp_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete employee assignment
    cursor.execute("""
        DELETE FROM Order_Line_Employee 
        WHERE Order_Line_ID = %s AND Emp_ID = %s
    """, (order_line_id, emp_id))
    conn.commit()

    cursor.close()
    conn.close()
    flash('Employee assignment removed successfully!', 'success')
    return redirect(url_for('view_order_lines'))




##################################
@app.route('/sales-details', methods=['GET'])
def sales_details():
    """
    Display sales with associated order lines.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            S.Sale_ID,
            S.Date,
            S.Quantity,
            S.Total_Amount,
            S.Payment_Method,
            C.Name AS Customer_Name,
            OL.Order_Line_ID,
            OL.Car_ID,
            OLS.Service_ID,
            OL.Real_Price,
            OL.Discount_Percentage,
            OL.Final_Price
        FROM Sale S
        JOIN Customer C ON S.Customer_ID = C.Customer_ID
        LEFT JOIN Order_Line OL ON S.Sale_ID = OL.Sale_ID
        LEFT JOIN order_line_service OLS ON OL.Order_Line_ID = OLS.Order_Line_ID
        ORDER BY S.Date DESC;
    """
    cursor.execute(query)
    sales_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Structure data: Sale -> Order Lines
    sales_dict = {}
    for row in sales_data:
        sale_id = row['Sale_ID']
        if sale_id not in sales_dict:
            sales_dict[sale_id] = {
                'Sale_ID': sale_id,
                'Date': row['Date'],
                'Customer_Name': row['Customer_Name'],
                'Total_Amount': row['Total_Amount'],
                'Payment_Method': row['Payment_Method'],
                'Order_Lines': []
            }
        if row['Order_Line_ID']:
            sales_dict[sale_id]['Order_Lines'].append({
                'Order_Line_ID': row['Order_Line_ID'],
                'Car_ID': row['Car_ID'],
                'Service_ID': row['Service_ID'],
                'Real_Price': row['Real_Price'],
                'Discount_Percentage': row['Discount_Percentage'],
                'Final_Price': row['Final_Price']
            })

    return render_template('sales_details.html', sales=list(sales_dict.values()))

##--------------------------------------------------- Create a order_total table to view
def create_order_totals_view():
    """
    Create the Order_Totals view in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        view_query = """
        CREATE OR REPLACE VIEW Order_Totals AS
        SELECT 
            S.Sale_ID,
            SUM(OL.Final_Price) AS Total_Amount
        FROM Sale S
        LEFT JOIN Order_Line OL ON S.Sale_ID = OL.Sale_ID
        GROUP BY S.Sale_ID;
        """
        cursor.execute(view_query)
        conn.commit()
    except Exception as e:
        print(f"Error creating Order_Totals view: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/order-totals', methods=['GET'])
def order_totals():
    """
    Display the totals from the Order_Totals view.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Order_Totals"
    cursor.execute(query)
    totals = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('order_totals.html', totals=totals)



#--------------------------------------HANDLE ERRORS --------------------#

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    create_order_totals_view()  # Ensure the view exists before running the app
    app.run(debug=True)