from sqlalchemy import Column, Integer, Enum, Float, ForeignKey, String
from database.database import Base
from sqlalchemy.orm import relationship
from utils.status import Status


class Package(Base):
    __tablename__ = 'package'

    package_id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    sender_login = Column(String(128), ForeignKey('default_user.login'))
    sender = relationship('DefaultUser', foreign_keys=[sender_login],
                          backref='sent_packages', cascade='save-update', single_parent=True)
    recipient_login = Column(String(128), ForeignKey('default_user.login'))
    recipient = relationship('DefaultUser', foreign_keys=[recipient_login],
                             backref='received_packages', cascade='save-update', single_parent=True)
    status = Column(Enum(Status), default=Status.IN_WAREHOUSE)
