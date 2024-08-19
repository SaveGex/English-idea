from english.models import Answer_Correct_Model ,Answer_Wrong_Model, Task_Model



def formating(text: str, task_model: Task_Model) -> str:
    if not task_model.pk:  # Перевірка, чи модель не збережена
        raise ValueError("Task model must be saved before creating Answer_Model.")
    symbol_wrong_word_start = '_'
    symbol_wrong_word_end = '_'
    symbol_correct_word_start = '\\'
    symbol_correct_word_end = '\\'
    text = list(text.split())
    index = 0
    wrong_index_start = 0
    return_ticket = False
    input_index_counter = 1
    list_class = []
    #wrong cycle
    for word in text:
        if return_ticket:
            break
        index += 1
        if word.startswith(symbol_wrong_word_start):
            wrong_index_start = index
            #якщо виділено лише одне слово
            if word.startswith(symbol_wrong_word_start) and word.endswith(symbol_wrong_word_end) and len(word)>1:
                wrong = Answer_Wrong_Model(task = task_model, will_showed = text[index-1], position_wrong = wrong_index_start)
                wrong.save()
                # list_class.append(Answer_Wrong_Model(task_model, text[index-1], wrong_index_start))
                text = deformating(text, index-1, f"<input type='text' class='form-control' name='wrong_word{input_index_counter}' placeholder=\"{ text[index-1].strip('_ ') }\"" + f" size=\"{ len(text[index-1]) }\">")
                input_index_counter += 1
            #якщо лише один ключовий символ
            elif count_func(text, symbol_wrong_word_start) < 2:
                return_ticket = True
            else:
                break_cycle = break_cycle2 = False
                wrong_list = ''
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
                    if word.endswith(symbol_wrong_word_end) or break_cycle and break_cycle2:
                        wrong_index_start -= 1
                        text = delete_keysymbolS(text, wrong_index_start, symbol_wrong_word_start)
                        text = deformating(text, wrong_index_start, f"<input type='text' class='form-control' name='wrong_word' placeholder=\"{ wrong_list.strip(' _') }\"" + " size=\"{{ wrong_list|length }}\">")
                        wrong = Answer_Wrong_Model(task = task_model, will_showed = text[index-1], position_wrong = wrong_index_start)
                        wrong.save()
                        # list_class.append(Answer_Wrong_Model(task_model, wrong_list, wrong_index_start))
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
                print(correct_word_list)
                # list_class.append(Answer_Correct_Model(text, correct_word_list, correct_index_word))
                cor = Answer_Correct_Model(task = task_model, correct_word = correct_word_list, position_correct = correct_index_word)
                cor.save()
            #якщо лише один ключовий символ
            elif count_func(text, symbol_correct_word_start) < 2:
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
                        cor = Answer_Correct_Model(task = task_model, correct_word = correct_word_list, position_correct = correct_index_word)
                        cor.save()
                        # list_class.append(Answer_Correct_Model(text, correct_word_list, correct_index_word))
                        break
    # correct_index_word = correct_index_word + (wrong_index_start - correct_index_word)
    # дізнатись довжину неправильного слова і додати до правильного. Це якщо спочатку додати до тексту спочатку неправильне а потім правильне
    # # # text = ' '.join(text)
    # # # return list_class
    # correct_index_word = correct_index_word + (wrong_index_start - correct_index_word)
    # дізнатись довжину неправильного слова і додати до правильного. Це якщо спочатку додати до тексту спочатку неправильне а потім правильне
    # text = deformating(text, wrong_index_start, f"<input type='text' name='wrong_word' placeholder=\"{ wrong_list }\" size=\"{ len(wrong_list) }\">")
    # text = ' '.join(text)
    # answer_model = Answer_Model(task=task_model, will_showed=wrong_list, correct_word=correct_word_list, position_wrong=wrong_index_start, position_correct=correct_index_word)
    # answer_model.save()

    return text



def deformating(text: str, index: int, word_list: str) -> str:
    text.insert(index, word_list)
    return text


def delete_keysymbolS(text: str, index_for_change: int, symbol: str) -> str:
    myself_index = 0
    for index in range(len(text)-1):
        myself_index+=1
        if text[myself_index].startswith(symbol):
            text.pop(myself_index)
            myself_index-=1
        elif text[myself_index].strip(' ').endswith(symbol):
            text[index_for_change] = "BONK"
    return text



def count_func(text: str, symbol: str) -> int:
    count = 0
    for word in text:
        for sym in word:
            if sym == symbol:
                count+=1 
    return count