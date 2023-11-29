from slack_sdk.errors import SlackApiError

from functions import query_graphql_for_case

class Cases:

    def update_message_cases(event, ack, body, logger, client):
        ack()
        event = body["message"]
        channel_id = body["channel"]["id"]
        thread_ts = event.get("ts", None)
        name = body["user"]["id"]
        text_user = f"*<@{name}> Selecione abaixo a opção sobre cases! 🚀*"

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
                                                                        "text": "Enviar Cases"},
                                                              "style": "danger",
                                                              "action_id": "send_cases",
                                                              },
                                                              {"type": "button",
                                                              "text": {"type": "plain_text",
                                                                        "text": "Consultar Cases"},
                                                              "style": "danger",
                                                              "action_id": "consult_cases",
                                                              },
                                                              ]}],
                                        thread_ts=thread_ts)
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error: {e}")


    def update_message_send_cases(event, ack, body, logger, client):
        ack()
        event = body["message"]
        channel_id = body["channel"]["id"]
        thread_ts = event.get("ts", None)
        name = body["user"]["id"]
        text = f"*<@{name}>, se prepare para a sua apresentação, siga abaixo o roteiro para produção do seu áudio.*"
        text_info = f"*Após ter lido o roteiro, grave e envie o seu áudio diretamente para mensagem direta comigo no privado.*"

        imgur_image_url = "IMAGE_URL"

        try:
            result = client.chat_update(
                channel=channel_id,
                ts=thread_ts,
                blocks=[
                    {
                        "type": "actions",
                        "block_id": "go_back",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": " ↩ Voltar ao Início"},
                                "action_id": "go_back",
                            },
                        ],
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": text},
                    },
                    {
                        "type": "actions",
                        "block_id": "case_info",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Roteiro"},
                                "style": "primary",
                                "url": "URL",
                                "action_id": "cases_production",
                            },
                        ],
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": text_info},
                    },
                    {
                        "type": "image",
                        "block_id": "case_image",
                        "image_url": imgur_image_url,
                        "alt_text": "Descrição da imagem",
                    },
                ],
                thread_ts=thread_ts,
            )
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error: {e}")
    

    def create_request_search_case(ack, body, logger, client):
        ack()
        name = body["user"]["id"]
        text = f"Olá <@{name}>! \n Aqui você vai indicar a área que deseja consultar os cases!"
        try:
            modal = {
                "type": "modal",
                "callback_id": "send_request_search_case",
                "title": {
                    "type": "plain_text",
                    "text": "Selecionar a Área",
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
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Selecione a Área",
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Advocacia",
                                },
                                "value": "advocacia"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "B2B",
                                },
                                "value": "b2b"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Educação",
                                },
                                "value": "educacao"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Energia Solar",
                                },
                                "value": "energia_solar"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Franqueado",
                                },
                                "value": "franqueado"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Imobiliária | Construção Civil",
                                },
                                "value": "imobiliaria_civil"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Odontologia",
                                },
                                "value": "odontologia"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Outros",
                                },
                                "value": "outros"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Saúde",
                                },
                                "value": "saude"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Serviço de Alimentação",
                                },
                                "value": "saude"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Serviço Financeiro",
                                },
                                "value": "servico_financeiro"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Telecom",
                                },
                                "value": "telecom"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Turismo",
                                },
                                "value": "turismo"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Varejo",
                                },
                                "value": "varejo"
                            },
                        ],
                        "action_id": "static_select-case"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Selecione o Case",
                    }
                } 
                ],
            }
            client.views_open(trigger_id=body["trigger_id"], view=modal)
        except SlackApiError as e:
            logger.error(f"Error opening modal: {e.response}")
    

    def handle_request_submission_search_case(event, ack, body, logger, client):
        ack()
        user_id = body["user"]["id"]
        selected_case = None
        for block_id, block_data in body["view"]["state"]["values"].items():
            if "static_select-case" in block_data:
                selected_option = block_data["static_select-case"]["selected_option"]
                selected_case = selected_option["text"]["text"]

        cases_data = query_graphql_for_case(selected_case)
        
        if cases_data:
          try:
              messages = [f"*{case['title']}*\nURL: {case['uri']}" for case in cases_data]
              if len(cases_data) < 5:
                  messages.append("Não há mais cases disponíveis para a área selecionada.")
              message = "\n\n".join(messages)
              client.chat_postMessage(channel=user_id, text=message)
          except SlackApiError as e:
              logger.error(f"Erro ao enviar mensagem: {e.response}")
        elif not cases_data:
            client.chat_postMessage(channel=user_id, text="Nenhum case encontrado para a seleção.")