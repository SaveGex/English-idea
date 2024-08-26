from django.utils import timezone
from . import models

input_index_counter = 0

symbol_word_start = '('
symbol_word_end = ')'
symbol_field = '....'
 
back_slash = '\\'
forward_slash = '/'
count_of_dots_in_Sfield = len(symbol_field)-1

global_list_correct_model = []


def change_name_for_field() -> str:
    global input_index_counter
    input_index_counter += 1
    field = f"<input type='text' class='' name='wrong_word{input_index_counter}' placeholder=\"{'something...'}\" size=\"{len('something...')}\">"
    return field


def processed_sentence_and_save(copy_text: str, Sentence: models.Sentence) -> str:
    # for count indexes in
    index_indexs_words_list = 0
    count_fields = copy_text.count(symbol_field)
    index = 0 
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    start_index = 0
    saved_answers = 0
    concat_list = []
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True and start_index != num_sym:
            # me in future don't forget about .strip() done with correct answer
            # need will make to save indexes of fields of correct sentence in Correct_Answer
            speciment = models.Correct_Answer(index = 0, phrase = copy_text[start_index:num_sym].strip(), text = Sentence)
            global_list_correct_model.append(speciment)
            
            # - 1 because i done + 1 to skip first symbol 
            saved_answers += 1
            # + 1 beause not include last symbol
            start_index = num_sym + 1
            index_indexs_words_list += 1
            
            can_or_not = False if saved_answers == count_fields else True
            # can_or_not = False if saved_answers == len(indexs_words_list) else True
            '''if sudden wrote empty answer'''
        elif start_index == num_sym and ((sym == back_slash or sym == forward_slash) or sym == symbol_word_start) and find_start == True and can_or_not == True:
            start_index += 1
        elif sym == symbol_word_end and find_start == True:
            if start_index != num_sym:
                speciment = models.Correct_Answer(index = 0, phrase = copy_text[start_index:num_sym].strip(), text = Sentence)
                global_list_correct_model.append(speciment)
            else:
                start_index += 1
            find_start = False
            concat_list.append({"to": start_text-1,
                                "from": num_sym + 1
                                })
            pass
        elif sym == symbol_word_end and find_start == False:
            concat_list.append({"to": start_text-1,
                                "from": start_text
                                })
            pass
        
    for dict_obj in reversed(concat_list):
        copy_text = copy_text[:dict_obj["to"]] + copy_text[dict_obj["from"]:]
    return copy_text


def processed_sentence_without_save(copy_text: str) -> str:
    #cycle for remember index fields in original text and delete correct answers from processed text
    find_start = False
    # true mean can, false mean can't
    can_or_not = True
    start_text = 0
    concat_list = []
    for num_sym, sym in enumerate(copy_text):
        if sym == symbol_word_start and find_start == False and can_or_not == True:
            start_index = start_text = num_sym + 1
            find_start = True
        elif sym == symbol_word_end and find_start == True:
            find_start = False
            concat_list.append({"to": start_text-1,
                                "from": num_sym + 1
                                })
            pass
        elif sym == symbol_word_end and find_start == False:
            concat_list.append({"to": start_text-1,
                                "from": start_text
                                })
            pass
    for dict_obj in reversed(concat_list):
        copy_text = copy_text[:dict_obj["to"]] + copy_text[dict_obj["from"]:]
    return copy_text


def to_processed_of_text(text: str, Sentence: models.Sentence, index=0) -> str:
    text_HTML = processed_sentence_and_save(text, Sentence).split()
    correct_sentence = []
    index = 0
    indexs_words_list = []

    while index < len(text_HTML):
        word = text_HTML[index]
        if word.find(symbol_field) != -1:
            word = word.replace(symbol_field, f" {symbol_field} ").strip()
            text_HTML[index] = word
            text_HTML = " ".join(text_HTML).split()
            addition_index = index + 1 if word != symbol_field else index
            indexs_words_list.append(addition_index)
        index += 1

    correct_sentence = text_HTML.copy()

    for i, index in enumerate(indexs_words_list):
        if i < len(global_list_correct_model):
            field = change_name_for_field()
            text_HTML[index] = field

    processed_sentence_str = " ".join(text_HTML)

    # Створюємо новий екземпляр Sentence щоразу
    new_sentence = models.Sentence(
        name=f"UniqueName_{Sentence.name}_{timezone.now()}",
        comment=Sentence.comment,
        user_sentence=Sentence.user_sentence,
        correct_sentence=correct_sentence,
        processed_sentence=processed_sentence_str,
        fields=len(indexs_words_list),
        answers=len(global_list_correct_model)
    )
    new_sentence.save()

    return processed_sentence_str


