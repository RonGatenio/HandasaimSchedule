from requests.models import RequestEncodingMixin
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handasaim_schedule import get_schedule_html_safe
from telegram_utils import make_inline_keyboard


class Buttons:
    REFRESH = '🔄'

INLINE_KEYBOARD = make_inline_keyboard(Buttons.REFRESH)


class HandasaimBotUpdater(Updater):
    def __init__(self, api_token, class_id):
        super().__init__(api_token)

        self._class_id = class_id

        self.dispatcher.add_handler(CommandHandler('start', self._start_command_handler))
        self.dispatcher.add_handler(CallbackQueryHandler(self._keyboard_click_handler))
        self.dispatcher.add_error_handler(self._error_handler)

    def _get_schedule(self):
        return get_schedule_html_safe(self._class_id)

    def _start_command_handler(self, update, context):
        update.message.reply_text(
            self._get_schedule(),
            parse_mode=ParseMode.HTML,
            reply_markup=INLINE_KEYBOARD,
        )

    def _keyboard_click_handler(self, update, context):
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        if query.data != Buttons.REFRESH:
            return

        query.edit_message_text(
            self._get_schedule(),
            parse_mode=ParseMode.HTML,
            reply_markup=INLINE_KEYBOARD,
        )
    
    def _error_handler(self, update, context):
        """Log Errors caused by Updates."""
        # LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


class HandasaimBot:
    def __init__(self, api_token, class_id):
        self._api_token = api_token
        self._updater = HandasaimBotUpdater(api_token, class_id)

    def run_polling(self):
        # Start the Bot
        self._updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        self._updater.idle()

    def run_webhooks(self, base_url, port):
        self._updater.start_webhook(
            listen='0.0.0.0',
            port=port,
            url_path=self._api_token,
        )
        self._updater.bot.set_webhook(f'{base_url}/{self._api_token}')
