from slack_sdk.errors import SlackApiError


def update_message_lookingahead(event, ack, logger, body, client):
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
                                             "block_id": "looking_ahead_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Infos"},
                                                           "style": "danger",
                                                           "action_id": "la_infos",
                                                           "url": "URL"
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Comprar Ingressos"},
                                                           "style": "danger",
                                                           "action_id": "la_buy_tickets",
                                                           "url": "URL"
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")
