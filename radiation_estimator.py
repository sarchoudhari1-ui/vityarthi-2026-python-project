"""Estimate radiation-related characteristics of common mobile functions.

This is an educational model. It does not measure electromagnetic fields or
replace a phone manufacturer's SAR report.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class MobileFunction:
    name: str
    radiation_type: str
    frequency: str
    transmit_power_w: float
    sar_w_per_kg: float | None
    explanation: str


FUNCTIONS = {
    "call": MobileFunction(
        "Voice call", "Radiofrequency (RF), non-ionizing", "700 MHz-3.5 GHz",
        0.25, 0.40, "The phone usually transmits continuously; power changes with signal strength.",
    ),
    "mobile-data": MobileFunction(
        "Mobile data", "Radiofrequency (RF), non-ionizing", "600 MHz-6 GHz",
        0.20, 0.30, "Uploads, video calls, and weak cellular signals can increase transmission power.",
    ),
    "wifi": MobileFunction(
        "Wi-Fi", "Radiofrequency (RF), non-ionizing", "2.4, 5, or 6 GHz",
        0.10, 0.10, "The phone transmits in bursts to a nearby access point; receiving data uses less RF power.",
    ),
    "bluetooth": MobileFunction(
        "Bluetooth", "Radiofrequency (RF), non-ionizing", "2.4 GHz",
        0.0025, 0.01, "Bluetooth Low Energy normally uses very short, low-power bursts.",
    ),
    "gps": MobileFunction(
        "GPS location", "Radiofrequency received by the phone, non-ionizing", "1.176-1.575 GHz",
        0.0, 0.0, "GPS is primarily receive-only on a phone, so this model assigns no intentional transmit power.",
    ),
    "nfc": MobileFunction(
        "NFC", "Radiofrequency (RF), non-ionizing", "13.56 MHz",
        0.001, 0.001, "NFC works only at very short range and generally transmits during a tap or scan.",
    ),
    "airplane": MobileFunction(
        "Airplane mode", "No intentional radio transmitter; heat and visible light remain", "None",
        0.0, 0.0, "The phone can still produce heat and screen light. Wi-Fi or Bluetooth may be re-enabled separately.",
    ),
    "charging": MobileFunction(
        "Charging", "Low-frequency electric/magnetic fields and heat; no intentional RF", "50/60 Hz and switching frequencies",
        0.0, None, "Charging is not represented by a phone RF SAR value in this model.",
    ),
}


def estimate(function_name: str, minutes: float) -> dict[str, object]:
    """Return an educational exposure estimate for a function and duration."""
    if minutes < 0:
        raise ValueError("minutes must be zero or greater")

    try:
        function = FUNCTIONS[function_name.lower()]
    except KeyError as error:
        available = ", ".join(sorted(FUNCTIONS))
        raise ValueError(f"unknown function '{function_name}'. Choose: {available}") from error

    energy_wh = function.transmit_power_w * minutes / 60
    return {
        "function": function,
        "minutes": minutes,
        "energy_wh": energy_wh,
    }


def print_estimate(result: dict[str, object]) -> None:
    function = result["function"]
    assert isinstance(function, MobileFunction)
    sar = "not applicable" if function.sar_w_per_kg is None else f"{function.sar_w_per_kg:.3f} W/kg (illustrative)"
    print(f"\n{function.name}")
    print(f"Radiation:       {function.radiation_type}")
    print(f"Frequency:       {function.frequency}")
    print(f"Estimated power: {function.transmit_power_w:g} W")
    print(f"SAR estimate:    {sar}")
    print(f"Energy in use:   {result['energy_wh']:.5f} Wh over {result['minutes']:g} minutes")
    print(f"Note:            {function.explanation}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate radiation type and typical transmit power for a mobile function."
    )
    parser.add_argument("function", choices=sorted(FUNCTIONS), help="mobile function to estimate")
    parser.add_argument("--minutes", type=float, default=60, help="duration in minutes (default: 60)")
    parser.add_argument("--list", action="store_true", help="list functions and exit")
    return parser


def main() -> None:
    parser = build_parser()
    arguments = parser.parse_args()
    if arguments.list:
        for key, function in FUNCTIONS.items():
            print(f"{key:12} - {function.name}: {function.radiation_type}")
        return
    try:
        print_estimate(estimate(arguments.function, arguments.minutes))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()