import json

class Request:
    def __init__(self) -> None:
        self.__body = None
    
    def parse_body(self, body: dict):
        self.__body = json.loads(body)
        return self

    def has_fields(self, fields: list) -> bool:
        keys = self.__body.keys()
        asserted = 0

        for i in range(len(fields)):
            if fields[i] in keys:
                asserted += 1

        return asserted == len(fields)

    def get(self, key: str):
        return self.__body[key]

    def get_all(self):
        return self.__body