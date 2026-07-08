## General
start-greeting = Hello, { $name }! 🎬 Welcome to Cinema Bot.
sub-required = To use this bot, please subscribe to the following channel(s):
sub-button = 📢 Subscribe
sub-check-button = ✅ Check
sub-not-yet = ❌ You haven't subscribed to all channels yet. Subscribe and check again.
sub-success = ✅ Thank you! You can now use the bot.

## Reply menu
menu-search-code = 🔍 Search by code
menu-search-name = 🎬 Search by movie name
menu-search-genre = 🎭 Search by genre
menu-search-country = 🌍 Search by country
menu-settings = ⚙️ Settings
menu-request-movie = 🎬 Request movie
menu-back = ⬅️ Back

## Settings
settings-title = ⚙️ Settings
settings-language = 🌐 Change language
settings-favorites = ❤️ My favorite movies
settings-requests = 📩 My movie requests
language-choose = Choose a language:
language-changed = ✅ Language changed successfully!

## Search - code
ask-code = Enter the movie code (e.g. 1001):
code-not-found = ❌ No movie found with this code.
invalid-code = ⚠️ Please enter numbers only.

## Search - name
ask-name = Enter the movie name:
name-not-found = ❌ No movie found with this name.
name-results = 🔎 Search results:

## Genre / Country
choose-genre = 🎭 Choose a genre:
choose-country = 🌍 Choose a country:
no-movies-in-category = There are no movies in this category yet.

## Movie card
movie-card =
    🎬 <b>{ $title }</b>

    🌍 Country: { $country }
    🎭 Genre: { $genre }
    📅 Year: { $year }
    ⭐️ Rating: { $rating }

    📝 { $description }
movie-like-button = ❤️ Like ({ $count })
movie-liked = ❤️ Liked!
movie-already-liked = You have already liked this movie.

## Favorites
favorites-title = ❤️ Your favorite movies:
favorites-empty = You don't have any favorite movies yet.

## Requests
ask-request-name = Which movie are you looking for? Type its name and we'll pass it to the admin:
request-sent = ✅ Your request has been received. It will be reviewed soon!

## Pagination
page-indicator = { $current }/{ $total }
prev-button = ⬅️
next-button = ➡️

## Errors
error-generic = ⚠️ Something went wrong. Please try again later.
access-denied = ⛔️ You do not have access to this command.
blocked-user-message = ⛔️ You are blocked from using this bot. Contact the administrator.

## ---- ADMIN ----
admin-panel-title = 🛠 Admin panel
admin-movies = 🎬 Movies
admin-add-movie = ➕ Add
admin-delete-movie = 🗑 Delete
admin-edit-movie = ✏️ Edit
admin-channels = 📡 Channels
admin-add-mandatory = ➕ Add mandatory channel
admin-remove-mandatory = ➖ Remove mandatory channel
admin-add-optional = ➕ Add optional channel
admin-remove-optional = ➖ Remove optional channel
admin-broadcast = 📣 Broadcast
admin-stats = 📊 Statistics
admin-export = 📊 Excel Export
admin-all-codes = 📋 All movie codes
admin-block-user = 🚫 Block user
admin-blocked-users = 🚫 Blocked users
admin-back = ⬅️ Admin menu
admin-block-user-inline = 🚫 Block
admin-unblock-user-inline = ✅ Unblock
admin-all-users-title = 👥 All users:
admin-blocked-users-title = 🚫 Blocked users:
admin-no-users = There are no users yet.
admin-ask-user-id-or-username = Enter the user ID or username you want to block:
admin-ask-user-id-or-username-unblock = Enter the user ID or username you want to unblock:
admin-invalid-user-target = ⚠️ Please enter an ID or username.
admin-user-not-found = ❌ User not found.
admin-user-already-blocked = ⚠️ This user is already blocked.
admin-user-not-blocked = ⚠️ This user is not blocked.
admin-confirm-block-user = Are you sure you want to block this user?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-confirm-unblock-user = Are you sure you want to unblock this user?
    • ID: { $user_id }
    • Username: @{ $username }
    • Nickname: { $nickname }
admin-user-blocked = ✅ User blocked.
admin-user-unblocked = ✅ User unblocked.

admin-ask-code = Enter the movie code (integer):
admin-code-exists = ⚠️ This code is already taken. Enter another one.
admin-ask-title = Enter the movie title:
admin-ask-genre = Choose a genre:
admin-ask-country = Choose a country:
admin-ask-year = Enter the release year:
admin-ask-rating = Enter the rating (e.g. 8.5):
admin-ask-description = Enter the description:
admin-ask-file = Now send the movie video file:
admin-confirm-add = Add the movie with the following data?
admin-movie-added = ✅ Movie added successfully!
admin-movie-deleted = ✅ Movie deleted.
admin-movie-updated = ✅ Movie updated.
admin-choose-field = Which field do you want to edit?
admin-field-title = Title
admin-field-genre = Genre
admin-field-country = Country
admin-field-year = Year
admin-field-rating = Rating
admin-field-description = Description
admin-field-file = File
admin-ask-new-value = Enter the new value:

admin-ask-channel-id = Enter the channel ID or username (e.g. @channel or -100123456):
admin-ask-channel-title = Enter the channel title:
admin-channel-added = ✅ Channel added.
admin-channel-removed = ✅ Channel removed.
admin-no-channels = There are no channels yet.

admin-ask-broadcast = Send the message you want to broadcast (text, photo, video, etc.):
admin-broadcast-confirm = Confirm sending this message to all users?
admin-broadcast-yes = ✅ Yes, send
admin-broadcast-no = ❌ Cancel
admin-broadcast-started = 📣 Broadcast started...
admin-broadcast-progress = 📊 Sent: { $sent }/{ $total }
admin-broadcast-done =
    ✅ Broadcast finished!

    ✅ Sent: { $sent }
    ❌ Failed: { $failed }
    🚫 Blocked: { $blocked }

admin-stats-title =
    📊 <b>Statistics</b>

    👥 Total users: { $total }
    📅 Today: { $today }
    📆 This week: { $week }
    🗓 This month: { $month }

admin-export-caption = 📊 Users list (Excel)

admin-all-codes-title = 📋 All movie codes:
admin-code-item = { $code } - { $title }
admin-confirm-delete = ❗️ Confirm deleting "{ $title }" ({ $code })?
admin-yes = ✅ Yes
admin-no = ❌ No
admin-cancelled = Cancelled.

## Genres
genre-action = Action
genre-comedy = Comedy
genre-drama = Drama
genre-horror = Horror
genre-romance = Romance
genre-thriller = Thriller
genre-fantasy = Fantasy
genre-scifi = Sci-Fi
genre-animation = Animation
genre-documentary = Documentary
genre-adventure = Adventure
genre-crime = Crime
genre-family = Family
genre-musical = Musical
genre-war = War
genre-history = History
genre-mystery = Mystery
genre-sport = Sport

## Countries
country-uzbekistan = Uzbekistan
country-turkey = Turkey
country-usa = USA
country-russia = Russia
country-india = India
country-south_korea = South Korea
country-france = France
country-germany = Germany
country-china = China
country-japan = Japan
country-united_kingdom = United Kingdom
country-italy = Italy
country-spain = Spain
country-brazil = Brazil
country-mexico = Mexico
country-canada = Canada
country-iran = Iran
country-egypt = Egypt
country-kazakhstan = Kazakhstan
country-other = Other
