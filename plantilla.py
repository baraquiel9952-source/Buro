from fpdf import FPDF
from datetime import datetime
import io


class ReporteBuroPDF(FPDF):
    """Réplica del Reporte de Buró de Crédito Real"""

    def __init__(self, reporte):
        super().__init__('P', 'mm', 'Letter')
        self.r = reporte
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() == 1:
            # Título principal
            self.set_font('Helvetica', 'B', 18)
            self.cell(0, 10, 'REPORTE DE CRÉDITO', align='C', new_x='LMARGIN', new_y='NEXT')
            self.cell(0, 10, 'ESPECIAL', align='C', new_x='LMARGIN', new_y='NEXT')
            self.ln(3)
            
            # Fecha y folio
            self.set_font('Helvetica', 'B', 8)
            self.cell(60, 5, 'Fecha de Consulta:')
            self.set_font('Helvetica', '', 8)
            self.cell(60, 5, self.r['encabezado']['fecha'])
            self.set_font('Helvetica', 'B', 8)
            self.cell(50, 5, 'Folio de Consulta:')
            self.set_font('Helvetica', '', 8)
            self.cell(0, 5, f"{int(self.r['encabezado']['folio']):,}", new_x='LMARGIN', new_y='NEXT')
            
            self.set_font('Helvetica', 'B', 8)
            self.cell(60, 5, 'Fecha de Registro de BC:')
            self.set_font('Helvetica', '', 8)
            self.cell(0, 5, '01-ABR-2016', new_x='LMARGIN', new_y='NEXT')
            self.ln(3)
            
            # Personas Físicas
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, 'Personas Físicas', align='C', new_x='LMARGIN', new_y='NEXT')
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)

    def _seccion(self, titulo):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 8, titulo, new_x='LMARGIN', new_y='NEXT')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def construir(self):
        self.add_page()
        r = self.r

        # DATOS GENERALES
        self._seccion('DATOS GENERALES')
        
        self.set_font('Helvetica', 'B', 9)
        self.cell(40, 6, 'Nombre:')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 6, r['consumidor']['nombre'], new_x='LMARGIN', new_y='NEXT')
        
        self.set_font('Helvetica', 'B', 9)
        self.cell(40, 6, 'Fecha de Nacimiento:')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 6, r['consumidor'].get('fecha_nacimiento', 'NO DISPONIBLE'), new_x='LMARGIN', new_y='NEXT')
        
        self.set_font('Helvetica', 'B', 9)
        self.cell(40, 6, 'RFC:')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 6, r['consumidor']['rfc'], new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

        # DOMICILIOS
        self._seccion('DOMICILIO(S) REPORTADO(S)')
        
        domicilios = r['consumidor'].get('domicilios', [r['consumidor'].get('domicilio', {})])
        
        for dom in domicilios:
            # Tabla de domicilio
            self.set_fill_color(240, 240, 245)
            self.set_draw_color(180, 180, 190)
            
            y0 = self.get_y()
            # Encabezados
            self.set_font('Helvetica', 'B', 7)
            self.set_fill_color(220, 225, 235)
            self.cell(35, 6, ' Calle y Número', fill=True, border=1)
            self.cell(30, 6, ' Colonia', fill=True, border=1)
            self.cell(30, 6, ' Del/Mpio', fill=True, border=1)
            self.cell(35, 6, ' Ciudad', fill=True, border=1)
            self.cell(20, 6, ' C.P.', fill=True, border=1)
            self.cell(25, 6, ' País', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
            
            # Datos
            self.set_font('Helvetica', '', 7)
            self.cell(35, 6, f" {dom.get('calle','')} {dom.get('numero_exterior','')}", border=1)
            self.cell(30, 6, f" {dom.get('colonia','')}", border=1)
            self.cell(30, 6, f" {dom.get('municipio','')}", border=1)
            self.cell(35, 6, f" {dom.get('estado','')}", border=1)
            self.cell(20, 6, f" {dom.get('codigo_postal','')}", border=1)
            self.cell(25, 6, ' México', border=1, new_x='LMARGIN', new_y='NEXT')
            self.ln(4)

        # SCORE
        self._seccion('SCORE DE CRÉDITO')
        
        score = r['score']['puntaje']
        color = (46, 125, 50) if score >= 680 else (255, 193, 7) if score >= 600 else (198, 40, 40)
        
        self.set_font('Helvetica', 'B', 32)
        self.set_text_color(*color)
        self.cell(0, 12, str(score), align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*color)
        self.cell(0, 6, r['score']['interpretacion'], align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(4)

        # CRÉDITOS
        self._seccion('DETALLE DE CRÉDITOS')
        
        for credito in r['creditos']:
            color_estado = (46, 125, 50) if credito['estatus'] == 'Al corriente' else (255, 193, 7) if '30' in credito['estatus'] else (198, 40, 40)
            
            y0 = self.get_y()
            self.set_fill_color(248, 248, 252)
            self.set_draw_color(180, 180, 190)
            self.rect(10, y0, 195, 30, 'DF')
            
            self.set_xy(13, y0 + 2)
            self.set_font('Helvetica', 'B', 9)
            self.cell(0, 5, f"Crédito #{credito['numero']} - {credito['institucion']}")
            
            self.set_xy(13, y0 + 9)
            self.set_font('Helvetica', '', 7)
            self.cell(0, 4, f"Tipo: {credito['tipo']}  |  Monto: ${credito['monto_original']:,.2f}  |  Saldo: ${credito['saldo_actual']:,.2f}")
            
            self.set_xy(13, y0 + 15)
            self.cell(0, 4, f"Pago: ${credito['pago_mensual']:,.2f}  |  Apertura: {credito['fecha_apertura']}")
            
            self.set_xy(13, y0 + 22)
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*color_estado)
            self.cell(0, 4, f"Estado: {credito['estatus']}")
            self.set_text_color(0, 0, 0)
            
            self.set_y(y0 + 32)
            self.ln(2)

        # CONSULTAS
        self._seccion('CONSULTAS REALIZADAS')
        
        self.set_fill_color(220, 225, 235)
        self.set_font('Helvetica', 'B', 7)
        self.cell(35, 5, ' Fecha', fill=True, border=1)
        self.cell(70, 5, ' Institución', fill=True, border=1)
        self.cell(0, 5, ' Tipo', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
        
        for consulta in r['consultas'][:15]:
            self.set_font('Helvetica', '', 7)
            self.cell(35, 4, f" {consulta['fecha']}", border=1)
            self.cell(70, 4, f" {consulta['institucion']}", border=1)
            self.cell(0, 4, f" {consulta['tipo']}", border=1, new_x='LMARGIN', new_y='NEXT')

        return self.output()


def generar_pdf_reporte(reporte):
    pdf = ReporteBuroPDF(reporte)
    return pdf.construir()
