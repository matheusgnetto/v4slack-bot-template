from slack_sdk.errors import SlackApiError

from functions import addRowUserAction, get_user_email, start_webhook_workflow
from getUnit import get_user_unit


def update_message_architecture(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}>, Clique abaixo e envie seus projetos para análise e esclareça dúvidas gerais sobre a arquitetura e branding da sua unidade!*"

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
                                             "block_id": "architecture",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Assessoria de Arquitetura"},
                                                           "action_id": "architecture_action",
                                                           "url": "URL",
                                                           "style": "primary"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Solicitação de Projetos"},
                                                           "action_id": "architecture_project",
                                                           "url": "URL",
                                                           "style": "primary"},
                                                          ]},
                                            ],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_architecture_action(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text = f"*Investidor <@{name}>, seu problema/dúvida foi resolvido pelo formulário?!*"
    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": text,
                                                      }},
                                            {"type": "actions",
                                             "block_id": "architecture_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Sim"},
                                                           "style": "primary",
                                                           "action_id": "architecture_yes",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Não"},
                                                           "style": "danger",
                                                           "action_id": "architecture_no",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")

def update_message_architecture_yes(event, ack, body, logger, client):
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

        area = "Facilities"
        action = "Sim"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_architecture_support(event, ack, body, logger, client):
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
        
        area = "Facilities"
        action = "Nao"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def handle_architecture_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "WEBHOOK_URL"

    update_message_architecture_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
