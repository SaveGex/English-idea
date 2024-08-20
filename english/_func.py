from english.models import Answer_Correct_Model, Answer_Wrong_Model, Task_Model


def formating(text: str, task_model: Task_Model) -> str:
    if not task_model.pk:  # Перевірка, чи модель не збережена
        raise ValueError("Task model must be saved before creating Answer_Model.")

    # Символи для маркування неправильних і правильних слів
    symbol_wrong_word_start = '_'
    symbol_wrong_word_end = '_'
    symbol_correct_word_start = '\\'
    symbol_correct_word_end = '\\'

    text_list = text.split()  # Розбиваємо текст на слова
    index = 0
    input_index_counter = 1

    while index < len(text_list):
        word = text_list[index]

        # Обробка неправильних слів
        if word.startswith(symbol_wrong_word_start):
            wrong_list = []
            wrong_index_start = index + 1

            while index < len(text_list):
                wrong_word = text_list[index].strip(symbol_wrong_word_start + symbol_wrong_word_end + ' ')
                wrong_list.append(wrong_word)

                # Перевірка на кінець виділення
                if text_list[index].endswith(symbol_wrong_word_end):
                    wrong_list_str = ' '.join(wrong_list)
                    text_list[index] = f"<input type='text' class='' name='wrong_word{input_index_counter}' placeholder=\"{wrong_list_str}\" size=\"{len(wrong_list_str)}\">"
                    wrong = Answer_Wrong_Model(task=task_model, will_showed=wrong_list_str, position_wrong=wrong_index_start)
                    wrong.save()
                    input_index_counter += 1
                    break

                text_list.pop(index)  # Видаляємо проміжне слово, бо воно вже оброблене

            index -= len(wrong_list) - 1  # Коригування індексу після видалення

        # Обробка правильних слів
        elif word.startswith(symbol_correct_word_start):
            correct_list = []
            correct_index_start = index + 1

            while index < len(text_list):
                correct_word = text_list[index].strip(symbol_correct_word_start + symbol_correct_word_end + ' ')
                correct_list.append(correct_word)

                # Перевірка на кінець виділення
                if text_list[index].endswith(symbol_correct_word_end):
                    correct_list_str = ' '.join(correct_list)
                    text_list[index] = ''
                    # text_list[index] = correct_list_str
                    cor = Answer_Correct_Model(task=task_model, correct_word=correct_list_str, position_correct=correct_index_start)
                    cor.save()
                    break

                text_list.pop(index)  # Видаляємо проміжне слово, бо воно вже оброблене

            index -= len(correct_list) - 1  # Коригування індексу після видалення

        index += 1

    return ' '.join(text_list)


def deformating(text: str, index: int, word_list: str) -> str:
    text.insert(index, word_list)
    return text


def delete_keysymbolS(text: str, index_for_change: int, symbol: str) -> str:
    myself_index = 0
    for index in range(len(text) - 1):
        myself_index += 1
        if text[myself_index].startswith(symbol):
            text.pop(myself_index)
            myself_index -= 1
        elif text[myself_index].strip(' ').endswith(symbol):
            text[index_for_change] = "BONK"
    return text


def count_func(text: str, symbol: str) -> int:
    count = 0
    for word in text:
        for sym in word:
            if sym == symbol:
                count += 1
    return count
