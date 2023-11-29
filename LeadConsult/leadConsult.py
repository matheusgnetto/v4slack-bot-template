from slack_sdk.errors import SlackApiError
from functions import addRowUserLeadConsult, formatar_cnpj, get_current_datetime, get_user_email
from getCnpj import get_cnpj


def create_request_leadconsult(ack, body, logger, client):
    ack()
    name = body["user"]["id"]
    text = f"Olá <@{name}>! \n Insira abaixo o CNPJ do seu lead para verificar na nossa base de dados! "
    try:
        modal = {
            "type": "modal",
            "callback_id": "send_request_lead_consult",
            "title": {
                "type": "plain_text",
                "text": "Consulta de Lead",
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
                    "text": "*Insira somente números, no formato 00.000.000/0000-00 ou 00000000000000*"
                  }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-cnpj",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "00.000.000/0000-00"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "CNPJ do Lead",
                    }
                },
            ],
        }
        client.views_open(trigger_id=body["trigger_id"], view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response}")


def handle_request_submission_leadconsult(ack, body, client):
    ack()
    name = body["user"]["id"]
    date = get_current_datetime()
    email = get_user_email(name)
    cnpj = None
    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-cnpj" in block_data:
            cnpj = block_data["plain_text_input-cnpj"]["value"]
    
    cleaned_cnpj = cnpj.replace('-', '').replace('/', '').replace('.', '')
    formatted_cnpj = formatar_cnpj(cnpj)

    if cnpj:
        leadConsult = get_cnpj(cleaned_cnpj, formatted_cnpj)
        if "error" not in leadConsult:
            message = f"{formatted_cnpj}: {leadConsult}"
            client.chat_postMessage(
                channel=name,
                text=message
            ),
            addRowUserLeadConsult(date, email, cnpj, leadConsult)
        else:
            message = "Error consulting this lead"
            client.chat_postMessage(
                channel=name,
                text=message
            )
    else:
        print("Error consulting this lead: CNPJ is invalid!")


