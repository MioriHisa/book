from django.urls import path
from . import views

urlpatterns = [
    # 書籍一覧 (ホーム)
    path("", views.book_list, name="list"),

    # 書籍詳細 (pk=書籍ID)
    path("detail/<int:pk>/", views.BookReserveDetail.as_view(), name="detail"),

    # 書籍の新規追加
    path("add/", views.BookReserveCreate.as_view(), name="add"),

    # 書籍の削除
    path("delete/<int:pk>/", views.BookReserveDelete.as_view(), name="delete"),

    # 💡 予約処理 (JSが 'reserve' を参照するため、この名前に統一)
    path("reserve/<int:pk>/", views.reserve_book, name="reserve"),

    # 書籍の更新（主に返却処理に使用）
    path("update/<int:pk>/", views.BookReserveUpdate.as_view(), name="update"),

    # 💡 新規書籍リクエスト
    path('request/', views.BookReserveRequest.as_view(), name='book_request'), 
]
