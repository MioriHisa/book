from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.forms import ModelForm

# 💡 BookRequestと既存のBookReserveモデルの両方をインポート
from .models import BookRequest, BookReserve as Book


# --- 依存解消のための内部フォーム定義 ---

class BookReserveForm(ModelForm):
    """
    既存書籍の編集・更新（BookReserveUpdate）のためのフォーム定義。
    forms.pyへの依存を解消するため、views.py内に直接定義します。
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'picture', 'reservation_availability', 'reserver', 'return_date']

# --- 関数ベースビュー (既存のロジック) ---
def book_list(request):
    """書籍一覧を表示し、検索を処理する（BookReserveモデルを使用）"""
    books = Book.objects.all()
    query = request.GET.get('q')

    if query:
        books = books.filter(title__icontains=query)
    
    is_empty = not books.exists()
    
    context = {
        'books': books,
        'query': query,
        'is_empty': is_empty,
    }
    return render(request, 'bookreserve/bookreserve_list.html', context)

@require_POST
@login_required
def reserve_book(request, pk):
    """書籍の予約処理を行う（BookReserveモデルを使用）"""
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': '不正なリクエストです。'}, status=400)

    try:
        book = get_object_or_404(Book, pk=pk)
        if not book.reservation_availability:
            return JsonResponse({'error': 'この書籍は現在予約できません。'}, status=400)

        # 予約処理
        book.reservation_availability = False
        book.reserver = request.user.username
        book.return_date = date.today() + timedelta(weeks=3)
        book.save()

        print(f"書籍ID {pk} ({book.title}) がユーザー {request.user.username} によって予約されました。")
        return JsonResponse({'message': '予約が完了しました', 'book_id': pk})

    except Exception as e:
        print(f"予約処理中にエラーが発生しました: {e}")
        return JsonResponse({'error': f'予約処理中にエラーが発生しました: {str(e)}'}, status=500)


# --- クラスベースビュー ---

# 既存の書籍（BookReserve）のビュー
class BookReserveDetail(DetailView):
    model = Book
    context_object_name = "book"

class BookReserveCreate(CreateView):
    model = Book
    # 💡 ユーザー様のモデルに合わせてfieldsを修正
    fields = ['title', 'author', 'publication_date', 'picture', 'reservation_availability', 'reserver', 'return_date']
    success_url = reverse_lazy("list")

class BookReserveUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    # 💡 内部定義したフォームを使用
    form_class = BookReserveForm

class BookReserveDelete(DeleteView):
    model = Book
    context_object_name = "books"
    success_url = reverse_lazy("list")


# --- 新規追加: 書籍リクエスト機能 (BookRequestモデルを使用) ---

class BookRequestForm(ModelForm):
    """
    書籍リクエスト用のフォーム。BookRequestモデルを参照。
    """
    class Meta:
        # 💡 新しい BookRequest モデルを参照
        model = BookRequest 
        fields = ['title', 'author', 'url'] 
        labels = {
            'title': '書籍タイトル (必須)',
            'author': '著者名 (必須)',
            'url': '商品URL (任意)',
        }

class BookReserveRequest(CreateView):
    """
    書籍リクエストを処理するためのビュー。
    """
    # 💡 新しい BookRequest モデルを参照
    model = BookRequest
    form_class = BookRequestForm
    template_name = "bookreserve/bookreserve_request_form.html"
    success_url = reverse_lazy("list")
    
    def form_valid(self, form):
        """フォームが有効だった場合の処理"""
        # ログインユーザーがリクエストした場合、requested_byを設定
        if self.request.user.is_authenticated:
            request_instance = form.save(commit=False)
            request_instance.requested_by = self.request.user
            request_instance.save()
            return redirect(self.get_success_url())
        
        # ログインしていないユーザーでもリクエスト自体は可能（requested_byはnull）
        return super().form_valid(form)
