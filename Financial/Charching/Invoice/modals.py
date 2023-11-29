from slack_sdk.errors import SlackApiError
from functions import get_current_datetime, get_user_email, iuguNewTicket


def create_request_newInvoice(ack, body, logger, client):
    ack()
    name = body["user"]["id"]
    text = f"Olá <@{name}>! \n Insira abaixo o ID IUGU do boleto que deseja reemitir. 🚀 "
    try:
        modal = {
            "type": "modal",
            "callback_id": "send_request_ticketfinancial",
            "title": {
                "type": "plain_text",
                "text": "Reemissão de Boletos",
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
                    "text": "* - Boletos vencidos com mais de 10 dias não será possível reemitir por aqui.* \n * - Considere somente dias ÚTEIS na contagem, Ex: Se hoje é quinta, e você quer reemitir para terça, considere 3 dias*"
                  }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-ticket",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Ex: 06AF51CAAE6841208901665F6ECF7444"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "ID IUGU do Boleto:",
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-days",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Somente o número, Ex: 3"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Reemitir para quantos dias após a data atual:",
                    }
                },
            ],
        }
        client.views_open(trigger_id=body["trigger_id"], view=modal)
    except SlackApiError as e:
        logger.error(f"Error opening modal: {e.response}")


def handle_request_submission_ticketfinancial(ack, body, client):
    ack()
    name = body["user"]["id"]
    date = get_current_datetime()
    email = get_user_email(name)
    iugu_id = None
    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-ticket" in block_data:
            iugu_id = block_data["plain_text_input-ticket"]["value"]

    for block_id, block_data in body["view"]["state"]["values"].items():
        if "plain_text_input-days" in block_data:
            days = block_data["plain_text_input-days"]["value"]

    if iugu_id:
        generateNewTicket = iuguNewTicket(iugu_id, days, date, email)
        print(generateNewTicket)
        if "error" not in generateNewTicket:
            message = f"Segue novo boleto gerado: {generateNewTicket}"
            client.chat_postMessage(
                channel=name,
                text=message
            ),
        else:
            message = "Error generating new ticket."
            client.chat_postMessage(
                channel=name,
                text=message
            )
    else:
        print("Error generating new ticket: No valid ticket was found for this ID!")
