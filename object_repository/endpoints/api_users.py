from PyAuto.PyAutoRest import PyRest


# Using endpoints improves code maintenance and readability
class ApiUsers(PyRest):

    def __init__(self, rest_client):
        # call super class constructor, to inherit the self.response instance variable
        super().__init__()
        self.rest_client = rest_client  # PyRest object
        self.end_point = 'api/users'

    def get_users_page_2(self):
        # call only the endpoint, this will save result in self.response in super class
        # do all the validation in your test step using method chaining
        self.rest_client.get(self.end_point, params={'page': 2})
        return self.rest_client

    def get_user_id(self, user_id):
        self.rest_client.get(self.end_point+"/"+user_id, params={'page': 2})
        return self.rest_client

    def post_user(self, json_data):
        self.rest_client.post(self.end_point, json=json_data)
        return self.rest_client
