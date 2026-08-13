from fpdf import FPDF
from datetime import datetime
import io


class ReporteBuroPDF(FPDF):
    def __init__(self, reporte):
        super().__init__('P', 'mm', 'Letter')
        self.r = reporte
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() == 1:
            self.set_fill_color(26, 35, 126)
            self.rect(0, 0, 215.9, 25, 'F')
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.set_xy(0, 5)
            self.cell(215.9, 8, 'BURÓ DE CRÉDITO', align='C')
            self.set_font('Helvetica', '', 10)
            self.set_xy(0, 15)
            self.cell(215.9, 5, self.r['encabezado']['tipo'], align='C')
            self.set_font('Helvetica', '', 7)
            self.set_xy(0, 20)
            self.cell(215.9, 3, f"Folio: {self.r['encabezado']['folio']}  |  {self.r['encabezado']['fecha']} {self.r['encabezado']['hora']}", align='C')
            self.set_text_color(0, 0, 0)
            self.set_y(28)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 7)
        self.cell(0, 5, f'Página {self.page_no()} - Reporte sintético sin validez oficial', align='C')

    def construir(self):
        self.add_page()
        r = self.r

        # ============================================================
        # DATOS DEL CONSUMIDOR
        # ============================================================
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, '  DATOS DEL CONSUMIDOR', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        self.set_font('Helvetica', '', 10)
        datos = [
            ('Nombre:', r['consumidor']['nombre']),
            ('RFC:', r['consumidor']['rfc']),
            ('CURP:', r['consumidor']['curp']),
            ('Empleo:', r['consumidor']['empleo']),
        ]
        for etiqueta, valor in datos:
            self.set_font('Helvetica', 'B', 9)
            self.cell(30, 5, etiqueta)
            self.set_font('Helvetica', '', 9)
            self.cell(0, 5, str(valor), new_x='LMARGIN', new_y='NEXT')

        # Domicilio
        dom = r['consumidor']['domicilio']
        self.set_font('Helvetica', 'B', 9)
        self.cell(30, 5, 'Domicilio:')
        self.set_font('Helvetica', '', 9)
        self.cell(0, 5, f"{dom.get('calle','')} {dom.get('numero_exterior','')}, Col. {dom.get('colonia','')}, CP {dom.get('codigo_postal','')}", new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

        # ============================================================
        # SCORE
        # ============================================================
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, '  SCORE DE CRÉDITO', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

        score = r['score']['puntaje']
        self.set_font('Helvetica', 'B', 28)
        self.cell(0, 12, str(score), align='C', new_x='LMARGIN', new_y='NEXT')
        
        # Barra visual
        self.set_fill_color(200, 200, 200)
        self.rect(50, self.get_y(), 110, 5, 'F')
        ancho = int((score - 400) / 450 * 110)
        if score >= 680:
            self.set_fill_color(46, 125, 50)
        elif score >= 600:
            self.set_fill_color(255, 193, 7)
        else:
            self.set_fill_color(198, 40, 40)
        self.rect(50, self.get_y(), ancho, 5, 'F')
        self.ln(7)

        self.set_font('Helvetica', 'B', 11)
        color_score = (46, 125, 50) if score >= 680 else (255, 193, 7) if score >= 600 else (198, 40, 40)
        self.set_text_color(*color_score)
        self.cell(0, 6, r['score']['interpretacion'], align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(4)

        # ============================================================
        # RESUMEN
        # ============================================================
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, '  RESUMEN GENERAL', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        resumen = r['resumen']
        items = [
            ('Total de créditos:', str(resumen['total_creditos'])),
            ('Saldo total:', f"${resumen['total_saldo']:,.2f}"),
            ('Pago mensual total:', f"${resumen['total_pago']:,.2f}"),
            ('Al corriente:', str(resumen['al_corriente'])),
            ('Atrasados:', str(resumen['atrasados'])),
        ]
        for etiqueta, valor in items:
            self.set_font('Helvetica', '', 9)
            self.cell(50, 5, etiqueta)
            self.set_font('Helvetica', 'B', 9)
            self.cell(0, 5, valor, new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

        # ============================================================
        # DETALLE DE CRÉDITOS
        # ============================================================
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, '  DETALLE DE CRÉDITOS', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        for credito in r['creditos']:
            color_estado = (46, 125, 50) if credito['estatus'] == 'Al corriente' else (255, 193, 7) if '30' in credito['estatus'] else (198, 40, 40)
            
            # Caja del crédito
            self.set_fill_color(245, 245, 250)
            self.set_draw_color(200, 200, 200)
            self.rect(10, self.get_y(), 195, 45, 'DF')
            
            x0 = self.get_x() + 5
            y0 = self.get_y() + 2
            
            self.set_xy(x0, y0)
            self.set_font('Helvetica', 'B', 10)
            self.cell(0, 5, f"CRÉDITO #{credito['numero']} - {credito['institucion']}")
            
            self.set_xy(x0, y0 + 6)
            self.set_font('Helvetica', '', 8)
            self.cell(0, 4, f"Tipo: {credito['tipo']}")
            
            self.set_xy(x0, y0 + 10)
            self.cell(0, 4, f"Monto original: ${credito['monto_original']:,.2f}  |  Saldo: ${credito['saldo_actual']:,.2f}")
            
            self.set_xy(x0, y0 + 14)
            self.cell(0, 4, f"Pago mensual: ${credito['pago_mensual']:,.2f}  |  Apertura: {credito['fecha_apertura']}")
            
            self.set_xy(x0, y0 + 18)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*color_estado)
            self.cell(0, 4, f"Estado: {credito['estatus']}")
            self.set_text_color(0, 0, 0)
            
            self.set_y(y0 + 44)
            self.ln(3)

        # ============================================================
        # CONSULTAS
        # ============================================================
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, '  CONSULTAS REALIZADAS', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        self.set_font('Helvetica', 'B', 8)
        self.cell(30, 5, 'FECHA')
        self.cell(70, 5, 'INSTITUCIÓN')
        self.cell(0, 5, 'TIPO', new_x='LMARGIN', new_y='NEXT')
        
        self.set_font('Helvetica', '', 8)
        for consulta in r['consultas'][:15]:
            self.cell(30, 4, consulta['fecha'])
            self.cell(70, 4, consulta['institucion'])
            self.cell(0, 4, consulta['tipo'], new_x='LMARGIN', new_y='NEXT')

        return self.output()


def generar_pdf_reporte(reporte):
    pdf = ReporteBuroPDF(reporte)
    return pdf.construir()
