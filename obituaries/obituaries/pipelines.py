import json
import os


class ObituariesPipeline:
    def __init__(self):
        self.spider_data = {}

    def open_spider(self, spider):
        # Create an empty list for each spider to store its items
        self.spider_data[spider.name] = []

    def process_item(self, item, spider):
        # Append items to the spider-specific list
        self.spider_data[spider.name].append(item)
        return item

    def close_spider(self, spider):
        # Save each spider's data into a separate JSON file
        file_name = f"{spider.name}_data.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self.spider_data[spider.name], f, ensure_ascii=False, indent=4)

        # After all spiders have run, combine data into a single file
        self.combine_files()

    def combine_files(self):
        # Check if combined file already exists and remove it
        combined_file = "combined_obituaries.json"
        if os.path.exists(combined_file):
            os.remove(combined_file)

        # Combine all individual spider JSON files
        combined_data = []
        for file_name in os.listdir():
            if file_name.endswith("_data.json"):
                with open(file_name, 'r', encoding='utf-8') as f:
                    combined_data.extend(json.load(f))

        # Save combined data
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=4)
