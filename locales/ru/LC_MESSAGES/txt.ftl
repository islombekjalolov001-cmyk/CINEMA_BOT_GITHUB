## Общее
start-greeting = Здравствуйте, { $name }! 🎬 Добро пожаловать в Cinema бот.
sub-required = Для использования бота подпишитесь на следующие каналы:
sub-button = 📢 Подписаться
sub-check-button = ✅ Проверить
sub-not-yet = ❌ Вы ещё не подписались на все каналы. Подпишитесь и проверьте снова.
sub-success = ✅ Спасибо! Теперь вы можете пользоваться ботом.

## Reply меню
menu-search-code = 🔍 Поиск по коду
menu-search-name = 🎬 Поиск по названию
menu-search-genre = 🎭 Поиск по жанру
menu-search-country = 🌍 Поиск по стране
menu-settings = ⚙️ Настройки
menu-request-movie = 🎬 Запросить фильм
menu-back = ⬅️ Назад

## Настройки
settings-title = ⚙️ Раздел настроек
settings-language = 🌐 Изменить язык
settings-favorites = ❤️ Мои избранные фильмы
settings-requests = 📩 Мои запросы фильмов
language-choose = Выберите язык:
language-changed = ✅ Язык успешно изменён!

## Поиск - код
ask-code = Введите код фильма (например: 1001):
code-not-found = ❌ Фильм с таким кодом не найден.
invalid-code = ⚠️ Пожалуйста, введите только число.

## Поиск - название
ask-name = Введите название фильма:
name-not-found = ❌ Фильм с таким названием не найден.
name-results = 🔎 Результаты поиска:

## Жанр / Страна
choose-genre = 🎭 Выберите жанр:
choose-country = 🌍 Выберите страну:
no-movies-in-category = В этом разделе пока нет фильмов.

## Карточка фильма
movie-card =
    🎬 <b>{ $title }</b>

    🌍 Страна: { $country }
    🎭 Жанр: { $genre }
    📅 Год: { $year }
    ⭐️ Рейтинг: { $rating }

    📝 { $description }
movie-like-button = ❤️ Лайк ({ $count })
movie-liked = ❤️ Лайк поставлен!
movie-already-liked = Вы уже поставили лайк этому фильму.

## Избранное
favorites-title = ❤️ Ваши избранные фильмы:
favorites-empty = У вас пока нет избранных фильмов.

## Запросы
ask-request-name = Какой фильм вы ищете? Напишите название, мы передадим админу:
request-sent = ✅ Ваш запрос принят. Скоро будет рассмотрен!

## Пагинация
page-indicator = { $current }/{ $total }
prev-button = ⬅️
next-button = ➡️

## Ошибки
error-generic = ⚠️ Произошла ошибка. Попробуйте немного позже.
access-denied = ⛔️ У вас нет доступа к этой команде.
blocked-user-message = ⛔️ Вы заблокированы в боте. Обратитесь к администратору.

## ---- АДМИН ----
admin-panel-title = 🛠 Админ-панель
admin-movies = 🎬 Фильмы
admin-add-movie = ➕ Добавить
admin-delete-movie = 🗑 Удалить
admin-edit-movie = ✏️ Редактировать
admin-channels = 📡 Каналы
admin-add-mandatory = ➕ Добавить обязательный канал
admin-remove-mandatory = ➖ Удалить обязательный канал
admin-add-optional = ➕ Добавить необязательный канал
admin-remove-optional = ➖ Удалить необязательный канал
admin-broadcast = 📣 Рассылка
admin-stats = 📊 Статистика
admin-export = 📊 Экспорт в Excel
admin-all-codes = 📋 Все коды фильмов
admin-block-user = 🚫 Заблокировать пользователя
admin-blocked-users = 🚫 Заблокированные пользователи
admin-back = ⬅️ Меню админа
admin-block-user-inline = 🚫 Заблокировать
admin-unblock-user-inline = ✅ Разблокировать
admin-all-users-title = 👥 Все пользователи:
admin-blocked-users-title = 🚫 Заблокированные пользователи:
admin-no-users = Пока нет пользователей.
admin-ask-user-id-or-username = Введите ID или username пользователя, которого хотите заблокировать:
admin-ask-user-id-or-username-unblock = Введите ID или username пользователя, которого хотите разблокировать:
admin-invalid-user-target = ⚠️ Пожалуйста, введите ID или username.
admin-user-not-found = ❌ Пользователь не найден.
admin-user-already-blocked = ⚠️ Этот пользователь уже заблокирован.
admin-user-not-blocked = ⚠️ Этот пользователь не заблокирован.
admin-confirm-block-user = Вы уверены, что хотите заблокировать этого пользователя?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-confirm-unblock-user = Вы уверены, что хотите разблокировать этого пользователя?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-user-blocked = ✅ Пользователь заблокирован.
admin-user-unblocked = ✅ Пользователь разблокирован.

admin-ask-code = Введите код фильма (целое число):
admin-code-exists = ⚠️ Этот код занят. Введите другой.
admin-ask-title = Введите название фильма:
admin-ask-genre = Выберите жанр:
admin-ask-country = Выберите страну:
admin-ask-year = Введите год выпуска:
admin-ask-rating = Введите рейтинг (например 8.5):
admin-ask-description = Введите описание:
admin-ask-file = Теперь отправьте видеофайл фильма:
admin-confirm-add = Добавить фильм со следующими данными?
admin-movie-added = ✅ Фильм успешно добавлен!
admin-movie-deleted = ✅ Фильм удалён.
admin-movie-updated = ✅ Фильм обновлён.
admin-choose-field = Какое поле хотите изменить?
admin-field-title = Название
admin-field-genre = Жанр
admin-field-country = Страна
admin-field-year = Год
admin-field-rating = Рейтинг
admin-field-description = Описание
admin-field-file = Файл
admin-ask-new-value = Введите новое значение:

admin-ask-channel-id = Введите ID или username канала (например @channel или -100123456):
admin-ask-channel-title = Введите название канала:
admin-channel-added = ✅ Канал добавлен.
admin-channel-removed = ✅ Канал удалён.
admin-no-channels = Пока нет каналов.

admin-ask-broadcast = Отправьте сообщение для рассылки (текст, фото, видео и т.д.):
admin-broadcast-confirm = Подтверждаете отправку этого сообщения всем пользователям?
admin-broadcast-yes = ✅ Да, отправить
admin-broadcast-no = ❌ Отмена
admin-broadcast-started = 📣 Рассылка началась...
admin-broadcast-progress = 📊 Отправлено: { $sent }/{ $total }
admin-broadcast-done =
    ✅ Рассылка завершена!

    ✅ Отправлено: { $sent }
    ❌ Ошибок: { $failed }
    🚫 Заблокировали: { $blocked }

admin-stats-title =
    📊 <b>Статистика</b>

    👥 Всего пользователей: { $total }
    📅 Сегодня: { $today }
    📆 За неделю: { $week }
    🗓 За месяц: { $month }

admin-export-caption = 📊 Список пользователей (Excel)

admin-all-codes-title = 📋 Все коды фильмов:
admin-code-item = { $code } - { $title }
admin-confirm-delete = ❗️ Подтверждаете удаление "{ $title }" ({ $code })?
admin-yes = ✅ Да
admin-no = ❌ Нет
admin-cancelled = Отменено.

## Жанры
genre-action = Боевик
genre-comedy = Комедия
genre-drama = Драма
genre-horror = Ужасы
genre-romance = Романтика
genre-thriller = Триллер
genre-fantasy = Фэнтези
genre-scifi = Фантастика
genre-animation = Мультфильм
genre-documentary = Документальный
genre-adventure = Приключения
genre-crime = Криминал
genre-family = Семейный
genre-musical = Мюзикл
genre-war = Военный
genre-history = Исторический
genre-mystery = Детектив
genre-sport = Спорт

## Страны
country-uzbekistan = Узбекистан
country-turkey = Турция
country-usa = США
country-russia = Россия
country-india = Индия
country-south_korea = Южная Корея
country-france = Франция
country-germany = Германия
country-china = Китай
country-japan = Япония
country-united_kingdom = Великобритания
country-italy = Италия
country-spain = Испания
country-brazil = Бразилия
country-mexico = Мексика
country-canada = Канада
country-iran = Иран
country-egypt = Египет
country-kazakhstan = Казахстан
country-other = Другое
