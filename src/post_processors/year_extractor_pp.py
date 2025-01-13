from datetime import datetime

class YearExtractorPostProcessor:
    def process(self, car):
        first_register = car.get('firstRegister', '')
        if first_register:
            try:
                year = datetime.strptime(first_register, '%m/%Y').year
                car['year'] = year
            except ValueError:
                car['year'] = None
        else:
            car['year'] = None
        return car