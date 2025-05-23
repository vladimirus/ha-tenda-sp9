from abc import abstractmethod
import asyncio
import logging
from .tenda import TendaBeliPlug, TendaBeliServer

from homeassistant.components.sensor import (SensorEntity)
from homeassistant.helpers.entity_registry import async_get
from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN, HUB

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None):
    
    async def remove_entity_if_exist(unique_id):
        try:
            entity_registry = async_get(hass)
            entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, unique_id)
            if not entity_id == None:
                entity_registry.async_remove(entity_id)
                _LOGGER.debug(f"Succesfully removed {entity_id}")
        except Exception as err:
                _LOGGER.debug(f"Unexpected error during entity removal, {err=}, {type(err)=}")
                raise
        
    async def process_callback(sn: str, msg: str):
        try:
            if msg == "setup":
                power = TendaBeliPower(hass.data[DOMAIN][HUB], sn)
                energy = TendaBeliEnergy(hass.data[DOMAIN][HUB], sn)
                await remove_entity_if_exist(f"tbp_power_{sn}")
                await remove_entity_if_exist(f"tbp_energy_{sn}")
                async_add_entities([power, energy], True)
                _LOGGER.debug(f"Succesfully added sensor entities for {sn}")

            elif msg == "discard":
                await remove_entity_if_exist(f"tbp_power_{sn}")
                await remove_entity_if_exist(f"tbp_energy_{sn}")

        except Exception as err:
                _LOGGER.debug(f"Unexpected error during setup, {err=}, {type(err)=}")
                raise
    try:
        hub: TendaBeliServer = hass.data[DOMAIN][HUB]
        hub.register_setup_callback(process_callback)
    except Exception as err:
        _LOGGER.debug(f"Unexpected {err=}, {type(err)=}")
        raise
    
class TendaBeliSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, hub, sn):
        self._sn: str | None = sn
        self._hub: TendaBeliServer = hub
        self._plug: TendaBeliPlug = self._hub.get_TBP(self._sn)

        self._available = False
        self._state = "unknown"
        self._attr_device_class = None
        self._attr_unit_of_measurement = None
        self._attr_state_class = None

    async def async_added_to_hass(self):
        self._hub.register_operational_callback(self.process_callback, self._sn)

    async def async_will_remove_from_hass(self):
        self._hub.remove_operational_callback(self.process_callback, self._sn)

    async def process_callback(self):
        self._available = self._plug.alive
        await self.async_update()
        self.async_write_ha_state()
    
    @abstractmethod
    async def async_update(self) -> None:
        pass
    
    @property
    def available(self) -> bool:
        return self._available 

    @property
    def state(self):
        return self._state

    @property
    def should_poll(self):
        return False
    
    @property
    def device_class(self):
        return self._attr_device_class

    @property
    def unit_of_measurement(self):
        return self._attr_unit_of_measurement
    
    @property
    def state_class(self):
        return self._attr_state_class
    
class TendaBeliPower(TendaBeliSensor):
    
    def __init__(self, hub, sn):

        super().__init__(hub, sn)
        self._attr_name = f"tbp_power_{self._sn[-4:]}"
        self._attr_unique_id = f"tbp_power_{self._sn}"
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_unit_of_measurement = "W"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        

    async def async_update(self) -> None:
        self._state = self._plug.power

class TendaBeliEnergy(TendaBeliSensor):
    
    def __init__(self, hub, sn):

        super().__init__(hub, sn)
        self._attr_name = f"tbp_energy_{self._sn[-4:]}"
        self._attr_unique_id = f"tbp_energy_{self._sn}"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_unit_of_measurement = "kWh"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    async def async_update(self) -> None:
        self._state = self._plug.energy