# product_inventory_system

This is a backend API to manage products, variants, and stock levels. It uses **Django** for the backend and **MySQL** as the database.
## How to Set Up:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/repository-name.git
    cd repository-name
    ```

2. **Create and Configure MySQL Database**:
    - You need to have **MySQL** installed and running.
    - Create a database in MySQL (e.g., `inventory_system`).
    pip install mysqlclient
    Example SQL query to create a database:
    ```sql
    CREATE DATABASE inventory_system;
    ```

3. **Set Up the Database Connection**:
    - Go to your project folder, and open the `settings.py` file.
    - Replace the database settings in the `DATABASES` section like this:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'inventory_system',  # Use the database you just created
            'USER': 'root',  # Use your MySQL username
            'PASSWORD': '',  # Use your MySQL password
            'HOST': 'localhost',  # Usually localhost for local setups
            'PORT': '3306',  # Default MySQL port
        }
    }
    ```

4. **Install Dependencies**:
    In your project folder, install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run Database Migrations**:
    This will create all the necessary tables in your database.
    ```bash
    python manage.py migrate
    ```
    
6. **For admin login creation**:
   ```bash
   python manage.py createsuperuser

 
8. **Enter the details**:
 ```bash
Username : admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.



10. **Run the Server**:
    Now you can start the Django development server:

    python manage.py runserver



8. **Frontend react running server**:
    npm start 

9 enter user name and password to login   

   
