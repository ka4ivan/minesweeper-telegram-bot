"""1. Get all texts
pybabel extract --input-dirs=bot -o bot/locales/messages.pot --project=messages

2. Init translations
pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l en
pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l ru
pybabel init -i bot/locales/messages.pot -d bot/locales -D messages -l uk

3. Compile translations
pybabel compile -d bot/locales -D messages --statistics

pybabel update -i bot/locales/messages.pot -d bot/locales -D messages

"""
from aiogram import BaseMiddleware
from bot.utils.i18n import i18n, SUPPORTED_LOCALES

class I18nMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)

        locale = (
            user.language_code.split("-")[0]
            if user and user.language_code
            else i18n.default_locale
        )

        if locale not in SUPPORTED_LOCALES:
            locale = i18n.default_locale

        data["locale"] = locale

        with i18n.use_locale(locale):
            return await handler(event, data)
