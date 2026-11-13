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

class EconomyPassenger(Passenger):
    CLASS_NAME = "Economy"

    def __init__(self, name, location, destination, date, seat_preference):
        super().__init__(name, location, destination, date)
        self.seat_preference = seat_preference

    @classmethod
    def extra_fields(cls):
        return [("seat_preference",
                 "Seat preference [1] Window [2] Aisle [3] Middle",
                 parse_seat)]

    def extra_details(self):
        return {"Seat": self.seat_preference}


class BusinessPassenger(Passenger):
    CLASS_NAME = "Business"
    BAGGAGE_KG = 100 

    def __init__(self, name, location, destination, date, lounge_pass_code):
        super().__init__(name, location, destination, date)
        self.lounge_pass_code = lounge_pass_code

    @classmethod
    def extra_fields(cls):
        return [("lounge_pass_code", "Lounge pass code", parse_code)]

    def extra_details(self):
        return {"Lounge pass": self.lounge_pass_code}


class FirstClassPassenger(Passenger):
    CLASS_NAME = "First Class"

    def __init__(self, name, location, destination, date,
                 suite_number, chauffeur_service):
        super().__init__(name, location, destination, date)
        self.suite_number = suite_number
        self.chauffeur_service = chauffeur_service  # True / False

    @classmethod
    def extra_fields(cls):
        return [("suite_number", "Suite number", parse_code),
                ("chauffeur_service", "Chauffeur service? (yes/no)", parse_yes_no)]

    def extra_details(self):
        return {"Suite": self.suite_number,
                "Chauffeur": "Yes" if self.chauffeur_service else "No"}


# ---------------------------------------------------------------------------
# Quick test for Part 1 only (runs only when this file is run directly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    passenger = Passenger("Eden", "Kigali", "Nairobi", date(2026, 12, 20))
    print(passenger)
    print("Allowance:", passenger.get_weight_allowance(), "kg")
    print("Booking reference:", passenger.booking_ref)
    
# Test for the inheritance implementation Part 2
    economy = EconomyPassenger("Divine", "Kigali", "Lagos", date(2026, 12, 20), "Window")
    business = BusinessPassenger("Divine", "Kigali", "Nairobi", date(2026, 12, 20), "AB12")
    first = FirstClassPassenger("Divine", "Kigali", "Dubai", date(2026, 12, 20), "S3", True)
    
    

    for passenger in (economy, business, first):
        print(passenger)
        print()

    print("Economy is a Passenger:", isinstance(economy, Passenger))
    print("Business allowance:", business.get_weight_allowance(), "kg")
    print("Economy allowance:", economy.get_weight_allowance(), "kg")
    
    
