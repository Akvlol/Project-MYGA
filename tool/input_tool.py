import json
from urllib.parse import urlencode
from urllib.request import urlopen

class InputTool:

    @staticmethod
    def valid_value(prompt, valid_values, prompt_error, continue_if_empty=True):
        while True:
            data = input(prompt).strip()
            if data == "":
                if continue_if_empty:
                    continue
                else:
                    return ""
            if data in valid_values:
                return data
            else:
                print(prompt_error)

    #Nếu người dùng nhập chuỗi rỗng thì trả về None, ngược lại trả về chuỗi đã nhập
    @staticmethod
    def empty_is_none(prompt):
        data = input(prompt).strip()
        if data != "":
            return data
        else:
            return None
    
    #Chỉ nhận integer hoặc chuỗi rỗng, nếu chuỗi rỗng trả về None, ngược lại trả về integer
    @staticmethod
    def int_or_none(prompt, prompt_error):
        while True:
            data = input(prompt).strip()
            if data == "":
                return None
            try:
                return int(data)
            except ValueError:
                print(prompt_error)

    #Chỉ nhận y/n hoặc yes/no, trả về True nếu là y/yes, False nếu là n/no
    @staticmethod
    def yes_or_no(prompt):
        while True:
            data = input(prompt + " [y/n]: ").strip().lower()
            if data in ["y", "n", "yes", "no"]:
                return data in ["y", "yes"]
            else:
                print("Please enter 'y' or 'n'")

    #Chỉ nhận integer trong khoảng min_value và max_value
    @staticmethod
    def valid_int(prompt, min_value, max_value):
        while True:
            try:
                value = int(input(f'{prompt} [{min_value}->{max_value}]: ').strip())
                if value < min_value or value > max_value:
                    print(f"Value must be between {min_value} and {max_value}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid integer.")

    #Check duplicate value
    @staticmethod
    def is_duplicate(value, existing_values):
        if value in existing_values:
            print(f"'{value}' already exists.")
            return True
        return False

    #get youtube title from id
    @staticmethod
    def get_youtube_title(id = None):
        if id is None:
            return None
        url = f"https://www.youtube.com/watch?v={id}"
        params = {
            "url": url,
            "format": "json"
        }
        endpoint = "https://www.youtube.com/oembed?" + urlencode(params)

        try:
            with urlopen(endpoint) as response:
                data = json.loads(response.read().decode("utf-8"))

            return data.get("title")

        except Exception:
            return None