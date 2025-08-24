from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator


class DatabaseClient():
    def __init__(self, url: str) -> None:
        self.engine = create_engine(url=url)
        self.sessionmaker = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Yields a new SQLAlchemy session.
        Ensures that the session is properly closed after use.

        Yields
        ------
        Session
            A new SQLAlchemy session.
        """

        session: Session = self.sessionmaker()

        try:
            yield session
        finally:
            session.close()
