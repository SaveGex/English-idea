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

class Index_View(generic.TemplateView):
    template_name = "English/common.html"
    paginate_by = 6
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        paginator = Paginator(models.Task_Model.objects.order_by("-publish_date"), per_page=3)
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
            'body_instruction': _(f"<span class='text-success blockquote'<br>In field <span class='{mark_color}'>'Name of task'</span> you have to write name of task. <br/>In field <span class='{mark_color}'>'Comment'</span> you can write description of task. <br/>In field <span class='{mark_color}'>'Sentence'</span> you have to write sentence, and words which you want make field for answer mark that <span class='{mark_color}'><span class='text-danger'>_</span>your word<span class='text-danger'>_</span></span> and in form it will showed as field for input. </span>"),
        })
        return context
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Зберігаємо об'єкт форми та виконуємо перенаправлення
        messages.success(self.request, "Post created successfully")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(form=form)
        form_data = form.data

        name = comment = sentence = ''

        if not form_data.get("name"):
            name = "Name cannot be empty"
        if not form_data.get("comment"):
            comment = "Comment cannot be empty"
        if not form_data.get("sentence"):
            sentence = "Sentence cannot be empty"

        context.update({
            "form_data": form_data,
            "name_error": name,
            "comment_error": comment,
            "sentence_error": sentence,
        })
        
        return self.render_to_response(context)
