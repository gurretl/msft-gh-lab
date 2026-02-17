import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse


class InMemoryDeviceRepository:
    def __init__(self):
        self._devices: Dict[str, DeviceResponse] = {}

    async def get_devices(self) -> List[DeviceResponse]:
        return list(self._devices.values())

    async def get_device(self, device_id: str) -> Optional[DeviceResponse]:
        return self._devices.get(device_id)

    async def create_device(self, device: DeviceCreate) -> DeviceResponse:
        now = datetime.now(timezone.utc)
        device_id = str(uuid.uuid4())
        dev = DeviceResponse(
            id=device_id,
            name=device.name,
            assigned_to=device.assigned_to,
            created_at=now,
            updated_at=now,
        )
        self._devices[device_id] = dev
        return dev

    async def update_device(self, device_id: str, device: DeviceUpdate) -> Optional[DeviceResponse]:
        existing = self._devices.get(device_id)
        if not existing:
            return None
        updated = existing.copy(update={
            "name": device.name if device.name is not None else existing.name,
            "assigned_to": device.assigned_to if device.assigned_to is not None else existing.assigned_to,
            "updated_at": datetime.now(timezone.utc),
        })
        self._devices[device_id] = updated
        return updated

    async def delete_device(self, device_id: str) -> bool:
        return self._devices.pop(device_id, None) is not None
