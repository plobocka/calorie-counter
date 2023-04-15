USERS_TABLE = """
                CREATE TABLE IF NOT EXISTS Users (
                    IdUser INTEGER PRIMARY KEY AUTOINCREMENT,
                    Login TEXT NOT NULL,
                    Password TEXT NOT NULL,
                    Email TEXT NOT NULL,
                    CaloriesIntake INTEGER NOT NULL
                );
                """

WEIGHTS_TABLE = """
                CREATE TABLE IF NOT EXISTS Weights (
                    IdWeight INTEGER PRIMARY KEY AUTOINCREMENT,
                    IdUser INTEGER NOT NULL,
                    WeightValue REAL NOT NULL,
                    WeightDate TEXT NOT NULL,
                    FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                );
                """

PRODUCTS_TABLE = """
                CREATE TABLE IF NOT EXISTS Products (
                    IdProduct INTEGER PRIMARY KEY AUTOINCREMENT,
                    IdUser INTEGER NOT NULL,
                    Name TEXT NOT NULL,
                    Calories TEXT NOT NULL,
                    FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                );
                """

CONSUMED_PRODUCTS_TABLE = """
                CREATE TABLE IF NOT EXISTS ConsumedProducts (
                    IdConsumedProduct INTEGER PRIMARY KEY AUTOINCREMENT,
                    IdProduct INTEGER NOT NULL,
                    IdUser INTEGER NOT NULL,
                    ConsumptionDate TEXT NOT NULL,
                    Grammage INTEGER NOT NULL,
                    FOREIGN KEY (IdProduct) REFERENCES Products (IdProduct),
                    FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                );
                """                
