import requests
import os
import json
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

class DkcApi:
    __url = "http://www.dkc-bro.nl/api/rule"

    @classmethod
    def send_request(cls):
        return requests.get(url=cls.__url)

    @classmethod
    def get_json(cls):
        return cls.send_request()
    
    @staticmethod
    def export_json(findings: dict) -> None:
        output_folder = os.path.join(os.path.dirname(__file__), "output")
        file_name = datetime.now().strftime('%Y-%m-%d') + "_rules.json"
        with open(f"{os.path.join(output_folder, file_name)}", "w") as output_file:
            json.dump(findings, output_file, indent=4)

    @property
    def get_rules(self) -> None:
        findings_json = self.get_json()
        if findings_json.status_code == 200:
            self.export_json(findings_json.json())
            logging.info(f"Rules are exported to output folder!")
        else:
            logging.warning(f"Something went wrong, statuscode of HTML request is {findings_json.status_code}")


if __name__ == "__main__":
    logo = """
    ######   #    #   #####          ######   ######   ####### 
    #     #  #   #   #     #         #     #  #     #  #     # 
    #     #  #  #    #               #     #  #     #  #     # 
    #     #  ###     #        #####  ######   ######   #     # 
    #     #  #  #    #               #     #  #   #    #     # 
    #     #  #   #   #     #         #     #  #    #   #     # 
    ######   #    #   #####          ######   #     #  ####### 
                                                            
    """
    print(logo)
    print("Welcome to the DKC-BRO Expert Services! \nThis service retrieves all active rules "
          "from dkc-bro.nl and exports these in the output folder as a json format.")
    DkcApi().get_rules
