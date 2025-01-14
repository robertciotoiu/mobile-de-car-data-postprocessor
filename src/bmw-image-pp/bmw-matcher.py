import json

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.readlines()

def parse_unique_bmw_model_year(data):
    models = []
    for line in data:
        parts = line.strip().split()
        if len(parts) == 3:
            model, year = f"{parts[0]} {parts[1]}", parts[2]
            models.append((model, year))
    return models

def parse_bmw_car_models_codes(data):
    model_codes = {}
    for line in data:
        parts = line.strip().split(' : ')
        if len(parts) == 3:
            model, years, code = parts
            model_codes[code] = (model, years)
    return model_codes

def year_in_interval(year, interval):
    if year == "None":
        return False
    start, end = interval.split('–')
    end = "2025" if end == "present" else end
    return int(start) <= int(year) <= int(end)

def match_models(mobile_models, ground_truth_model_codes):
    matches = {}
    for model, year in mobile_models:
        for gt_model_code, (gt_model, years) in ground_truth_model_codes.items():
            # if model contains Other, skip
            if 'Other' in model:
                continue
            if is_model_match(gt_model, model, year, years):
                matches[model + ' ' + year] = gt_model_code
                break
    return matches

# mobile mode: bmw 114 2013 . gt_model: 
def is_model_match(gt_model, mobile_model, year, years):
    is_model_match = False
    is_year_match = year_in_interval(year, years)
    if not is_year_match:
        return False
    
    trimmed_model = mobile_model.replace('BMW', '').strip()
    if trimmed_model.startswith('M'):
        extracted_model = 'M' + ''.join(filter(str.isdigit, trimmed_model.split('M')[1]))
    elif trimmed_model.startswith('Z'):
        extracted_model = 'Z' + ''.join(filter(str.isdigit, trimmed_model.split('Z')[1]))
    elif trimmed_model.startswith('iX'):
        extracted_model = 'iX' + ''.join(filter(str.isdigit, trimmed_model.split('iX')[1]))
    elif trimmed_model.startswith('XM'):
        extracted_model = 'XM' + ''.join(filter(str.isdigit, trimmed_model.split('XM')[1]))
    elif trimmed_model.startswith('X'):
        extracted_model = 'X' + ''.join(filter(str.isdigit, trimmed_model.split('X')[1]))
    elif trimmed_model.startswith('i'):
        extracted_model = 'i' + ''.join(filter(str.isdigit, trimmed_model.split('i')[1]))
    else:
        extracted_model = ''.join(filter(str.isdigit, trimmed_model))[:1]
    if gt_model.startswith(extracted_model):
        is_model_match = True
    
    return is_model_match


def save_matches(matches, filepath):
    with open(filepath, 'w') as file:
        json.dump(matches, file)

def main():
    unique_bmw_model_year_data = read_file('src/bmw-image-pp/unique_bmw_model_year.txt')
    bmw_car_models_codes_data = read_file('src/bmw-image-pp/bmw-car-models-codes.txt')

    unique_models = parse_unique_bmw_model_year(unique_bmw_model_year_data)
    model_codes = parse_bmw_car_models_codes(bmw_car_models_codes_data)

    matches = match_models(unique_models, model_codes)
    save_matches(matches, 'src/image-downloader/bmw-model-code-map.json')

if __name__ == "__main__":
    main()