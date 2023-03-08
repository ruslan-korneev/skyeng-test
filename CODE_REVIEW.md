В общих чертах - код довольно чистый, ошибки в основном связанны с тем,
что не привыкли к новому инструменту,
либо не знаете каких-то общепринятых вещей, но это все не критично,
оценил бы работу на 6 баллов, если закроете issues, что я описал ниже

## `junior_developers.settings`
1. Если используешь переменные окружения для django проекта
можно также выносить значение переменной DEBUG,
поставить по умолчанию, например, True, а на production будет False
2. в INSTALLED_APPS свои приложения лучше отделять визуально от django's и third-party приложений:
```python
INSTALLED_APPS = [
    # Django's
    # 'django.contrib.admin',
    'django.contrib.auth',
    ...,
    'django.contrib.staticfiles',
    # Third-party
    "django_extensions",  # как пример, установленная библиотека-плагин для django
    ...,
    # My Apps
    'vacancies',
]
```

## `vacancies.views`
1. вместо try-except с raise Http404 можно использовать `get_object_or_404` из `django.shortcuts`,
таким образом не пишем то, что уже есть, но если бы этого не было в django,
я бы посоветовал написать свою реализацию этой функции, она не сложная,
но при этом не будет дублирования кода.
2. если используете try-except лучше указывать конкретные исключения,
в данном случае `DoesNotExists`, но благодаря `get_object_or_404` тут не придется писать try-except
3. для сбора вакансий с фильтром по компании или специальности можно использовать полученную специальность
пример
```python
from vacancies.models import Company

company = Company.objects.get(id=1)
company.vacancies.all()
company.vacancies.filter(salary=...)
```
аттрибут `vacancies` внутри `company` выступает как `RelatedManager` модели Vacancy с фильтром по компании `company`
4. `view` в названии view-функциях лучше писать в единственном числе, это касается только данных view-функций,
т.к. там только одно возможное представление на одну view-функцию.
таким образом jobs_views надо переименовать в jobs_view. Бывает когда у вас несколько представлений в функции или классе,
тогда это принято называть view set (`job_viewset` / `JobViewSet`), но тогда название сущности в единственном числе.
это не является ошибкой, просто так принято в обществе разработчиков.

## `vacancies.models`
1. id поле уже есть по умолчанию, в задании не сказано его изменять:
```python
from django.db import models

# по умолчанию
models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
# ваша версия
models.IntegerField(primary_key=True)
```
Подробнее почитать про [AutoField](https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.AutoField)
Суть в том, что это IntegerField который автоматически увеличивается.

2. проверьте название полей у моделей, сравните с тем, что просят в задании.(предоставленные мок-данные jobs хранят поле
posted, что некорректно, либо в задании надо менять название, либо в мок-данных)

## `vacancies.management.commands.data_to_sql`
1. библиотека dotmap - лишняя, можно обойтись распаковкой python, (*args, **kwargs, в данном случае **kwargs)
```python
# with DotMap
for company in companies:
    item = DotMap(company)
    new_item = Company(
        id=item.id,
        title=item.title,
        location=item.location,
        logo=item.logo,
        description=item.description,
        employee_count=item.employee_count
    )
    ...

# with python unpacking
for company in companies:
    new_item = Company(**company)
    ...
```
(опять же, в мок-данных стоят id, в задании не было ничего сказано про свое id поле,
я бы подкорректировал мок-данные, не просто убрав id, а изменив структуру. Компаний с вакансиями,
чтобы было сопоставление)

2. можно использовать bulk_create, для того, чтобы сократить количество запросов в базу данных.
bulk_create создаст сразу все объекты за 1 запрос
```python
from vacancies.data import companies
from vacancies.models import Company

# как пример - компании
new_companies = [Company(**company) for company in companies]
Company.objects.bulk_create(new_companies)

# или еще более короткий, при этом также хорошо читаемый код
Company.objects.bulk_create(
    [Company(**company) for company in companies]
)
```
