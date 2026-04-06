# Frame-OOP

Jednoduchý OOP model síťové komunikace v Pythonu.

Projekt implementuje základní datovou jednotku (PDU) a ethernetový rámec (EthFrame). Ukazuje práci s dědičností, zapouzdřením a validací dat.

---

## Funkce

* abstraktní třída PDU
* třída EthFrame dědící z PDU
* validace MAC adres pomocí regexu
* automatický výpočet FCS při změně dat
* kontrola integrity dat přes `is_valid()`
* simulace poškození dat

---

## Požadavky

* Python 3.x
* žádné externí knihovny

---

## Ukázka použití

```python
from ethframe import EthFrame

frame = EthFrame(
    dmac="AA:BB:CC:DD:EE:FF",
    smac="11:22:33:44:55:66",
    eth_type=0x0800,
    payload="Hello"
)

print(frame)
print("Valid:", frame.is_valid())

frame.corrupt_data()
print("Valid after corruption:", frame.is_valid())
```

---

## Princip

* každá změna dat přepočítá FCS
* `is_valid()` porovnává uložený a aktuální FCS
* rozdíl znamená poškození dat
