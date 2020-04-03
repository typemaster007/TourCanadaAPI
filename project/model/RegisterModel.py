__author__ = "Daksh Patel"
from project.model import dynamodb, scan_table


class Login:
    def __init__(self):
        self.dynamodb = dynamodb
        self.table = dynamodb.Table('users')

    def getUserDetails(self, username):
        response = scan_table(table_name='users', filter_key='username', filter_value=username)
        # print(response)
        return response

    def checkUserCredentials(self, username, password):
        error = None
        matched = False
        response = self.getUserDetails(username)
        if response.get('Count') == 0:
            error = "No user Found!"
            return matched, error
        else:
            pwd = response.get('Items')[0].get('password')
            if pwd == password:
                matched = True
            else:
                error = "Incorrect Password!"
                matched = False
            return matched, error
