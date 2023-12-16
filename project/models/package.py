from sqlalchemy import Column, Integer, Enum, Double, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from enums.status import Status


class Package(Base):
    __tablename__ = 'package'

    package_id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    weight = Column(Double, nullable=False)
    sender_id = Column(Integer, ForeignKey('default_user.default_user_id'))
    recipient_id = Column(Integer, ForeignKey('default_user.default_user_id'))
    default_user = relationship('DefaultUser', backref='package', cascade='save-update', single_parent=True)
    status = Column(Enum(Status), default=Status.IN_WAREHOUSE)
