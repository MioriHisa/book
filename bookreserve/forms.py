{% extends 'bookreserve/base.html' %} 

{% block header %}
<h1 class="display-5 text-center my-4 text-primary">書籍リクエスト</h1>
{% endblock header %}

{% block content %}

<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow-lg border-0 p-3">
            <div class="card-body p-5">
                <h2 class="card-title text-center mb-4 h4">探している本をリクエスト</h2>
                <p class="text-center text-muted mb-4">以下のフォームに必要事項を記入してください。</p>

                <form method="post">
                    {% csrf_token %}
                    
                    {% for field in form %}
                        <div class="mb-3 row"> 
                            
                            <label for="{{ field.id_for_label }}" class="col-sm-3 col-form-label fw-bold text-gray-700">
                                {{ field.label }} 
                            </label>

                            <div class="col-sm-9">
                                
                                {% if field.field.widget.input_type == 'textarea' %}
                                    <textarea name="{{ field.name }}" id="{{ field.id_for_label }}" 
                                        class="form-control border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                                        {% if field.field.required %}required{% endif %}>{{ field.value|default_if_none:"" }}</textarea>
                                {% else %}
                                    <input type="{{ field.field.widget.input_type }}" name="{{ field.name }}" id="{{ field.id_for_label }}" 
                                        value="{{ field.value|default_if_none:"" }}"
                                        class="form-control border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                                        {% if field.field.required %}required{% endif %}>
                                {% endif %}

                                
                                {% if field.errors %}
                                    <div class="text-danger small mt-1">
                                        {% for error in field.errors %}
                                            {{ error|striptags }}
                                        {% endfor %}
                                    </div>
                                {% endif %}

                                
                                {% if field.help_text %}
                                    <div class="form-text text-muted small mt-1">
                                        {{ field.help_text }}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    {% endfor %}

                    
                    <div class="d-grid gap-2 mt-4">
                        <button type="submit" class="btn btn-primary btn-lg">
                            リクエストを送信
                        </button>
                    </div>
                </form>

                
                <div class="text-center mt-3">
                    <a href="{% url 'list' %}" class="text-secondary small">
                        &larr; 一覧に戻る
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
