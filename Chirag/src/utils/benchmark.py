import time
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def benchmark_api_call(function, *args, **kwargs):
    """
    Benchmark the execution time of an API call
    
    Args:
        function: The API function to benchmark
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        tuple: (function_result, execution_time_ms)
    """
    start_time = time.time()
    result = function(*args, **kwargs)
    end_time = time.time()
    
    # Calculate execution time in milliseconds
    execution_time_ms = round((end_time - start_time) * 1000, 2)
    
    # Log benchmark result
    log_benchmark(function.__name__, args, kwargs, execution_time_ms)
    
    return result, execution_time_ms

def log_benchmark(function_name, args, kwargs, execution_time_ms):
    """
    Log benchmark results to file
    
    Args:
        function_name: Name of the function being benchmarked
        args: Arguments passed to the function
        kwargs: Keyword arguments passed to the function
        execution_time_ms: Execution time in milliseconds
    """
    timestamp = datetime.now().isoformat()
    
    # Create benchmark log entry
    log_entry = {
        'timestamp': timestamp,
        'function': function_name,
        'execution_time_ms': execution_time_ms,
        'args': str(args),  # Convert args to string for JSON serialization
        'kwargs': str(kwargs)  # Convert kwargs to string for JSON serialization
    }
    
    # Ensure directory exists
    os.makedirs('data/benchmarks', exist_ok=True)
    
    # Append to benchmark log file
    with open('data/benchmarks/api_benchmark.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def generate_benchmark_report(output_file='data/reports/benchmark_report.html'):
    """
    Generate a report of all API benchmarks
    
    Args:
        output_file: Path to save the HTML report
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Read benchmark data
    benchmark_data = []
    try:
        with open('data/benchmarks/api_benchmark.jsonl', 'r') as f:
            for line in f:
                benchmark_data.append(json.loads(line))
    except FileNotFoundError:
        print("No benchmark data found")
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(benchmark_data)
    
    # Generate statistics by function
    stats_by_function = df.groupby('function')['execution_time_ms'].agg(['mean', 'min', 'max', 'count']).reset_index()
    
    # Plot benchmark results
    plt.figure(figsize=(12, 6))
    plt.bar(stats_by_function['function'], stats_by_function['mean'])
    plt.xlabel('API Function')
    plt.ylabel('Average Execution Time (ms)')
    plt.title('API Benchmark Results')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plot_path = 'data/reports/benchmark_chart.png'
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Benchmark Report</title>
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
        <h1>API Benchmark Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Summary Statistics</h2>
        <table>
            <tr>
                <th>Function</th>
                <th>Average Time (ms)</th>
                <th>Min Time (ms)</th>
                <th>Max Time (ms)</th>
                <th>Call Count</th>
            </tr>
    """
    
    # Add table rows
    for _, row in stats_by_function.iterrows():
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
        
        <h2>Benchmark Chart</h2>
        <div class="chart">
            <img src="benchmark_chart.png" alt="Benchmark Chart">
        </div>
    </body>
    </html>
    """
    
    # Write HTML report
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"Benchmark report generated: {output_file}")
