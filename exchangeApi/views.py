from rest_framework.response import Response
from datetime import datetime
from urllib.request import urlopen
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from urllib.request import urlopen
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse

import requests
import re

class ExchangesListView (APIView):
  throttle_classes = [UserRateThrottle]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    # Banco de México
    today = datetime.today().strftime('%Y-%m-%d')
    requestBanxico = requests.get(f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{today}/{today}", headers={'Bmx-Token': 'bf982f112edbe825fd6b99b4c330378ffac8ee6b8e6951dba0aad5b04c4a5779'})
    #Diario Oficial de la Federación
    remoteUrl = urlopen("https://www.banxico.org.mx/tipcamb/tipCamMIAction.do")

    for number in range(0, 210):
      remoteUrl.readline()
    date = remoteUrl.readline().decode('utf-8')
    remoteUrl.readline()
    remoteUrl.readline()
    value = remoteUrl.readline().decode('utf-8')

    if re.sub('[^A-Za-z0-9.]+', '', value) == 'NE':
      remoteUrl.readline()
      remoteUrl.readline()
      value = remoteUrl.readline().decode('utf-8')

    if re.sub('[^A-Za-z0-9.]+', '', value) == 'NE':
      remoteUrl.readline()
      remoteUrl.readline()
      value = remoteUrl.readline().decode('utf-8')

    # Banco de México
    requestFixer = requests.get(f"http://data.fixer.io/api/latest?access_key=462f895ba54baf9898ec1935bb54af81&symbols=USD,MXN&format=1")

    banxico_date = requestBanxico.json()['bmx']['series'][0]['datos'][0]['fecha'] if "datos" in requestBanxico.json()['bmx']['series'][0] else "Sin datos"
    banxico_value = float(requestBanxico.json()['bmx']['series'][0]['datos'][0]['dato']) if "datos" in requestBanxico.json()['bmx']['series'][0] else "Sin datos"

    results = {
      "rates": {
        "provider_1": {
          "name": "Banco de México",
          "last_updated": banxico_date,
          "value": banxico_value,
        },
        "provider_2": {
          "name": "Diario Oficial de la Federación",
          "last_updated": re.sub('[^A-Za-z0-9/]+', '', date),
          "value": float(re.sub('[^A-Za-z0-9.]+', '', value)),
        },
        "provider_3": {
          "name": "Fixer.io",
          "last_updated": datetime.fromtimestamp(requestFixer.json()['timestamp']).strftime('%d/%m/%Y'),
          "value": round(requestFixer.json()['rates']['MXN']/requestFixer.json()['rates']['USD'],4),
        },
      }
    }

    return Response(results)

def index(request):
    return render(request, 'index.html')
