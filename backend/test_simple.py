#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

try:
    from app.reports import report_generator
    print('Report generator:', report_generator)
    
    if report_generator:
        print('Testando geração de PDF...')
        test_data = [{'id': 1, 'descricao': 'Teste', 'status': 'Pendente'}]
        config = {
            'title': 'Teste', 
            'period_label': 'Hoje', 
            'user_name': 'Teste', 
            'report_type': 'pedidos'
        }
        
        try:
            buffer = report_generator.generate_pdf_report(test_data, config)
            print('PDF gerado com sucesso! Tamanho:', len(buffer.getvalue()), 'bytes')
        except Exception as e:
            print('Erro ao gerar PDF:', e)
            import traceback
            traceback.print_exc()
    else:
        print('Report generator não foi inicializado')
        
except Exception as e:
    print('Erro ao importar:', e)
    import traceback
    traceback.print_exc() 