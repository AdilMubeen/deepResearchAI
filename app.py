"""Flask web interface for the research agent."""
from flask import Flask, render_template, request, jsonify, send_file
from agent import run_research
import json
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)
app.temp_reports = {}

# Pre-made research data
PRESET_REPORTS = {
    'elizabeth-holmes': {
        'target': 'Elizabeth Holmes',
        'status': 'available',
        'risk_breakdown': {
            'financial': 95,
            'legal': 98,
            'reputational': 100,
            'association': 30,
            'integrity': 100,
            'operational': 85
        },
        'stats': {
            'sources': 47,
            'people': 12,
            'organizations': 18,
            'events': 23
        },
        'summary': 'Founder of Theranos convicted of fraud. High risk across multiple categories.'
    },
    'sam-bankman': {
        'target': 'Sam Bankman-Fried',
        'status': 'available',
        'risk_breakdown': {
            'financial': 100,
            'legal': 100,
            'reputational': 98,
            'association': 45,
            'integrity': 95,
            'operational': 90
        },
        'stats': {
            'sources': 52,
            'people': 15,
            'organizations': 24,
            'events': 31
        },
        'summary': 'FTX founder convicted of fraud. Extreme risk in financial and legal categories.'
    },
    'martin-shkreli': {
        'target': 'Martin Shkreli',
        'status': 'available',
        'risk_breakdown': {
            'financial': 85,
            'legal': 90,
            'reputational': 100,
            'association': 40,
            'integrity': 88,
            'operational': 75
        },
        'stats': {
            'sources': 38,
            'people': 9,
            'organizations': 14,
            'events': 19
        },
        'summary': 'Former pharmaceutical executive convicted of securities fraud. Known for controversial drug pricing.'
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_preset/<preset_id>')
def get_preset(preset_id):
    preset_file = f'static/presets/{preset_id}.json'
    try:
        with open(preset_file, 'r') as f:
            data = json.load(f)
            data['report_id'] = preset_id
            # Store in temp_reports for PDF download
            app.temp_reports[preset_id] = data.get('full_report_markdown', '')
            return jsonify(data)
    except FileNotFoundError:
        # Fallback to placeholder data
        if preset_id not in PRESET_REPORTS:
            return jsonify({'error': 'Preset not found'}), 404
        
        data = PRESET_REPORTS[preset_id].copy()
        data['full_report_markdown'] = f"# Risk Assessment Report: {data['target']}\n\n{data['summary']}\n\n*This is a placeholder. Click 'Re-run Deep Research' to generate the full report.*"
        data['report_id'] = preset_id
        # Store in temp_reports for PDF download
        app.temp_reports[preset_id] = data['full_report_markdown']
        return jsonify(data)


@app.route('/research', methods=['POST'])
def research():
    """Execute research and return JSON results."""
    try:
        target = request.form.get('target', '').strip()
        if not target:
            return jsonify({'error': 'Target name is required'}), 400
        
        final_state = run_research(
            target=target,
            max_depth=3,
            context=request.form.get('context', '').strip(),
            focus=request.form.get('focus', '').strip(),
            time_period=request.form.get('time_period', '').strip(),
            industry=request.form.get('industry', '').strip(),
            location=request.form.get('location', '').strip()
        )
        
        # Parse risk and entity data
        try:
            risk_data = json.loads(final_state.get('risk_analysis', '{}'))
        except:
            risk_data = {'total_risk_score': 'N/A'}
        
        try:
            entities = json.loads(final_state.get('entities', '{}'))
        except:
            entities = {}
        
        # Store report for download
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = "".join(c if c.isalnum() else "_" for c in target)
        report_filename = f"{safe_name}_{timestamp}.md"
        app.temp_reports[report_filename] = final_state.get('final_report', '')
        
        return jsonify({
            'success': True,
            'target': target,
            'risk_score': risk_data.get('total_risk_score', 'N/A'),
            'risk_breakdown': {
                'financial': risk_data.get('financial', {}).get('score', 'N/A'),
                'legal': risk_data.get('legal', {}).get('score', 'N/A'),
                'reputational': risk_data.get('reputational', {}).get('score', 'N/A'),
                'association': risk_data.get('association', {}).get('score', 'N/A'),
                'integrity': risk_data.get('integrity', {}).get('score', 'N/A'),
                'operational': risk_data.get('operational', {}).get('score', 'N/A'),
            },
            'entities': {
                'people': len(entities.get('people', [])),
                'organizations': len(entities.get('organizations', [])),
                'timeline': len(entities.get('timeline', [])),
                'legal': len(entities.get('legal', [])),
            },
            'sources': final_state.get('num_sources', 0),
            'report': final_state.get('final_report', ''),
            'report_file': report_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# PDF generation helpers

def _escape_xml(text):
    """Escape special characters for ReportLab."""
    if not text:
        return text
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _convert_bold(text):
    """Convert markdown bold syntax to HTML tags."""
    result = []
    parts = text.split('**')
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(_escape_xml(part))
        else:
            result.append(f'<b>{_escape_xml(part)}</b>')
    return ''.join(result)


def _safe_paragraph(text, style):
    """Create paragraph with fallback for malformed content."""
    try:
        return Paragraph(text, style)
    except:
        try:
            return Paragraph(_escape_xml(text.replace('<b>', '').replace('</b>', '')), style)
        except:
            return Paragraph("", style)


def _markdown_to_pdf(markdown_text):
    """Convert markdown report to PDF buffer."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Title2', parent=styles['Heading1'], fontSize=24, spaceAfter=30))
    styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], fontSize=16, spaceAfter=12, spaceBefore=12))
    styles.add(ParagraphStyle(name='H3', parent=styles['Heading3'], fontSize=12, spaceAfter=10, spaceBefore=10, textColor=colors.grey))
    styles.add(ParagraphStyle(name='Body2', parent=styles['Normal'], fontSize=10, spaceAfter=6, leading=14))
    styles.add(ParagraphStyle(name='List2', parent=styles['Normal'], fontSize=10, spaceAfter=4, leftIndent=20, leading=14))
    
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        try:
            if line.startswith('# '):
                elements.append(Paragraph(_escape_xml(line[2:]), styles['Title2']))
                elements.append(Spacer(1, 0.2*inch))
            elif line.startswith('## '):
                elements.append(Paragraph(_escape_xml(line[3:]), styles['H2']))
            elif line.startswith('### '):
                elements.append(Paragraph(_escape_xml(line[4:]), styles['H3']))
            elif line.startswith('- ') or line.startswith('* '):
                elements.append(_safe_paragraph('• ' + _convert_bold(line[2:]), styles['List2']))
            elif len(line) > 2 and line[0].isdigit() and line[1] in '.):':
                elements.append(_safe_paragraph(_convert_bold(line), styles['List2']))
            elif line.startswith('|'):
                # Parse markdown table
                table_data = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    row = [_escape_xml(c.strip()) for c in lines[i].strip().split('|')[1:-1]]
                    if not all('---' in c or '--' in c or c == '' for c in row):
                        table_data.append(row)
                    i += 1
                if table_data and len(table_data) > 1:
                    t = Table([[Paragraph(c, styles['Normal']) for c in r] for r in table_data])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ]))
                    elements.append(t)
                    elements.append(Spacer(1, 0.2*inch))
                continue
            elif '**' in line:
                elements.append(_safe_paragraph(_convert_bold(line), styles['Body2']))
            else:
                elements.append(_safe_paragraph(_escape_xml(line), styles['Body2']))
        except:
            pass
        
        i += 1
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


@app.route('/download/<filename>')
def download(filename):
    """Download report as PDF."""
    try:
        if filename in app.temp_reports:
            pdf_buffer = _markdown_to_pdf(app.temp_reports[filename])
            return send_file(
                pdf_buffer, mimetype='application/pdf', as_attachment=True,
                download_name=filename.replace('.md', '.pdf')
            )
        return "Report not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Deep Research AI Agent")
    print("="*50)
    print("\nOpen: http://localhost:5001\n")
    app.run(debug=False, host='0.0.0.0', port=5001)
