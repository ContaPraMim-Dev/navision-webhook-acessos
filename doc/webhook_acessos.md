# Webhook de Acessos - Navision

## Endpoint

```
POST https://api.navisionapp.online/webhooks/acessos
```

## Autenticacao

A autenticacao e feita via header `X-Api-Key`.

| Header | Valor |
|--------|-------|
| X-Api-Key | `<sua_api_key>` |

## Request

### Headers

| Header | Valor |
|--------|-------|
| Content-Type | application/json |
| X-Api-Key | `<sua_api_key>` |

### Body

```json
{
  "event_id": "b7e2b9c9-4f3a-4e1d-9f6c-7c6f0c9e9d2a",
  "event_type": "acessos",
  "data": {
    "isps_code": "A7A2B4F1",
    "nome_completo": "JOSUEL DA SILVA",
    "tipo_acesso": "VERMELHO",
    "motivacao_inicio": "2023-01-23",
    "motivacao_fim": "2028-11-25T23:59:59-03:00",
    "empresa": "AUTORIDADE PORTUARIA DE SANTOS",
    "id_foto": 399,
    "gate": 10
  }
}
```

### Campos

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| event_id | UUID | Sim | Identificador unico do evento (formato UUID) |
| event_type | string | Sim | Tipo do evento. Para acessos, usar: `acessos` |
| data | object | Sim | Objeto contendo os dados do acesso |
| data.isps_code | string | Sim | Codigo ISPS do usuario |
| data.nome_completo | string | Sim | Nome completo do usuario |
| data.tipo_acesso | string | Sim | Tipo de acesso: `VERMELHO` ou `VERDE` |
| data.motivacao_inicio | string | Sim | Data de inicio da motivacao (formato: `yyyy-mm-dd`) |
| data.motivacao_fim | string | Sim | Data/hora de fim da motivacao (formato ISO 8601: `yyyy-mm-ddTHH:MM:SS-03:00`) |
| data.empresa | string | Sim | Nome da empresa |
| data.id_foto | integer | Sim | ID da foto do usuario |
| data.gate | integer | Sim | Numero do gate de acesso |

## Responses

### 200 OK - Sucesso

```json
{
  "status": "sucesso"
}
```

### 400 Bad Request - Parametros invalidos

Retornado quando algum campo esta ausente ou com formato invalido.

```json
{
  "status": "erro",
  "mensagem": "Erro de requisicao — <descricao do erro>"
}
```

Possiveis mensagens de erro:
- `event_type e obrigatorio.`
- `event_type '<valor>' nao e valido.`
- `event_id deve ser um UUID valido.`
- `data deve ser um objeto.`
- `isps_code deve ser uma string.`
- `nome_completo deve ser uma string.`
- `tipo_acesso deve ser VERMELHO ou VERDE.`
- `motivacao_inicio deve estar no formato yyyy-mm-dd.`
- `motivacao_fim deve estar no formato ISO 8601 (ex: 2028-11-25T23:59:59-03:00).`
- `empresa deve ser uma string.`
- `id_foto deve ser um inteiro.`
- `gate deve ser um inteiro.`

### 401 Unauthorized - API Key invalida

Retornado quando a API key nao e fornecida ou e invalida.

```json
{
  "status": "erro",
  "mensagem": "Chave de API nao autorizada."
}
```

### 409 Conflict - Evento duplicado

Retornado quando ja existe um evento com o mesmo `event_id`.

```json
{
  "status": "erro",
  "mensagem": "Conflito — evento ja registrado."
}
```

### 500 Internal Server Error - Erro interno

Retornado quando ocorre um erro interno no servidor.

```json
{
  "status": "erro",
  "mensagem": "Erro interno do servidor."
}
```

## Exemplo com cURL

```bash
curl -X POST https://api.navisionapp.online/webhooks/acessos \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: <sua_api_key>" \
  -d '{
    "event_id": "b7e2b9c9-4f3a-4e1d-9f6c-7c6f0c9e9d2a",
    "event_type": "acessos",
    "data": {
      "isps_code": "A7A2B4F1",
      "nome_completo": "JOSUEL DA SILVA",
      "tipo_acesso": "VERMELHO",
      "motivacao_inicio": "2023-01-23",
      "motivacao_fim": "2028-11-25T23:59:59-03:00",
      "empresa": "AUTORIDADE PORTUARIA DE SANTOS",
      "id_foto": 399,
      "gate": 10
    }
  }'
```
