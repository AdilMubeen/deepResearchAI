#!/usr/bin/env python3
"""Generate preset reports for Elizabeth Holmes, Sam Bankman-Fried, and Martin Shkreli."""
import sys
sys.path.insert(0, '/Users/adilmubeen/Documents/test')

from agent import run_research
import json

PRESETS = [
    {
        'id': 'elizabeth-holmes',
        'target': 'Elizabeth Holmes',
        'context': 'Founder of Theranos',
        'focus': 'fraud, legal issues',
        'time_period': '2010-2024',
        'industry': 'healthcare, biotech',
        'location': 'Silicon Valley'
    },
    {
        'id': 'sam-bankman',
        'target': 'Sam Bankman-Fried',
        'context': 'Founder of FTX',
        'focus': 'fraud, bankruptcy, criminal charges',
        'time_period': '2019-2024',
        'industry': 'cryptocurrency, finance',
        'location': 'Bahamas'
    },
    {
        'id': 'martin-shkreli',
        'target': 'Martin Shkreli',
        'context': 'Pharmaceutical executive',
        'focus': 'fraud, legal issues, price gouging',
        'time_period': '2010-2024',
        'industry': 'pharmaceuticals',
        'location': 'New York'
    }
]

def generate_preset_report(preset):
    print(f"\n{'='*60}")
    print(f"Generating report for: {preset['target']}")
    print(f"{'='*60}\n")
    
    try:
        result = run_research(
            target=preset['target'],
            max_depth=3,
            context=preset['context'],
            focus=preset['focus'],
            time_period=preset['time_period'],
            industry=preset['industry'],
            location=preset['location']
        )
        
        # Extract data
        try:
            risk_data = json.loads(result.get('risk_analysis', '{}'))
        except:
            risk_data = {}
        
        try:
            entities = json.loads(result.get('entities', '{}'))
        except:
            entities = {}
        
        # Save report
        report_data = {
            'target': preset['target'],
            'risk_breakdown': {
                'financial': risk_data.get('financial', {}).get('score', 0),
                'legal': risk_data.get('legal', {}).get('score', 0),
                'reputational': risk_data.get('reputational', {}).get('score', 0),
                'association': risk_data.get('association', {}).get('score', 0),
                'integrity': risk_data.get('integrity', {}).get('score', 0),
                'operational': risk_data.get('operational', {}).get('score', 0),
            },
            'stats': {
                'sources': result.get('num_sources', 0),
                'people': len(entities.get('people', [])),
                'organizations': len(entities.get('organizations', [])),
                'events': len(entities.get('timeline', [])),
            },
            'full_report_markdown': result.get('final_report', 'No report generated')
        }
        
        # Save to file
        filename = f"/Users/adilmubeen/Documents/test/static/presets/{preset['id']}.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n✅ Report saved to: {filename}")
        print(f"   Risk Score: {risk_data.get('total_risk_score', 'N/A')}/100")
        print(f"   Sources: {report_data['stats']['sources']}")
        print(f"   Report Length: {len(report_data['full_report_markdown'])} chars\n")
        
        return report_data
    
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import os
    os.makedirs('/Users/adilmubeen/Documents/test/static/presets', exist_ok=True)
    
    print("\n" + "="*60)
    print("PRESET REPORT GENERATOR")
    print("="*60)
    print("\nThis will generate 3 comprehensive reports.")
    print("Each report takes ~2-3 minutes.\n")
    
    try:
        input("Press ENTER to start (or Ctrl+C to cancel)...")
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(0)
    
    results = []
    for i, preset in enumerate(PRESETS, 1):
        print(f"\n[{i}/3] Processing: {preset['target']}")
        result = generate_preset_report(preset)
        if result:
            results.append(result)
    
    print("\n" + "="*60)
    print(f"COMPLETE: {len(results)}/3 reports generated")
    print("="*60)
    print("\nFiles saved to: /Users/adilmubeen/Documents/test/static/presets/")
    print("\nRestart Flask server to see updated reports.\n")

