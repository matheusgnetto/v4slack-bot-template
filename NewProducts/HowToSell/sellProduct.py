from slack_sdk.errors import SlackApiError

def update_message_sell_product(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Selecione abaixo o item que voce precisa de suporte! 🚀*"

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
                                             "block_id": "financial_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Como usar a Planilha"},
                                                           "style": "danger",
                                                           "url": "URL"
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Objeções"},
                                                           "style": "danger",
                                                           "url": "URL",
                                                           "action_id": "product_objections",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")