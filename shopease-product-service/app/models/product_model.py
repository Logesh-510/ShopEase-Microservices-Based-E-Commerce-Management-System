from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    id: int
    name: str
    description: str | None
    price: float
    stock_quantity: int
    category: str
    status: str = "Active"
    created_at: datetime = field(default_factory=datetime.now)
