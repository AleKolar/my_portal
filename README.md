**Здравствуйте!

Установить Redis. (RabbitMQ, Redis - IP заблокирован, хоть убейся)

Установить Celery.

Произвести необходимые конфигурации Django для соединения всех компонентов системы.

Реализовать рассылку уведомлений подписчикам после создания новости.

Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра)

- В Windows все немного по другому, и кажеся Celery запускается один поток celery -A my_portal worker --pool=solo -l info
- 
- Казалось бы все просто использовали django signals, а теперь под управлением celery, это, вообще, не так, а Вы знали!
- 
- И кажется , я не выполнил "поэтому рекомендуется передавать ID объектов или параметры", хотя или параметы, у меня там
- content[:50] он же храниться в сериализованном виде.  Сериализация - опять же!  Столько - нюансов! Начинаешь по  настоящему ценить время!
========================================================================*
**Здравствуйте!

  п.1 - news/views.py
  
  п.2 - news/signals.py
  
  п.3 - news/apps.py
  
  п.4 - sign/signals.py_регистрироваться надо через accounts/signup, потому что там на allauth завязано(или, уже, нет)
  
  Это было трудно! Надо было по другому архитектуру приложения выстраивать, хотя мы же по учебной программе идем, да это
  я изначально subscribers-ов в Post засунул и когда email начал getattr-ом доставать понял, что такое не должно с людьми
  случаться. А потом решил перестраховаться дай думаю в models побольше насую всякого, чтоб связи всякие были всех со 
  всеми, чтоб до любого добраться можно было. По итогу выстроил, что - то внятное, как мне кажется. Но без Exceptions и 
  Loggers, времени не хватает, время самый дорогой ресурс!
========================================================================*



Здравствуйте!

1. В классе-представлении редактирования профиля добавить проверку аутентификации. 
Здесь, наверное имелось ввиду news/views.py: PostUpdate c template edit, что мы ранее делали(но там две кнопки только). В итоге(как я понял) сделал в sign/views.py: update_profile с profile, ну и models, form соответственно.
Это вообще не из "коробки", это, прям, ООП, Вам думаю это близко. Сложновато, такое чувство, что ты, что-то не то делаешь(типа ты - тупой и не понимаешь, что от тебя требуется). Пришлось заводить Codium_test для тестов, чтоб все проверять. Ну мощная, конечно, вещь!

2, 3, 4, 5. Далее все по ТЗ.

6. Все настроенно, только надо приложение в Google зарегистрировать, но там денег хотят. Или я чего не понял(Да, потому что все урывками и на работе все в отпуск ушли).

7, 8, 9.  Далее все по ТЗ, как в примерах.

10. Если бы это было просто в django admin Permission галочек наставить, то задания такого не было бы. Поэтому "вручную" в models прописал.

11, 12. Далее все по ТЗ.
Извиняюсь! за всякие "излишки" мне, просто, нужна визуализация, а то я так путаюсь. Я искал лаконичный способ с url, но как видите не нашел еще.

=========================================================================================

Здравствуйте!

Сделано в соответствии с ТЗ, может, я только немного добавил последовательности (за счет urls), так чтоб человек открыл новости, выбрал, провалился в конкретику,
ИСПРАВИЛ - не понравилось. УДАЛИЛ. 
Лишнего из проекта не удалял, чтоб можно было отследить логику развития проекта (может я, вообще, не в том раправлении двигаюсь?!)
ДЗ начинался интересней с виджетами там всякими, попыткой поиска по ForeignKey и чтоб не author.object (1), а чтоб прям Вася Пупкин. Но конечно, тут надо быть мегавнимательным! Пришлось остановится на том, что успел постичь, 
потому что отлавливать какую-нибудь ошибку(в шаблоне например) - это нужно быть по настоящему свободным человеком, причем от всего, чтоб столько времени было!
Я почти уверен, что в серьёзных организациях, чтоб избежать ошибок пользуются какими - нибудь железобетонными шаблонами из железобетонной библиотеки. Ну понятно, что тестят, но вот, чтоб прям сначала, со стартовой позиции что-то же есть.
Вот Яндекс например, у них максимум, что меняется - это шапку Дед Мороза на лейбл на Новый год надевают.

==========================================================================================
Здравствуте!

Сделано следующее, в соответствии с ТЗ:

- Создать новую страницу с адресом /news/, на которой должен выводиться список всех новостей.

Вывести все статьи в виде заголовка, даты публикации и первых 20 символов текста.(Это же не касается только "новостей",
если - Да! Надо "раскомитеть" фильтр #queryset = Post.objects.filter(post_type='news').order_by('-created_at')[:21])

Новости должны выводиться в порядке от более свежей к самой старой.

- Сделать отдельную страницу для полной информации о статье /news/<id новости>.

На этой странице должна быть вся информация о статье. Название, текст и дата загрузки в формате день.месяц.год.

- Написать собственный фильтр censor, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ «*».

- Все новые страницы должны использовать шаблон default.html как основу.

Я оставил много лишнего: во views, flatpages, html-шаблоны, пути в urls, НО МНЕ ЭТО НУЖНО ДЛЯ ВИЗУАЛИЗАЦИИ И ЗАКРЕПЛЕНИЯ МАТЕРИАЛА!

*Извиняюсь, если не совсем "УДОБОЧИТАЕМО"! Я ,случайно, на этапе работы над ДЗ увидел, как создать динамическую страницу(или как правильно назвать: 
для перехода на отдельную страницу)  сделал и не стал удалять!

p.s. Django - заставляет задуматься над понятиями: смирение и терпимость! Я 4 раза пересоздавался! Психического напряжения хватило бы,
чтоб запитать маленький поселок.

