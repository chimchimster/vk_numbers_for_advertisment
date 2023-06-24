from datetime import datetime


class GetStrOrKey(dict):
    def __getitem__(self, key):
        return super().__getitem__(key)

    def get(self, key) -> str:
        if self.__contains__(key):
            return self.__getitem__(key)
        return ''


def vk_date_of_birth_universalizer(date_of_birth: str) -> datetime | None:

    if not date_of_birth:
        return

    date_of_birth = date_of_birth.split('.')

    if len(date_of_birth) < 3:
        return

    def number_checker(number: str):
        if len(number) < 2:
            number = '0' + number
        return number

    universalized = []
    for date in date_of_birth:
        universalized.append(number_checker(date))

    return datetime.strptime('.'.join(universalized), "%d.%m.%Y")