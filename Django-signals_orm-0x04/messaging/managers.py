import sqlite3


class UnreadMessagesManager:
    def unread_for_user(self, user_id, only_fields=None):
        class contextManager:
            def __init__(self, user_id, only_fields):
                self.user_id = user_id
                self.only_fields = only_fields or [
                    'id', 'sender_id', 'content', 'sent_at']
                self.conn = None
                self.result = None

            def __enter__(self):
                self.conn = sqlite3.connect('user_db')
                cursor = self.conn.cursor()
                fields = ', '.join(self.only_fields)
                query = (
                    f'SELECT {fields} FROM messages '
                    'WHERE recipient_id=? AND read=0'
                )
                cursor.execute(query, (self.user_id))
                self.result = cursor.fetchall()
                return self.result

            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.conn:
                    print('closing database')
                    self.conn.close()
                if exc_val:
                    return False
        return contextManager(user_id, only_fields)
