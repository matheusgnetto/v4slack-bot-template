from slack_sdk.errors import SlackApiError
from functions import get_user_email, start_webhook_workflow
from getUnit import get_user_unit

def update_message_cs(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Selecione abaixo a opção que voce precisa de suporte! 🚀*"

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
                                            {"type": "actions",
                                             "block_id": "cs_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Treinamento para o meu CS"},
                                                           "style": "danger",
                                                           "action_id": "cs_training",
                                                           }
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "cs_support1",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Dúvidas Jornada da Retenção"},
                                                           "style": "danger",
                                                           "url": "URL",
                                                           "action_id": "cs_retention",
                                                           }
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "cs_support2",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Dúvidas Tratativas em Andamento"},
                                                           "style": "danger",
                                                           "action_id": "cs_dealings",
                                                           },
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "cs_support3",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Ajuda do CS para Tratativa"},
                                                           "style": "danger",
                                                           "action_id": "cs_help",
                                                           }
                                                          ]},
                                            {"type": "actions",
                                             "block_id": "cs_support4",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Problemas com Distrato"},
                                                           "style": "danger",
                                                           "action_id": "cs_problem",
                                                           }
                                                          ]}
                                                          ],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_csproblem_support(event, ack, body, logger, client):
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


def handle_csproblem_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]

    webhook_url = "WEBHOOK_URL"

    update_message_csproblem_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
