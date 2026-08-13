from fpdf import FPDF
from datetime import datetime
import io


class ReporteBuroPDF(FPDF):
    """
    Reporte de Buró de Crédito - Versión Compacta.
    Máximo 3-4 páginas, detallado pero simplificado.
    """

    # Colores
    AZUL = (26, 35, 126)
    GRIS_CLARO = (245, 245, 250)
    GRIS_BORDE = (200, 200, 210)
    VERDE = (46, 125, 50)
    AMARILLO = (255, 193, 7)
    ROJO = (198, 40, 40)
    BLANCO = (255, 255, 255)

    def __init__(self, reporte):
        super().__init__('P', 'mm', 'Letter')
        self.r = reporte
        self.set_auto_page_break(auto=True, margin=12)

    def header(self):
        if self.page_no() == 1:
            # Franja azul compacta
            self.set_fill_color(*self.AZUL)
            self.rect(0, 0, 215.9, 18, 'F')
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(*self.BLANCO)
            self.set_xy(0, 3)
            self.cell(215.9, 6, 'REPORTE DE CRÉDITO ESPECIAL', align='C')
            self.set_font('Helvetica', '', 7)
            self.set_xy(0, 10)
            self.cell(215.9, 4, f"Folio: {self.r['encabezado']['folio_formateado']}  |  Fecha: {self.r['encabezado']['fecha']}  |  Registro BC: {self.r['encabezado']['fecha_registro']}", align='C')
            self.set_text_color(0, 0, 0)
            self.set_y(20)
        else:
            self.set_font('Helvetica', '', 7)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, f"Folio: {self.r['encabezado']['folio_formateado']}", align='R', new_x='LMARGIN', new_y='NEXT')
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 6)
        self.set_text_color(150, 150, 150)
        self.cell(0, 4, f'Página {self.page_no()}  |  Reporte sintético sin validez oficial', align='C')
        self.set_text_color(0, 0, 0)

    def _seccion(self, titulo):
        """Título de sección compacto."""
        if self.get_y() > 250:
            self.add_page()
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(230, 232, 240)
        self.set_text_color(*self.AZUL)
        self.cell(0, 6, f'  {titulo}', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def _campo_compacto(self, etiqueta, valor, ancho=35):
        """Campo en línea: etiqueta negrita + valor."""
        self.set_font('Helvetica', 'B', 7)
        self.cell(ancho, 4, etiqueta)
        self.set_font('Helvetica', '', 7)
        self.cell(0, 4, str(valor), new_x='LMARGIN', new_y='NEXT')

    def construir(self):
        self.add_page()
        r = self.r
        c = r['consumidor']

        # ============================================================
        # PÁGINA 1: DATOS GENERALES + SCORE + RESUMEN
        # ============================================================

        # DATOS GENERALES (compacto, 2 columnas)
        self._seccion('DATOS GENERALES')
        self.set_font('Helvetica', '', 8)
        x_izq = self.get_x() + 5
        self.set_xy(x_izq, self.get_y())
        self.cell(100, 4, f"Nombre: {c['nombre']}")
        self.set_xy(x_izq + 105, self.get_y())
        self.cell(95, 4, f"RFC: {c['rfc'] or 'N/D'}")
        self.ln(5)
        
        self.set_xy(x_izq, self.get_y())
        self.cell(100, 4, f"F. Nacimiento: {c['fecha_nacimiento']}")
        self.set_xy(x_izq + 105, self.get_y())
        self.cell(95, 4, f"CURP: {c['curp'] or 'N/D'}")
        self.ln(5)
        
        self.set_xy(x_izq, self.get_y())
        self.cell(100, 4, f"Empleo: {c['empleo']}")
        self.ln(4)

        # DOMICILIOS (compacto, tabla)
        self._seccion('DOMICILIOS REPORTADOS')
        for dom in c.get('domicilios', [])[:3]:
            if self.get_y() > 260:
                self.add_page()
            self.set_font('Helvetica', '', 7)
            direccion = f"{dom.get('calle','')} {dom.get('numero_exterior','')}, Col. {dom.get('colonia','')}, {dom.get('municipio','')}, {dom.get('estado','')}, CP {dom.get('codigo_postal','')}"
            self.set_x(10)
            self.multi_cell(195, 4, direccion, align='L')
            self.ln(1)

        # SCORE (visual, compacto)
        self._seccion('SCORE DE CRÉDITO')
        score = r['score']['puntaje']
        color = self.VERDE if score >= 680 else self.AMARILLO if score >= 600 else self.ROJO
        
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(*color)
        self.cell(0, 10, str(score), align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        
        # Barra compacta
        x_barra = 70
        y_barra = self.get_y()
        self.set_fill_color(220, 220, 220)
        self.rect(x_barra, y_barra, 75, 4, 'F')
        ancho_lleno = int((score - 400) / 450 * 75)
        self.set_fill_color(*color)
        self.rect(x_barra, y_barra, ancho_lleno, 4, 'F')
        self.ln(6)
        
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*color)
        self.cell(0, 5, r['score']['interpretacion'], align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(3)

        # RESUMEN (tabla compacta)
        self._seccion('RESUMEN GENERAL')
        resumen = r['resumen']
        
        # 2 columnas
        self.set_font('Helvetica', '', 7)
        datos_resumen = [
            f"Créditos: {resumen['total_creditos']}",
            f"Saldo total: ${resumen['total_saldo']:,.2f}",
            f"Pago mensual: ${resumen['total_pago']:,.2f}",
            f"Límite total: ${resumen['total_limite']:,.2f}",
            f"Al corriente: {resumen['al_corriente']}",
            f"Atrasados: {resumen['atrasados']}",
        ]
        for i, dato in enumerate(datos_resumen):
            x_pos = 10 + (i % 2) * 100
            if i % 2 == 0 and i > 0:
                self.ln(4)
            self.set_xy(x_pos, self.get_y())
            self.cell(95, 4, dato)
        self.ln(4)

        # ============================================================
        # PÁGINA 2+: CRÉDITOS (compactos)
        # ============================================================
        self._seccion('DETALLE DE CRÉDITOS')
        
        for credito in r['creditos']:
            if self.get_y() > 250:
                self.add_page()
                self._seccion('DETALLE DE CRÉDITOS (continuación)')
            
            color_estado = self.VERDE if credito['estatus'] == 'Al corriente' else self.AMARILLO if '30' in credito['estatus'] else self.ROJO
            
            y0 = self.get_y()
            self.set_fill_color(248, 248, 252)
            self.set_draw_color(*self.GRIS_BORDE)
            self.rect(8, y0, 200, 20, 'DF')
            
            # Línea 1: Institución + Estado
            self.set_xy(10, y0 + 1)
            self.set_font('Helvetica', 'B', 8)
            self.cell(120, 4, f"#{credito['numero']} - {credito['institucion']}")
            self.set_font('Helvetica', 'B', 7)
            self.set_text_color(*color_estado)
            self.cell(70, 4, credito['estatus'], align='R')
            self.set_text_color(0, 0, 0)
            
            # Línea 2: Tipo + Monto + Saldo
            self.set_xy(10, y0 + 6)
            self.set_font('Helvetica', '', 7)
            self.cell(0, 4, f"Tipo: {credito['tipo']}  |  Monto: ${credito['monto_original']:,.0f}  |  Saldo: ${credito['saldo_actual']:,.0f}  |  Pago: ${credito['pago_mensual']:,.0f}")
            
            # Línea 3: Historial resumido
            self.set_xy(10, y0 + 11)
            al_corriente = sum(1 for h in credito['historial'] if h['estado'] == 'AL CORRIENTE')
            total_hist = len(credito['historial'])
            self.cell(0, 4, f"Historial: {al_corriente}/{total_hist} al corriente  |  Apertura: {credito['fecha_apertura']}")
            
            self.set_y(y0 + 22)
            self.ln(1)

        # ============================================================
        # CONSULTAS (tabla compacta)
        # ============================================================
        self._seccion('CONSULTAS RECIENTES')
        
        self.set_fill_color(220, 225, 235)
        self.set_font('Helvetica', 'B', 6)
        self.cell(30, 4, ' Fecha', fill=True, border=1)
        self.cell(75, 4, ' Institución', fill=True, border=1)
        self.cell(0, 4, ' Tipo', fill=True, border=1, new_x='LMARGIN', new_y='NEXT')
        
        self.set_font('Helvetica', '', 6)
        for consulta in r['consultas'][:10]:
            if self.get_y() > 265:
                self.add_page()
            self.cell(30, 4, f" {consulta['fecha']}", border=1)
            self.cell(75, 4, f" {consulta['institucion']}", border=1)
            self.cell(0, 4, f" {consulta['tipo']}", border=1, new_x='LMARGIN', new_y='NEXT')

        # ============================================================
        # AVISOS DE RETIRO
        # ============================================================
        if r.get('avisos_retiro'):
            self._seccion('AVISOS DE RETIRO')
            self.set_font('Helvetica', '', 6)
            for aviso in r['avisos_retiro']:
                self.set_x(10)
                self.multi_cell(195, 4, f"• {aviso['descripcion']} Fecha estimada: {aviso['fecha_retiro']}")
                self.ln(1)

        return self.output()


def generar_pdf_reporte(reporte):
    pdf = ReporteBuroPDF(reporte)
    return pdf.construir()
