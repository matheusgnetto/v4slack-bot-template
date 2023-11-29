import os
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from dotenv import load_dotenv


from Architecture.architecture import handle_architecture_support, update_message_architecture, update_message_architecture_action, update_message_architecture_yes
from Cases.cases import Cases
from Churn.churn import update_message_churn, update_message_churn_conditional, update_message_churn_incubadora, update_message_churn_proccess_yes, update_message_incubadora, update_message_incubadora_ticket
from Compliance.compliance import handle_compliance_support, update_message_compliance, update_message_compliance_action
from CustomerSuccess.Care.care import handle_care_support
from CustomerSuccess.CsTraining.csTraining import handle_cstraining_support
from CustomerSuccess.Retention.journeyRetention import handle_retention_support, update_message_retention_csat, update_message_retention_yes
from CustomerSuccess.cs import handle_csproblem_support, update_message_cs
from DataTech.dataTech import handle_datatech_support, update_message_datatech_action, update_message_techdata
from Documents.StackDigital.stackDigital import update_message_stackdigital
from Farmer.farmerSupport import handle_farmer_support, update_message_farmer, update_message_farmer_action, update_message_farmer_yes
from Financial.Charching.CharchingStatus.chargeStatus import create_request_charges_consult, handle_charges_support, handle_request_submission_client_consult, update_message_charges_feedback, update_message_charges_yes
from Financial.Charching.CreditCard.credit import handle_credit_action
from Financial.Charching.charges import handle_invoice_support, update_message_charges_action, update_message_charging, update_message_fee_support, update_message_fee_yes, update_message_invoice_csat, update_message_invoice_ticket_action, update_message_invoice_yes
from Financial.Contracts.renewContracts import update_message_contracts_support
from Financial.FinancialData.updateClients import handle_financialdata_support, update_message_financialdata
from Financial.FinancialSupport.financialSupport import handle_financial_support
from Financial.SapTeam.sap import handle_sap_action
from Financial.Charching.Invoice.conditionals import update_message_financial_bad, update_message_financial_good
from Financial.financial import update_message_financial
from Financial.Charching.Invoice.modals import create_request_newInvoice, handle_request_submission_ticketfinancial
from LeadConsult.leadConsult import create_request_leadconsult, handle_request_submission_leadconsult
from LookingAhead.lookingAhead import update_message_lookingahead
from NewProducts.HowToSell.sellProduct import update_message_sell_product
from NewProducts.newProducts import handle_product_support, update_message_product_yes, update_message_products, update_message_products_action
from Operations.Certifications.certification import handle_certification_support, update_message_certification, update_message_certification_yes, update_message_certifications_questions
from Operations.Education.Certification.attendantment import update_message_attendantment
from Operations.Education.KnowledgeBase.knowledgeBase import update_message_knowledge_base
from Operations.Education.Leadership.leadership import update_message_leadership
from Operations.Education.education import handle_education_support, update_message_education, update_message_education_action, update_message_education_yes
from Operations.Ekyte.ekyte import handle_ekyte_support, update_message_ekyte, update_message_ekyte_questions, update_message_ekyte_yes
from Operations.Helpflag.helpflag import handle_helpflag_support, update_message_helpflag, update_message_helpflag_yes
from Operations.RoiWeek.roiWeek import handle_roiweek_support, update_message_roiweek, update_message_roiweek_yes
from Operations.Stamps.stamps import handle_stamps_support, update_message_stamps, update_message_stamps_questions, update_message_stamps_yes
from Operations.GrowthAdvisory.growthAdvisory import handle_wor_support, update_message_wor, update_message_wor_action
from Operations.operations import handle_profit_support, update_message_operations
from People.Culture.Investor.investorProblem import handle_investorproblem_support
from People.Culture.Rituals.ritual import handle_culture_support
from People.Culture.culture import update_message_culture
from People.Hiring.hiring import handle_hiring_support, update_message_hiring, update_message_hiring_action, update_message_hiring_yes
from People.people import handle_peoplebp_support, update_message_new_access, update_message_people
from Documents.Tools.conditionals import update_message_nao, update_message_sim
from Documents.Tools.helpdesk import update_message_helpdesk
from Documents.Tools.tools import update_message_ferramentas
from Sales.Brokers.Lead.lead import create_request_lead_add_comment, create_request_lead_update_phase, handle_request_submission_add_comment, handle_request_submission_update_phase, update_message_lead_update
from Sales.Brokers.Leadbroker.leadbroker import handle_leadbroker_support, update_message_leadbroker, update_message_leadbroker_action, update_message_leadbroker_yes
from Sales.Brokers.Meetingbroker.meetingbroker import handle_meetingbroker_support, update_message_meetingbroker, update_message_meetingbroker_action, update_message_meetingbroker_ask_help, update_message_meetingbroker_help, update_message_meetingbroker_yes
from Sales.Brokers.brokers import update_message_broker_action, update_message_broker_yes, update_message_brokers
from Sales.sales import update_message_sales_services
from Slack.slack import handle_slack_support, update_message_slack, update_message_slack_action, update_message_slack_link, update_message_slack_problem, update_message_slack_ws_problem
from functions import process_audio

load_dotenv()

# Ler variáveis de ambiente
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
signing_secret = os.getenv("SIGNING_SECRET")

# Inicializar o app Slack
app = App(
    token=slack_bot_token,
    signing_secret=signing_secret
)

def handle_file_created(ack, body, say):
    ack()
    
    files = body["event"]["files"]
    user_id = body["event"]["user"]
    
    for file_info in files:
        file_id = file_info["id"]
        process_audio(file_id, user_id)
        say(f"Recebemos o seu áudio! Em até 15 minutos você receberá no privado o case que geramos.")

@app.event("message")
def handle_some_mention(event, ack, say, logger, body):
    if event.get("channel_type") == "im" and "files" in body["event"]:
        handle_file_created(ack, body, say)
    bot = "USER_ID"
    if (
        event.get("channel_type") == "im" and not "files" in body["event"]
        or f"<@{bot}>" in event.get("text", "")
    ):
        ack()
        user = event["user"]
        text = f"*Olá <@{user}>* 👋\n \n *Confira o conteúdo disponível na base de conhecimento e se necessário, selecione a opção na qual você necessita de suporte da matriz!* \n"
        event = body["event"]
        thread_ts = event.get("thread_ts", None) or event["ts"]
        logger.info(say(blocks=[{"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": text}},
                                {"type": "divider"},
                                {"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": "*Base de Conhecimento*  :v4company:"}},
                                {"type": "actions",
                                 "block_id": "entrada",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Acessar"},
                                               "action_id": "base_conhecimento",
                                               "style": "danger",
                                               "url": "URL"
                                               },
                                              ]},
                                {"type": "divider"},
                                {"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": "*Suporte* 🤝"}},
                                {"type": "actions",
                                 "block_id": "suportes",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Operação"},
                                               "action_id": "operations",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Data & Tech"},
                                               "action_id": "datatech",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Financeiro"},
                                               "action_id": "financial",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Compliance"},
                                               "action_id": "compliance",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Customer Success"},
                                               "action_id": "cs",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Farmer"},
                                               "action_id": "farmer",
                                               "style": "primary"},
                                              ]},
                                {"type": "actions",
                                 "block_id": "suportes1",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "People & Performance"},
                                               "action_id": "people",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Projetos Arquitetônicos"},
                                               "action_id": "architecture",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Ferramentas"},
                                               "action_id": "ferramentas",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Nova Produtização"},
                                               "action_id": "products",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Sinalizar Tratativa"},
                                               "action_id": "churn",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Consultar Lead"},
                                               "action_id": "leadconsult",
                                               "style": "primary"},
                                              ]},
                                {"type": "actions",
                                 "block_id": "suportes2",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Vendas"},
                                               "action_id": "sales_services",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Problemas com Slack"},
                                               "action_id": "slack",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Cases"},
                                               "action_id": "cases",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "LookingAhead 2024"},
                                               "action_id": "looking_ahead",
                                               "style": "primary"},
                                              ]}],
                        thread_ts=thread_ts))


@app.action("go_back")
def update_message(event, ack, say, logger, body, client):
    ack()
    event = body["message"]
    channel_id = body["channel"]["id"]
    thread_ts = event.get("ts", None)
    user = body["user"]["id"]
    text = f"*Olá <@{user}>* 👋\n \n *Confira o conteúdo disponível na base de conhecimento e se necessário, selecione a opção na qual você necessita de suporte da matriz!* \n"
    
    try:
        result = client.chat_update(channel=channel_id,
                                    ts=thread_ts,
                                    blocks=[{"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": text}},
                                {"type": "divider"},
                                {"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": "*Base de Conhecimento*  :v4company:"}},
                                {"type": "actions",
                                 "block_id": "entrada",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Acessar"},
                                               "action_id": "base_conhecimento",
                                               "style": "danger",
                                               "url": "URL"
                                               },
                                              ]},
                                {"type": "divider"},
                                {"type": "section",
                                 "text": {"type": "mrkdwn",
                                          "text": "*Suporte* 🤝"}},
                                {"type": "actions",
                                 "block_id": "suportes",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Operação"},
                                               "action_id": "operations",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Data & Tech"},
                                               "action_id": "datatech",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Financeiro"},
                                               "action_id": "financial",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Compliance"},
                                               "action_id": "compliance",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Customer Success"},
                                               "action_id": "cs",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Farmer"},
                                               "action_id": "farmer",
                                               "style": "primary"},
                                              ]},
                                {"type": "actions",
                                 "block_id": "suportes1",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "People & Performance"},
                                               "action_id": "people",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Projetos Arquitetônicos"},
                                               "action_id": "architecture",
                                               "style": "primary"},
                                                      {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Ferramentas"},
                                               "action_id": "ferramentas",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Nova Produtização"},
                                               "action_id": "products",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Sinalizar Tratativa"},
                                               "action_id": "churn",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Consultar Lead"},
                                               "action_id": "leadconsult",
                                               "style": "primary"},
                                              ]},
                                {"type": "actions",
                                 "block_id": "suportes2",
                                 "elements": [{"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Vendas"},
                                               "action_id": "sales_services",
                                               "style": "primary"},
                                              {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Problemas com Slack"},
                                               "action_id": "slack",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "Cases"},
                                               "action_id": "cases",
                                               "style": "primary"},
                                               {"type": "button",
                                               "text": {"type": "plain_text",
                                                        "text": "LookingAhead 2024"},
                                               "action_id": "looking_ahead",
                                               "style": "primary"},
                                              ]}],             
                    thread_ts=thread_ts)
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error: {e}")



# Structure 1


@app.action("ferramentas")
def update_message(event, ack, say, logger, body, client):
    return update_message_ferramentas(event, ack, say, logger, body, client)


@app.action("stack_digital")
def update_message(event, ack, logger, body, client):
    return update_message_stackdigital(event, ack, logger, body, client)


@app.action("operations")
def update_message(event, ack, logger, body, client):
    return update_message_operations(event, ack, logger, body, client)


@app.action("people")
def update_message(event, ack, logger, body, client):
    return update_message_people(event, ack, logger, body, client)


@app.action("architecture")
def update_message(event, ack, logger, body, client):
    return update_message_architecture(event, ack, logger, body, client)


@app.action("financial")
def update_message(event, ack, logger, body, client):
    return update_message_financial(event, ack, logger, body, client)


@app.action("compliance")
def update_message(event, ack, logger, body, client):
    return update_message_compliance(event, ack, logger, body, client)


@app.action("cs")
def update_message(event, ack, logger, body, client):
    return update_message_cs(event, ack, logger, body, client)


@app.action("datatech")
def update_message(event, ack, logger, body, client):
    return update_message_techdata(event, ack, logger, body, client)


@app.action("products")
def update_message(event, ack, logger, body, client):
    return update_message_products(event, ack, logger, body, client)


@app.action("churn")
def update_message(event, ack, logger, body, client):
    return update_message_churn(event, ack, body, logger, client)


@app.action("slack")
def update_message(event, ack, logger, body, client):
    return update_message_slack(event, ack, logger, body, client)


@app.action("sales_services")
def update_message(event, ack, logger, body, client):
    return update_message_sales_services(event, ack, logger, body, client)


@app.action("looking_ahead")
def update_message(event, ack, logger, body, client):
    return update_message_lookingahead(event, ack, logger, body, client)



# Structure 2


@app.action("protest_statement")
@app.action("credit_card")
def handle_some_action(event, ack, body, logger, client):
    return handle_credit_action(event, ack, body, logger, client)


@app.action("culture")
def update_message(event, ack, logger, body, client):
    return update_message_culture(event, ack, logger, body, client)


@app.action("charging")
def update_message(event, ack, logger, body, client):
    return update_message_charging(event, ack, logger, body, client)


@app.action("knowledge_base")
def update_message(event, ack, logger, body, client):
    return update_message_knowledge_base(event, ack, logger, body, client)


@app.action("farmer")
def update_message(event, ack, logger, body, client):
    return update_message_farmer(event, ack, logger, body, client)


@app.action("leadership")
def update_message(event, ack, logger, body, client):
    return update_message_leadership(event, ack, logger, body, client)


@app.action("education")
def update_message(event, ack, logger, body, client):
    return update_message_education(event, ack, logger, body, client)


@app.action("helpdesk")
def update_message(event, ack, body, logger, client):
    return update_message_helpdesk(event, ack, body, logger, client)


@app.action("stamps")
def update_message(event, ack, logger, body, client):
    return update_message_stamps(event, ack, logger, body, client)


@app.action("helpflag")
def update_message(event, ack, logger, body, client):
    return update_message_helpflag(event, ack, logger, body, client)


@app.action("roi_week")
def update_message(event, ack, logger, body, client):
    return update_message_roiweek(event, ack, logger, body, client)


@app.action("stamps_request")
@app.action("stamps_questions")
def update_message(event, ack, logger, body, client):
    return update_message_stamps_questions(event, ack, logger, body, client)


@app.action("ekyte")
def update_message(event, ack, logger, body, client):
    return update_message_ekyte(event, ack, logger, body, client)


@app.action("certifications")
def update_message(event, ack, logger, body, client):
    return update_message_certification(event, ack, logger, body, client)


@app.action("ekyte_request")
def update_message(event, ack, logger, body, client):
    return update_message_ekyte_questions(event, ack, logger, body, client)


@app.action("certification_request")
@app.action("certification_questions")
def update_message(event, ack, logger, body, client):
    return update_message_certifications_questions(
        event, ack, logger, body, client)


@app.action("compliance_action1")
@app.action("compliance_action2")
@app.action("compliance_action3")
def update_message(event, ack, logger, body, client):
    return update_message_compliance_action(event, ack, body, logger, client)


@app.action("growth_advisory")
def update_message(event, ack, logger, body, client):
    return update_message_wor(event, ack, logger, body, client)


@app.action("wor_action1")
@app.action("wor_action2")
def update_message(event, ack, logger, body, client):
    return update_message_wor_action(event, ack, body, logger, client)

@app.action("scientist_test")
@app.action("attendant_subscription")
@app.action("attendantment_access")
@app.action("knowledge_first_access")
@app.action("knowledge_access")
@app.action("leadership_sub")
@app.action("leadership_customer")
@app.action("g4skills_access")
@app.action("v4academy_access")
@app.action("scout")
@app.action("apollo")
def update_message(event, ack, logger, body, client):
    return update_message_education_action(event, ack, body, logger, client)


@app.action("attendantment_cert")
def update_message(event, ack, logger, body, client):
    return update_message_attendantment(event, ack, logger, body, client)

@app.action("product_objections")
@app.action("product_spreadsheet")
@app.action("other_doubts")
@app.action("pricing")
def update_message(event, ack, logger, body, client):
    return update_message_products_action(event, ack, body, logger, client)


@app.action("how_to_sell")
def update_message(event, ack, logger, body, client):
    return update_message_sell_product(event, ack, logger, body, client)


@app.action("farmer_question")
@app.action("farmer_v4x")
def update_message(event, ack, logger, body, client):
    return update_message_farmer_action(event, ack, body, logger, client)


@app.action("access_gupy")
@app.action("candidate_approval")
@app.action("open_vacancy")
def update_message(event, ack, logger, body, client):
    return update_message_hiring_action(event, ack, body, logger, client)


@app.action("architecture_project")
@app.action("architecture_action")
def update_message(event, ack, logger, body, client):
    return update_message_architecture_action(event, ack, body, logger, client)


@app.action("service_desk")
def update_message(event, ack, logger, body, client):
    return update_message_datatech_action(event, ack, body, logger, client)


@app.action("cs_retention")
def update_message(event, ack, logger, body, client):
    return update_message_retention_csat(event, ack, body, logger, client)


@app.action("hiring")
def update_message(event, ack, logger, body, client):
    return update_message_hiring(event, ack, logger, body, client)


@app.action("update_data_financial")
def update_message(event, ack, logger, body, client):
    return update_message_financialdata(event, ack, body, logger, client)


@app.action("slack_access_problem")
def update_message(event, ack, logger, body, client):
    return update_message_slack_problem(event, ack, logger, body, client)


@app.action("slack_redev4_ws")
def update_message(event, ack, body, logger, client):
    return update_message_slack_link(event, ack, body, logger, client)


@app.action("slack_all_ws")
@app.action("slack_my_ws")
def update_message(event, ack, logger, body, client):
    return update_message_slack_ws_problem(event, ack, logger, body, client)

@app.action("slack_paid_user")
@app.action("slack_new_paid_user")
def update_message(event, ack, body, logger, client):
    return update_message_slack_action(event, ack, body, logger, client)


@app.action("slack_other")
@app.action("slack_find_ws")
@app.action("slack_error_403")
@app.action("slack_adm_approve")
@app.action("slack_expired_link")
def update_message(event, ack, body, logger, client):
    return handle_slack_support(event, ack, body, logger, client)


@app.action("sales_brokers")
def update_message(event, ack, logger, body, client):
    return update_message_brokers(event, ack, logger, body, client)


@app.action("sales_leadbroker")
def update_message(event, ack, logger, body, client):
    return update_message_leadbroker(event, ack, logger, body, client)


@app.action("leadbroker_lost")
@app.action("leadbroker_playbook")
def update_message(event, ack, body, logger, client):
    return update_message_leadbroker_action(event, ack, body, logger, client)

@app.action("sales_leadbroker_access")
def update_message(event, ack, body, logger, client):
    return update_message_broker_action(event, ack, body, logger, client)


@app.action("sales_meetingbroker")
def update_message(event, ack, logger, body, client):
    return update_message_meetingbroker(event, ack, logger, body, client)


@app.action("meetingbroker_lost")
@app.action("meetingbroker_playbook")
def update_message(event, ack, body, logger, client):
    return update_message_meetingbroker_action(event, ack, body, logger, client)


@app.action("meetingbroker_help")
def update_message(event, ack, body, logger, client):
    return update_message_meetingbroker_ask_help(event, ack, body, logger, client)


@app.action("fee_exemption")
@app.action("fee_discount")
def update_message(event, ack, body, logger, client):
    return update_message_charges_action(event, ack, body, logger, client)


@app.action("invoice_ticket")
def update_message(event, ack, body, logger, client):
    return update_message_invoice_ticket_action(event, ack, body, logger, client)


@app.action("cases")
def update_message(event, ack, body, logger, client):
    return Cases.update_message_cases(event, ack, body, logger, client)


@app.action("send_cases")
def update_message(event, ack, body, logger, client):
    return Cases.update_message_send_cases(event, ack, body, logger, client)


@app.action("update_lead")
def update_message(event, ack, logger, body, client):
    return update_message_lead_update(event, ack, logger, body, client)


# Modals


@app.action("open_modal_ticketfinancial")
def create_request(event, ack, body, logger, client):
    return create_request_newInvoice(
        ack, body, logger, client), update_message_invoice_csat(
        event, ack, body, logger, client)


@app.action("leadconsult")
def create_request(ack, body, logger, client):
    return create_request_leadconsult(
        ack, body, logger, client),


@app.action("charge_status")
def create_request(event, ack, body, logger, client):
    return create_request_charges_consult(
        ack, body, logger, client), update_message_charges_feedback(
            event, ack, body, logger, client)


@app.action("phase_advance")
def create_request(ack, body, logger, client):
    return create_request_lead_update_phase(ack, body, logger, client)


@app.action("add_comment")
def create_request(ack, body, logger, client):
    return create_request_lead_add_comment(ack, body, logger, client)


@app.action("consult_cases")
def create_request(ack, body, logger, client):
    return Cases.create_request_search_case(ack, body, logger, client)

# Churn


@app.action("incubadora_no")
def update_message(event, ack, logger, body, client):
    return update_message_churn_conditional(event, ack, body, logger, client)


@app.action("churn_no")
def update_message(event, ack, logger, body, client):
    return update_message_churn_incubadora(event, ack, body, logger, client)


@app.action("churn_conditional_yes")
@app.action("incubadora_yes")
@app.action("churn_yes")
def update_message(event, ack, logger, body, client):
    return update_message_incubadora(event, ack, body, logger, client)


@app.action("churn_conditional_no")
def update_message(event, ack, logger, body, client):
    return update_message_churn_proccess_yes(event, ack, body, logger, client)


@app.action("cs_incubadora")
def update_message(event, ack, logger, body, client):
    return update_message_incubadora_ticket(event, ack, body, logger, client)

@app.action("new_access")
def update_message(event, ack, body, logger, client):
    return update_message_new_access(event, ack, body, logger, client)


# Webhooks


@app.action("sap")
def handle_some_action(event, ack, body, logger, client):
    return handle_sap_action(event, ack, body, logger, client)


@app.action("financial_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_financial_support(event, ack, body, logger, client)


@app.action("compliance_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_compliance_support(event, ack, body, logger, client)


@app.action("wor_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_wor_support(event, ack, body, logger, client)


@app.action("farmer_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_farmer_support(event, ack, body, logger, client)


@app.action("education_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_education_support(event, ack, body, logger, client)


@app.action("product_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_product_support(event, ack, body, logger, client)


@app.action("invoice_more")
@app.action("update_data_client")
@app.action("contract_renovation")
def handle_some_action(event, ack, body, logger, client):
    return update_message_contracts_support(event, ack, body, logger, client)


@app.action("update_data_unit")
def handle_some_action(event, ack, body, logger, client):
    return handle_financialdata_support(event, ack, body, logger, client)


@app.action("datatech_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_datatech_support(event, ack, body, logger, client)


@app.action("profit_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_profit_support(event, ack, body, logger, client)


@app.action("bp_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_peoplebp_support(event, ack, body, logger, client)


@app.action("hiring_no")
@app.action("hiring_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_hiring_support(event, ack, body, logger, client)


@app.action("ekyte_no")
@app.action("ekyte_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_ekyte_support(event, ack, body, logger, client)


@app.action("culture_support")
@app.action("rituals_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_culture_support(event, ack, body, logger, client)


@app.action("architecture_no")
def handle_some_action(event, ack, body, logger, client):
    return handle_architecture_support(event, ack, body, logger, client)


@app.action("investor_problem")
def handle_some_action(event, ack, body, logger, client):
    return handle_investorproblem_support(event, ack, body, logger, client)


@app.action("cs_problem")
def handle_some_action(event, ack, body, logger, client):
    return handle_csproblem_support(event, ack, body, logger, client)


@app.action("cs_dealings")
@app.action("cs_help")
@app.action("care_support")
def handle_some_action(event, ack, body, logger, client):
    return handle_care_support(event, ack, body, logger, client)


@app.action("cs_training")
def handle_some_action(event, ack, body, logger, client):
    return handle_cstraining_support(event, ack, body, logger, client)


@app.action("leadbroker_support")
@app.action("leadbroker_no")
@app.action("leadbroker_specialist")
def handle_some_action(event, ack, body, logger, client):
    return handle_leadbroker_support(event, ack, body, logger, client)


# Conditional Triggers

@app.action("broker_yes")
def update_message(event, ack, body, logger, client):
    return update_message_broker_yes(event, ack, body, logger, client)


@app.action("broker_support")
def update_message(event, ack, logger, body, client):
    return update_message_techdata(event, ack, logger, body, client)


@app.action("leadbroker_yes")
def update_message(event, ack, body, logger, client):
    return update_message_leadbroker_yes(event, ack, body, logger, client)


@app.action("meetingbroker_yes")
def update_message(event, ack, body, logger, client):
    return update_message_meetingbroker_yes(event, ack, body, logger, client)


@app.action("meetingbroker_help_yes")
def update_message(event, ack, logger, body, client):
    return update_message_meetingbroker_help(event, ack, logger, body, client)

@app.action("meetingbroker_support")
@app.action("meetingbroker_no")
@app.action("meetingbroker_help_support")
def update_message(event, ack, body, logger, client):
    return handle_meetingbroker_support(event, ack, body, logger, client)


@app.action("stamps_no")
def update_message(event, ack, body, logger, client):
    return handle_stamps_support(event, ack, body, logger, client)


@app.action("stamps_yes")
def update_message(event, ack, body, logger, client):
    return update_message_stamps_yes(event, ack, body, logger, client)


@app.action("certs_no")
def update_message(event, ack, body, logger, client):
    return handle_certification_support(event, ack, body, logger, client)


@app.action("certs_yes")
def update_message(event, ack, body, logger, client):
    return update_message_certification_yes(event, ack, body, logger, client)


@app.action("education_yes")
def update_message(event, ack, body, logger, client):
    return update_message_education_yes(event, ack, body, logger, client)


@app.action("products_yes")
def update_message(event, ack, body, logger, client):
    return update_message_product_yes(event, ack, body, logger, client)


@app.action("farmer_yes")
def update_message(event, ack, body, logger, client):
    return update_message_farmer_yes(event, ack, body, logger, client)


@app.action("hiring_yes")
def update_message(event, ack, body, logger, client):
    return update_message_hiring_yes(event, ack, body, logger, client)

@app.action("architecture_yes")
def update_message(event, ack, body, logger, client):
    return update_message_architecture_yes(event, ack, body, logger, client)


@app.action("ekyte_yes")
def update_message(event, ack, body, logger, client):
    return update_message_ekyte_yes(event, ack, body, logger, client)


@app.action("helpflag_no")
def update_message(event, ack, body, logger, client):
    return handle_helpflag_support(event, ack, body, logger, client)


@app.action("helpflag_yes")
def update_message(event, ack, body, logger, client):
    return update_message_helpflag_yes(event, ack, body, logger, client)


@app.action("roiweek_no")
def update_message(event, ack, body, logger, client):
    return handle_roiweek_support(event, ack, body, logger, client)


@app.action("retention_yes")
def update_message(event, ack, body, logger, client):
    return update_message_retention_yes(event, ack, body, logger, client)


@app.action("retention_no")
def update_message(event, ack, body, logger, client):
    return handle_retention_support(event, ack, body, logger, client)


@app.action("invoice_yes")
def update_message(event, ack, body, logger, client):
    return update_message_invoice_yes(event, ack, body, logger, client)


@app.action("invoice_no")
def update_message(event, ack, body, logger, client):
    return handle_invoice_support(event, ack, body, logger, client)


@app.action("charges_status_yes")
def update_message(event, ack, body, logger, client):
    return update_message_charges_yes(event, ack, body, logger, client)


@app.action("charges_status_no")
def update_message(event, ack, body, logger, client):
    return handle_charges_support(event, ack, body, logger, client)


@app.action("charges_yes")
def update_message(event, ack, body, logger, client):
    return update_message_fee_yes(event, ack, body, logger, client)


@app.action("charges_no")
def update_message(event, ack, body, logger, client):
    return update_message_fee_support(event, ack, body, logger, client)


@app.action("roiweek_yes")
def update_message(event, ack, body, logger, client):
    return update_message_roiweek_yes(event, ack, body, logger, client)


@app.action("submitNao")
def update_message(event, ack, body, logger, client):
    return update_message_nao(event, ack, body, logger, client)


@app.action("submitSim")
def update_message(event, ack, body, logger, client):
    return update_message_sim(event, ack, body, logger, client)


@app.action("financial_bad")
def update_message(event, ack, body, logger, client):
    return update_message_financial_bad(event, ack, body, logger, client)


@app.action("financial_good")
def update_message(event, ack, body, logger, client):
    return update_message_financial_good(event, ack, body, logger, client)


@app.view("send_request_ticketfinancial")
def handle_submission(ack, body, client):
    return handle_request_submission_ticketfinancial(ack, body, client)

@app.view("send_request_lead_consult")
def handle_submission(ack, body, client):
    return handle_request_submission_leadconsult(ack, body, client)

@app.view("send_request_charges_consult")
def handle_submission(event, ack, body, logger, client):
    return handle_request_submission_client_consult(ack, body, client)


@app.view("send_request_lead_update_phase")
def handle_submission(event, ack, body, logger, client):
    return handle_request_submission_update_phase(event, ack, body, logger, client)


@app.view("send_request_lead_add_coment")
def handle_submission(event, ack, body, logger, client):
    return handle_request_submission_add_comment(event, ack, body, logger, client)


@app.view("send_request_search_case")
def handle_submission(event, ack, body, logger, client):
    return Cases.handle_request_submission_search_case(event, ack, body, logger, client)


# Cada açao de click button selections devem ser registrados com seu code.
@app.action("la_buy_tickets")
@app.action("la_infos")
@app.action("looking_ahead")
@app.action("add_comment")
@app.action("phase_advance")
@app.action("update_lead")
@app.action("create_error")
@app.action("how_request")
@app.action("new_access")
@app.action("send_cases")
@app.action("consult_cases")
@app.action("cases_production")
@app.action("cases")
@app.action("protest_statement")
@app.action("charges_no")
@app.action("charges_yes")
@app.action("fee_exemption")
@app.action("fee_discount")
@app.action("sales_leadbroker_access")
@app.action("sales_services")
@app.action("sales_brokers")
@app.action("sales_leadbroker")
@app.action("broker_yes")
@app.action("broker_support")
@app.action("leadbroker_lost")
@app.action("leadbroker_playbook")
@app.action("leadbroker_support")
@app.action("sales_leadbroker_access")
@app.action("sales_meetingbroker")
@app.action("meetingbroker_playbook")
@app.action("meetingbroker_help")
@app.action("leadbroker_no")
@app.action("leadbroker_yes")
@app.action("meetingbroker_no")
@app.action("meetingbroker_yes")
@app.action("meetingbroker_support")
@app.action("meetingbroker_help_yes")
@app.action("meetingbroker_help_support")
@app.action("meetingbroker_lost")
@app.action("slack")
@app.action("slack_redev4_ws")
@app.action("slack_access_problem")
@app.action("slack_all_ws")
@app.action("slack_my_ws")
@app.action("slack_paid_user")
@app.action("slack_new_paid_user")
@app.action("slack_other")
@app.action("slack_find_ws")
@app.action("slack_error_403")
@app.action("slack_adm_approve")
@app.action("slack_expired_link")
@app.action("charge_status")
@app.action("leadconsult")
@app.action("attendantment_cert")
@app.action("scientist_test")
@app.action("attendant_subscription")
@app.action("attendantment_access")
@app.action("update_data_financial")
@app.action("churn")
@app.action("churn_no")
@app.action("churn_yes")
@app.action("churn_conditional_yes")
@app.action("churn_conditional_no")
@app.action("cs_incubadora")
@app.action("compliance_action1")
@app.action("compliance_action2")
@app.action("compliance_action3")
@app.action("wor_action1")
@app.action("wor_action2")
@app.action("service_desk")
@app.action("access_gupy")
@app.action("knowledge_first_access")
@app.action("knowledge_access")
@app.action("knowledge_base")
@app.action("open_vacancy")
@app.action("farmer_question")
@app.action("farmer_v4x")
@app.action("leadership")
@app.action("leadership_sub")
@app.action("leadership_customer")
@app.action("g4skills_access")
@app.action("v4academy_access")
@app.action("scout")
@app.action("apollo")
@app.action("open_modal_ticketfinancial")
@app.action("open_modal_question")
@app.action("open_modal")
@app.action("send_answer")
@app.action("approved")
@app.action("denied")
@app.action("architecture_no")
@app.action("architecture_yes")
@app.action("stamps_yes")
@app.action("stamps_no")
@app.action("certs_yes")
@app.action("certs_no")
@app.action("charges_status_no")
@app.action("charges_status_yes")
@app.action("helpflag_yes")
@app.action("helpflag_no")
@app.action("roiweek_yes")
@app.action("roiweek_no")
@app.action("ekyte_yes")
@app.action("ekyte_no")
@app.action("cs_training")
@app.action("cs_dealings")
@app.action("cs_help")
@app.action("invoice_yes")
@app.action("invoice_no")
@app.action("invoice_ticket")
@app.action("products_yes")
@app.action("education_yes")
@app.action("retention_yes")
@app.action("farmer_yes")
@app.action("hiring_yes")
@app.action("retention_no")
@app.action("financial_bad")
@app.action("financial_good")
@app.action("stack_digital")
@app.action("roi_week")
@app.action("culture")
@app.action("credit_card")
@app.action("people")
@app.action("farmer")
@app.action("hiring")
@app.action("cs")
@app.action("cs_retention")
@app.action("stamps")
@app.action("helpflag")
@app.action("go_back")
@app.action("certifications")
@app.action("wor")
@app.action("certification_request")
@app.action("care_info")
@app.action("compliance")
@app.action("products")
@app.action("architecture")
@app.action("financial")
@app.action("ekyte")
@app.action("franchise_support")
@app.action("financial_support")
@app.action("compliance_support")
@app.action("care_support")
@app.action("ekyte_support")
@app.action("datatech_support")
@app.action("profit_support")
@app.action("education_support")
@app.action("achitecture_support")
@app.action("culture_support")
@app.action("rituals_support")
@app.action("hiring_support")
@app.action("bp_support")
@app.action("farmer_support")
@app.action("investor_problem")
@app.action("candidate_approval")
@app.action("care_action")
@app.action("product_objections")
@app.action("product_spreadsheet")
@app.action("other_doubts")
@app.action("how_to_sell")
@app.action("pricing")
@app.action("stamps_questions")
@app.action("certification_questions")
@app.action("update_data_unit")
@app.action("update_data_client")
@app.action("contract_renovation")
@app.action("ferramentas")
@app.action("operations")
@app.action("datatech")
@app.action("email")
@app.action("powerbi")
@app.action("leadbroker")
@app.action("v4academy")
@app.action("eduv4")
@app.action("base_conhecimento")
@app.action("mktlab")
@app.action("labfinanceiro")
@app.action("unbounce")
@app.action("zapier")
@app.action("g4skills")
@app.action("activecampaign")
@app.action("tray")
@app.action("kommo")
@app.action("vindi")
@app.action("letalk")
@app.action("helpdesk")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


@app.event("app_mention")
def handle_app_mention_events(body, logger):
    logger.info(body)


@app.event("file_shared")
def handle_file_shared(body, logger):
    logger.info(body)


@app.view("send_request_search_case")
@app.view("send_request_lead_add_coment")
@app.view("send_request_lead_update_phase")
@app.view("send_request_charges_consult")
@app.view("send_request_lead_consult")
@app.view("send_request_ticketfinancial")
@app.view("send_request")
def handle_view_submission_events(ack, body, logger):
    ack()
    logger.info(body)


if __name__ == "__main__":
    app.start(port=3030)
