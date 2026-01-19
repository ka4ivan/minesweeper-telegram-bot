from aiogram.utils.i18n import I18n

SUPPORTED_LOCALES = {"en", "uk", "ru"}

i18n = I18n(
    path="bot/locales",
    default_locale="en",
    domain="messages",
)

_ = i18n.gettext
