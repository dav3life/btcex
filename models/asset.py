import logging
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from models import Base


logger = logging.getLogger(__file__)


class Asset(Base):

    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=True)

    # We keep track of when `Asset`s were removed
    previous_name = Column(String(100), nullable=True)
    removed_at = Column(DateTime, nullable=True)

    @classmethod
    def create_asset(cls, name):
        if name is not None:
            asset = cls(name=name.strip().upper())
            return asset

    def remove(self, session):
        self.name, self.previous_name = None, self.name
        self.removed_at = datetime.now()
        session.add(self)
        logger.info('Added Asset instance {} for removal'.format(self.id))

    @property
    def removed(self):
        return self.removed_at is not None
