from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from main import generar_reporte
from plantilla import generar_pdf_reporte
from datetime import datetime
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/reporte', methods=['POST'])
def api_reporte():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON requerido'}), 400
        
        nombre = data.get('nombre', '')
        if not nombre:
            return jsonify({'error': 'Nombre requerido'}), 400
        
        # Procesar personalización
        rango_score = data.get('rango_score')
        num_creditos = data.get('num_creditos')
        institucion = data.get('institucion')
        tipo_credito = data.get('tipo_credito')
        fecha_nac = data.get('fecha_nacimiento', '')
        rfc = data.get('rfc', '')
        curp = data.get('curp', '')
        empleo = data.get('empleo', '')
        
        reporte = generar_reporte({
            'nombre': nombre,
            'fecha_nacimiento': fecha_nac,
            'rfc': rfc,
            'curp': curp,
            'empleo': empleo,
            'num_creditos': num_creditos,
            'rango_score': tuple(rango_score) if rango_score else None,
            'institucion': institucion,
            'tipo_credito': tipo_credito,
            'domicilio': {},
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
        
        # CLAVE: Usar el reporte completo que envía el frontend
        reporte = data.get('reporte')
        
        if not reporte:
            # Fallback: si no viene reporte, generarlo desde los datos
            nombre = data.get('nombre', '')
            if not nombre:
                return jsonify({'error': 'Reporte o nombre requerido'}), 400
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
