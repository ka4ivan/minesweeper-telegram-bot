#!/bin/sh

# RUN
#chmod +x bot/scripts/i18n.sh
#./bot/scripts/i18n.sh

pybabel extract --input-dirs=bot -o bot/locales/messages.pot --project=messages

pybabel update -i bot/locales/messages.pot -d bot/locales -D messages

pybabel compile -d bot/locales -D messages --statistics
echo "✅ i18n updated and compiled"
