import json
import requests

from handlers import HANDLERS


def _read_event(event: str | dict) -> tuple[dict, dict]:
    if isinstance(event, str):
        try:
            new_event = json.loads(event)
        except json.JSONDecodeError:
            print("Erro ao decodificar o JSON do evento.")
            return {}, {}
    elif not isinstance(event, dict):
        print("Evento não é um dicionário ou string JSON.")
        return {}, {}
    else:
        new_event = event

    body = new_event.get("body", {})
    headers = new_event.get("headers", {})

    if not body:
        body = event

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            print("Corpo da requisição inválido")
            return {}, {}

    return body, headers


def validar_datas(data: str) -> str | None:
    """
    Valida se a data está no formato YYYY-MM-DD.
    Retorna a data se válida, caso contrário retorna None.
    """
    try:
        partes = data.split("-")
        if len(partes) != 3:
            return None
        ano, mes, dia = partes
        if len(ano) != 4 or len(mes) != 2 or len(dia) != 2:
            return None
        int(ano)
        int(mes)
        int(dia)
        return data
    except ValueError:
        return None


def webhook_navision(event, context):
    """
    Endpoint do webhook para o Navision.
    Roteia para o handler correto baseado no event_type.
    Recebe a API key no header X-Api-Key.
    """
    try:
        body, headers = _read_event(event)

        print("Body:", body)
        print("Headers:", headers)

        # Validação de autenticação - API key no header X-Api-Key
        api_key = headers.get("X-Api-Key") or headers.get("x-api-key")

        if not api_key:
            return {
                "statusCode": 401,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "erro",
                    "mensagem": "Chave de API não autorizada."
                })
            }

        # Validação do event_type
        event_type = body.get("event_type")
        if not event_type or not isinstance(event_type, str):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "erro",
                    "mensagem": "Erro de requisição — event_type é obrigatório."
                })
            }

        # Buscar handler correspondente
        handler = HANDLERS.get(event_type)
        if not handler:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "status": "erro",
                    "mensagem": f"Erro de requisição — event_type '{event_type}' não é válido."
                })
            }

        # Chamar o handler
        return handler(body, api_key)

    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "erro",
                "mensagem": "Erro interno do servidor."
            })
        }
