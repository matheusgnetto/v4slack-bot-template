from slack_sdk.errors import SlackApiError

from functions import get_user_email, start_webhook_leadflow, start_webhook_workflow


def update_message_lead_update(event, ack, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Selecione abaixo a opção que você precisa de suporte! 🚀*"

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
                                             "block_id": "leadbroker_support",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Avançar Fase"},
                                                           "style": "danger",
                                                           "action_id": "phase_advance",
                                                           },
                                                           {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Adicionar Comentário"},
                                                           "style": "danger",
                                                           "action_id": "add_comment",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def create_request_lead_update_phase(ack, body, logger, client):
    ack()
    name = body["user"]["id"]
    text = f"Olá <@{name}>! \n Insira as informações do Lead abaixo! "
    try:
        modal = {
            "type": "modal",
            "callback_id": "send_request_lead_update_phase",
            "title": {
                "type": "plain_text",
                "text": "Avançar Fase de Lead",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-lead_name",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Razão Social"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Razão Social do Lead",
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Selecione a Fase",
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Desqualificado",
                                },
                                "value": "desqualificado"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Em contato",
                                },
                                "value": "em_contato"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Contato Agendado",
                                },
                                "value": "contato_agendado"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Qualificar",
                                },
                                "value": "qualificar"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Agendamento",
                                },
                                "value": "agendamento"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Pronto para reunião",
                                },
                                "value": "pronto_para_reuniao"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "NoShow",
                                },
                                "value": "noshow"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Convertido/Oportunidade",
                                },
                                "value": "convertido_oportunidade"
                            },
                        ],
                        "action_id": "static_select-phase"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Label",
                    }
                }
            ],
        }
        client.views_open(trigger_id=body["trigger_id"], view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response}")


def handle_request_submission_update_phase(event, ack, body, logger, client):
    ack()
    user_id = body["user"]["id"]
    lead = None
    fase_destino = None
    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-lead_name" in block_data:
            lead = block_data["plain_text_input-lead_name"]["value"]
        if "static_select-phase" in block_data:
            selected_option = block_data["static_select-phase"]["selected_option"]
            fase_destino = selected_option["text"]["text"]

    webhook_url = "WEBHOOK_URL"

    email = get_user_email(user_id)
    start_webhook_leadflow(webhook_url, lead, user_id, email, fase_destino)


def create_request_lead_add_comment(ack, body, logger, client):
    ack()
    name = body["user"]["id"]
    text = f"Olá <@{name}>! \n Insira o comentário sobre o Lead abaixo! "
    try:
        modal = {
            "type": "modal",
            "callback_id": "send_request_lead_add_coment",
            "title": {
                "type": "plain_text",
                "text": "Comentário sobre Lead",
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-add_comment_name",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Razão Social do Lead",
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-add_comment",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Insira o Comentário",
                    }
                },
                
            ],
        }
        client.views_open(trigger_id=body["trigger_id"], view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response}")


def handle_request_submission_add_comment(event, ack, body, logger, client):
    ack()
    user_id = body["user"]["id"]
    lead = None
    comment = None
    fase_destino = None
    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-add_comment_name" in block_data:
            lead = block_data["plain_text_input-add_comment_name"]["value"]
        if "plain_text_input-add_comment" in block_data:
            comment = block_data["plain_text_input-add_comment"]["value"]
        

    webhook_url = "WEBHOOK_URL"

    email = get_user_email(user_id)
    start_webhook_leadflow(webhook_url, lead, user_id, email, comment=comment, fase_destino=None)