from django.test import TestCase
from .models import Sentence, Correct_Answer
from ._func import to_processed_of_text, processed_sentence_and_save, processed_sentence_without_save, symbol_field

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
        
        # Перевіряємо, що оброблений текст не містить правильної відповіді
        self.assertNotIn("(correct)", result)

        # Перевіряємо, що екземпляр моделі зберігся лише один раз
        sentence_count = Sentence.objects.count()
        self.assertEqual(sentence_count, 1)

        # Перевіряємо, що збережений екземпляр має правильне значення user_sentence
        saved_sentence = Sentence.objects.first()
        self.assertEqual(saved_sentence.user_sentence, "it'....s(my name) word which....(/bonk) (\\inner)....")


    def test_processed_sentence_without_save(self):
        text = "This is a (correct) sentence."
        result = processed_sentence_without_save(text)
        
        # Перевіряємо, що правильна відповідь була видалена
        self.assertNotIn("(correct)", result)
        # self.assertIn(symbol_field, result)

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
        text = f"This is a {symbol_field} test sentence with {symbol_field} symbols."
        correct_answer = Correct_Answer.objects.create(
            key=self.model_sentence, 
            phrase="test",
            index=0
        )
        global_list_correct_model = [correct_answer]
        
        result = to_processed_of_text(text, self.model_sentence)
        
        # Перевірка, що правильні відповіді зберігаються з коректними індексами
        correct_answer.refresh_from_db()
        self.assertEqual(correct_answer.index, 3, "Індекс правильного слова збережено некоректно.")

    def tearDown(self):
        # Чистимо базу даних після тестів
        Sentence.objects.all().delete()
        Correct_Answer.objects.all().delete()
