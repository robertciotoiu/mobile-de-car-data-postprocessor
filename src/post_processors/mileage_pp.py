class MileagePostProcessor:
    def convert_to_float(self, car):
        mileage = car.get('mileage', '')
        if mileage:
            numeric_mileage = ''.join(filter(str.isdigit, mileage.replace(",", "")))
            if numeric_mileage:
                return float(numeric_mileage) if numeric_mileage else None
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['mileage'] = self.convert_to_float(car)
        return processed_car