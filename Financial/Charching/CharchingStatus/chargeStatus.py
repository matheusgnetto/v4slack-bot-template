from slack_sdk.errors import SlackApiError
from functions import addRowUserChargesConsult, addRowUserChargesStatus, get_current_datetime, get_user_email, start_webhook_workflow
from getCharges import get_charges
from getUnit import get_user_unit


def create_request_charges_consult(ack, body, logger, client):
    ack()
    name = body["user"]["id"]
    text = f"Olá <@{name}>! \n Consulte aqui o status da cobrança do seu cliente!"
    try:
        modal = {
            "type": "modal",
            "callback_id": "send_request_charges_consult",
            "title": {
                "type": "plain_text",
                "text": "Consulta de Cobranças",
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
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Insira o ID do Cliente do Lab Financeiro (Numérico)*"
                  }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-client_id",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "12345"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "ID do Cliente",
                    }
                },
            ],
        }
        client.views_open(trigger_id=body["trigger_id"], view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response}")


def handle_request_submission_client_consult(ack, body, client):
    ack()
    name = body["user"]["id"]
    date = get_current_datetime()
    email = get_user_email(name)
    client_id = None
    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-client_id" in block_data:
            client_id = block_data["plain_text_input-client_id"]["value"]
    
    if client_id:
        chargesConsult = get_charges(client_id)
        if "error" not in chargesConsult:
            message = f"{chargesConsult}"
            client.chat_postMessage(
                channel=name,
                text=message
            ),
            addRowUserChargesConsult(date, email, client_id)
        else:
            message = "Error consulting this client"
            client.chat_postMessage(
                channel=name,
                text=message
            )
    else:
        print("Error consulting this client: ClientID is invalid!")

def update_message_charges_feedback(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    text_user = f"*<@{name}> Após enviado o ID, consultarei o status de cobrança e enviarei uma mensagem com o resultado.* \n*Você obteve ajuda pela minha resposta?*"

    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "section",
                                             "text": {"type": "mrkdwn",
                                                      "text": text_user}},
                                            {"type": "divider"},
                                            {"type": "actions",
                                             "block_id": "submitBlock",
                                             "elements": [{"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Sim"},
                                                           "style": "primary",
                                                           "action_id": "charges_status_yes",
                                                           },
                                                          {"type": "button",
                                                           "text": {"type": "plain_text",
                                                                    "text": "Não"},
                                                           "style": "danger",
                                                           "action_id": "charges_status_no",
                                                           },
                                                          ]}],
                                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")


def update_message_charges_yes(event, ack, body, logger, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    name = body["user"]["id"]
    value = "Sim"
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

        email = get_user_email(name)
        date = get_current_datetime()
        addRowUserChargesStatus(date, email, value)

    except SlackApiError as e:
        logger.error(f"Error: {e}")

def update_message_charges_support(event, ack, body, logger, client):
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

def handle_charges_support(event, ack, body, logger, client):
    ack()

    user_id = body["user"]["id"]
    value = "Não"

    webhook_url = "WEBHOOK_URL"

    update_message_charges_support(event, ack, body, logger, client)
    user_email = get_user_email(user_id)
    unit = get_user_unit(user_email)
    start_webhook_workflow(webhook_url, user_id, unit)
    email = get_user_email(user_id)
    date = get_current_datetime()
    addRowUserChargesStatus(date, email, value)
