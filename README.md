# Generador de Reporte Buró de Crédito Sintético

API que genera reportes de buró de crédito falsos para testing.

## Despliegue en Vercel

1. Sube los archivos a un repo de GitHub
2. Ve a vercel.com → New Project → Importa tu repo
3. Framework: Other
4. Build: `pip install -r requirements.txt`
5. Deploy

## Endpoints

- `POST /api/reporte` → JSON con datos del reporte
- `POST /api/reporte/pdf` → PDF descargable

## Uso

```bash
curl -X POST https://tu-api.vercel.app/api/reporte \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Perez Gonzalez"}'
