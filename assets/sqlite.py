import sqlite3


class SQLighter():

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_pr_msg(self, chat_id):

        with self.connection:

            return self.cursor.execute("SELECT `pr_message` FROM `messages` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def add_new_user(self, chat_id, pr_message):
        with self.connection:

            return self.cursor.execute("INSERT INTO `messages` (`id`, `pr_message`) VALUES (?, ?)", (chat_id, pr_message))

    def check_user(self, chat_id):

        with self.connection:

            user = self.cursor.execute("SELECT * FROM `messages` WHERE `id` = ?", (chat_id, )).fetchall()
        
        if len(user) > 0:
            return True
        else:
            return False

    def change_msg(self, chat_id, message_id):
        with self.connection:

            return self.cursor.execute("UPDATE `messages` SET `pr_message` = ? WHERE `id` = ?", (message_id, chat_id ))

    def get_state(self, chat_id):
        with self.connection:
            return self.connection.execute("SELECT `state` FROM `messages` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def change_state(self, chat_id, state):
        with self.connection:
            return self.connection.execute("UPDATE `messages` SET `state` = ? WHERE `id` = ?", (state, chat_id))

    def get_cl_type(self, chat_id):
        with self.connection:
            return self.connection.execute("SELECT `cl_type` FROM `messages` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def change_cl_type(self, chat_id, cl_type):
        with self.connection:
            return self.connection.execute("UPDATE `messages` SET `cl_type` = ? WHERE `id` = ?",(cl_type, chat_id))


# sql = SQLighter("database/db.db")
# print(sql.change_cl_type(952657043, 1))