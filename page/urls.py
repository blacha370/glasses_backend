from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/<int:current_page>/a/', views.admin_orders, name='orders_admin'),
    path('orders/<int:current_page>/u/', views.user_orders, name='orders'),
    path('orders/archive/<int:current_page>/a/', views.admin_archive, name='archive_admin'),
    path('orders/archive/<int:current_page>/u/', views.user_archive, name='archive'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/thread/<str:message_topic>/<int:current_page>', views.message_thread, name='message'),
    path('message/new/', views.new_message, name='new_message'),
    path('message/add/<str:thread_subject>/', views.add_message, name='add_message'),
    path('message/add_new/', views.add_new_message, name='add_new_message'),
    path('message/delete/<int:thread_id>', views.delete_message_thread, name='thread_delete'),
    path('add/order/', views.add_order, name='add_order'),
    path('<int:order_id>/', views.details, name='details'),
    path('change/<int:order_id>/', views.change, name='change'),
    path('change_confirmed/<int:order_id>/<str:order_status>', views.change_confirmation, name="change_confirmed"),
    path('l/', views.login_user, name='login_user'),
    path('o/', views.logout_user, name='logout_user'),
    path('archive/', views.archive_inbox, name='archive_inbox'),
    path('archive/<str:message_topic>/<int:current_page>', views.archive_thread, name='archive_thread')
]
