from enum import Enum


class Status(Enum):
    IN_WAREHOUSE = 'IN_WAREHOUSE'
    ON_WAY = 'ON_WAY'
    DELIVERED = 'DELIVERED'
