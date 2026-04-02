from django import forms
from .models import BookRequest, BookReserve

class BookReserveForm(forms.ModelForm):
    """
    既存書籍の編集・更新（BookReserveUpdate）のためのフォーム定義。
    forms.pyへの依存を解消するため、views.py内に直接定義します。
    """
    class Meta:
        model = BookReserve
        fields = ['title', 'author', 'publication_date', 'picture']

        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookRequestForm(forms.ModelForm):
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
