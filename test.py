import csv
input_file_path = 'cleanedd_KOL_profile_status_count_more_than_200.csv'
with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        import ipdb; ipdb.set_trace()
        screen_names = [row['screen_name'] for row in reader]