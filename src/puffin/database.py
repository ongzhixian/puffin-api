import logging
from contextlib import contextmanager
from os import environ
import psycopg2

# Set up logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseRepository:
    """A base class for database repositories with a context-managed cursor."""
    
    _CONNECTION_STRING = environ.get('PUFFIN_DB_CONNECTION_STRING')

    if not _CONNECTION_STRING:
        raise ValueError("Environment variable 'PUFFIN_DB_CONNECTION_STRING' is not set.")
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @contextmanager
    def db_cursor(self):
        """Yields a context-managed database cursor."""
        db = None
        cursor = None
        try:
            db = psycopg2.connect(self._CONNECTION_STRING)
            cursor = db.cursor()
            self.logger.info("Database connection and cursor opened.")
            yield cursor
            db.commit()
            self.logger.info("Transaction committed.")
        except psycopg2.Error as e:
            if db:
                db.rollback()
                self.logger.error("Transaction rolled back due to error: %s", e)
            raise  # Re-raises the exception
        finally:
            if cursor:
                cursor.close()
                self.logger.info("Cursor closed.")
            if db:
                db.close()
                self.logger.info("Database connection closed.")

