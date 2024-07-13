from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


# def post_list(request):
#     post_list = Post.published.all()
#     # постраничная разбивка
#     paginator = Paginator(post_list, 3)  # кол-во объектов
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # если page_number не цлое число, то вернуть первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#         # если вызванная страница находится за пределами существующего диапазона,
#         # то вернуть последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'posts': posts})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'  # если необъявить, в шаблон будет передана переменная object_list
    # context_object_name будет передан в шаблон по имени page_obj
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} реккомендует вам прочитать {post.title}'
            message = f'Прочитай "{post.title}" по адресу {post_url}\n\nКомментарий от {cd["name"]}: {cd["comments"]}'
            send_mail(subject, message, 'same@mail.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
