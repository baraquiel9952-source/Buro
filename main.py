import random
import string
import json
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
EMPLEOS = ['Empleado', 'Independiente', 'Empresario', 'Profesionista', 'Comerciante', 'Obrero', 'Técnico']

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def generar_folio():
    return ''.join(random.choices(string.digits, k=10))

def formatear_fecha_buro(fecha):
    meses = {'JANUARY':'ENE','FEBRUARY':'FEB','MARCH':'MAR','APRIL':'ABR',
             'MAY':'MAY','JUNE':'JUN','JULY':'JUL','AUGUST':'AGO',
             'SEPTEMBER':'SEP','OCTOBER':'OCT','NOVEMBER':'NOV','DECEMBER':'DIC'}
    for en, es in meses.items():
        fecha = fecha.replace(en, es)
    return fecha

def generar_score():
    return random.randint(400, 850)

def interpretar_score(score):
    if score >= 750: return 'EXCELENTE'
    elif score >= 680: return 'BUENO'
    elif score >= 600: return 'REGULAR'
    elif score >= 500: return 'MALO'
    else: return 'MUY MALO'

def generar_historial(meses=24):
    historial = []
    ahora = datetime.now()
    for i in range(meses):
        fecha = ahora - timedelta(days=30*i)
        prob = random.random()
        if prob < 0.85: estado = 'AL CORRIENTE'
        elif prob < 0.92: estado = 'ATRASO 30'
        elif prob < 0.97: estado = 'ATRASO 60'
        else: estado = 'ATRASO 90+'
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
    if estatus_roll < 0.80: estatus = 'Al corriente'
    elif estatus_roll < 0.90: estatus = 'Atraso 30 días'
    elif estatus_roll < 0.95: estatus = 'Atraso 60 días'
    else: estatus = 'Atraso 90+ días'
    return {
        'numero': num,
        'institucion': random.choice(INSTITUCIONES),
        'tipo': random.choice(TIPOS_CREDITO),
        'monto_original': monto_orig,
        'saldo_actual': saldo,
        'pago_mensual': random.randint(500, 15000),
        'estatus': estatus,
        'fecha_apertura': (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%d/%m/%Y'),
        'limite_credito': random.randint(10000, 300000),
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

def generar_avisos_retiro(creditos):
    avisos = []
    for credito in creditos:
        if 'Atraso' in credito['estatus']:
            dias = 30 if '30' in credito['estatus'] else 60 if '60' in credito['estatus'] else 90
            fecha_retiro = datetime.now() + timedelta(days=(6*365) - dias)
            avisos.append({
                'institucion': credito['institucion'],
                'fecha_retiro': fecha_retiro.strftime('%d/%m/%Y'),
                'descripcion': f"Registro de {credito['institucion']} será eliminado."
            })
    return avisos

def generar_domicilios(estado='CIUDAD DE MEXICO'):
    """Genera 1-3 domicilios aleatorios."""
    colonias = ['CENTRO', 'ROMA NORTE', 'CONDESA', 'POLANCO', 'DEL VALLE', 'JUAREZ']
    calles = ['AV. INSURGENTES', 'CALLE MADERO', 'EJE CENTRAL', 'AV. REFORMA', 'CALLE 5 DE MAYO']
    num_dom = random.randint(1, 3)
    domicilios = []
    for _ in range(num_dom):
        domicilios.append({
            'calle': random.choice(calles),
            'numero_exterior': str(random.randint(10, 9999)),
            'colonia': random.choice(colonias),
            'municipio': estado,
            'estado': estado,
            'codigo_postal': f"{random.randint(1000, 9999)}0",
        })
    return domicilios


# ============================================================
# GENERADOR PRINCIPAL
# ============================================================

def generar_reporte(datos_persona):
    """
    Genera Reporte de Buró completo.
    Soporta personalización opcional.
    """
    # Personalización opcional
    num_creditos = datos_persona.get('num_creditos', random.randint(2, 8))
    rango_score = datos_persona.get('rango_score')  # tuple (min, max) o None
    institucion_especifica = datos_persona.get('institucion')  # str o None
    tipo_especifico = datos_persona.get('tipo_credito')  # str o None
    
    # Score personalizado o aleatorio
    if rango_score:
        score = random.randint(rango_score[0], rango_score[1])
    else:
        score = generar_score()
    
    # Créditos
    creditos = []
    for i in range(num_creditos):
        credito = generar_credito(i+1)
        if institucion_especifica:
            credito['institucion'] = institucion_especifica
        if tipo_especifico:
            credito['tipo'] = tipo_especifico
        creditos.append(credito)
    
    folio = generar_folio()
    fecha_actual = formatear_fecha_buro(datetime.now().strftime('%d-%B-%Y').upper())
    
    total_saldo = sum(c['saldo_actual'] for c in creditos)
    total_pago = sum(c['pago_mensual'] for c in creditos)
    total_limite = sum(c['limite_credito'] for c in creditos)
    al_corriente = sum(1 for c in creditos if c['estatus'] == 'Al corriente')
    
    estado = datos_persona.get('domicilio', {}).get('estado', 'CIUDAD DE MEXICO')
    domicilios = datos_persona.get('domicilios') or generar_domicilios(estado)
    
    return {
        'encabezado': {
            'tipo': 'REPORTE DE CRÉDITO ESPECIAL',
            'folio': folio,
            'folio_formateado': f"{int(folio):,}",
            'fecha': fecha_actual,
            'fecha_registro': '01-ABR-2016',
            'persona_tipo': 'Personas Físicas',
        },
        'consumidor': {
            'nombre': datos_persona.get('nombre', '').upper(),
            'rfc': datos_persona.get('rfc', ''),
            'curp': datos_persona.get('curp', ''),
            'fecha_nacimiento': datos_persona.get('fecha_nacimiento', 'NO DISPONIBLE'),
            'domicilios': domicilios,
            'empleo': random.choice(EMPLEOS),
        },
        'score': {
            'puntaje': score,
            'interpretacion': interpretar_score(score),
            'escala': '400 - 850',
        },
        'resumen': {
            'total_creditos': len(creditos),
            'total_saldo': total_saldo,
            'total_pago': total_pago,
            'total_limite': total_limite,
            'al_corriente': al_corriente,
            'atrasados': len(creditos) - al_corriente,
        },
        'creditos': creditos,
        'consultas': generar_consultas(),
        'avisos_retiro': generar_avisos_retiro(creditos),
                          }
