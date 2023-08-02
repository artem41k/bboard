from django.shortcuts import render

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

class OtherView(TemplateView):
    def get_template_names(self):
        return [f"main/{self.kwargs['page']}.html"]