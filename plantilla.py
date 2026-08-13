from fpdf import FPDF
from datetime import datetime
import io


class ReporteBuroPDF(FPDF):
    """Reporte de Buró de Crédito - Versión Profesional"""

    # Colores
    AZUL_OSCURO = (26, 35, 126)
    AZUL_MEDIO = (40, 53, 147)
    GRIS_CLARO = (245, 245, 250)
    GRIS_BORDE = (200, 200, 210)
    VERDE = (46, 125, 50)
    AMARILLO = (255, 193, 7)
    ROJO = (198, 40, 40)
    BLANCO = (255, 255, 255)

    def __init__(self, reporte):
        super().__init__('P', 'mm', 'Letter')
        self.r = reporte
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Franja azul superior
        self.set_fill_color(*self.AZUL_OSCURO)
        self.rect(0, 0, 215.9, 28, 'F')
        
        # Título
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(*self.BLANCO)
        self.set_xy(0, 5)
        self.cell(215.9, 8, 'BURÓ DE CRÉDITO', align='C')
        
        self.set_font('Helvetica', '', 9)
        self.set_xy(0, 14)
        self.cell(215.9, 5, self.r['encabezado']['tipo'], align='C')
        
        # Folio y fecha
        self.set_font('Helvetica', '', 6)
        self.set_xy(0, 21)
        self.cell(215.9, 3, f"Folio: {self.r['encabezado']['folio']}    |    Fecha: {self.r['encabezado']['fecha']} {self.r['encabezado']['hora']}", align='C')
        
        self.set_text_color(0, 0, 0)
        self.set_y(32)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*self.GRIS_BORDE)
        self.line(10, self.get_y(), 205, self.get_y())
        self.set_font('Helvetica', '', 6)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, f'Página {self.page_no()}  |  Reporte sintético sin validez oficial  |  Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C')
        self.set_text_color(0, 0, 0)

    def _titulo_seccion(self, titulo):
        """Escribe un título de sección con fondo gris."""
        self.set_font('Helvetica', 'B', 11)
        self.set_fill_color(230, 232, 240)
        self.set_text_color(*self.AZUL_OSCURO)
        self.cell(0, 8, f'  {titulo}', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def _campo(self, etiqueta, valor, ancho_etiqueta=35):
        """Escribe un campo etiqueta: valor."""
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*self.AZUL_MEDIO)
        self.cell(ancho_etiqueta, 5, etiqueta)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, str(valor), new_x='LMARGIN', new_y='NEXT')

    def construir(self):
        self.add_page()
        r = self.r

        # ============================================================
        # SECCIÓN: DATOS DEL CONSUMIDOR
        # ============================================================
        self._titulo_seccion('DATOS DEL CONSUMIDOR')
        
        self._campo('Nombre:', r['consumidor']['nombre'])
        self._campo('RFC:', r['consumidor']['rfc'])
        self._campo('CURP:', r['consumidor']['curp'])
        self._campo('Empleo:', r['consumidor']['empleo'])
        
        dom = r['consumidor']['domicilio']
        self._campo('Domicilio:', f"{dom.get('calle','')} {dom.get('numero_exterior','')}, Col. {dom.get('colonia','')}, CP {dom.get('codigo_postal','')}")
        self.ln(4)

        # ============================================================
        # SECCIÓN: SCORE DE CRÉDITO
        # ============================================================
        self._titulo_seccion('SCORE DE CRÉDITO')
        
        score = r['score']['puntaje']
        
        # Número grande
        self.set_font('Helvetica', 'B', 36)
        color_score = self.VERDE if score >= 680 else self.AMARILLO if score >= 600 else self.ROJO
        self.set_text_color(*color_score)
        self.cell(0, 14, str(score), align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        # Barra visual
        x_barra = 60
        y_barra = self.get_y()
        ancho_total = 95
        self.set_fill_color(220, 220, 220)
        self.rect(x_barra, y_barra, ancho_total, 6, 'F')
        
        ancho_lleno = int((score - 400) / 450 * ancho_total)
        self.set_fill_color(*color_score)
        self.rect(x_barra, y_barra, ancho_lleno, 6, 'F')
        
        # Borde de la barra
        self.set_draw_color(180, 180, 180)
        self.rect(x_barra, y_barra, ancho_total, 6)
        self.ln(9)
        
        # Interpretación
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*color_score)
        self.cell(0, 6, r['score']['interpretacion'], align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        self.set_font('Helvetica', '', 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 4, 'Escala: 400 - 850', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(4)

        # ============================================================
        # SECCIÓN: RESUMEN GENERAL
        # ============================================================
        self._titulo_seccion('RESUMEN GENERAL')
        
        resumen = r['resumen']
        
        # Tabla resumen
        self.set_fill_color(*self.AZUL_OSCURO)
        self.set_text_color(*self.BLANCO)
        self.set_font('Helvetica', 'B', 8)
        self.cell(95, 6, '  CONCEPTO', fill=True, border=1)
        self.cell(0, 6, '  VALOR', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        items = [
            ('Total de créditos', str(resumen['total_creditos'])),
            ('Saldo total', f"${resumen['total_saldo']:,.2f}"),
            ('Pago mensual total', f"${resumen['total_pago']:,.2f}"),
            ('Al corriente', str(resumen['al_corriente'])),
            ('Atrasados', str(resumen['atrasados'])),
        ]
        
        for i, (concepto, valor) in enumerate(items):
            if i % 2 == 0:
                self.set_fill_color(250, 250, 252)
            else:
                self.set_fill_color(240, 240, 245)
            
            self.set_font('Helvetica', '', 8)
            self.cell(95, 5, f'  {concepto}', fill=True, border=1)
            self.set_font('Helvetica', 'B', 8)
            self.cell(0, 5, f'  {valor}', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
        
        self.ln(5)

        # ============================================================
        # SECCIÓN: DETALLE DE CRÉDITOS
        # ============================================================
        self._titulo_seccion('DETALLE DE CRÉDITOS')
        
        for credito in r['creditos']:
            color_estado = self.VERDE if credito['estatus'] == 'Al corriente' else self.AMARILLO if '30' in credito['estatus'] else self.ROJO
            
            # Tarjeta del crédito
            y_inicio = self.get_y()
            self.set_fill_color(252, 252, 255)
            self.set_draw_color(*self.GRIS_BORDE)
            self.rect(10, y_inicio, 195, 42, 'DF')
            
            # Encabezado de la tarjeta
            self.set_fill_color(235, 236, 245)
            self.rect(10, y_inicio, 195, 7, 'F')
            self.set_xy(13, y_inicio + 1)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*self.AZUL_OSCURO)
            self.cell(0, 4, f"CRÉDITO #{credito['numero']}  |  {credito['institucion']}")
            self.set_text_color(0, 0, 0)
            
            # Datos
            self.set_xy(13, y_inicio + 9)
            self.set_font('Helvetica', '', 7.5)
            self.cell(0, 4, f"Tipo: {credito['tipo']}")
            
            self.set_xy(13, y_inicio + 14)
            self.cell(0, 4, f"Monto original: ${credito['monto_original']:,.2f}    |    Saldo actual: ${credito['saldo_actual']:,.2f}")
            
            self.set_xy(13, y_inicio + 19)
            self.cell(0, 4, f"Pago mensual: ${credito['pago_mensual']:,.2f}    |    Apertura: {credito['fecha_apertura']}")
            
            # Estado
            self.set_xy(13, y_inicio + 25)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*color_estado)
            self.cell(0, 4, f"Estado: {credito['estatus']}")
            self.set_text_color(0, 0, 0)
            
            # Historial mini
            self.set_xy(120, y_inicio + 25)
            self.set_font('Helvetica', '', 6)
            historial_str = ' '.join(h['estado'][:1] for h in credito['historial'][:24])
            self.cell(0, 4, f"Historial: {historial_str}")
            
            self.set_y(y_inicio + 44)
            self.ln(2)

        # ============================================================
        # SECCIÓN: CONSULTAS
        # ============================================================
        self._titulo_seccion('CONSULTAS REALIZADAS')
        
        # Encabezados de tabla
        self.set_fill_color(*self.AZUL_OSCURO)
        self.set_text_color(*self.BLANCO)
        self.set_font('Helvetica', 'B', 7)
        self.cell(35, 5, '  FECHA', fill=True, border=1)
        self.cell(80, 5, '  INSTITUCIÓN', fill=True, border=1)
        self.cell(0, 5, '  TIPO', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        for i, consulta in enumerate(r['consultas'][:15]):
            if i % 2 == 0:
                self.set_fill_color(250, 250, 252)
            else:
                self.set_fill_color(240, 240, 245)
            self.set_font('Helvetica', '', 7)
            self.cell(35, 4, f'  {consulta["fecha"]}', fill=True, border=1)
            self.cell(80, 4, f'  {consulta["institucion"]}', fill=True, border=1)
            self.cell(0, 4, f'  {consulta["tipo"]}', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')

        return self.output()


def generar_pdf_reporte(reporte):
    pdf = ReporteBuroPDF(reporte)
    return pdf.construir()
