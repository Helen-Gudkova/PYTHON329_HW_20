import json
from dataclasses import dataclass
from typing import List

@dataclass
class Palindrome:
    """
    Датакласс Palindrome
    """
    word: str
    meaning: str

    def __init__(self, word: str, meaning: str) -> None:
        """
        Конструктор датакласса Palindrome
        :param word: Строка, содержащая слово
        :param meaning: Строка, описывающая значение слова
        :return: None
        """
        self.word = word
        self.meaning = meaning

    def __bool__(self) -> bool:
        """
        Магический метод реализующий проверку,
        является ли `word` палиндромом
        :return: boolean value
        """
        return self.word == self.word[::-1]

    @classmethod
    def load_from_json(cls, json_path: str) -> List['Palindrome']:
        """
        Метод загрузки информации о словах палиндромах из JSON файла.
        :param json_path:JSON файл
        :return: List['Palindrome'] - список объектов
        """
        with open(json_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
            palindromes = []
            for item in data:
                if 'слово' in item:
                    palindrome = Palindrome(word=item['слово'], meaning=item.get('значение', ''))
                    palindromes.append(palindrome)
        return palindromes


def main():
    palindromes = Palindrome.load_from_json('palindromes.json')
    print(f"Список объектов из JSON файла:\n{palindromes}")
    palindrome_count = 0
    non_palindrome_count = 0

    for palindrome in palindromes:
        if palindrome:
            print(f"{palindrome.word} - это палиндром!")
            palindrome_count += 1
        else:
            print(f"{palindrome.word} - это не-палиндром!")
            non_palindrome_count += 1

    print(f"Количество палиндромов: {palindrome_count}")
    print(f"Количество не-палиндромов: {non_palindrome_count}")


if __name__ == "__main__":
    main()
