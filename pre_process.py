import hashlib
import json
import os


def add_md5_to_entries(har_path):
    if har_path.endswith('_md5.har'):
        print(f"MD5 already added to entries: |{har_path}|")
        return har_path

    new_file_path = har_path.replace('.har', '_md5.har')
    if os.path.exists(new_file_path):
        print(f"MD5 already added to entries: |{har_path}|")
        return new_file_path

    with open(har_path, "r", encoding="utf-8-sig") as f:
        har = json.load(f)

    for entry in har['log']['entries']:
        entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        entry_hash = hashlib.md5(entry_str.encode()).hexdigest()
        entry['md5'] = entry_hash

    with open(new_file_path, 'w', encoding='utf-8') as f:
        json.dump(har, f, ensure_ascii=False, sort_keys=True, indent=2)

    print(f"MD5 added to entries."
          f"|{har_path}| --> |{new_file_path}|")

    return new_file_path


def add_md5_all():
    har_files_dir = os.listdir("./har_files")
    for har_file in har_files_dir:
        if har_file.endswith('.har'):
            old_file_path = f"./har_files/{har_file}"
            new_file_path = add_md5_to_entries(old_file_path)
            if new_file_path != old_file_path:
                os.rename(old_file_path, f"./har_files/filtered_no_md5/{har_file}")


if __name__ == '__main__':
    user_input = input("This script will add MD5 hash to each entry in all HAR files in ./har_files directory.\n"
                       "Press y to continue: ")
    if user_input.lower() == 'y':
        add_md5_all()
    pass
