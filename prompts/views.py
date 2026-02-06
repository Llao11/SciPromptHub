from django.shortcuts import render, redirect
from .models import Tag, Prompt
from .forms import PromptForm
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


def add_prompt(request):
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.save()

            tags_str = form.cleaned_data.get("tags_input", "")
            if tags_str:
                tag_names = [
                    name.strip() for name in tags_str.split(",") if name.strip()
                ]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    prompt.tags.add(tag)
            return redirect("list_prompts")
    else:
        form = PromptForm()
    return render(
        request,
        "prompts/add_prompt.html",
        {
            "form": form,
            "all_tags": Tag.objects.all(),
        },
    )


def list_prompts(request):
    query = request.GET.get("q")
    tag_filter = request.GET.get("tag")
    prompts = Prompt.objects.all().order_by("-created_at")
    if query:
        # filter by text or description
        prompts = prompts.filter(
            Q(text__icontains=query) | Q(description__icontains=query)
        )
    if tag_filter:
        prompts = prompts.filter(tags__name=tag_filter)
        # pagination
    paginator = Paginator(prompts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "prompts/list_prompts.html",
        {
            "prompts": page_obj,
            "search_query": query,
            "tag_filter": tag_filter,
            "page_obj": page_obj,
            "all_tags": Tag.objects.all(),
        },
    )


def prompt_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    return render(request, "prompts/prompt_detail.html", {"prompt": prompt})


def delete_prompt(request, pk):
    if request.method == "POST":
        prompt = get_object_or_404(Prompt, pk=pk)
        prompt.delete()
    return redirect("list_prompts")


def prompt_list_api(request):
    prompts = Prompt.objects.all().order_by("-created_at")
    data = []
    for prompt in prompts:
        data.append(
            {
                "id": prompt.id,
                "name": prompt.name,
                "description": prompt.description or "",
                "tags": [tag.name for tag in prompt.tags.all()],
            }
        )
    return JsonResponse(data, safe=False)


# class PromptViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Prompt.objects.all()
#     serializer_class = PromptSerializer
