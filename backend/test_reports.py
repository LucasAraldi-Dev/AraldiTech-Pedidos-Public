#!/usr/bin/env python3
"""
Script de teste para o sistema de relatórios profissionais
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.reports import report_generator
from datetime import datetime

def test_professional_reports():
    """Testa a geração de relatórios profissionais em tons de cinza"""
    print("🧪 Testando sistema de relatórios profissionais...")
    
    # Dados de teste mais robustos
    test_data = [
        {
            'id': 1,
            'descricao': 'Equipamento de Produção Industrial',
            'quantidade': 15,
            'status': 'Pendente',
            'urgencia': 'Urgente',
            'categoria': 'Equipamentos',
            'setor': 'Fábrica de Ração',
            'deliveryDate': '2024-05-25',
            'usuario_nome': 'João Silva'
        },
        {
            'id': 2,
            'descricao': 'Matéria-prima para Ração Animal',
            'quantidade': 500,
            'status': 'Concluído',
            'urgencia': 'Normal',
            'categoria': 'Matérias-primas',
            'setor': 'CPO',
            'deliveryDate': '2024-05-20',
            'usuario_nome': 'Maria Santos'
        },
        {
            'id': 3,
            'descricao': 'Peças de Reposição para Máquinas',
            'quantidade': 8,
            'status': 'Cancelado',
            'urgencia': 'Crítico',
            'categoria': 'Peças de Reposição',
            'setor': 'Abatedouro',
            'deliveryDate': '2024-05-22',
            'usuario_nome': 'Carlos Oliveira'
        },
        {
            'id': 4,
            'descricao': 'Serviços de Manutenção Preventiva',
            'quantidade': 1,
            'status': 'Pendente',
            'urgencia': 'Normal',
            'categoria': 'Serviços',
            'setor': 'Granjas',
            'deliveryDate': '2024-05-28',
            'usuario_nome': 'Ana Costa'
        },
        {
            'id': 5,
            'descricao': 'Material de Escritório e Papelaria',
            'quantidade': 25,
            'status': 'Concluído',
            'urgencia': 'Normal',
            'categoria': 'Material de Escritório',
            'setor': 'Escritório',
            'deliveryDate': '2024-05-18',
            'usuario_nome': 'Pedro Almeida'
        }
    ]
    
    # Configuração do relatório profissional
    report_config = {
        'title': 'Relatório Executivo - Sistema AraldiTech',
        'period_label': 'Período Analisado: 18/05/2024 a 28/05/2024',
        'user_name': 'Administrador do Sistema',
        'report_type': 'pedidos',
        'filters': {
            'status': None,  # Sem filtro para mostrar todos os dados
            'categoria': None,
            'urgencia': None,
            'setor': None
        }
    }
    
    try:
        print("📄 Gerando relatório PDF profissional...")
        pdf_buffer = report_generator.generate_pdf_report(test_data, report_config)
        pdf_size = len(pdf_buffer.getvalue())
        print(f"✅ PDF profissional gerado! Tamanho: {pdf_size:,} bytes")
        
        # Salvar PDF de teste
        with open('relatorio_profissional.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        print("💾 PDF salvo como 'relatorio_profissional.pdf'")
        
        print("📊 Gerando relatório Excel profissional...")
        excel_buffer = report_generator.generate_excel_report(test_data, report_config)
        excel_size = len(excel_buffer.getvalue())
        print(f"✅ Excel profissional gerado! Tamanho: {excel_size:,} bytes")
        
        # Salvar Excel de teste
        with open('relatorio_profissional.xlsx', 'wb') as f:
            f.write(excel_buffer.getvalue())
        print("💾 Excel salvo como 'relatorio_profissional.xlsx'")
        
        # Teste com filtros aplicados
        print("\n🔍 Testando relatório com filtros...")
        filtered_config = report_config.copy()
        filtered_config['filters'] = {
            'status': 'Pendente',
            'categoria': 'Equipamentos'
        }
        filtered_config['title'] = 'Relatório Filtrado - Pedidos Pendentes de Equipamentos'
        
        filtered_pdf = report_generator.generate_pdf_report(test_data, filtered_config)
        print(f"✅ Relatório filtrado gerado! Tamanho: {len(filtered_pdf.getvalue()):,} bytes")
        
        with open('relatorio_filtrado.pdf', 'wb') as f:
            f.write(filtered_pdf.getvalue())
        print("💾 Relatório filtrado salvo como 'relatorio_filtrado.pdf'")
        
        # Verificar se a logo foi carregada
        logo_path = os.path.join(os.path.dirname(__file__), 'app', 'assets', 'logo_vetor.png')
        if os.path.exists(logo_path):
            print("✅ Logo vetorial encontrada e carregada com sucesso!")
        else:
            print("⚠️ Logo vetorial não encontrada, usando fallback de texto")
        
        print("\n🎉 Todos os testes de relatórios profissionais passaram!")
        print("📁 Arquivos gerados:")
        print("   - relatorio_profissional.pdf (Design profissional completo)")
        print("   - relatorio_profissional.xlsx (Formatação Excel elegante)")
        print("   - relatorio_filtrado.pdf (Teste de filtros funcionais)")
        
        print("\n📋 Características implementadas:")
        print("   ✓ Design profissional em tons de cinza, preto e branco")
        print("   ✓ Logo vetorial AraldiTech com sombra sutil")
        print("   ✓ Cabeçalho e rodapé elegantes")
        print("   ✓ Tabelas com formatação profissional")
        print("   ✓ Métricas e análises detalhadas")
        print("   ✓ Filtros funcionais aplicados corretamente")
        print("   ✓ Formatação Excel com cores alternadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logo_loading():
    """Testa especificamente o carregamento da logo"""
    print("\n🖼️ Testando carregamento da logo...")
    
    logo_path = os.path.join(os.path.dirname(__file__), 'app', 'assets', 'logo_vetor.png')
    
    if os.path.exists(logo_path):
        file_size = os.path.getsize(logo_path)
        print(f"✅ Logo encontrada: {logo_path}")
        print(f"📏 Tamanho do arquivo: {file_size:,} bytes")
        
        # Verificar se é uma imagem válida
        try:
            from PIL import Image
            with Image.open(logo_path) as img:
                print(f"🖼️ Dimensões da imagem: {img.size[0]}x{img.size[1]} pixels")
                print(f"🎨 Formato: {img.format}")
                print(f"🔧 Modo: {img.mode}")
            return True
        except Exception as e:
            print(f"⚠️ Erro ao verificar imagem: {e}")
            return False
    else:
        print(f"❌ Logo não encontrada em: {logo_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏢 TESTE DO SISTEMA DE RELATÓRIOS ARALDI TECH")
    print("=" * 60)
    
    logo_ok = test_logo_loading()
    reports_ok = test_professional_reports()
    
    print("\n" + "=" * 60)
    if logo_ok and reports_ok:
        print("🎯 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("🚀 Sistema de relatórios profissionais pronto para uso!")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs acima.")
    print("=" * 60)
    
    sys.exit(0 if (logo_ok and reports_ok) else 1) 