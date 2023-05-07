from django.urls import path

from .views.auth.login_view import LoginView, RefreshTokenView
from .views.auth.register_view import AdminsView, EmployeesView
from .views.reservations_view import (ReservationDetailsView,
                                      ReservationSlotsView, ReservationsView,
                                      TodayReservationsView)
from .views.tables_view import TableDetailsView, TablesView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('refresh_token', RefreshTokenView.as_view()),
    path('admins', AdminsView.as_view()),
    path('employees', EmployeesView.as_view()),
    path('tables', TablesView.as_view()),
    path('tables/<int:id>', TableDetailsView.as_view()),
    path('reservations', ReservationsView.as_view()),
    path('reservations/today', TodayReservationsView.as_view()),
    path('reservations/<int:id>', ReservationDetailsView.as_view()),
    path('reservations/available-slots', ReservationSlotsView.as_view()),
    
    
]
