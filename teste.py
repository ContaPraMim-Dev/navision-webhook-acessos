import requests
import json

url = "https://xkit-1dzl-gome.n7c.xano.io/api:yXFPZvLr/webhook_acessos"

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "GVbjccJRI2Mz0fRBoPSoAjhhaERprBup"
}

body = {
    "event_id": "b7e2b9c9-4f3a-4e1d-9f6c-7c6f0c9e9d2a",
    "isps_code": "A7A2B4F1",
    "nome_completo": "JOSUEL DA SILVA",
    "tipo_acesso": "VERMELHO",
    "motivacao_inicio": "2023-01-23",
    "motivacao_fim": "2028-11-25T23:59:59-03:00",
    "empresa": "AUTORIDADE PORTUÁRIA DE SANTOS",
    "id_foto": 399,
    "gate": 10
    
}

response = requests.post(url, json=body, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
