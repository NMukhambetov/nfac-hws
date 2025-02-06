import sys

def load_banner_from_file(filepath):
    """Загружает ASCII-арт из файла в словарь."""
    banner_dict = {}
    try:
        with open(filepath, 'r') as file:
            lines = file.read().splitlines()

        while len(lines) % 8 != 0:
            lines.append(" " * 8)

        num_chars = len(lines) // 8
        for i in range(num_chars):
            char_art = lines[i:(i+1)*8]
            char = chr(i)
            banner_dict[char] = char_art

        return banner_dict
    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден.")
        sys.exit(1)


def print_word_in_banner(word, banner_dict):
    """Выводит слово с использованием ASCII-арт."""
    lines_to_print = ['' for _ in range(8)]

    for char in word:
        if char == '\n':
            print("\n".join(lines_to_print))
            print()
            lines_to_print = ['' for _ in range(8)]
        elif char in banner_dict:
            art = banner_dict[char]
            for i in range(8):
                lines_to_print[i] += art[i]
        else:
            print(f"Ошибка: символ '{char}' отсутствует в шаблоне.")
            sys.exit(1)

    if any(lines_to_print):
        print("\n".join(lines_to_print))

def main():
    if len(sys.argv) != 3:
        print("Использование: python3 main.py <строка> <путь_к_файлу>")
        sys.exit(1)

    input_string = sys.argv[1].replace("\\n", "\n")
    banner_file = sys.argv[2]
    banner_dict = load_banner_from_file(banner_file)
    print_word_in_banner(input_string, banner_dict)

if __name__ == "__main__":
    main()
