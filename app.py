from flask import Flask, request, jsonify, Response, send_file
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
        if not nombre:
            return jsonify({'error': 'Nombre requerido'}), 400
        
        rango_score = data.get('rango_score')
        if rango_score and isinstance(rango_score, list) and len(rango_score) == 2:
            rango_score = tuple(rango_score)
        
        reporte = generar_reporte({
            'nombre': nombre,
            'fecha_nacimiento': data.get('fecha_nacimiento', ''),
            'rfc': data.get('rfc', ''),
            'curp': data.get('curp', ''),
            'empleo': data.get('empleo', ''),
            'num_creditos': data.get('num_creditos'),
            'rango_score': rango_score,
            'institucion': data.get('institucion'),
            'tipo_credito': data.get('tipo_credito'),
            'domicilio': data.get('domicilio', {}),
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
        
        reporte = data.get('reporte')
        
        if not reporte:
            return jsonify({'error': 'Reporte requerido'}), 400
        
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
