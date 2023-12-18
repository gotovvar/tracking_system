from sqlalchemy import Column, Integer, Enum, Float, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
from enums.status import Status


class Package(Base):
    __tablename__ = 'package'

    package_id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    sender_id = Column(Integer, ForeignKey('default_user.default_user_id'))
    sender = relationship('DefaultUser', foreign_keys=[sender_id],
                          backref='sent_packages', cascade='save-update', single_parent=True)
    recipient_id = Column(Integer, ForeignKey('default_user.default_user_id'))
    recipient = relationship('DefaultUser', foreign_keys=[recipient_id],
                             backref='received_packages', cascade='save-update', single_parent=True)
    status = Column(Enum(Status), default=Status.IN_WAREHOUSE)
