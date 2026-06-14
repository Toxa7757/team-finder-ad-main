from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'github_url']

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на домен github.com")
        return url
