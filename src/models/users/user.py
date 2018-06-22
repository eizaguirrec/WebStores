import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one(collection=UserConstants.COLLECTION,  query={'email': email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user name does not exists.")
        if not Utils.check_hashed_password(password,  user_data['password']):
            raise UserErrors.IncorrectPasswordError("Incorrect password")
        else:
            return True

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one(collection=UserConstants.COLLECTION, query={'email': email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email does not have the correct format.")
        User(email, Utils.hash_pasword(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.update(UserConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)

    @staticmethod
    def change_user_password(email, password, new_password, _id):
        if not User.is_login_valid(email, password):
            raise UserErrors.IncorrectPasswordError("Incorrect password")
        User(email, Utils.hash_pasword(new_password), _id).save_to_db()

        return True
