from django.shortcuts import render
from django.urls import reverse_lazy # Import reverse_lazy for redirection after registration
from django.views.generic.detail import DetailView # Keep this specific import as per your request
from django.contrib.auth.forms import UserCreationForm # NEW: Import UserCreationForm for registration
from django.contrib.auth import login # Import your Book and Library models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required 
from .models import Book
from .models import Library
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse # NEW: Import reverse for named URL redirection



def book_list(request):
    """
    Function-based view to list all books.
    This view will render a simple text list of book titles and their authors.
    It passes a 'books' queryset to the template.
    """
    books = Book.objects.all() # Retrieve all Book objects from the database
    context = {
        'books': books # Pass the queryset as 'books' to the template
    }
    # Renders the 'list_books.html' template located in 'relationship_app/templates/relationship_app/'
    return render(request, 'relationship_app/list_books.html', context)



class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library,
    listing all books available in that library.
    Utilizes Django’s DetailView.
    """
    model = Library # Specifies that this view operates on the Library model
    template_name = 'relationship_app/library_detail.html' # Defines the template to be used for rendering
    context_object_name = 'library' # Sets the name of the context variable used in the template (e.g., {{ library.name }})

    # DetailView automatically fetches a single object based on the URL's primary key (pk) or slug.
    # The related books can then be accessed directly in the template using library.books.all()


# --- Registration View ---
def register(request):
    """
    Function-based view for user registration.
    Handles user creation using Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            # Uses reverse_lazy to ensure URL is resolved after app loading
            return redirect('relationship_app:login') # Use the namespaced URL as defined in urls.py
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Helper functions for role checks ---
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'ADMIN'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'LIBRARIAN'

def is_member(user):
    # All authenticated users are members by default, or specific check
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'MEMBER'


# --- NEW: Role-based views ---
@login_required # Ensures user is logged in
@user_passes_test(is_admin, login_url='/relationship/accounts/login/', redirect_field_name=None) # Redirect if not admin
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})


@login_required
@user_passes_test(is_librarian, login_url='/relationship/accounts/login/', redirect_field_name=None)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})


@login_required
@user_passes_test(is_member, login_url='/relationship/accounts/login/', redirect_field_name=None)
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})


# --- Dashboard Redirect View ---
@login_required
def dashboard_redirect(request):
    if hasattr(request.user, 'userprofile'):
        if request.user.userprofile.role == 'ADMIN':
            return redirect(reverse('relationship_app:admin_dashboard'))
        elif request.user.userprofile.role == 'LIBRARIAN':
            return redirect(reverse('relationship_app:librarian_dashboard'))
        elif request.user.userprofile.role == 'MEMBER':
            return redirect(reverse('relationship_app:member_dashboard'))
    # Fallback if no profile or unknown role (e.g., to book list or a generic home)
    return redirect(reverse('relationship_app:book_list'))


@login_required # Ensures user is logged in
@permission_required('relationship_app.can_add_book', login_url='/relationship/accounts/login/', raise_exception=True)
def add_book_view(request):
    """
    View for adding a new book. Only accessible to users with 'can_add_book' permission.
    """
    # In a real scenario, you'd handle form submission here
    return render(request, 'relationship_app/add_book.html', {'message': 'You have permission to add books.'})


@login_required
@permission_required('relationship_app.can_change_book', login_url='/relationship/accounts/login/', raise_exception=True)
def change_book_view(request, book_id):
    """
    View for editing an existing book. Only accessible to users with 'can_edit_book' permission.
    """
    # In a real scenario, you'd fetch the book and handle form submission
    return render(request, 'relationship_app/edit_book.html', {'message': f'You have permission to edit book ID: {book_id}.'})

@login_required
@permission_required('relationship_app.can_delete_book', login_url='/relationship/accounts/login/', raise_exception=True)
def delete_book_view(request, book_id):
    """
    View for deleting a book. Only accessible to users with 'can_delete_book' permission.
    """
    # In a real scenario, you'd delete the book
    return render(request, 'relationship_app/delete_book.html', {'message': f'You have permission to delete book ID: {book_id}.'})
# Create your views here.
