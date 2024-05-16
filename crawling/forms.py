from django import forms
from crawling.models import Crawling, CrawlingSubject

class CrawlingForm(forms.ModelForm):

    class Meta:

        model = Crawling
        fields = '__all__'

class CrawlingSubjectForm(forms.ModelForm):

    class Meta:

        model = CrawlingSubject
        fields = '__all__'



