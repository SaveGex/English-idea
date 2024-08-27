from typing import Any
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import BaseModelForm

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import render

from django.contrib import messages
from django.views import generic

from . import models, forms
from english._func import to_processed_of_text
class Index_View(generic.TemplateView):
    template_name = "English/common.html"
    paginate_by = 6
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        paginator = Paginator(models.Sentence.objects.order_by("-published_date"), per_page=3)
        page_number = kwargs.get("page_number")
        page = paginator.get_page(page_number)
        
        page_subsequent3 = page_subsequent2 = 0
        page_previously3 = page_previously2 = 0
        if(page_number-2 > 0):
            page_previously2 = page_number-2
            if(page_number-3 > 0):
                page_previously3 = page_number-3

        if(page_number+2 <= paginator.num_pages):
            page_subsequent2 = page_number+2
            if(page_number+3 <= paginator.num_pages):
                page_subsequent3 = page_number+3
                

        context.update({
                        'page': page,
                        'page_number': page_number,
                        'page_subsequent2': page_subsequent2,
                        'page_subsequent3': page_subsequent3,
                        'page_previously2': page_previously2,
                        'page_previously3': page_previously3,
                        })

        return context
    

class Create_View(generic.CreateView):
    form_class = forms.Create
    template_name = 'English/create.html'
    success_url = reverse_lazy('English:common', kwargs = {"page_number": 1})


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mark_color = 'text-warning'
        context.update({
            'head_instruction': _("<span class='blockquote'>How it works? </span>"),
            'body_instruction': _(f"<span class='text-success blockquote'<br>In field <span class='{mark_color}'>'Name of task'</span> you have to write name of task. <br/>In field <span class='{mark_color}'>'Comment'</span> you can write description of task. <br/>In field <span class='{mark_color}'>'Sentence'</span> you have to write sentence, and words which you want will make fields for answer mark that <span class='{mark_color}'><span class='text-danger'>_</span>your word<span class='text-danger'>_</span></span> and in form it will showed as field for input. </span>"),
        })
        return context
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Викликаємо збереження форми, яке зберігає Sentence_model в базі даних
        response = super().form_valid(form)

        # Отримуємо збережений екземпляр Sentence_model
        Sentence_model = form.instance

        print(f"User sentence received: {form.cleaned_data['user_sentence']}")

        # Обробляємо речення та зберігаємо Answer_Model
        user_sentence = form.cleaned_data["user_sentence"]

        # Збереження екземпляра, щоб бути впевненим, що він існує в базі даних
        Sentence_model.save()

        # Виконуємо обробку речення після збереження моделі
        ready_model = to_processed_of_text(user_sentence, Sentence_model)

        # Оновлюємо поля моделі, які залежать від результату обробки
        Sentence_model.correct_sentence = ready_model.correct_sentence
        Sentence_model.processed_sentence = ready_model.processed_sentence
        Sentence_model.fields = ready_model.fields
        Sentence_model.answers = ready_model.answers

        # Зберігаємо модель знову з оновленими полями
        Sentence_model.save()

        messages.success(self.request, "Post created successfully")
        return response


    def form_invalid(self, form: BaseModelForm, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(form=form)
        form_data = form.data

        name = sentence = ''

        if not form_data.get("name"):
            name = "Name cannot be empty"
        
        if not form_data.get("sentence"):
            sentence = "Sentence cannot be empty"

        context.update({
            "form_data": form_data,
            "name_error": name,
            "sentence_error": sentence,
        })
        
        return self.render_to_response(context)


class Execute_View(generic.UpdateView):
    form_class = forms.Execute_Form
    pass



class Delete_View(generic.DeleteView):
    model = models.Sentence
    success_url = reverse_lazy('English:common', kwargs = {"page_number": 1})
    template_name = 'english/common.html'

    
    def get_success_url(self) -> str:
        return self.success_url  # Повертає успішний URL
