from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from main import generar_reporte
from plantilla import generar_pdf_reporte
from datetime import datetime
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/reporte', methods=['POST'])
def api_reporte():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        nombre = data.get('nombre', '')
        rfc = data.get('rfc', '')
        curp = data.get('curp', '')
        domicilio = data.get('domicilio', {})
        
        if not nombre:
            return jsonify({'error': 'Nombre requerido'}), 400
        
        reporte = generar_reporte({
            'nombre': nombre,
            'rfc': rfc,
            'curp': curp,
            'domicilio': domicilio,
        })
        
        return jsonify({'exito': True, 'reporte': reporte})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reporte/pdf', methods=['POST'])
def api_reporte_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        # Si viene un reporte completo, usarlo directamente
        reporte = data.get('reporte')
        if not reporte:
            # Si no, generar uno nuevo
            reporte = generar_reporte(data)
        
        pdf_bytes = generar_pdf_reporte(reporte)
        
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=reporte_buro_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
