from datetime import datetime


def vk_date_of_birth_universalizer(date_of_birth: str) -> datetime | None:

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