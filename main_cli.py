import argparse
from handasaim_bot import HandasaimBot


def start_polling(bot, _):
    bot.run_polling()


def start_webhooks(bot, args):
    bot.run_webhooks(args.url, args.port)


def parse_arguments(args=None):
    parser = argparse.ArgumentParser()

    parser.set_defaults(func=start_polling)

    parser.add_argument('-a', '--api_token',
                        metavar='TELEGRAM_BOT_API_KEY',
                        required=True)

    parser.add_argument('-c', '--class_id',
                        required=True)

    subparsers = parser.add_subparsers()
    webhooks_parser = subparsers.add_parser('webhooks', aliases=['wh'], help='use webhooks instead of polling')
    webhooks_parser.add_argument('url')
    webhooks_parser.add_argument('port', type=int)
    webhooks_parser.set_defaults(func=start_webhooks)

    return parser.parse_args(args)


def main(args=None):
    args = parse_arguments(args)
    bot = HandasaimBot(args.api_token, args.class_id)
    args.func(bot, args)


if __name__ == "__main__":
    main()
