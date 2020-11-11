from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class AuthorizePayload:
    id_token: Dict
    certificate: Optional[str] = None
    iso15118_certificate_hash_data: Optional[List] = None


@dataclass
class BootNotificationPayload:
    chargingStation: Dict
    reason: str
