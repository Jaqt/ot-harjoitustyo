from dataclasses import dataclass


@dataclass
class Transaction:
    user_id: int
    year: int
    month: int
    transaction_type: str
    category: str
    amount: float
    description: str = ""
    id: int | None = None
