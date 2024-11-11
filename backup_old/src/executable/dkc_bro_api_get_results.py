import requests
import os
import json
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)


class DkcApi:
    __url = "http://www.dkc-bro.nl/api/document/demo-dry"
    __request_uuid = "a7f7ac8d4e2e437c877bb7b8d7cc549c"

    def __init__(self) -> None:
        self.list_files = self.get_files()

    def get_files(self) -> list[tuple]:
        input_folder = os.path.join(os.path.dirname(__file__), "input")
        list_files = [
            (os.path.join(input_folder, file), file)
            for file in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, file))
        ]
        return list_files

    @classmethod
    def document_payload(cls, file_path: str, file_name: str) -> bytes:
        byte_file = open(file_path, "rb").read()
        boundary = b"--" + cls.__request_uuid.encode()
        body_boundary = f"""Content-Disposition: form-data; name="documents"; filename={file_name}\r\n"""
        payload = b"\r\n".join(
            [
                boundary,
                body_boundary.encode("utf-8"),
                byte_file,
                boundary + b"--\r\n",
            ]
        )
        return payload

    @classmethod
    def send_request(cls, file_path: str, file_name: str):
        payload = cls.document_payload(file_path, file_name)
        headers = {"Content-Type": f"multipart/form-data; boundary={cls.__request_uuid}"}
        return requests.post(url=cls.__url, data=payload, headers=headers)

    @classmethod
    def get_json(cls, file_path: str, file_name: str):
        return cls.send_request(file_path, file_name)

    @staticmethod
    def export_json(findings: dict, file_name: str) -> None:
        output_folder = os.path.join(os.path.dirname(__file__), "output")
        file_name = file_name[:-4] + ".json"
        with open(f"{os.path.join(output_folder, file_name)}", "w") as output_file:
            json.dump(findings, output_file, indent=4)

    def loop_through_files(self) -> None:
        for file in self.list_files:
            logging.info(f"File: {file[1]} is being validated")
            findings_json = self.get_json(file_path=file[0], file_name=file[1])
            if findings_json.status_code == 200:
                self.export_json(findings_json.json(), file[1])
                logging.info(f"Validation completed and exported to output folder!")
            else:
                logging.warning(
                    f"Something went wrong, statuscode of HTML request is {findings_json.status_code}"
                )


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
    print(
        "Welcome to the DKC-BRO Expert Services! \nThis service analyzes the xml files using dkc-bro.nl located in the input folder "
        "and exports the results in the output folder as a json format."
    )
    DkcApi().loop_through_files()
