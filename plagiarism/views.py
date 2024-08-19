# # views.py
# from django.shortcuts import render, redirect
# from .models import Document, UserDocument, PlagiarismCheckHistory
# from .forms import UserDocumentForm
# import difflib
# from django.contrib.auth.decorators import login_required

# @login_required
# def check_plagiarism(request):
#     if request.method == 'POST':
#         form = UserDocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_document = form.save(commit=False)
#             user_document.user = request.user
#             user_document.save()

#             all_documents = Document.objects.all()
#             similar_docs = []

#             for doc in all_documents:
#                 s = difflib.SequenceMatcher(None, user_document.content, doc.content)
#                 similarity = s.ratio() * 100

#                 similar_phrases = []
#                 for block in s.get_matching_blocks():
#                     if block.size > 20:
#                         start = block.a
#                         end = block.a + block.size
#                         similar_phrases.append(user_document.content[start:end])

#                 similar_docs.append({
#                     'document': doc,
#                     'similarity': similarity,
#                     'similar_phrases': similar_phrases
#                 })

#                 PlagiarismCheckHistory.objects.create(
#                     user=request.user,
#                     user_document=user_document,
#                     similarity_score=similarity,
#                     matched_document=doc
#                 )

#             context = {
#                 'user_document': user_document,
#                 'similar_docs': similar_docs,
#             }
#             return render(request, 'plagiarism/plagiarism_result.html', context)
#     else:
#         form = UserDocumentForm()

#     return render(request, 'plagiarism/check_plagiarism.html', {'form': form})






from django.shortcuts import render, redirect
from .models import Document, UserDocument, PlagiarismCheckHistory
from .forms import UserDocumentForm
import difflib
from django.contrib.auth.decorators import login_required

# login logout 
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm

def index(request):
    return render(request, 'plagiarism/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'plagiarism/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'plagiarism/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def history(request):
    history = PlagiarismCheckHistory.objects.filter(user=request.user)
    return render(request, 'plagiarism/history.html', {'history': history})




@login_required
def check_plagiarism(request):
    if request.method == 'POST':
        form = UserDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            user_document = form.save(commit=False)
            user_document.user = request.user
            user_document.save()

            all_documents = Document.objects.all()
            similar_docs = []

            for doc in all_documents:
                s = difflib.SequenceMatcher(None, user_document.content, doc.content)
                similarity = s.ratio() * 100

                similar_phrases = []
                for block in s.get_matching_blocks():
                    if block.size > 20:
                        start = block.a
                        end = block.a + block.size
                        similar_phrases.append(user_document.content[start:end])

                similar_docs.append({
                    'document': doc,
                    'similarity': similarity,
                    'similar_phrases': similar_phrases
                })

                PlagiarismCheckHistory.objects.create(
                    user=request.user,
                    user_document=user_document,
                    similarity_score=similarity,
                    matched_document=doc
                )

            context = {
                'user_document': user_document,
                'similar_docs': similar_docs,
            }
            return render(request, 'plagiarism/plagiarism_result.html', context)
    else:
        form = UserDocumentForm()

    return render(request, 'plagiarism/check_plagiarism.html', {'form': form})
