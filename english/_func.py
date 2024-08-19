from english.models import Answer_Model, Task_Model



def formating(text: str, task_model: Task_Model) -> str:
    if not task_model.pk:  # Перевірка, чи модель не збережена
        raise ValueError("Task model must be saved before creating Answer_Model.")
    symbol_wrong_word_start = '_'
    symbol_wrong_word_end = '_'
    symbol_correct_word_start = '\\'
    symbol_correct_word_end = '\\'
    text = list(text.split())
    wrong_list = ''
    index = 0
    wrong_index_start = 0
    return_ticket = False
    #wrong cycle
    for word in text:
        if return_ticket:
            break
        index += 1
        if word.startswith(symbol_wrong_word_start):
            wrong_index_start = index
            #якщо виділено лише одне слово
            if word.startswith(symbol_wrong_word_start) and word.endswith(symbol_wrong_word_end) and len(word)>1:
                wrong_list += word.strip(symbol_wrong_word_start + ' ')
                text.pop(index-1)
            #якщо лише один ключовий символ
            elif text.count(symbol_wrong_word_start) < 2:
                print(text.count(symbol_wrong_word_start))
                return_ticket = True
            else:
                break_cycle = break_cycle2 = False
                while True:
                    if text[index-1].find(symbol_wrong_word_end) != -1:
                        #видаляю непотрібні символи
                        result = text[index-1].strip(symbol_wrong_word_end + ' ')
                        word = str(result)
                        
                        if not break_cycle:
                            break_cycle = True
                        else:
                            break_cycle2 = True
                    else:
                        word = text[index-1]
                    if word:
                        wrong_list += word + ' '
                    text.pop(index-1)
                    if word.endswith(symbol_wrong_word_end) or break_cycle and break_cycle2:
                        break
        
    correct_index_word = 0
    correct_word_list = ''
    index = 0
    #оновлюємо
    return_ticket = False

    #correct cycle
    for word in text:
        index += 1
        if word.startswith(symbol_correct_word_start):
            correct_index_word = index + 1
            #якщо виділено лише одне слово
            if word.startswith(symbol_correct_word_start) and word.endswith(symbol_correct_word_end) and len(word)>1:
                correct_word_list += word.strip(symbol_correct_word_start + ' ')
                text.pop(index-1)
            #якщо лише один ключовий символ
            elif text.count(symbol_wrong_word_start) < 2:
                return_ticket = True
            else:
                break_cycle = break_cycle2 = False
                while True:
                    if text[index-1].find(symbol_correct_word_start) != -1:
                        #видаляю непотрібні символи
                        result = text[index-1].strip(symbol_correct_word_start+' ')
                        word = str(result)
                        
                        if not break_cycle:
                            break_cycle = True
                        else:
                            break_cycle2 = True
                    else:
                        word = text[index-1]
                    if word:
                        correct_word_list += word + ' '
                    text.pop(index-1)
                    if word.endswith(symbol_correct_word_end) or break_cycle and break_cycle2:
                        break
    
    text = ' '.join(text)
    answer_model = Answer_Model(task=task_model, will_showed=wrong_list, correct_word=correct_word_list, position_wrong=wrong_index_start, position_correct=correct_index_word)
    answer_model.save()

    return text
def deformating(text: str, index: int, word_list: str) -> str:
    text.insert(index, index)
    return text