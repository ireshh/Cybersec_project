from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User, Note
# fix A02 -> cryptographic failures
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def register(request):
    if request.method == 'POST':
        user = request.POST['username']
        pswd = request.POST['password']
        # flaw A02 -> cryptographic failures: storing plaintext password directly in database
        User.objects.create(username=user, password=pswd)

        # fix -> hash password before storing
        # User.objects.create(username=user, password=make_password(pswd))

        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        user = request.POST['username']
        pswd = request.POST['password']
        
        # flaw A02 -> cryptographic failures:we compare plaintext passwords directly
        try:
            user_obj = User.objects.get(username=user, password=pswd)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        
        # fix -> retrieve user by username and verify password securely
        # try:
        #     user_obj = User.objects.get(username=user)
        #     if not check_password(pswd, user_obj.password):
        #         raise User.DoesNotExist
        # except User.DoesNotExist:
        #     return render(request, 'login.html', {'error': 'Invalid username or password'})
        

        request.session['user_id'] = user_obj.id
        return redirect('notes')
    return render(request, 'login.html')

def log_out(request):
    request.session.flush()
    return redirect('login')

def notes(request):
    id = request.session.get('user_id')
    if not id:
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        info = request.POST.get('content')
        user_obj = User.objects.get(id=id)
        Note.objects.create(owner=user_obj, title=title, content=info)
        return redirect('notes')

    notes = Note.objects.filter(owner_id=id)
    user_obj = User.objects.get(id=id)

    return render(request, 'notes.html', {'notes': notes, 'username': user_obj.username})

def find_note(request):
    id = request.session.get('user_id')
    if not id:
        return redirect('login')

    query = request.GET.get('q', '')
    notes = []

    if query:
        # flaw A03 -> injection: raw query allows SQL injection
        sql = f"select * from notes_note where title = '{query}'"
        notes = Note.objects.raw(sql)

        # fix -> use parameterized query
        # notes = Note.objects.raw("select * from notes_note where title = %s", [query])

    user_obj = User.objects.get(id=id)
    return render(request, 'notes.html', {'notes': notes, 'query': query, 'username': user_obj.username})

# flaw A01 -> broken access control: no check for the notes owner
def del_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.delete()

    return redirect('notes')

    # fix -> check if note belongs to user before deleting
    # note = get_object_or_404(Note, pk=note_id)
    # if note.owner_id != request.session.get('user_id'):
    #     return redirect('notes')
    # note.delete()
    # return redirect('notes')

# flaw CSRF -> no protection against CSRF (cross-site request forgery)
@csrf_exempt
def del_note_csrf(request, note_id):
    # we let both GET and POST requests delete notes, which is a MAJOR security risk.
    note = get_object_or_404(Note, pk=note_id)
    note.delete()

    return redirect('notes')

# fix -> Remove @csrf_exempt and have only POST requests
# def del_note_csrf(request, note_id):
#     if request.method == 'POST':
#         note = get_object_or_404(Note, pk=note_id)
#         if note.owner_id == request.session.get('user_id'):
#             note.delete()
#     return redirect('notes')