from slack_sdk.errors import SlackApiError


def update_message_financial(event, ack, logger, body, client):
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
                                             "block_id": "financial_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Cobranças"},
                                                           "style": "danger",
                                                           "action_id": "charging",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Projeto SAP"},
                                                           "style": "danger",
                                                           "action_id": "sap",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Renovação de Contrato"},
                                                           "style": "danger",
                                                           "action_id": "contract_renovation",
                                                           "url": "URL",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Atualizar Dados Financeiros"},
                                                           "style": "danger",
                                                           "action_id": "update_data_financial",
                                                           },
                                                           {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Comunicado de Protesto"},
                                                           "style": "danger",
                                                           "action_id": "protest_statement",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Nenhuma das Opções"},
                                                           "style": "danger",
                                                           "action_id": "financial_support",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")
