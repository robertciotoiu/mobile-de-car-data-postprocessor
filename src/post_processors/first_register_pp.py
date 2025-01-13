from datetime import datetime

class FirstRegisterPostProcessor:
    def convert_to_date(self, car):
        first_register = car.get('firstRegister', '')
        if first_register:
            try:
                return datetime.strptime(first_register, '%m/%Y')
            except ValueError:
                return None
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['firstRegister'] = self.convert_to_date(car)
        return processed_car