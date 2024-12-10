from flask import Flask, jsonify, request
from datetime import datetime
import os
from google.cloud import firestore

# Vytvoříme Flask aplikaci
app = Flask(__name__)

# Inicializujeme Firestore klienta - v Cloud Run se automaticky autentizuje
db = firestore.Client()

# Základní endpoint pro kontrolu, že aplikace běží
@app.route('/')
def hello():
    return 'Hello World!'

# Endpoint pro přijímání nových zpráv
@app.route('/api/message', methods=['POST'])
def receive_message():
    # Získáme data z požadavku
    data = request.get_json()
    
    # Kontrola, zda požadavek obsahuje zprávu
    if not data or 'message' not in data:
        return jsonify({
            'error': 'Chybí povinné pole message'
        }), 400
    
    try:
        # Vytvoříme nový dokument ve Firestore s automaticky generovaným ID
        message_ref = db.collection('messages').document()
        message_ref.set({
            'content': data['message'],
            'created_at': datetime.utcnow().isoformat()
        })
        
        # Vrátíme úspěšnou odpověď
        return jsonify({
            'status': 'OK',
            'message_id': message_ref.id,
            'created_at': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': f'Chyba při ukládání zprávy: {str(e)}'
        }), 500

# Endpoint pro získání všech zpráv
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        # Získáme reference na kolekci zpráv
        messages_ref = db.collection('messages')
        # Seřadíme podle času vytvoření sestupně (nejnovější první)
        docs = messages_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
        
        # Převedeme všechny dokumenty na seznam
        messages = []
        for doc in docs:
            message_data = doc.to_dict()
            message_data['id'] = doc.id
            messages.append(message_data)
            
        return jsonify(messages)
    except Exception as e:
        return jsonify({
            'error': f'Chyba při načítání zpráv: {str(e)}'
        }), 500

# Spuštění aplikace
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)