Здравствуйте!
Сделано в соответствии с ТЗ, может я , только немного добавил последовательности (за счет urls), так чтоб человек открыл новости, выбрал, провалился в конкретику,

ИСПРАВИЛ - не понравилось. УДАЛИЛ. 

Лишнего из проекта не удалял, чтоб можно было отследить логику развития проекта (может я, вообще, не в том раправлении двигаюсь?!)

ДЗ начинался интересней с виджетами там всякими, фильтации по дате и т.д. Но конечно, тут надо быть мегавнимательным! Пришлось остановится на том, что успел понять, 

потому что отлавливать какую-нибудь ошибку(в шаблоне например) - это нужно быть по настоящему свободным человеком, причем от всего, чтоб столько времени было!
======================================================================================================================================================================
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

