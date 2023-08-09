from .models import SubRubric


def rubrics_context_processor(request):
    context = {
        "rubrics": SubRubric.objects.all()
    }
    return context
