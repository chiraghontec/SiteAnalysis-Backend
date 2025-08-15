import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class DataAnalyzer:
    """
    Utility for analyzing API response data and generating reports
    """
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
    
    def load_data_files(self, api_type):
        """
        Load all data files for a specific API type
        
        Args:
            api_type (str): Type of API ('thematic_stats', 'route', 'geoid')
            
        Returns:
            list: List of data from files
        """
        data_list = []
        
        # Find all files that match the api_type prefix
        for filename in os.listdir(self.data_dir):
            if filename.startswith(api_type) and filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Extract coordinates from filename
                    parts = filename.split('_')
                    if api_type == 'route':
                        origin_lat, origin_lng = parts[1], parts[2]
                        dest_lat, dest_lng = parts[4], parts[5]
                        metadata = {
                            'origin_lat': origin_lat,
                            'origin_lng': origin_lng,
                            'dest_lat': dest_lat,
                            'dest_lng': dest_lng,
                            'filename': filename
                        }
                    else:
                        lat, lng = parts[1], parts[2]
                        metadata = {
                            'lat': lat,
                            'lng': lng,
                            'filename': filename
                        }
                    
                    # Combine data with metadata
                    data_list.append({
                        'metadata': metadata,
                        'data': data
                    })
        
        return data_list
    
    def generate_api_summary(self, api_type):
        """
        Generate a summary of data from a specific API type
        
        Args:
            api_type (str): Type of API ('thematic_stats', 'route', 'geoid')
            
        Returns:
            dict: Summary statistics and information
        """
        data_list = self.load_data_files(api_type)
        
        if not data_list:
            return {"error": f"No data found for API type: {api_type}"}
        
        # This is a placeholder - actual analysis would depend on the API response format
        summary = {
            'api_type': api_type,
            'file_count': len(data_list),
            'timestamp': datetime.now().isoformat(),
            'data_fields': self._extract_common_fields(data_list)
        }
        
        return summary
    
    def _extract_common_fields(self, data_list):
        """Extract common fields from data responses"""
        if not data_list:
            return []
            
        # Get keys from first data item
        sample_data = data_list[0]['data']
        if isinstance(sample_data, dict):
            return list(sample_data.keys())
        return []
    
    def generate_comparison_report(self, output_file='data/reports/api_comparison.html'):
        """
        Generate a comparison report of all API types
        
        Args:
            output_file: Path to save the HTML report
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Load benchmark data
        try:
            benchmark_data = []
            with open('data/benchmarks/api_benchmark.jsonl', 'r') as f:
                for line in f:
                    benchmark_data.append(json.loads(line))
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(benchmark_data)
            
            # Group by function name
            grouped = df.groupby('function')['execution_time_ms'].agg(['mean', 'min', 'max', 'count']).reset_index()
            
            # Generate chart
            plt.figure(figsize=(10, 6))
            plt.bar(grouped['function'], grouped['mean'])
            plt.xlabel('API Function')
            plt.ylabel('Average Execution Time (ms)')
            plt.title('API Performance Comparison')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            chart_path = 'data/reports/api_comparison_chart.png'
            plt.savefig(chart_path)
            
            # Generate HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Comparison Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    h1, h2 {{ color: #333; }}
                    .chart {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>API Comparison Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>Performance Comparison</h2>
                <table>
                    <tr>
                        <th>API Function</th>
                        <th>Average Time (ms)</th>
                        <th>Min Time (ms)</th>
                        <th>Max Time (ms)</th>
                        <th>Call Count</th>
                    </tr>
            """
            
            # Add table rows
            for _, row in grouped.iterrows():
                html_content += f"""
                    <tr>
                        <td>{row['function']}</td>
                        <td>{row['mean']:.2f}</td>
                        <td>{row['min']:.2f}</td>
                        <td>{row['max']:.2f}</td>
                        <td>{row['count']}</td>
                    </tr>
                """
            
            html_content += """
                </table>
                
                <h2>Comparison Chart</h2>
                <div class="chart">
                    <img src="api_comparison_chart.png" alt="API Comparison Chart">
                </div>
            """
            
            # Add API-specific summaries
            for api_type in ['thematic_stats', 'route', 'geoid']:
                summary = self.generate_api_summary(api_type)
                
                html_content += f"""
                <h2>{api_type.replace('_', ' ').title()} API Summary</h2>
                """
                
                if 'error' in summary:
                    html_content += f"<p>{summary['error']}</p>"
                else:
                    html_content += f"""
                    <p>Files analyzed: {summary['file_count']}</p>
                    <h3>Data Fields</h3>
                    <ul>
                    """
                    
                    for field in summary['data_fields']:
                        html_content += f"<li>{field}</li>"
                    
                    html_content += "</ul>"
            
            html_content += """
            </body>
            </html>
            """
            
            # Write HTML report
            with open(output_file, 'w') as f:
                f.write(html_content)
            
            return {"status": "success", "message": f"Report generated: {output_file}"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to generate report: {str(e)}"}
