from slack_sdk.errors import SlackApiError

from functions import get_user_email, start_webhook_workflow
from getUnit import get_user_unit


def update_message_operations(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*Agora <@{name}>, selecione a área para obter suporte!*"

    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "actions",
                                             "block_id": "go_back",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": " ↩ Voltar ao Início"},
                                                           "action_id": "go_back",
                                                           },
                                                          ]},
                                            {"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": text_user}},
                                            {"type": "divider"},
                                            {"type": "actions",
                                             "block_id": "docs_operations",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Growth Advisory"},
                                                           "action_id": "growth_advisory",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Ekyte"},
                                                           "action_id": "ekyte",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Selos"},
                                                           "action_id": "stamps",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Certificações"},
                                                           "action_id": "certifications",
                                                           "style": "danger"},
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "docs_operations2",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Helpflag"},
                                                           "action_id": "helpflag",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "ROI Week"},
                                                           "action_id": "roi_week",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                           {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Education"},
                                                           "action_id": "education",
                                                           "style": "danger"},
                                                           {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Nenhuma das Opções"},
                                                           "action_id": "profit_support",
                                                           "style": "danger"},
                                                          ]},
                                            ],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")

def update_message_profit_support(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
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


def handle_profit_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "WEBHOOK_URL"

    update_message_profit_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
