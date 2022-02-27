from django.urls import path
from .import views

app_name = 'myexpense'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exp_accounts/', views.exp_accounts, name='exp_accounts'),
    path('set_default/<int:id>', views.set_default, name='set_default'),
    path('borrow_lent/', views.borrow_lent_money, name='borrow_lent'),
    path('transactions/', views.my_trnsactions, name='transactions'),
    path('manage_borrow_lent/', views.manage_borrow_lent, name='manage_borrow_lent'),
    path('show_all_records/', views.manage_borrow_lent, name='show_all_records'),
    path('make_paid_transaction/', views.make_paid_transaction, name='make_paid_transaction'),
    path('make_notpaid_transaction/', views.make_notpaid_transaction, name='make_notpaid_transaction'),
    path('individual_person_account/', views.individual_p_account, name='individual_person_account'),
    path('manage_individual_person_account/<int:id>', views.manage_individual_p_account, name='manage_individual_person_account'),

]