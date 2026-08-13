import random
import string
from datetime import datetime, timedelta

# ============================================================
# CONFIGURACIÓN
# ============================================================

INSTITUCIONES = [
    'BBVA México', 'Banorte', 'Santander', 'HSBC', 'Citibanamex',
    'Scotiabank', 'BanCoppel', 'Banco Azteca', 'American Express',
    'Liverpool', 'Coppel', 'Elektra', 'Nu México', 'Stori',
    'RappiCard', 'Kueski', 'Creditea', 'Financiera Independencia',
]

TIPOS_CREDITO = [
    'Tarjeta de Crédito', 'Préstamo Personal', 'Crédito Hipotecario',
    'Crédito Automotriz', 'Préstamo de Nómina', 'Crédito de Tienda',
    'Línea de Crédito', 'Financiamiento', 'Arrendamiento',
]

MESES = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']


# ============================================================
# FUNCIONES GENERADORAS
# ============================================================

def generar_score():
    """Score entre 400 y 850."""
    return random.randint(400, 850)


def interpretar_score(score):
    if score >= 750:
        return 'EXCELENTE'
    elif score >= 680:
        return 'BUENO'
    elif score >= 600:
        return 'REGULAR'
    elif score >= 500:
        return 'MALO'
    else:
        return 'MUY MALO'


def generar_historial(meses=24):
    historial = []
    ahora = datetime.now()
    for i in range(meses):
        fecha = ahora - timedelta(days=30*i)
        prob = random.random()
        if prob < 0.85:
            estado = 'AL CORRIENTE'
        elif prob < 0.92:
            estado = 'ATRASO 30'
        elif prob < 0.97:
            estado = 'ATRASO 60'
        else:
            estado = 'ATRASO 90+'
        historial.append({
            'mes': f"{MESES[fecha.month-1]}-{str(fecha.year)[2:]}",
            'estado': estado,
            'monto': random.randint(500, 50000)
        })
    return historial


def generar_credito(num):
    monto_orig = random.randint(10000, 500000)
    saldo = random.randint(0, monto_orig)
    estatus_roll = random.random()
    
    if estatus_roll < 0.80:
        estatus = 'Al corriente'
    elif estatus_roll < 0.90:
        estatus = 'Atraso 30 días'
    elif estatus_roll < 0.95:
        estatus = 'Atraso 60 días'
    else:
        estatus = 'Atraso 90+ días'
    
    return {
        'numero': num,
        'institucion': random.choice(INSTITUCIONES),
        'tipo': random.choice(TIPOS_CREDITO),
        'monto_original': monto_orig,
        'saldo_actual': saldo,
        'pago_mensual': random.randint(500, 15000),
        'estatus': estatus,
        'fecha_apertura': (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%d/%m/%Y'),
        'historial': generar_historial(random.randint(12, 36))
    }


def generar_consultas():
    consultas = []
    for _ in range(random.randint(3, 10)):
        fecha = datetime.now() - timedelta(days=random.randint(30, 730))
        consultas.append({
            'fecha': fecha.strftime('%d/%m/%Y'),
            'institucion': random.choice(INSTITUCIONES),
            'tipo': random.choice(['Consulta normal', 'Consulta promocional', 'Revisión de cuenta'])
        })
    return sorted(consultas, key=lambda x: x['fecha'], reverse=True)


def generar_reporte(datos_persona):
    num_creditos = random.randint(2, 8)
    creditos = [generar_credito(i+1) for i in range(num_creditos)]
    score = generar_score()
    
    total_saldo = sum(c['saldo_actual'] for c in creditos)
    total_pago = sum(c['pago_mensual'] for c in creditos)
    al_corriente = sum(1 for c in creditos if c['estatus'] == 'Al corriente')
    
    return {
        'encabezado': {
            'tipo': 'REPORTE DE CRÉDITO ESPECIAL',
            'folio': ''.join(random.choices(string.digits, k=16)),
            'fecha': datetime.now().strftime('%d/%m/%Y'),
            'hora': datetime.now().strftime('%H:%M:%S'),
        },
        'consumidor': {
            'nombre': datos_persona.get('nombre', ''),
            'rfc': datos_persona.get('rfc', ''),
            'curp': datos_persona.get('curp', ''),
            'domicilio': datos_persona.get('domicilio', {}),
            'empleo': random.choice(['Empleado', 'Independiente', 'Empresario', 'Profesionista', 'Comerciante']),
        },
        'score': {
            'puntaje': score,
            'interpretacion': interpretar_score(score),
        },
        'resumen': {
            'total_creditos': len(creditos),
            'total_saldo': total_saldo,
            'total_pago': total_pago,
            'al_corriente': al_corriente,
            'atrasados': len(creditos) - al_corriente,
        },
        'creditos': creditos,
        'consultas': generar_consultas(),
      }
