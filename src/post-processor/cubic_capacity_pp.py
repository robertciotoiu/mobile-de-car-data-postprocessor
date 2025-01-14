class CubicCapacityPostProcessor:
    def convert_to_float(self, car):
        cubic_capacity = car.get('cubicCapacity', '')
        if cubic_capacity:
            numeric_capacity = ''.join(filter(str.isdigit, cubic_capacity.replace(",", "")))
            if numeric_capacity:
                return float(numeric_capacity) if numeric_capacity else None
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['cubicCapacity'] = self.convert_to_float(car)
        return processed_car