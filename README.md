# Topvisor API Client for Python
[Перейти к русскому описанию](#библиотека-для-работы-с-API-Topvisor)

This library provides a convenient interface for working with the Topvisor API. 
In the current version, only GET methods of the API are supported, as well as two main services: 
`positions` and `projects` . However, the functionality of the library will gradually be expanded.

## Initializing the Client
To get started, you need to create an instance of the Topvisor class, passing your `user_id` and `api_key`.

```python
from pytopvisor.topvisor import Topvisor

topvisor = Topvisor(user_id="your_user_id", api_key="your_api_key")
```

## Performing Operations
Currently, the library supports the following operations:

- **get_projects**: Retrieve a list of projects.
- **get_competitors**: Retrieve a list of competitors for a specific project.
- **get_history**: Retrieve the history of position checks.
- **get_summary**: Retrieve a summary of positions for two dates.
- **get_summary_chart**: Retrieve data for a summary chart.

### Retrieving a List of Projects
The method `get_projects` allows you to retrieve a list of all projects available for your account. 
You can specify additional parameters such as `show_site_stat` (display site statistics), 
`show_searchers_and_regions` (display search engines and regions), and `include_positions_summary` (include a summary of positions).

```python
projects = topvisor.run_task(
    "get_projects",
    show_site_stat=True,  # Display site statistics
    show_searchers_and_regions=1,  # Display search engines and regions (1 - yes)
    include_positions_summary=True  # Include a summary of positions
)
```

### Retrieving a List of Competitors for a Specific Project
The method `get_competitors` allows you to retrieve a list of competitors for a specific project. 
You can specify additional parameters such as `only_enabled` (display only active competitors) and 
`include_project` (include the project itself in the list).

```python
competitors = topvisor.run_task(
    "get_competitors",
    project_id=12345,
    only_enabled=True,  # Display only active competitors
    include_project=False  # Do not include the project itself in the list
)
```

### Retrieving the History of Position Checks
The method `get_history` is used to retrieve data about position checks for keywords over a 
specified period or on specific dates. You can specify regions, competitors, date range type, 
depth of displayed positions, and other parameters.
```python
history = topvisor.run_task(
    "get_history",
    project_id=12345,
    regions_indexes=[643],  # Region indexes (e.g., 643 - Russia)
    date1="2023-01-01",  # Start date of the period
    date2="2023-01-31",  # End date of the period
    competitors_ids=[123, 456],  # Competitor IDs
    type_range=2,  # Date range type (2 - automatic selection)
    count_dates=10,  # Number of dates in the result
    only_exists_first_date=True,  # Display only keywords present in the first check
    show_headers=True,  # Add result headers
    show_visitors=True,  # Add visitor data
    show_top_by_depth=10  # Add data for the specified depth of the TOP
)
```
### Retrieving a Summary of Positions for Two Dates
The method `get_summary` allows you to retrieve a summary of keyword positions for 
two specified dates. You can specify additional parameters for displaying dynamics, 
average values, visibility, etc.
```python
summary = topvisor.run_task(
    "get_summary",
    project_id=12345,
    region_index=643,  # Region index (e.g., 643 - Russia)
    dates=["2023-01-01", "2023-01-31"],  # A list of two dates for comparison
    competitor_id=123,  # Competitor ID (optional)
    only_exists_first_date=True,  # Consider keywords present in both dates
    show_dynamics=True,  # Add position dynamics
    show_tops=True,  # Add TOP data
    show_avg=True,  # Add average position
    show_visibility=True,  # Add visibility
    show_median=True  # Add median position
)
```

### Retrieving Data for a Summary Chart
The method `get_summary_chart` allows you to retrieve data for building a summary chart of keyword positions over a specified period. You can specify dates, competitors, date range type, and display parameters.
```python
summary_chart = topvisor.run_task(
    "get_summary_chart",
    project_id=12345,
    region_index=643,  # Region index (e.g., 643 - Russia)
    date1="2023-01-01",  # Start date of the period
    date2="2023-01-31",  # End date of the period
    competitors_ids=[123, 456],  # Competitor IDs
    type_range=2,  # Date range type (2 - automatic selection)
    only_exists_first_date=True,  # Consider keywords present in all dates
    show_tops=True,  # Add TOP data
    show_avg=True,  # Add average position
    show_visibility=True  # Add visibility
)
```
## Error Handling
The client automatically handles API errors and raises appropriate exceptions. Below is a list of the main exceptions:

- AuthenticationError
- RateLimitError
- InvalidRequestError
- ServerError

# Библиотека для работы с API Topvisor

Эта библиотека предоставляет удобный интерфейс для работы с API Topvisor. В текущей версии поддерживаются только GET-методы API, а также два основных сервиса: positions и projects . Однако функционал библиотеки будет постепенно расширяться.


## Инициализация клиента
Для начала вам нужно создать экземпляр класса Topvisor, передав в него ваш user_id и api_key.

```python
from pytopvisor.topvisor import Topvisor

topvisor = Topvisor(user_id="your_user_id", api_key="your_api_key")
```

## Выполнение операций
На текущий момент библиотека поддерживает следующие операции:

- **get_projects**: Получение списка проектов.
- **get_competitors**: Получение списка конкурентов для указанного проекта.
- **get_history**: Получение истории проверок позиций.
- **get_summary**: Получение сводки по позициям за две даты.
- **get_summary_chart**: Получение данных для графика сводки.

### Получение списка проектов
Метод `get_projects` позволяет получить список всех проектов, доступных для вашего аккаунта. Вы можете указать дополнительные параметры, такие как `show_site_stat` (показывать статистику сайта), `show_searchers_and_regions` (показывать поисковые системы и регионы) и `include_positions_summary` (включать сводку по позициям).

```python
projects = topvisor.run_task(
    "get_projects",
    show_site_stat=True,  # Показывать статистику сайта
    show_searchers_and_regions=1,  # Показывать поисковые системы и регионы (1 - да)
    include_positions_summary=True  # Включать сводку по позициям
)
```
### Получение списка конкурентов для указанного проекта
Метод `get_competitors` позволяет получить список конкурентов для конкретного проекта. Вы можете указать дополнительные параметры, такие как `only_enabled` (показывать только активных конкурентов) и `include_project` (включать ли сам проект в список).

```python
competitors = topvisor.run_task(
    "get_competitors",
    project_id=12345,
    only_enabled=True,  # Показывать только активных конкурентов
    include_project=False  # Не включать сам проект в список
)
```
### Получение истории проверок позиций
Метод `get_history` используется для получения данных о проверках позиций ключевых фраз в определенном периоде времени или на конкретные даты. Вы можете указать регионы, конкурентов, тип диапазона дат, глубину показа позиций и другие параметры.


```python
history = topvisor.run_task(
    "get_history",
    project_id=12345,
    regions_indexes=[643],  # Индексы регионов (например, 643 - Россия)
    date1="2023-01-01",  # Начальная дата периода
    date2="2023-01-31",  # Конечная дата периода
    competitors_ids=[123, 456],  # ID конкурентов
    type_range=2,  # Тип диапазона дат (2 - автоматический выбор)
    count_dates=10,  # Количество дат в результате
    only_exists_first_date=True,  # Отображать только ключевые фразы, присутствующие в первой проверке
    show_headers=True,  # Добавить заголовки результатов
    show_visitors=True,  # Добавить данные о количестве визитов
    show_top_by_depth=10  # Добавить данные по ТОПу указанной глубины
)
```
### Получение сводки по позициям за две даты
Метод `get_summary` позволяет получить сводку по позициям ключевых фраз за две заданные даты. Вы можете указать дополнительные параметры для отображения динамики, средних значений, видимости и т.д.


```python
summary = topvisor.run_task(
    "get_summary",
    project_id=12345,
    region_index=643,  # Индекс региона (например, 643 - Россия)
    dates=["2023-01-01", "2023-01-31"],  # Список из двух дат для сравнения
    competitor_id=123,  # ID конкурента (опционально)
    only_exists_first_date=True,  # Учитывать ключевые фразы, присутствующие в обеих датах
    show_dynamics=True,  # Добавить динамику позиций
    show_tops=True,  # Добавить данные по ТОПам
    show_avg=True,  # Добавить среднюю позицию
    show_visibility=True,  # Добавить видимость
    show_median=True  # Добавить медианную позицию
)
```
### Получение данных для графика сводки
Метод `get_summary_chart` позволяет получить данные для построения графика сводки позиций ключевых фраз за определенный период времени. Вы можете указать даты, конкурентов, тип диапазона дат и параметры отображения данных.

```python
summary_chart = topvisor.run_task(
    "get_summary_chart",
    project_id=12345,
    region_index=643,  # Индекс региона (например, 643 - Россия)
    date1="2023-01-01",  # Начальная дата периода
    date2="2023-01-31",  # Конечная дата периода
    competitors_ids=[123, 456],  # ID конкурентов
    type_range=2,  # Тип диапазона дат (2 - автоматический выбор)
    only_exists_first_date=True,  # Учитывать ключевые фразы, присутствующие во всех датах
    show_tops=True,  # Добавить данные по ТОПам
    show_avg=True,  # Добавить среднюю позицию
    show_visibility=True  # Добавить видимость
)
```

## Обработка ошибок
Клиент автоматически обрабатывает ошибки API и выбрасывает соответствующие исключения. Вот список основных исключений:

- AuthenticationError
- RateLimitError
- InvalidRequestError
- ServerError
