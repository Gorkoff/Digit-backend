import json
import glob


def merge_json_files(file_pattern, output_file):
    all_data = [] # Чтение и объединение данных из каждого файла

    for file_name in glob.glob(file_pattern):
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.extend(data)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(all_data, output_file, ensure_ascii=False, indent=4)


# Использование функции
merge_json_files('D:\\dataset\\*', 'dataset_tass.json')