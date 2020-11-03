from django.urls import path

from . import views

# codestart:001
app_name = 'blog'
urlpatterns = [
    path('', views.default_view, name='default_view'),
    path('redirect', views.redirect_view, name='redirect_view'),
    path('<slug:author_name>/', views.BlogIndex.as_view(), name='index'),
    path('<slug:author_name>/<int:pk>/', views.BlogDetail.as_view(), name='detail'),
    path('<slug:author_name>/search', views.BlogSearch.as_view(), name='search'),

    path('<slug:author_name>/comment/<int:post_id>/', views.comment, name='comment'),
    path('<slug:author_name>/comment/<int:comment_id>/update', views.comment_update, name='comment_update'),
    path('<slug:author_name>/reply/<int:comment_id>/', views.reply, name='reply'),
]
# codeend:001

urlpatterns += [
    path('<slug:author_name>/<slug:template_name>/', views.BlogDetailTest.as_view(), name='detail_test'),
]