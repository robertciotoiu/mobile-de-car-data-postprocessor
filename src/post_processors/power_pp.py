import re

class PowerPostProcessor:
    def convert_to_hp(self, car):
        power = car.get('power', '')
        if power:
            # Try to extract the HP value from the string
            match_hp = re.search(r'\((\d+)\s*hp\)', power)
            if match_hp:
                return int(match_hp.group(1))
            
            # If HP value is not found, try to extract the kW value and convert it to HP
            match_kw = re.search(r'(\d+)\s*kW', power)
            if match_kw:
                kw_value = int(match_kw.group(1))
                return int(kw_value * 1.341)
        return None

    def process(self, car):
        processed_car = car.copy()
        processed_car['power'] = self.convert_to_hp(car)
        return processed_car