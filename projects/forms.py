from django import forms

from .models import ProjectImage, ProjectModel


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ["title", "description", "github_url", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


ProjectImageFormSet = forms.inlineformset_factory(
    ProjectModel,
    ProjectImage,
    fields=["image", "order"],
    extra=3,
    can_delete=True,
)
