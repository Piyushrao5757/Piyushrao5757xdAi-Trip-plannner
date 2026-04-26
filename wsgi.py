services:
  - type: web
    name: ai-trip-planner-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: GOOGLE_MAPS_API_KEY
        sync: false
      - key: AMADEUS_API_KEY
        sync: false
      - key: AMADEUS_SECRET
        sync: false
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: BOOKING_COM_API_KEY
        sync: false
