class MileagePostProcessor:
    def convert_to_long(self, car):
        mileage = car.get('mileage', '')
        if mileage:
            # Extract only numeric characters
            numeric_mileage = ''.join(filter(str.isdigit, mileage.replace(",", "")))
            if numeric_mileage:
                return int(numeric_mileage) if numeric_mileage else None
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['mileage'] = self.convert_to_long(car)
        return processed_car