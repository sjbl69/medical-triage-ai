## API Deployment

The medical triage system was exposed through a FastAPI REST API.

Main endpoints:

- `GET /`
- `GET /test`
- `POST /generate`

The API receives a symptom description and returns:
- a triage classification,
- a generated medical response,
- response latency.

Example:

```json
{
  "symptom": "chest pain"
}
```

Response:

```json
{
  "triage": "URGENCE",
  "message": "⚠️ Call emergency services immediately.",
  "latency": 0.142
}
```

---

## Docker Deployment

The application was containerized using Docker to ensure:
- reproducibility,
- portability,
- isolated environments.

Dockerfile:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## CI/CD Pipeline

A CI/CD pipeline was implemented using GitHub Actions.

Automated steps:
- repository checkout,
- dependency installation,
- Docker image build,
- API startup test,
- deployment preparation.

This ensures reproducible deployments and automated validation.

---

## Cloud Deployment

The API was deployed on Railway as a pilot cloud environment.

Observed deployment logs:

```text
Application startup complete.
Uvicorn running on http://0.0.0.0:8080
```

Public endpoint:

```text

https://medical-triage-ai-production-a675.up.railway.app/
```

Swagger documentation:

```text
https://medical-triage-ai-production-a675.up.railway.app/docs
```

---

## Safety System

A rule-based safety layer was implemented to prioritize critical situations before model generation.

Critical symptoms detected:
- chest pain,
- breathing difficulty,
- stroke symptoms,
- heavy bleeding,
- loss of consciousness,
- overdose.

This prevents unsafe responses in emergency situations.

---

## Latency and Performance

Measured latency:

| Scenario | Average Response Time |
|---|---|
| Simple request | ~100 ms |
| Emergency case | ~120 ms |
| Text generation | ~150–300 ms |

The API remains responsive for real-time demonstration purposes.

---

## Robustness Testing

The system was tested on:
- urgent symptoms,
- non-urgent symptoms,
- malformed prompts,
- incomplete inputs,
- unsafe generations.

Fallback mechanisms were implemented to ensure stable behavior even when the model output is invalid.

---

## Traceability

Interaction logs were added for debugging and auditability.

Example:

```text
[LOG] Symptom: chest pain
[LOG] Triage: URGENCE
[LOG] Latency: 0.142s
```

Logged information:
- input symptoms,
- predicted triage,
- generated response,
- response latency.

---

## Security Considerations

The following precautions were implemented:
- rule-based emergency prioritization,
- fallback responses,
- container isolation,
- cloud deployment isolation.

Current limitations:
- no authentication layer,
- no database persistence,
- no clinical certification.

This project remains a Proof of Concept and must not be used for real medical decision-making.

---

## Roadmap

Short-term:
- API authentication,
- monitoring dashboards,
- persistent logging,
- better error handling.

Mid-term:
- full vLLM integration,
- GPU optimization,
- scalable deployment architecture.

Long-term:
- clinical validation,
- GDPR compliance,
- hospital integration,
- certified medical deployment.

---

## Go / No-Go

### Go if:
- API remains stable,
- latency stays below 1 second,
- emergency rules are reliable,
- endpoint is accessible.

### No-Go if:
- critical errors appear,
- unsafe responses are generated,
- deployment becomes unstable,
- endpoint becomes unavailable.

---

## Conclusion

This project demonstrates the development of a complete AI-powered medical triage prototype combining:
- language model fine-tuning,
- LoRA and DPO alignment,
- FastAPI deployment,
- Docker containerization,
- CI/CD automation,
- cloud deployment,
- safety mechanisms,
- traceability and evaluation.

The resulting architecture provides a strong foundation for future industrialization and medical AI experimentation.
