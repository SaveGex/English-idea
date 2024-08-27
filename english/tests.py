from django.test import TestCase
from .models import Sentence, Correct_Answer
from ._func import (
    to_processed_of_text, 
    processed_sentence_and_save, 
    processed_sentence_without_save, 
    symbol_field, 
    symbol_word_end, 
    symbol_word_start, 
    global_list_correct_model
)

class YourFunctionsTestCase(TestCase):
    
    def setUp(self):
        # Створюємо тестовий об'єкт Sentence
        self.model_sentence = Sentence.objects.create(
            correct_sentence = [],
            processed_sentence="",
            user_sentence="it'....s(my name) word which....(/bonk) (\\inner)....",
            comment = None,
            fields=0,
            answers=0
        )

    def test_processed_sentence_and_save(self):
        text = "This is a (correct) sentence."
        result = processed_sentence_and_save(text, self.model_sentence)
        
        # Перевіряємо, що правильна відповідь була видалена
        self.assertNotIn("(correct)", result)

        # Перевіряємо, що об'єкти Correct_Answer збережені правильно
        self.assertEqual(len(global_list_correct_model), 1, "Повинна бути одна правильна відповідь.")
        self.assertEqual(global_list_correct_model[0].phrase, "correct", "Неправильно збережена фраза.")

        # Перевіряємо, що екземпляр Sentence зберігся правильно
        saved_sentence = Sentence.objects.first()
        self.assertEqual(saved_sentence.user_sentence, "it'....s(my name) word which....(/bonk) (\\inner)....")


    def test_processed_sentence_without_save(self):
        text = "This is a (correct) sentence."
        result = processed_sentence_without_save(text)
        
        # Перевіряємо, що правильна відповідь була видалена
        self.assertNotIn("(correct)", result)

        # Перевіряємо, що фраза "(correct)" видалена з тексту
        self.assertIn(symbol_field, result)

    def test_to_processed_of_text(self):
        text = "This is a (correct) sentence with .... a field."
        result = to_processed_of_text(text, self.model_sentence)

        # Перевірка, що символи поля правильно замінені
        self.assertIn("<input type='text'", result.processed_sentence)
        
        # Перевірка, що кількість полів правильна
        self.assertEqual(result.fields, 1)

        # Перевірка, що правильна відповідь збережена
        correct_answers = Correct_Answer.objects.filter(key=self.model_sentence)
        self.assertEqual(correct_answers.count(), 1)
        self.assertEqual(correct_answers.first().phrase, "correct")

    def test_indexing_correctness(self):
        text = f"This is a {symbol_field} test sentence with {symbol_field} symbols."
        result = to_processed_of_text(text, self.model_sentence)
        
        # Перевіряємо, що індекси слів з символом поля правильно зберігаються
        expected_indexes = [3, 7]  # Позиції слів з `symbol_field`
        actual_indexes = [index for index, word in enumerate(result.processed_sentence.split()) if word.startswith('<input')]
        
        self.assertEqual(expected_indexes, actual_indexes, "Індекси полів обчислені некоректно.")
    
    def test_text_processing(self):
        text = f"This is a {symbol_field} test sentence with {symbol_field} symbols."
        result = to_processed_of_text(text, self.model_sentence)
        
        # Перевірка, що текст обробляється коректно
        self.assertIn('<input', result.processed_sentence, "Поле введення не додано до обробленого тексту.")
        self.assertEqual(result.fields, 2, "Кількість полів не відповідає очікуваній.")
    
    def test_correct_answer_mapping(self):
        # Приклад тексту з правильними відповідями
        text = f"This is a {symbol_word_start}correct{symbol_word_end} test sentence with {symbol_word_start}another{symbol_word_end} correct answer."

        # Виклик функції для обробки тексту та створення моделі Sentence
        processed_sentence = to_processed_of_text(text, self.model_sentence)
        
        # Перевірка правильних відповідей до збереження в базі даних
        for i, correct_answer in enumerate(global_list_correct_model):
            self.assertEqual(correct_answer.index, i, "Індекс правильного слова в списку обчислено некоректно.")
            self.assertEqual(correct_answer.phrase, ["correct", "another"][i], "Фраза правильного слова збережена некоректно.")

        # Тепер збережемо всі об'єкти в базі даних
        for correct_answer in global_list_correct_model:
            correct_answer.save()

        # Перевірка збережених значень у базі даних
        correct_answer_in_db = Correct_Answer.objects.get(key=self.model_sentence, phrase="correct")
        self.assertEqual(correct_answer_in_db.index, 0, "Індекс правильного слова 'correct' збережено некоректно.")

        correct_answer_in_db = Correct_Answer.objects.get(key=self.model_sentence, phrase="another")
        self.assertEqual(correct_answer_in_db.index, 1, "Індекс правильного слова 'another' збережено некоректно.")

        # Перевірка кінцевого стану моделі Sentence
        self.assertEqual(processed_sentence.fields, 2, "Кількість полів введення збережена некоректно.")
        self.assertEqual(processed_sentence.answers, 2, "Кількість правильних відповідей збережена некоректно.")


    def tearDown(self):
        # Чистимо базу даних після тестів
        Sentence.objects.all().delete()
        Correct_Answer.objects.all().delete()
