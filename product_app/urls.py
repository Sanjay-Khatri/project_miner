from django.contrib import admin
from django.urls import path
import product_app.views


urlpatterns = [
    path('browse/', product_app.views.browse, name='browse'),
    path('browse/<str:product_category>/',product_app.views.browse, name='browse_category'),
    path('my_account/', product_app.views.my_acc, name='my_account'),
    path('submit/', product_app.views.submit, name='sumbit'),
    path('<int:product_id>/',product_app.views.detail, name='detail'),
    path('delete/<int:product_id>/',product_app.views.deleter, name='deleter'),
    path('comment/',product_app.views.comment, name='comment'),
    path('hash_rate/',product_app.views.hash_rate, name='hash_rate'),
    path('example/',product_app.views.example, name='example'),
    path('<int:product_id>/upvote',product_app.views.upvote, name='upvote'),
    path('<int:product_id>/report',product_app.views.report, name='report'),
    path('my_account/edit', product_app.views.edit_profile, name='edit_profile'),
    path('change-password/', product_app.views.changepassword, name='change_password'),
    # path('edit-post/', product_app.views.edit_post, name='edit-post'),
]
