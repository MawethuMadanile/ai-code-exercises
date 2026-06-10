from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    def __init__(self, host, port, username, password, database,
                 use_ssl=False, connection_timeout=30, retry_attempts=3,
                 pool_size=5, charset='utf8'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.use_ssl = use_ssl
        self.connection_timeout = connection_timeout
        self.retry_attempts = retry_attempts
        self.pool_size = pool_size
        self.charset = charset
        self.connection = None

    @abstractmethod
    def build_connection_string(self):
        pass

    def connect(self):
        print(f"Connecting to {self.__class__.__name__} database...")
        connection_string = self.build_connection_string()
        print(f"Connection string: {connection_string}")
        print("Connection successful!")
        return self.connection


class MySQLConnection(DatabaseConnection):
    def build_connection_string(self):
        conn_str = (
            f"mysql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            f"?charset={self.charset}"
            f"&connectionTimeout={self.connection_timeout}"
        )
        if self.use_ssl:
            conn_str += "&useSSL=true"
        return conn_str


class PostgreSQLConnection(DatabaseConnection):
    def build_connection_string(self):
        conn_str = (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        if self.use_ssl:
            conn_str += "?sslmode=require"
        return conn_str


class MongoDBConnection(DatabaseConnection):
    def build_connection_string(self):
        conn_str = (
            f"mongodb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            f"?retryAttempts={self.retry_attempts}"
            f"&poolSize={self.pool_size}"
        )
        if self.use_ssl:
            conn_str += "&ssl=true"
        return conn_str


class RedisConnection(DatabaseConnection):
    def build_connection_string(self):
        return f"redis://{self.host}:{self.port}/{self.database}"


class DatabaseConnectionFactory:
    _connection_types = {
        'mysql': MySQLConnection,
        'postgresql': PostgreSQLConnection,
        'mongodb': MongoDBConnection,
        'redis': RedisConnection
    }

    @staticmethod
    def create(db_type, host, port, username, password, database, **kwargs):
        connection_class = DatabaseConnectionFactory._connection_types.get(db_type)
        if not connection_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        return connection_class(host, port, username, password, database, **kwargs)


# Example usage
if __name__ == "__main__":
    mysql_db = DatabaseConnectionFactory.create(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='db_user',
        password='password123',
        database='app_db',
        use_ssl=True
    )
    mysql_db.connect()

    mongo_db = DatabaseConnectionFactory.create(
        db_type='mongodb',
        host='mongodb.example.com',
        port=27017,
        username='mongo_user',
        password='mongo123',
        database='analytics',
        pool_size=10,
        retry_attempts=5
    )
    mongo_db.connect()