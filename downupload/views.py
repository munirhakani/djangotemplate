# from typing import Any
from django.views.generic.base import TemplateView
# from downupload.main import main


class AlertView(TemplateView):
    template_name = 'alert.html'
    extra_context = {'alert': 'This is an alert from AlertView.'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # main()
    
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     from application.models import Brand
    #     context_data['alert'] = ', '.join(list(Brand.objects.filter(active=1).order_by('isnotpopular', 'name').values_list('name', flat=True)))
    #     return context_data