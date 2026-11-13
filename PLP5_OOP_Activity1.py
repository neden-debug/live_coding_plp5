import random
import string
from datetime import date, datetime


# ===========================================================================
# PART 3 - HYGUETTE
# Error handling
# - ask() is the ONE input loop used everywhere: it rejects empty input and
#   keeps asking until the validator accepts the answer
# - Each validator either returns a clean value or raises ValueError with a
#   message telling the user what went wrong
# ===========================================================================
def ask(prompt, validator):
    while True:
        raw = input(f"  {prompt}: ").strip()
        try:
            if not raw:
                raise ValueError("This field cannot be empty.")
            return validator(raw)
        except ValueError as error:
            print(f"    x {error}")


def parse_text(raw):
    """Names and cities: letters, spaces, hyphens and apostrophes only."""
    if not all(ch.isalpha() or ch in " -'" for ch in raw):
        raise ValueError("Use letters only (spaces, - and ' are allowed).")
    return " ".join(raw.split()).title()


def different_from(origin):
    """Builds a validator that rejects a destination equal to the origin."""
    def validator(raw):
        place = parse_text(raw)
        if place.lower() == origin.lower():
            raise ValueError("Destination must be different from departure.")
        return place
    return validator


def parse_date(raw):
    try:
        travel_date = datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Use the format YYYY-MM-DD, e.g. 2026-12-20.")
    if travel_date < date.today():
        raise ValueError("The travel date cannot be in the past.")
    return travel_date


def parse_yes_no(raw):
    answer = raw.lower()
    if answer in ("y", "yes"):
        return True
    if answer in ("n", "no"):
        return False
    raise ValueError("Please answer y or n.")


def parse_code(raw):
    """Lounge codes and suite numbers: 1-10 letters or digits."""
    if not raw.isalnum() or len(raw) > 10:
        raise ValueError("Use 1-10 letters or digits, no spaces or symbols.")
    return raw.upper()


def menu_validator(options):
    """Accepts a menu number, or the option's name typed out (e.g. 'aisle')."""
    def validator(raw):
        if raw in options:
            return options[raw]
        for value in options.values():
            if isinstance(value, str) and value.lower() == raw.lower():
                return value
        raise ValueError(f"Choose one of: {', '.join(options)}.")
    return validator


SEATS = {"1": "Window", "2": "Aisle", "3": "Middle"}
parse_seat = menu_validator(SEATS)


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

# Test for Part 3: type WRONG answers first to see the errors
    print("\n--- Part 3: input validation ---")
    name = ask("Full name", parse_text)
    origin = ask("Departing from", parse_text)
    destination = ask("Destination", different_from(origin))
    travel_date = ask("Travel date (YYYY-MM-DD)", parse_date)
    seat = ask("Seat [1] Window [2] Aisle [3] Middle", parse_seat)
    code = ask("Lounge pass code", parse_code)
    chauffeur = ask("Chauffeur service? (y/n)", parse_yes_no)

    print("\nAll inputs accepted:")
    print(f"  {name}, {origin} -> {destination}, {travel_date}, "
          f"seat {seat}, code {code}, chauffeur {chauffeur}")
