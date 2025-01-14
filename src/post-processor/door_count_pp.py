class DoorCountPostProcessor:
    def convert_to_int(self, car):
        seat_count = car.get('seatCount', '')
        if seat_count:
            numeric_seat_count = ''.join(filter(str.isdigit, seat_count))
            if numeric_seat_count:
                return int(numeric_seat_count) if numeric_seat_count else None
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['seatCount'] = self.convert_to_int(car)
        return processed_car