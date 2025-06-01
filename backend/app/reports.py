import io
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging
import os
import base64
from io import BytesIO

# Imports do ReportLab com tratamento de erro
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ReportLab não disponível: {e}")
    REPORTLAB_AVAILABLE = False

# Imports do PIL com tratamento de erro
try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PIL não disponível: {e}")
    PIL_AVAILABLE = False

# Configurar logging
logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        """Inicializa o gerador de relatórios com verificações de dependências"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab não está disponível. Instale com: pip install reportlab")
        
        self.company_name = "AraldiTech"
        self.company_subtitle = "Sistema de Gestão de Pedidos"
        
        # Paleta de cores profissional em tons de cinza
        self.primary_color = colors.Color(0.2, 0.2, 0.2)      # #333333 - Cinza escuro
        self.secondary_color = colors.Color(0.4, 0.4, 0.4)    # #666666 - Cinza médio
        self.accent_color = colors.Color(0.6, 0.6, 0.6)       # #999999 - Cinza claro
        self.light_gray = colors.Color(0.9, 0.9, 0.9)         # #E6E6E6 - Cinza muito claro
        self.dark_gray = colors.Color(0.1, 0.1, 0.1)          # #1A1A1A - Quase preto
        self.shadow_color = colors.Color(0, 0, 0, alpha=0.15)  # Sombra sutil
        
        # Caminho para a logo vetorial preta
        self.logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo_vetor.png')
        
        # Cache de estilos
        self._styles_cache = None
        
    def create_professional_logo(self, canvas, x, y, width=120, height=40):
        """Cria o logo profissional da empresa com sombra sutil"""
        try:
            if os.path.exists(self.logo_path):
                # Desenhar sombra sutil
                canvas.saveState()
                canvas.setFillColor(self.shadow_color)
                canvas.rect(x + 1, y - 1, width, height, fill=1, stroke=0)
                canvas.restoreState()
                
                # Fundo branco para contraste
                canvas.setFillColor(colors.white)
                canvas.rect(x, y, width, height, fill=1, stroke=0)
                
                # Borda sutil
                canvas.setStrokeColor(self.light_gray)
                canvas.setLineWidth(0.5)
                canvas.rect(x, y, width, height, fill=0, stroke=1)
                
                # Desenhar o logo
                canvas.drawImage(self.logo_path, x + 5, y + 5, width=width-10, height=height-10, 
                               preserveAspectRatio=True, mask='auto')
                logger.info("Logo vetorial carregada com sucesso")
            else:
                logger.warning(f"Logo não encontrada em: {self.logo_path}")
                self.create_professional_text_logo(canvas, x, y, width, height)
        except Exception as e:
            logger.error(f"Erro ao carregar logo: {e}")
            self.create_professional_text_logo(canvas, x, y, width, height)
    
    def create_professional_text_logo(self, canvas, x, y, width, height):
        """Cria um logo de texto profissional como fallback"""
        try:
            # Sombra sutil
            canvas.saveState()
            canvas.setFillColor(self.shadow_color)
            canvas.rect(x + 1, y - 1, width, height, fill=1, stroke=0)
            canvas.restoreState()
            
            # Fundo branco
            canvas.setFillColor(colors.white)
            canvas.rect(x, y, width, height, fill=1, stroke=0)
            
            # Borda elegante
            canvas.setStrokeColor(self.primary_color)
            canvas.setLineWidth(1)
            canvas.rect(x, y, width, height, fill=0, stroke=1)
            
            # Texto da empresa
            canvas.setFillColor(self.dark_gray)
            canvas.setFont("Helvetica-Bold", 14)
            text_x = x + 10
            text_y = y + height - 18
            canvas.drawString(text_x, text_y, self.company_name)
            
            # Subtítulo
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(self.secondary_color)
            canvas.drawString(text_x, text_y - 15, "Sistema de Gestão")
            
            logger.info("Logo de texto criada como fallback")
        except Exception as e:
            logger.error(f"Erro ao criar logo de texto: {e}")
        
    def create_header_footer(self, canvas, doc):
        """Cria cabeçalho e rodapé profissionais em tons de cinza"""
        try:
            canvas.saveState()
            
            # === CABEÇALHO ===
            # Fundo do cabeçalho
            canvas.setFillColor(self.light_gray)
            canvas.rect(0, doc.height + 2*cm, doc.width + 2*cm, 2*cm, fill=1)
            
            # Linha superior elegante
            canvas.setStrokeColor(self.primary_color)
            canvas.setLineWidth(2)
            canvas.line(0, doc.height + 4*cm, doc.width + 2*cm, doc.height + 4*cm)
            
            # Logo profissional
            logo_x = 2*cm
            logo_y = doc.height + 2.3*cm
            self.create_professional_logo(canvas, logo_x, logo_y, width=120, height=40)
            
            # Informações da empresa no cabeçalho
            canvas.setFillColor(self.dark_gray)
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawRightString(doc.width, doc.height + 3.5*cm, "AraldiTech")
            
            canvas.setFont("Helvetica", 10)
            canvas.setFillColor(self.secondary_color)
            canvas.drawRightString(doc.width, doc.height + 3.2*cm, "Sistema de Gestão de Pedidos")
            
            canvas.setFont("Helvetica", 8)
            canvas.drawRightString(doc.width, doc.height + 2.9*cm, 
                                  f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
            
            # Linha decorativa no cabeçalho
            canvas.setStrokeColor(self.accent_color)
            canvas.setLineWidth(1)
            canvas.line(2*cm, doc.height + 2*cm, doc.width, doc.height + 2*cm)
            
            # === RODAPÉ ===
            # Fundo do rodapé
            canvas.setFillColor(self.primary_color)
            canvas.rect(0, 0, doc.width + 2*cm, 1.5*cm, fill=1)
            
            # Linha superior do rodapé
            canvas.setStrokeColor(self.accent_color)
            canvas.setLineWidth(1)
            canvas.line(0, 1.5*cm, doc.width + 2*cm, 1.5*cm)
            
            # Informações do rodapé
            canvas.setFillColor(colors.white)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(2*cm, 1*cm, f"© {datetime.now().year} {self.company_name}")
            
            canvas.setFont("Helvetica", 8)
            canvas.drawString(2*cm, 0.7*cm, "Sistema de Gestão de Pedidos - Relatório Confidencial")
            canvas.drawString(2*cm, 0.4*cm, "Este documento contém informações proprietárias da empresa")
            
            # Número da página
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawRightString(doc.width, 1*cm, f"Página {doc.page}")
            
            # Status do documento
            canvas.setFont("Helvetica", 8)
            canvas.drawRightString(doc.width, 0.7*cm, "DOCUMENTO CONTROLADO")
            canvas.drawRightString(doc.width, 0.4*cm, f"ID: RPT-{datetime.now().strftime('%Y%m%d%H%M')}")
            
            canvas.restoreState()
            
        except Exception as e:
            logger.error(f"Erro ao criar cabeçalho/rodapé: {e}")

    def get_professional_styles(self):
        """Define estilos profissionais em tons de cinza com cache"""
        if self._styles_cache is not None:
            return self._styles_cache
            
        try:
            styles = getSampleStyleSheet()
            
            # Título principal elegante
            title_style = ParagraphStyle(
                name='ProfessionalTitle',
                parent=styles['Title'],
                fontSize=24,
                spaceAfter=30,
                spaceBefore=20,
                textColor=self.dark_gray,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                borderWidth=2,
                borderColor=self.primary_color,
                borderPadding=20,
                backColor=colors.white,
                leftIndent=0,
                rightIndent=0
            )
            styles.add(title_style)
            
            # Subtítulo profissional
            subtitle_style = ParagraphStyle(
                name='ProfessionalSubtitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                spaceBefore=15,
                textColor=self.secondary_color,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                borderWidth=1,
                borderColor=self.accent_color,
                borderPadding=10,
                backColor=self.light_gray
            )
            styles.add(subtitle_style)
            
            # Cabeçalho de seção
            section_style = ParagraphStyle(
                name='SectionHeader',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=15,
                spaceBefore=25,
                textColor=colors.white,
                fontName='Helvetica-Bold',
                borderWidth=0,
                borderPadding=12,
                backColor=self.primary_color,
                leftIndent=0,
                alignment=TA_LEFT
            )
            styles.add(section_style)
            
            # Texto normal profissional
            normal_style = ParagraphStyle(
                name='ProfessionalNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                textColor=self.dark_gray,
                fontName='Helvetica',
                leading=16,
                alignment=TA_JUSTIFY
            )
            styles.add(normal_style)
            
            # Texto de destaque
            highlight_style = ParagraphStyle(
                name='ProfessionalHighlight',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                spaceBefore=8,
                textColor=self.dark_gray,
                fontName='Helvetica-Bold',
                backColor=self.light_gray,
                borderPadding=10,
                borderWidth=1,
                borderColor=self.accent_color,
                leftIndent=15,
                rightIndent=15
            )
            styles.add(highlight_style)
            
            # Caixa de informações
            info_style = ParagraphStyle(
                name='InfoBox',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=15,
                spaceBefore=15,
                textColor=self.secondary_color,
                fontName='Helvetica',
                borderWidth=1,
                borderColor=self.accent_color,
                borderPadding=15,
                backColor=colors.white,
                leftIndent=20,
                rightIndent=20
            )
            styles.add(info_style)
            
            self._styles_cache = styles
            logger.info("Estilos profissionais criados com sucesso")
            return styles
            
        except Exception as e:
            logger.error(f"Erro ao criar estilos: {e}")
            # Retornar estilos básicos como fallback
            return getSampleStyleSheet()

    def create_professional_summary_table(self, data: Dict[str, Any]):
        """Cria tabela de resumo profissional em tons de cinza"""
        try:
            summary_data = [
                ['MÉTRICA', 'VALOR', 'OBSERVAÇÕES']
            ]
            
            # Dados básicos
            summary_data.extend([
                ['Total de Registros', str(data.get('total_records', 0)), 'Registros encontrados no período'],
                ['Período do Relatório', data.get('period_label', 'N/A'), 'Intervalo de datas analisado'],
                ['Data de Geração', datetime.now().strftime('%d/%m/%Y %H:%M'), 'Momento da criação do relatório'],
                ['Usuário Responsável', data.get('user_name', 'Sistema'), 'Usuário que solicitou o relatório']
            ])
            
            # Adicionar métricas específicas
            if data.get('report_type') == 'pedidos':
                pending = data.get('pending_count', 0)
                completed = data.get('completed_count', 0)
                cancelled = data.get('cancelled_count', 0)
                completion_rate = data.get('completion_rate', 0)
                total_records = max(data.get('total_records', 1), 1)
                
                summary_data.extend([
                    ['', '', ''],  # Linha separadora
                    ['ANÁLISE DE PEDIDOS', '', ''],
                    ['Pedidos Pendentes', str(pending), f'{(pending/total_records*100):.1f}% do total'],
                    ['Pedidos Concluídos', str(completed), f'{(completed/total_records*100):.1f}% do total'],
                    ['Pedidos Cancelados', str(cancelled), f'{(cancelled/total_records*100):.1f}% do total'],
                    ['Taxa de Conclusão', f"{completion_rate:.1f}%", 'Eficiência do processo de pedidos'],
                    ['Status Predominante', self.get_predominant_status(pending, completed, cancelled), 'Status com maior volume']
                ])
                
            elif data.get('report_type') == 'atividades':
                creation = data.get('creation_count', 0)
                update = data.get('update_count', 0)
                query = data.get('query_count', 0)
                
                summary_data.extend([
                    ['', '', ''],  # Linha separadora
                    ['ANÁLISE DE ATIVIDADES', '', ''],
                    ['Atividades de Criação', str(creation), 'Novos registros criados no sistema'],
                    ['Atividades de Atualização', str(update), 'Registros modificados pelos usuários'],
                    ['Atividades de Consulta', str(query), 'Acessos e visualizações realizadas'],
                    ['Total de Interações', str(creation + update + query), 'Soma de todas as atividades']
                ])
            
            table = Table(summary_data, colWidths=[5*cm, 3.5*cm, 6.5*cm])
            table.setStyle(TableStyle([
                # Cabeçalho principal
                ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Dados principais
                ('BACKGROUND', (0, 1), (-1, 4), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, 4), self.dark_gray),
                ('FONTNAME', (0, 1), (-1, 4), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, 4), 10),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                
                # Linha separadora
                ('BACKGROUND', (0, 5), (-1, 5), self.light_gray),
                
                # Seções de métricas
                ('BACKGROUND', (0, 6), (-1, 6), self.secondary_color),
                ('TEXTCOLOR', (0, 6), (-1, 6), colors.white),
                ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 6), (-1, 6), 10),
                ('SPAN', (0, 6), (2, 6)),
                ('ALIGN', (0, 6), (-1, 6), 'CENTER'),
                
                # Dados das métricas
                ('TEXTCOLOR', (0, 7), (-1, -1), self.dark_gray),
                ('FONTNAME', (0, 7), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 7), (-1, -1), 9),
                
                # Bordas profissionais
                ('GRID', (0, 0), (-1, -1), 1, self.secondary_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10)
            ]))
            
            # Cores alternadas para as linhas de dados
            for i in range(7, len(summary_data)):
                if i % 2 == 0:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), self.light_gray)
                    ]))
                else:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), colors.white)
                    ]))
            
            return table
            
        except Exception as e:
            logger.error(f"Erro ao criar tabela de resumo: {e}")
            # Retornar tabela simples como fallback
            simple_data = [['Erro ao gerar resumo', str(e)]]
            return Table(simple_data)

    def get_predominant_status(self, pending, completed, cancelled):
        """Determina o status predominante"""
        try:
            statuses = {'Pendente': pending, 'Concluído': completed, 'Cancelado': cancelled}
            return max(statuses, key=statuses.get)
        except Exception:
            return 'N/A'

    def create_professional_data_table(self, df: pd.DataFrame, title: str = "Dados do Relatório"):
        """Cria tabela de dados profissional em tons de cinza"""
        try:
            if df.empty:
                empty_table = Table([['NENHUM DADO ENCONTRADO PARA O PERÍODO SELECIONADO']], 
                                   colWidths=[16*cm])
                empty_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), self.light_gray),
                    ('TEXTCOLOR', (0, 0), (-1, -1), self.secondary_color),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 30),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
                    ('GRID', (0, 0), (-1, -1), 2, self.secondary_color)
                ]))
                return empty_table
            
            # Preparar dados da tabela
            data = [df.columns.tolist()]
            for _, row in df.iterrows():
                formatted_row = []
                for value in row:
                    if isinstance(value, str) and len(value) > 30:
                        formatted_row.append(value[:27] + "...")
                    elif isinstance(value, float):
                        formatted_row.append(f"{value:.2f}")
                    else:
                        formatted_row.append(str(value) if value is not None else "")
                data.append(formatted_row)
            
            # Calcular larguras das colunas
            num_cols = len(df.columns)
            available_width = 16*cm
            col_width = available_width / num_cols if num_cols > 0 else available_width
            col_widths = [col_width] * num_cols
            
            table = Table(data, colWidths=col_widths, repeatRows=1)
            
            # Estilo profissional da tabela
            table_style = [
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Dados
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('TEXTCOLOR', (0, 1), (-1, -1), self.dark_gray),
                
                # Bordas e espaçamento
                ('GRID', (0, 0), (-1, -1), 0.5, self.secondary_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5)
            ]
            
            # Cores alternadas para as linhas
            for i in range(1, len(data)):
                if i % 2 == 0:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), self.light_gray))
                else:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
            
            table.setStyle(TableStyle(table_style))
            return table
            
        except Exception as e:
            logger.error(f"Erro ao criar tabela de dados: {e}")
            # Retornar tabela de erro como fallback
            error_data = [['Erro ao gerar tabela', str(e)]]
            return Table(error_data)

    def apply_filters(self, data: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """Aplica filtros personalizados aos dados"""
        try:
            if not filters or not data:
                return data
            
            filtered_data = data.copy()
            
            # Filtro por status
            if filters.get('status'):
                filtered_data = [item for item in filtered_data 
                               if item.get('status') == filters['status']]
            
            # Filtro por categoria
            if filters.get('categoria'):
                filtered_data = [item for item in filtered_data 
                               if item.get('categoria') == filters['categoria']]
            
            # Filtro por urgência
            if filters.get('urgencia'):
                filtered_data = [item for item in filtered_data 
                               if item.get('urgencia') == filters['urgencia']]
            
            # Filtro por setor
            if filters.get('setor'):
                filtered_data = [item for item in filtered_data 
                               if item.get('setor') == filters['setor']]
            
            # Filtro por usuário
            if filters.get('usuario'):
                filtered_data = [item for item in filtered_data 
                               if item.get('usuario_nome') == filters['usuario']]
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"Erro ao aplicar filtros: {e}")
            return data

    def generate_pdf_report(self, data: List[Dict], report_config: Dict[str, Any]) -> io.BytesIO:
        """Gera relatório PDF profissional em tons de cinza"""
        try:
            buffer = io.BytesIO()
            
            # Configurar documento
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=3.5*cm,
                bottomMargin=2.5*cm
            )
            
            # Aplicar filtros se especificados
            if report_config.get('filters'):
                data = self.apply_filters(data, report_config['filters'])
            
            # Preparar elementos do relatório
            elements = []
            styles = self.get_professional_styles()
            
            # Título do relatório
            title = report_config.get('title', 'Relatório do Sistema')
            elements.append(Paragraph(title, styles['ProfessionalTitle']))
            elements.append(Spacer(1, 20))
            
            # Subtítulo com período
            period_text = f"Período: {report_config.get('period_label', 'N/A')}"
            elements.append(Paragraph(period_text, styles['ProfessionalSubtitle']))
            elements.append(Spacer(1, 30))
            
            # Preparar dados para DataFrame
            if data:
                df = pd.DataFrame(data)
                
                # Remover colunas desnecessárias
                columns_to_remove = ['_id']
                df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
                
                # Renomear colunas para português
                column_mapping = {
                    'id': 'ID',
                    'descricao': 'Descrição',
                    'quantidade': 'Quantidade',
                    'status': 'Status',
                    'urgencia': 'Urgência',
                    'categoria': 'Categoria',
                    'setor': 'Setor',
                    'deliveryDate': 'Data de Entrega',
                    'tipo': 'Tipo',
                    'usuario_nome': 'Usuário',
                    'data': 'Data',
                    'pedido_id': 'ID do Pedido'
                }
                
                df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
                
                # Calcular métricas para o resumo
                summary_data = {
                    'total_records': len(data),
                    'period_label': report_config.get('period_label', 'N/A'),
                    'user_name': report_config.get('user_name', 'Sistema'),
                    'report_type': report_config.get('report_type', 'geral')
                }
                
                if report_config.get('report_type') == 'pedidos':
                    summary_data.update({
                        'pending_count': len([d for d in data if d.get('status') == 'Pendente']),
                        'completed_count': len([d for d in data if d.get('status') == 'Concluído']),
                        'cancelled_count': len([d for d in data if d.get('status') == 'Cancelado']),
                    })
                    total = len(data)
                    if total > 0:
                        summary_data['completion_rate'] = (summary_data['completed_count'] / total) * 100
                
                elif report_config.get('report_type') == 'atividades':
                    summary_data.update({
                        'creation_count': len([d for d in data if d.get('tipo') == 'criacao']),
                        'update_count': len([d for d in data if d.get('tipo') == 'atualizacao']),
                        'query_count': len([d for d in data if d.get('tipo') == 'consulta']),
                    })
                
                # Seção de resumo executivo
                elements.append(Paragraph("RESUMO EXECUTIVO", styles['SectionHeader']))
                elements.append(Spacer(1, 15))
                elements.append(self.create_professional_summary_table(summary_data))
                elements.append(Spacer(1, 30))
                
                # Seção de dados detalhados
                elements.append(Paragraph("DADOS DETALHADOS", styles['SectionHeader']))
                elements.append(Spacer(1, 15))
                
                # Informações sobre filtros aplicados
                if report_config.get('filters'):
                    filter_info = []
                    for key, value in report_config['filters'].items():
                        if value:
                            filter_info.append(f"{key.title()}: {value}")
                    
                    if filter_info:
                        filter_text = f"Filtros aplicados: {', '.join(filter_info)}"
                        elements.append(Paragraph(filter_text, styles['ProfessionalHighlight']))
                        elements.append(Spacer(1, 15))
                
                elements.append(self.create_professional_data_table(df, "Dados do Relatório"))
                
            else:
                elements.append(Paragraph("Nenhum dado encontrado para os critérios especificados.", 
                                        styles['ProfessionalNormal']))
            
            # Construir PDF com cabeçalho e rodapé profissionais
            doc.build(elements, onFirstPage=self.create_header_footer, 
                     onLaterPages=self.create_header_footer)
            
            buffer.seek(0)
            logger.info("Relatório PDF gerado com sucesso")
            return buffer
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório PDF: {e}")
            # Criar buffer de erro
            error_buffer = io.BytesIO()
            error_buffer.write(f"Erro ao gerar relatório: {str(e)}".encode())
            error_buffer.seek(0)
            return error_buffer

    def generate_excel_report(self, data: List[Dict], report_config: Dict[str, Any]) -> io.BytesIO:
        """Gera relatório Excel profissional em tons de cinza"""
        try:
            buffer = io.BytesIO()
            
            # Aplicar filtros se especificados
            if report_config.get('filters'):
                data = self.apply_filters(data, report_config['filters'])
            
            if not data:
                df = pd.DataFrame([['Nenhum dado encontrado para os critérios especificados']], 
                                columns=['Resultado'])
            else:
                df = pd.DataFrame(data)
                
                # Remover colunas desnecessárias
                columns_to_remove = ['_id']
                df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
                
                # Renomear colunas para português
                column_mapping = {
                    'id': 'ID',
                    'descricao': 'Descrição',
                    'quantidade': 'Quantidade',
                    'status': 'Status',
                    'urgencia': 'Urgência',
                    'categoria': 'Categoria',
                    'setor': 'Setor',
                    'deliveryDate': 'Data de Entrega',
                    'tipo': 'Tipo',
                    'usuario_nome': 'Usuário',
                    'data': 'Data',
                    'pedido_id': 'ID do Pedido'
                }
                
                df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
            
            # Criar arquivo Excel com formatação profissional
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Escrever dados principais
                df.to_excel(writer, sheet_name='Relatório', index=False, startrow=8)
                
                # Obter objetos de formatação
                workbook = writer.book
                worksheet = writer.sheets['Relatório']
                
                # Definir formatos profissionais
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#333333',
                    'font_color': 'white',
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                
                title_format = workbook.add_format({
                    'bold': True,
                    'font_size': 16,
                    'font_color': '#1A1A1A',
                    'align': 'center'
                })
                
                subtitle_format = workbook.add_format({
                    'bold': True,
                    'font_size': 12,
                    'font_color': '#666666',
                    'align': 'center'
                })
                
                info_format = workbook.add_format({
                    'font_size': 10,
                    'font_color': '#333333'
                })
                
                data_format = workbook.add_format({
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'font_color': '#1A1A1A'
                })
                
                alt_row_format = workbook.add_format({
                    'border': 1,
                    'align': 'center',
                    'valign': 'vcenter',
                    'bg_color': '#F0F0F0',
                    'font_color': '#1A1A1A'
                })
                
                # Cabeçalho do relatório
                worksheet.merge_range('A1:' + chr(65 + len(df.columns) - 1) + '1', 
                                    report_config.get('title', 'Relatório do Sistema'), title_format)
                
                worksheet.merge_range('A2:' + chr(65 + len(df.columns) - 1) + '2', 
                                    f"Período: {report_config.get('period_label', 'N/A')}", subtitle_format)
                
                worksheet.write('A4', f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", info_format)
                worksheet.write('A5', f"Usuário: {report_config.get('user_name', 'Sistema')}", info_format)
                worksheet.write('A6', f"© {datetime.now().year} AraldiTech - Sistema de Gestão", info_format)
                
                # Formatação do cabeçalho da tabela
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(8, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, 15)
                
                # Formatação dos dados com cores alternadas
                for row in range(len(df)):
                    for col in range(len(df.columns)):
                        if row % 2 == 0:
                            worksheet.write(row + 9, col, df.iloc[row, col], data_format)
                        else:
                            worksheet.write(row + 9, col, df.iloc[row, col], alt_row_format)
                
                # Informações sobre filtros
                if report_config.get('filters'):
                    filter_row = len(df) + 12
                    worksheet.write(filter_row, 0, "Filtros Aplicados:", 
                                  workbook.add_format({'bold': True, 'font_color': '#333333'}))
                    
                    filter_row += 1
                    for key, value in report_config['filters'].items():
                        if value:
                            worksheet.write(filter_row, 0, f"{key.title()}: {value}", info_format)
                            filter_row += 1
            
            buffer.seek(0)
            logger.info("Relatório Excel gerado com sucesso")
            return buffer
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório Excel: {e}")
            # Criar buffer de erro
            error_buffer = io.BytesIO()
            error_buffer.write(f"Erro ao gerar relatório: {str(e)}".encode())
            error_buffer.seek(0)
            return error_buffer

# Instância global do gerador de relatórios
try:
    report_generator = ReportGenerator()
    logger.info("Gerador de relatórios inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar gerador de relatórios: {e}")
    report_generator = None 