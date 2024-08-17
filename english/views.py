from typing import Any
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.forms import BaseModelForm

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

        paginator = Paginator(models.Model_Post.objects.order_by("-publish_date"), per_page=8, orphans=2)
        page = paginator.get_page(kwargs.get("page_number"))

        context['page'] = page
        
        return context
    

class Create_View(generic.CreateView):
    form_class = forms.Create
    template_name = 'English/create.html'
    success_url = reverse_lazy('English:common', kwargs = {"page_number": 1})

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
