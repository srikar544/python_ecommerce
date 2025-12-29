**Regarding Application:**

A full-stack e-commerce web application built with Flask, SQLAlchemy, MySQL, and Flask-Login.
Supports user authentication, cart management, checkout, and order history — designed with scalable database architecture similar to Amazon / Flipkart.

**Features of this Application:**

**Authentication:**
   *User Registration and Login.
   *Secure Password Hashing
   *Session Management using Flask-Login

**Product and Category Management:**
  *Categories(Electronics, Fashion etc)
  *Products with price,stock and description
  *stock validation while adding to the Cart

**Cart System**
  * One active Cart per User
  * Quantity based Cart Items
  * Increase/Decrease quantity
  * Prevents duplicate products in Cart

**Checkout and Orders**

 *Checkout Page with Grand Total
 *Convert Cart -> Order
 *Price Snaphot stored and purchase time
 *Order History with itemized totals

**OrderHistory**

  *View All Past Orders
  *Accurate Order Totals
  *Clean Tabular UI
  
**Architecture**   

##  Entity Relationship Overview

User
 ├── Cart (1:1)
 │    └── CartItem (1:N)
 │         └── Product
 │
 └── Order (1:N)
      └── OrderItem (1:N)
           └── Product


  **DB Design**
 
 *One Cart Per User
 *Price Snapshot in OrderItem
 *Cascading Deletes for cart cleanup
 *ORM-level relationships, not raw sql

 **Tech Stack used or this project**

| Layer     | Technology              |
|-----------|--------------------------|
| Backend   | Flask                   |
| ORM       | Flask-SQLAlchemy        |
| Database  | MySQL                   |
| Auth      | Flask-Login             |
| Templates | Jinja2                  |
| Styling   | HTML / CSS (extendable) |



##  Project Structure



---

 

 
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

 **Core Models**
      1.User
      2.Category
      3.Product
      4.Cart
      5.CartItem
      6.Order
      7.OrderItem

 **Important Constraints**
    User->Cart(One-to-One)
    Unique Product Per Cart
    Stored Price per order Item
    Foreign Key constraints with referential integrity

 **Installation and Setup**   

  Step-1) Clone the Repository.
  
  Clone the Project from https://github.com/srikar544/python_ecommerce.git
  cd flask-ecommerce
  
  Step-2) Create Virtual Environment
  
  venv\Scripts\activate from the visual studio
  
  Step-3) Install Dependencies
  pip install -r requirements.txt
  
  Step-4)Configure the Database
  app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user:password@localhost/ecommerce" - Need to use your own database 

  Step-5)Create Database tables 

  flask db init
  flask db migrate
  flask db upgrade

  Step-6)Run the Application
  python run.py

  Step-7) Visit and do the operations

  http://127.0.0.1:5000

  **Application flow**

  1.User adds products to cart
  2.Cart calculates grand total
  3.Checkout creates:
     3.1 Order
     3.2 OrderItem (with price snapshot)
  4.Cart is cleared
  5.User redirected to Order History

  **Sample Queries**

  SELECT * FROM user;
  SELECT * FROM product;
  SELECT * FROM cart;
  SELECT * FROM cart_item;
  SELECT * FROM `order`;
  SELECT * FROM order_item;

  order is a reserved keyword → always use backticks:

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

   <img width="1781" height="783" alt="image" src="https://github.com/user-attachments/assets/40defb26-4be9-41b7-9a03-112a796d4456" />

   <img width="1000" height="633" alt="image" src="https://github.com/user-attachments/assets/f67f3685-2bb0-4c98-afe6-2ed484884af8" />

  <img width="1655" height="1013" alt="image" src="https://github.com/user-attachments/assets/86e72344-49e5-42d4-b136-dc07f4c46001" />






