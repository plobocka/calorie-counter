import sqlite3
from Database import data_tables

# methods of operations on the database 
# connecting to database
def connect_to_db():
        database = "database.db"
        print("connecting...")
        connection = sqlite3.connect(database)
        return connection


def create_table(sql):
    print("creating table...")
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()


def create_tables():
    print("creating tables")
    create_table(data_tables.USERS_TABLE)
    create_table(data_tables.WEIGHTS_TABLE)
    create_table(data_tables.PRODUCTS_TABLE)
    create_table(data_tables.CONSUMED_PRODUCTS_TABLE)


# write data into database
def query(sql, data):
    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql, data)
    con.commit()
    cursor.close()


def insert_user(login, password, email, calories_intake):
    sql_cmd = """
            INSERT INTO Users (Login,Password,Email,CaloriesIntake)
            VALUES (?,?,?,?);
            """
    data = (login, password, email, calories_intake)
    query(sql_cmd, data)


def insert_weight(id_user, weight_value, weight_date):
    sql_cmd = """
            INSERT INTO Weights (IdUser,WeightValue,WeightDate)
            VALUES (?,?,?);
            """
    data = (id_user, weight_value, weight_date)
    query(sql_cmd, data)


def insert_product(id_user, product_name, calories):
    sql_cmd = """
            INSERT INTO Products (IdUser,Name,Calories)
            VALUES (?,?,?);
            """
    data = (id_user, product_name, calories)
    query(sql_cmd, data)


def insert_consumed_product(id_product, id_user, consumption_date, grammage):
    sql_cmd = """
          INSERT INTO ConsumedProducts (IdProduct,IdUser,ConsumptionDate,Grammage)
          VALUES (?,?,?,?);
          """
    data = (id_product, id_user, consumption_date, grammage)
    query(sql_cmd, data)


# get data from database
def get_user_by_login(login):
    sql_cmd = """
          SELECT * FROM Users WHERE Login=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (login,))
    
    row = cursor.fetchone()
    return row


def get_user_by_login_and_password(login, password):
    sql_cmd = """
          SELECT * FROM Users WHERE Login=? AND Password=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (login, password))
    
    row = cursor.fetchone()
    return row


def get_user_weight(user_id):
    sql_cmd = """
          SELECT * FROM Weights WHERE IdUser=? ORDER BY WeightDate DESC LIMIT 1;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id,))
    
    row = cursor.fetchone()
    return row

def get_first_weight_before_date(user_id, current_date):
    sql_cmd = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate<=? ORDER BY WeightDate DESC LIMIT 1;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id, current_date))
    
    row = cursor.fetchone()
    return row

def get_first_after_before_date(user_id, current_date):
    sql_cmd = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate>=? ORDER BY WeightDate ASC LIMIT 1;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id, current_date))
    
    row = cursor.fetchone()
    return row

def get_user_weight_by_date(user_id, date):
    sql_cmd = """
          SELECT * FROM Weights WHERE IdUser=? AND WeightDate=? LIMIT 1;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id, date))
    
    row = cursor.fetchone()
    return row


def get_user_products(user_id):
    sql_cmd = """
          SELECT * FROM Products WHERE IdUser=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id,))
    
    rows = cursor.fetchall()
    return rows


def get_user_consumed_products_by_date(user_id, curr_date):
    sql_cmd = """
          SELECT cp.IdConsumedProduct, cp.IdProduct, cp.IdUser, 
                cp.ConsumptionDate, cp.Grammage, p.Name, p.Calories
          FROM ConsumedProducts AS cp
          INNER JOIN Products AS p ON cp.IdProduct=p.IdProduct
          WHERE cp.IdUser=? AND cp.ConsumptionDate=?;
          """


    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id, curr_date))

    rows = cursor.fetchall()
    return rows

def get_user_calories_intake(user_id):
    sql_cmd = """
          SELECT CaloriesIntake FROM Users WHERE IdUser=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id,))
    
    row = cursor.fetchone()
    return row

# update some basic data
def update_user_weight_date(user_id, weight, date):
    sql_cmd = """
            UPDATE Weights SET WeightValue=? WHERE IdUser=? AND WeightDate=?;
            """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (user_id, weight, date))
    con.commit()


def update_product(product_id, name, calories):
    sql_cmd = """
          UPDATE Products SET Name=?,Calories=? WHERE IdProduct=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (product_id, name, calories))
    con.commit()


def update_consumed_product(product_consumed_id, grammage):
    sql_cmd = """
          UPDATE ConsumedProducts SET Grammage=? WHERE IdConsumedProduct=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (product_consumed_id, grammage))
    con.commit()

def update_calories_intake(calories_intake, user_id):
    sql_cmd = """
          UPDATE Users SET CaloriesIntake=? WHERE IdUser=?;
          """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (calories_intake, user_id))
    con.commit()


# delete data from database
def delete_consumed_product_user_id(user_id, consumed_product_id):
    print(consumed_product_id)
    sql_cmd = """
            DELETE FROM ConsumedProducts WHERE IdConsumedProduct=? AND IdUser=?;
            """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (consumed_product_id, user_id))
    con.commit()

def delete_consumed_product_by_id(consumed_product_id):
    sql_cmd = """
            DELETE FROM ConsumedProducts WHERE IdProduct=?;
            """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (consumed_product_id,))
    con.commit()


def delete_product(product_id, user_id):
    sql_cmd = """
            DELETE FROM Products WHERE IdProduct=? AND IdUser=?;
            """

    con = connect_to_db()
    cursor = con.cursor()
    cursor.execute(sql_cmd, (product_id, user_id))
    con.commit()
