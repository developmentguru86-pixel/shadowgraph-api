# A2A agent

| | |
|---|---|
| Agent card | `https://shadowalpha.online/.well-known/agent-card.json` ([copy](../spec/agent-card.json)) |
| Endpoint | `https://shadowalpha.online/_api/a2a` |
| Binding | JSON-RPC, A2A 1.0, method `SendMessage` |
| Streaming / push | No / no |

## Send a message

```bash
curl -s -X POST https://shadowalpha.online/_api/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
      "message": {
        "role": "ROLE_USER",
        "messageId": "m1",
        "parts": [{ "text": "What moved in global markets today?" }]
      }
    }
  }'
```

The answer is in `result.message.parts[0].text` (JSON as text).

Free skills: market recap, latest SEC filings, EU procurement search, free preview. Paid skills ($0.50–$5.00) answer with HTTP 402 and a `WWW-Authenticate: Payment` challenge, see [payments.md](payments.md).
