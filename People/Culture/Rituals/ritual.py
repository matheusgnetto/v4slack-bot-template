from slack_sdk.errors import SlackApiError
from functions import get_user_email, start_webhook_workflow
from getUnit import get_user_unit


def update_message_culture_support(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    # Para o BOT responder em forma de thread.
    thread_ts = event.get("ts", None)
    # Text para o BOT enviar ao canal do HelpDesk a açao do usuário.
    name = body["user"]["id"]
    channel = "CHANNEL_ID"
    text_user = f"*<@{name}> Seu suporte está sendo iniciado, acesse este canal <#{channel}> que haverá um ticket com seu nome aguardando para que você envie sua solicitação!* 🚀"

    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts, blocks=[
                                        {
                                            "type": "section",
                                            "text": {
                                                "type": "mrkdwn",
                                                "text": text_user
                                            }
                                        },
                                    ], thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def handle_culture_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "WEBHOOK_URL"

    update_message_culture_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
