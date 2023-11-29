from slack_sdk.errors import SlackApiError

from functions import addRowUserAction, get_user_email, start_webhook_workflow
from getUnit import get_user_unit


def update_message_education(event, ack, logger, body, client):
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
                                             "block_id": "docs_education",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Apollo"},
                                                           "action_id": "apollo",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Scout"},
                                                           "action_id": "scout",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Base de Conhecimento"},
                                                           "action_id": "knowledge_base",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Cursos V4 Academy"},
                                                           "action_id": "v4academy_access",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Acesso G4 Skills"},
                                                           "action_id": "g4skills_access",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Leadership"},
                                                           "action_id": "leadership",
                                                           "style": "danger"},
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "docs_education2",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Certificado de Atendimento"},
                                                           "action_id": "attendantment_cert",
                                                           "style": "danger"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Teste Nivelamento Cientista"},
                                                           "action_id": "scientist_test",
                                                           "url": "URL",
                                                           "style": "danger"},
                                                          ]},
                                            ],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_education_action(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text = f"*Investidor <@{name}>, o conteúdo apresentado conseguiu te ajudar?!*"
    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": text,
                                                      }},
                                            {"type": "actions",
                                             "block_id": "education_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Sim"},
                                                           "style": "primary",
                                                           "action_id": "education_yes",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Não"},
                                                           "style": "danger",
                                                           "action_id": "education_support",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")

def update_message_education_yes(event, ack, body, logger, client):
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

        area = "Education"
        action = "Sim"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_education_support(event, ack, body, logger, client):
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

        area = "Education"
        action = "Nao"
        addRowUserAction(area, email, action)
    except SlackApiError as e:
        logger.error(f"Error: {e}")


def handle_education_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "WEBHOOK_URL"

    update_message_education_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
