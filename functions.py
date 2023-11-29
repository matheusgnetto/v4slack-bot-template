import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests
import random

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "./credentials.json", scope)

clientSpread = gspread.authorize(credentials)


def get_current_datetime():
    return datetime.now()


def get_user_email(user_id):
    url = f"https://slack.com/api/users.info?user={user_id}"
    headers = {
        "Authorization": "Bearer xoxp..."
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response_json.get("ok"):
            return response_json["user"]["profile"]["email"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o e-mail do usuário: {e}")
        return None
  
def get_user_name(user_id):
    url = f"https://slack.com/api/users.info?user={user_id}"
    headers = {
        "Authorization": "Bearer xoxp...",
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response_json.get("ok"):
            return response_json["user"]["real_name"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o nome do usuário: {e}")
        return None


def addRowUserActionFinancial(date, email, iuguId, cleaned_iugu_id, clientId, dueDate, feeValue):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("Financeiro")

  formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

  values = [formatted_date, email, iuguId, cleaned_iugu_id, clientId, dueDate, feeValue]
  sheet.append_row(values)

def addRowUserInvoiceFinancial(date, email, value):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("FinanceiroSuccess")

  formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

  values = [formatted_date, email, value]
  sheet.append_row(values)

def addRowUserChargesStatus(date, email, value):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("CobrançaSuccess")

  formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

  values = [formatted_date, email, value]
  sheet.append_row(values)

def addRowUserLeadConsult(date, email, cnpj, leadConsult):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("ConsultaCnpj")

  formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

  values = [formatted_date, email, cnpj, leadConsult]
  sheet.append_row(values)

def addRowUserChargesConsult(date, email, client_id):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("StatusCobrança")

  formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")

  values = [formatted_date, email, client_id]
  sheet.append_row(values)


def iuguNewTicket(iugu_id, days, date, email):
    api_url = "API"
    token = "TOKEN"

    upper_case_iugu_id = iugu_id.upper()
    cleaned_iugu_id = upper_case_iugu_id.replace('-', '').replace('/', '')

    payload = {
        "iugu_id": cleaned_iugu_id,
        "days": days,
        "token": token
    }

    try:
        response = requests.post(api_url, json=payload)
        response_data = response.json()
        iuguId = response_data["iugu_id"]
        clientId = response_data["client_id"]
        dueDate = response_data["due_date"]
        feeValue = response_data["fee_value"]
        addRowUserActionFinancial(date, email, iuguId, cleaned_iugu_id, clientId, dueDate, feeValue)

        if response.status_code == 200:
            return response_data["payment_url"]

        else:
            return {"error": "Error generating new ticket"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error generating new ticket: {e}"}


def addRowUserAction(area, email, action):
  spreadsheet = clientSpread.open("BotSuporte Relatório")
  sheet = spreadsheet.worksheet("Actions")
  values = [area, email, action]
  sheet.append_row(values)


def start_webhook_workflow(webhook_url, user_id, unit):
    
    payload = {
        "user_id": user_id,
        "unit": unit
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Fluxo de trabalho iniciado com sucesso!")
        else:
            print("Erro ao iniciar o fluxo de trabalho:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)


def start_webhook_leadflow(webhook_url, lead, user_id, email, fase_destino=None, comment=None):
    payload = {
        "lead": lead,
        "user_id": user_id,
        "email": email
    }

    if fase_destino:
        payload["fase_destino"] = fase_destino

    if comment:
        payload["comment"] = comment

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Webhook iniciado com sucesso!")
        else:
            print("Erro ao iniciar o Webhook:", response.text)
    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)


def formatar_cnpj(cnpj):
    
    cnpj_numerico = ''.join(filter(str.isdigit, cnpj))

    cnpj_com_zeros = cnpj_numerico.zfill(14)

    cnpj_formatado = f"{cnpj_com_zeros[:2]}.{cnpj_com_zeros[2:5]}.{cnpj_com_zeros[5:8]}/{cnpj_com_zeros[8:12]}-{cnpj_com_zeros[12:]}"

    return cnpj_formatado


def process_audio(file_id, user_id):
    
    api_url = "API_URL"

    payload = {
        "file_id": file_id,
        "user_id": user_id
    }
    print(f"Processing audio for file_id: {file_id}")
    
    try:
        response = requests.post(api_url, json={"data": payload})
        response_data = response.json()

        if response.status_code == 200:
            print(f"Áudio processado com sucesso! Response: {response_data}")
        else:
            print(f"Falha ao processar áudio: {response_data}")
    except Exception as e:
        print(f"Error: {e}")
  

def query_graphql_for_case(selected_case):
    graphql_url = "GRAPHQL_URL" 
    query = """
        query MyQuery($categoryName: String!) {
            posts(where: {categoryId: 5793, categoryName: $categoryName}) {
                nodes {
                    uri
                    title
                }
            }
        }
    """
    variables = {"categoryName": selected_case}
    response = requests.post(graphql_url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['posts']['nodes']
        if posts:
            random.shuffle(posts)
            return posts[:5]
    return []