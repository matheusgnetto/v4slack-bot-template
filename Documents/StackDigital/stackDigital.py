from slack_sdk.errors import SlackApiError


def update_message_stackdigital(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}>, selecione a ferramenta onde voce possuí dúvidas sobre o processo.*"

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
                                            {"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": "*Stack Digital*"}},
                                            {"type": "actions",
                                             "block_id": "docs_suporte3",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Active Campaign"},
                                                           "action_id": "activecampaign",
                                                           "style": "danger",
                                                           "url": "URL"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Tray"},
                                                           "action_id": "tray",
                                                           "style": "danger",
                                                           "url": "URL"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Kommo"},
                                                           "action_id": "kommo",
                                                           "style": "danger",
                                                           "url": "URL"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Vindi"},
                                                           "action_id": "vindi",
                                                           "style": "danger",
                                                           "url": "URL"},
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Letalk"},
                                                           "action_id": "letalk",
                                                           "style": "danger",
                                                           "url": "URL"},
                                                          ]},
                                            ],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")
