from django.test import TestCase
from .models import Sentence, Correct_Answer
from ._func import to_processed_of_text, processed_sentence_and_save, processed_sentence_without_save, symbol_field

class YourFunctionsTestCase(TestCase):
    
    def setUp(self):
        # Створюємо тестовий об'єкт Sentence
        self.sentence = Sentence.objects.create(
            sentence="This is a test sentence.",
            processed_sentence="",
            user_sentence=None,
            fields=0,
            answers=0
        )

    def test_processed_sentence_and_save(self):
        text = "This is a (correct) sentence."
        result = processed_sentence_and_save(text, self.sentence)
        
        # Перевіряємо, що оброблений текст не містить правильної відповіді
        self.assertNotIn("(correct)", result)
        self.assertIn(symbol_field, result)

        # Перевіряємо, що правильна відповідь збережена в базі даних
        correct_answers = Correct_Answer.objects.filter(text=self.sentence)
        self.assertEqual(correct_answers.count(), 1)
        self.assertEqual(correct_answers.first().phrase, "correct")

    def test_processed_sentence_without_save(self):
        text = "This is a (correct) sentence."
        result = processed_sentence_without_save(text)
        
        # Перевіряємо, що правильна відповідь була видалена
        self.assertNotIn("(correct)", result)
        self.assertIn(symbol_field, result)

    def test_to_processed_of_text(self):
        text = "This is a (correct) sentence with .... a field."
        result = to_processed_of_text(text, self.sentence)

        # Перевірка, що символи поля правильно замінені
        self.assertIn("<input type='text'", result.processed_sentence)
        
        # Перевірка, що кількість полів правильна
        self.assertEqual(result.fields, 1)

        # Перевірка, що правильна відповідь збережена
        correct_answers = Correct_Answer.objects.filter(text=self.sentence)
        self.assertEqual(correct_answers.count(), 1)
        self.assertEqual(correct_answers.first().phrase, "correct")

    def tearDown(self):
        # Чистимо базу даних після тестів
        Sentence.objects.all().delete()
        Correct_Answer.objects.all().delete()
