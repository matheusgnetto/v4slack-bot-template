from slack_sdk.errors import SlackApiError

from functions import addRowUserAction, get_user_email, start_webhook_workflow
from getUnit import get_user_unit


def update_message_certification(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Selecione abaixo a opção que voce precisa de suporte! 🚀*"

    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": text_user}},
                                            {"type": "actions",
                                             "block_id": "certification_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Dúvidas sobre Certificações"},
                                                           "style": "danger",
                                                           "url": "URL",
                                                           "action_id": "certification_questions",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Enviar Certificação"},
                                                           "style": "danger",
                                                           "url": "URL",
                                                           "action_id": "certification_request",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_certifications_questions(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Sua dúvida foi resolvida pelo meu conteúdo apresentado?*"

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
                                        {
                                            "type": "divider"
                                        },
                                        {
                                            "type": "actions",
                                            "block_id": "submitBlock",
                                            "elements": [
                                                {
                                                    "type": "button",
                                                    "text": {
                                                        "type": "plain_text",
                                                        "text": "Sim"
                                                    },
                                                    "style": "primary",
                                                    "action_id": "certs_yes",
                                                },
                                                {
                                                    "type": "button",
                                                    "text": {
                                                        "type": "plain_text",
                                                        "text": "Não"
                                                    },
                                                    "style": "danger",
                                                    "action_id": "certs_no",
                                                },

                                            ]}
                                    ], thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_certification_yes(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    email = get_user_email(name)
    text_user = f"*Fico feliz em te ajudar <@{name}>!* \n *Sempre que precisar basta me acionar novamente.* 🚀 "
    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts, blocks=[
                                        {
                                            "type": "section",
                                            "text": {
                                                "type": "mrkdwn",
                                                "text": text_user,
                                            }
                                        },
                                    ], thread_ts=thread_ts)
        logger.info(result)

        area = "Certificaçoes"
        action = "Sim"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_certification_support(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    email = get_user_email(name)
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
        
        area = "Certificaçoes"
        action = "Nao"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def handle_certification_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "CHANNEL_ID"

    update_message_certification_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
