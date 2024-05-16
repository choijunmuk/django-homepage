from django.shortcuts import render, get_object_or_404, redirect

from .models import Question, Answer, Photo
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Q

def iindex(request):

    if request.user.is_authenticated:

        page = request.GET.get('page', '1')
        question_list = Question.objects.order_by('-create_date')

        kw = request.GET.get('kw', '')
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw) |  # 내용 검색
                Q(answer__content__icontains=kw) |  # 답변 내용 검색
                Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
                Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
            ).distinct()

        paginator = Paginator(question_list, 10)
        page_obj = paginator.get_page(page)

        context = {'question_list': page_obj}

        return render(request, 'main/question_list.html', context)

    else:

        return render(request, 'boarderr.html')

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'main/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":

        form = AnswerForm(request.POST)

        if form.is_valid():

            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()

            answer.question = question
            answer.save()

            return redirect('main:detail', question_id=question.id)

    else:

        return HttpResponseNotAllowed('Only POST is possible.')

    context = {'question': question, 'form': form}

    return render(request, 'main/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():

            question = form.save(commit=False)

            question.author = request.user

            question.create_date = timezone.now()

            question.save()

            for img in request.FILES.getlist('imgs'):

                photo = Photo()
                photo.post = question
                photo.image = img
                photo.save()

            return redirect('main:iindex')

    else:

        form = QuestionForm()

    context = {'form': form}

    return render(request, 'main/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:

        messages.error(request, '수정권한이 없음')

        return redirect('main:detail', question_id=question.id)

    if request.method == "POST":

        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():

            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()

            return redirect('main:detail', question_id=question.id)

    else:

        form = QuestionForm(instance=question)

    context = {'form': form}

    return render(request, 'main/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:

        messages.error(request, '삭제권한이 없음')

        return redirect('main:detail', question_id=question.id)

    question.delete()

    return redirect('main:iindex')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:

        messages.error(request, '수정권한이 없음')

        return redirect('main:detail', question_id=answer.question.id)

    if request.method == "POST":

        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():

            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()

            return redirect('main:detail', question_id=answer.question.id)

    else:

        form = AnswerForm(instance=answer)

    context = {'answer': answer, 'form': form}

    return render(request, 'main/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:

        messages.error(request, '삭제권한이 없음')

    else:

        answer.delete()

    return redirect('main:detail', question_id=answer.question.id)

# Create your views here.
