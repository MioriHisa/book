from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 1. 明示的に定義したログインとログアウトを残す（テンプレート名とリダイレクト先を制御）
    path('login/', auth_views.LoginView.as_view(template_name='bookreserve/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('list')), name='logout'),
    # 2. 管理サイト
    path("admin/", admin.site.urls),
    # 3. 書籍アプリ
    path("", include("bookreserve.urls")),
    # 4. 競合を防ぐためコメントアウト
    # path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
