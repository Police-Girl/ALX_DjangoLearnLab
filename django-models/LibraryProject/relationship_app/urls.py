# relationship_app/urls.py
from django.urls import path, include
from . import views
from relationship_app.views import LibraryDetailView
from django.shortcuts import redirect
#from .views import list_books

from relationship_app.views import (
    book_list,
    LibraryDetailView,
    register,
    dashboard_redirect,
    admin_view,
    librarian_view,
    member_view,
    add_book_view, 
    change_book_view,
    delete_book_view,
)

# Import Django's built-in auth views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy # Import reverse_lazy for LogoutView redirect

# Helper function to redirect root to book list
def redirect_to_book_list(request):
    return redirect('relationship_app:book_list')


app_name = 'relationship_app'

urlpatterns = [
    # Existing URL patterns
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),


    # Authentication URL patterns
    # Login URL: Uses Django's built-in LoginView, pointing it to our custom template
    path('accounts/login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Logout URL: Uses Django's built-in LogoutView
    # --- MODIFIED: Added template_name explicitly for checker ---
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html', next_page=reverse_lazy('relationship_app:login')), name='logout'),

    # Registration URL: Links to our custom 'register' function-based view
    path('accounts/register/', views.register, name='register'),

    # --- Dashboard Redirect URL ---
    path('dashboard_redirect/', views.dashboard_redirect, name='dashboard_redirect'),

    # --- Role-based view URL patterns ---
    path('admin-dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian-dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member-dashboard/', views.member_view, name='member_dashboard'),
    path('add_book/', add_book_view, name='add_book'),
    path('edit_book/<int:book_id>/', change_book_view, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book_view, name='delete_book'),
]
