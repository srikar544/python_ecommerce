🛒 Python E-Commerce Platform

**This Project is  production-style, scalable e-commerce backend built with Python and Flask. This project demonstrates real-world backend engineering practices including clean architecture, ORM-based data modeling, authentication, cart & order workflows, and extensibility for future business needs.**

 **Tech Stack used or this project**

| Layer     | Technology              |
|-----------|--------------------------|
| Backend   | Flask                   |
| ORM       | Flask-SQLAlchemy        |
| Database  | MySQL                   |
| Auth      | Flask-Login             |
| Templates | Jinja2                  |
| Styling   | HTML / CSS (extendable) |

**The Project supports below features** 

- User authentication
- Product catalog management
- Cart operations
- Checkout
- Persistent order history
 
**Key Highlights of this Project**

- Modular, scalable backend architecture
- Industry-style database modeling (User → Cart → Order)
- ORM-based data access (no raw SQL coupling)
- Authentication-ready design
- Clean separation of concerns
- Easy to extend for payments, shipping, and admin dashboards

**Features of this Application:**

**Authentication:**
   - User Registration and Login.
   - Secure Password Hashing
   - Session Management using Flask-Login

**Product and Category Management:**
   - Categories(Electronics, Fashion etc)
   - Products with price,stock and description
   - stock validation while adding to the Cart

**Cart System**

  - One active Cart per User
  - Quantity based Cart Items
  - Increase/Decrease quantity
  - Prevents duplicate products in Cart

**Checkout and Orders**

 - Checkout Page with Grand Total
 - Convert Cart -> Order
 - Price Snaphot stored and purchase time
 - Order History with itemized totals

**OrderHistory**

  - View All Past Orders
  - Accurate Order Totals
  - Clean Tabular UI
  
**Architecture**   

## Entity Relationship Overview

<pre>
User
├── Cart (1:1)
│   └── CartItem (1:N)
│       └── Product
│
└── Order (1:N)
    └── OrderItem (1:N)
        └── Product
</pre>


  **DB Design**
 
 - One Cart Per User
 - Price Snapshot in OrderItem
 - Cascading Deletes for cart cleanup
 - ORM-level relationships, not raw sql

##  Project Structure

<pre>
project/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── cart.py
│   ├── views.py
│   ├── auth.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── orders.html
│   │   └── home.html
│   └── static/
│
├── migrations/
├── requirements.txt
├── run.py
└── README.md
</pre>

**Database Models**

**Core Models** (These are the database tables in the project)

- User
- Category
- Product
- Cart
- CartItem
- Order
- OrderItem

**Important Constraints**

- User → Cart (One-to-One)
  - Enforces single active cart per user
- Unique Product Per Cart
- Stored Price per OrderItem
- Foreign Key constraints with referential integrity


 **Installation and Setup**   

 - Clone the Repository.
   - Clone the Project from https://github.com/srikar544/python_ecommerce.git
   - cd flask-ecommerce
 - Create Virtual Environment
    -  venv\Scripts\activate from the visual studio
 - Install Dependencies
     - pip install -r requirements.txt
 -Configure the Database
  app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user:password@localhost/ecommerce" - Need to use your own database 
 -Create Database tables 

  -flask db init
  -flask db migrate
  -flask db upgrade

 -Run the Application
   -python run.py

 -Run the seed_all.py class with this command so that all tables are created prior
   - python -m seeds.seed_all

   <img width="1023" height="372" alt="image" src="https://github.com/user-attachments/assets/7dc0d0aa-8fe6-44af-9ee5-a2409ef7101a" />


 
 - Visit and do the operations
   - http://127.0.0.1:5000

  **Application flow**

  - User adds products to cart 
  - Cart calculates grand total
  - Checkout creates:
     - Order
     - OrderItem (with price snapshot)
  - Cart is cleared
  - User redirected to Order History

  **Sample Queries**

  - SELECT * FROM user;
  - SELECT * FROM product;
  - SELECT * FROM cart;
  - SELECT * FROM cart_item;
  - SELECT * FROM `order`;
  - SELECT * FROM order_item;

  - order is a reserved keyword → always use backticks:

  **Output:**
   **Run python run.py from your root project**
   
   <img width="1012" height="437" alt="image" src="https://github.com/user-attachments/assets/93ce0964-c471-4961-a5f7-c4f592482b87" />

   <img width="1894" height="915" alt="image" src="https://github.com/user-attachments/assets/29d75f10-3d0b-4a0a-b101-9159b4d569aa" />

   **Click on Login button**

   <img width="1285" height="767" alt="image" src="https://github.com/user-attachments/assets/3aefcc3e-fb84-45b5-8a59-75d16d8378f5" />

   Enter right user name and password which has been seeded from **seed_users.py**

   <img width="1409" height="972" alt="image" src="https://github.com/user-attachments/assets/19a47c8c-502c-414d-ba86-ee9bd5c46ab0" />
 
   **Click on Add to cart as your wish**
   
   <img width="1886" height="845" alt="image" src="https://github.com/user-attachments/assets/dc7f25bd-476a-49b9-97f4-225a799645d9" />

   **Click on Proceed to Checkout**
   
   <img width="1781" height="783" alt="image" src="https://github.com/user-attachments/assets/40defb26-4be9-41b7-9a03-112a796d4456" />

   **Click on Place Order**

   <img width="1000" height="633" alt="image" src="https://github.com/user-attachments/assets/f67f3685-2bb0-4c98-afe6-2ed484884af8" />

  **All Previous orders are shown**
  <img width="1655" height="1013" alt="image" src="https://github.com/user-attachments/assets/86e72344-49e5-42d4-b136-dc07f4c46001" />



  SELECT * FROM user;

  <img width="835" height="399" alt="image" src="https://github.com/user-attachments/assets/e26bc53a-248c-460a-9b6d-42b1aaff9c99" />

  SELECT * FROM category; 

   <img width="595" height="451" alt="image" src="https://github.com/user-attachments/assets/471ae3b7-04c4-4e47-bfce-8bf2e921710e" />

  SELECT * FROM product

  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b2251dac-5d96-4a14-8ecc-e2db257fde06" />

  SELECT * FROM cart; 

  <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f2902a76-64a4-4ab2-9742-fd0ba23b4c65" />

  SELECT * FROM cart_item; 

  <img width="453" height="192" alt="image" src="https://github.com/user-attachments/assets/9538def6-fb3a-4640-a6f5-0e8ed5086c37" />

  SELECT * FROM `order`;

  <img width="421" height="327" alt="image" src="https://github.com/user-attachments/assets/ecdaa226-2eaf-413a-be6d-1c9b78964d19" />

  SELECT * FROM order_item;

  <img width="427" height="345" alt="image" src="https://github.com/user-attachments/assets/1e3fe84f-e093-425a-ac86-118439a14aad" />



