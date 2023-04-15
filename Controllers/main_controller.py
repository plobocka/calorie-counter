from Controllers.account_controller import AccountController
from Models.database_model import DataBaseModel


class MainController:
    def __init__(self, root):
        self.database_model = DataBaseModel()

        self.account_controller = AccountController(root, self.database_model)