from dataclasses import dataclass

@dataclass
class Config:
    token: str = 'BOT_TOKEN'
    admin_ids: int = 'ADMIN_IDS'