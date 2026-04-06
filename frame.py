from abc import ABC, abstractmethod
import re


class PDU(ABC):
    def __init__(self, payload: str):
        if payload is None:
            raise ValueError("Payload nesmí být None")
        self._payload = payload

    def get_payload(self) -> str:
        return self._payload

    def set_payload(self, val: str):
        if val is None:
            raise ValueError("Payload nesmí být None")
        self._payload = val

    @abstractmethod
    def is_valid(self) -> bool:
        pass


class EthFrame(PDU):
    MAC_REGEX = re.compile(r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")

    def __init__(self, dmac: str, smac: str, eth_type: int, payload: str, fcs: int = None):
        super().__init__(payload)

        if not self.is_valid_mac(dmac) or not self.is_valid_mac(smac):
            raise ValueError("Neplatná MAC adresa")

        self._dmac = dmac
        self._smac = smac
        self._type = eth_type
        self._fcs = fcs if fcs is not None else self.calculate_fcs()

    @staticmethod
    def is_valid_mac(mac: str) -> bool:
        return bool(EthFrame.MAC_REGEX.match(mac))

    def set_payload(self, val: str):
        super().set_payload(val)
        self._recalculate_fcs()

    def set_dmac(self, val: str):
        if not self.is_valid_mac(val):
            raise ValueError("Neplatná MAC")
        self._dmac = val
        self._recalculate_fcs()

    def set_smac(self, val: str):
        if not self.is_valid_mac(val):
            raise ValueError("Neplatná MAC")
        self._smac = val
        self._recalculate_fcs()

    def set_type(self, val: int):
        self._type = val
        self._recalculate_fcs()

    def get_fcs(self):
        return self._fcs

    def calculate_fcs(self) -> int:
        data = f"{self._dmac}{self._smac}{self._type}{self._payload}"
        return sum(ord(c) for c in data)

    def _recalculate_fcs(self):
        self._fcs = self.calculate_fcs()

    def is_valid(self) -> bool:
        return self._fcs == self.calculate_fcs()

    def corrupt_data(self):
        self._payload = "CORRUPTED_DATA"
        self._fcs += 1

    def __str__(self):
        return f"[EthFrame] SRC: {self._smac} DST: {self._dmac} TYPE: {self._type} DATA: {self._payload}"


# --- test ---
if __name__ == "__main__":
    frame = EthFrame(
        dmac="AA:BB:CC:DD:EE:FF",
        smac="11:22:33:44:55:66",
        eth_type=0x0800,
        payload="Hello"
    )

    print(frame)
    print("Valid:", frame.is_valid())

    frame.corrupt_data()
    print("Valid po poškození:", frame.is_valid())