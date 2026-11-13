import random
import string
from datetime import date


class Passenger:
    CLASS_NAME = "Standard"
    BAGGAGE_KG = 20  # default allowance

    def __init__(self, name, location, destination, date):
        self.name = name
        self.location = location
        self.destination = destination
        self.date = date  # a datetime.date object
        self.booking_ref = self._new_booking_ref()

    @staticmethod
    def _new_booking_ref():
        alphabet = string.ascii_uppercase + string.digits
        return "".join(random.choices(alphabet, k=6))

    @classmethod
    def extra_fields(cls):
        """(attribute, prompt, validator) for each class-specific field."""
        return []

    def extra_details(self):
        """Class-specific lines to show on the ticket."""
        return {}

    def get_weight_allowance(self):
        return self.BAGGAGE_KG

    def get_passenger_info(self):
        rows = {
            "Booking ref": self.booking_ref,
            "Passenger": self.name,
            "Route": f"{self.location} -> {self.destination}",
            "Date": self.date.strftime("%a, %d %b %Y"),
            "Class": self.CLASS_NAME,
            "Baggage": f"{self.get_weight_allowance()} kg",
            **self.extra_details(),
        }
        label_width = max(len(label) for label in rows)
        lines = [f" {label:<{label_width}} : {value} " for label, value in rows.items()]
        title = " BOARDING PASS "
        width = max(len(line) for line in lines + [title])

        card = ["╔" + "═" * width + "╗",
                "║" + title.center(width) + "║",
                "╠" + "═" * width + "╣"]
        card += ["║" + line.ljust(width) + "║" for line in lines]
        card.append("╚" + "═" * width + "╝")
        return "\n".join(card)

    def __str__(self):
        return self.get_passenger_info()


# ---------------------------------------------------------------------------
# Quick test for Part 1 only (runs only when this file is run directly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    passenger = Passenger("Eden", "Kigali", "Nairobi", date(2026, 12, 20))
    print(passenger)
    print("Allowance:", passenger.get_weight_allowance(), "kg")
    print("Booking reference:", passenger.booking_ref)