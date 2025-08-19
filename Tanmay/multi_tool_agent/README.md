# Multi Tool Agent - Site Analysis Backend Assistant

This project implements an intelligent AI assistant using the [Google ADK](https://github.com/google/adk) framework, specifically designed to help with the Site Analysis Backend project. The agent provides expert knowledge about Bhuvan APIs, geospatial analysis, and Indian geographical data processing.

## 🚀 Features

- **Comprehensive API Knowledge**: Expert guidance on all 7 integrated Bhuvan APIs
- **Intelligent Workflow Suggestions**: Recommends optimal API sequences for different use cases
- **Geographical Context Analysis**: Analyzes coordinates and suggests appropriate APIs
- **Usage Guides**: Detailed documentation for each API with examples
- **Project Status Monitoring**: Real-time information about project capabilities

## 📊 Supported Bhuvan APIs

The agent has comprehensive knowledge of these 7 production-ready APIs:

| API Service | Purpose | Avg Response Time | Use Cases |
|-------------|---------|------------------|-----------|
| **Postal & Hospital** | Find postal codes and nearby hospitals | 0.507s | Healthcare planning, emergency services |
| **Village Geocoding** | Convert village names to coordinates | 0.509s | Address standardization, rural mapping |
| **Village Reverse Geocoding** | Get village info from coordinates | 0.513s | Location identification, address generation |
| **LULC AOI Statistics** | Land use/land cover analysis | 0.582s | Environmental monitoring, urban planning |
| **Routing** | Navigation and route planning | 2.602s | Navigation, distance calculation |
| **Thematic Statistics** | District-wise LULC data | 0.773s | Policy development, statistical analysis |
| **Geoid** | Administrative boundary identification | 0.254s | Boundary mapping, government integration |

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- [Google ADK](https://github.com/google/adk)
- Access to the Site Analysis Backend project

### Installation

1. **Navigate to the multi_tool_agent directory**:
   ```powershell
   cd SiteAnalysis-Backend\Tanmay\multi_tool_agent
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install google-adk
   ```

4. **Configure Google ADK** (if not already done):
   ```powershell
   # Follow Google ADK setup instructions
   # Set up authentication and project configuration
   ```

## 🔧 Agent Tools

The agent provides 5 specialized tools:

### 1. `get_api_overview()`
Returns comprehensive overview of all 7 Bhuvan APIs including:
- Performance metrics
- Success rates
- API capabilities
- Response time benchmarks

### 2. `analyze_location_context(latitude, longitude)`
Analyzes geographical context for given coordinates:
- Validates if coordinates are within India
- Suggests appropriate APIs for the location
- Provides climate zone information
- Recommends priority APIs

### 3. `get_api_usage_guide(api_name)`
Provides detailed usage guide for specific APIs:
- Endpoint information
- Input/output format
- Example requests
- Use cases and limitations

### 4. `suggest_api_workflow(use_case)`
Suggests optimal API workflows for different scenarios:
- **Site Analysis**: Comprehensive development/research analysis
- **Navigation**: Route planning and navigation
- **Urban Planning**: Development and planning analysis
- **Emergency Response**: Disaster response and emergency services

### 5. `get_project_status()`
Returns current project status and capabilities:
- Technology stack information
- Testing and validation status
- Deployment readiness
- Key features overview

## 📝 Usage Examples

### Basic Agent Interaction

```python
from agent import root_agent

# Get overview of all APIs
overview = root_agent.tools[0]()  # get_api_overview
print(overview)

# Analyze location context
context = root_agent.tools[1](19.0760, 72.8777)  # Mumbai coordinates
print(context)

# Get usage guide for specific API
guide = root_agent.tools[2]("postal_hospital")
print(guide)

# Get workflow suggestion
workflow = root_agent.tools[3]("site analysis")
print(workflow)

# Check project status
status = root_agent.tools[4]()
print(status)
```

### Interactive Chat with Agent

```python
# The agent can be used in an interactive chat interface
# It understands natural language queries about:
# - API capabilities and usage
# - Geographical analysis
# - Workflow recommendations
# - Project status and features
```

## 🎯 Use Case Examples

### 1. Site Development Analysis
```python
# For a new site at specific coordinates
location_analysis = analyze_location_context(28.6139, 77.2090)  # Delhi
workflow = suggest_api_workflow("site analysis")

# The agent will recommend:
# 1. Use geoid API for administrative boundaries
# 2. Use village_reverse_geocoding for local context
# 3. Use postal_hospital for nearby facilities
# 4. Use lulc_aoi_statistics for land use analysis
```

### 2. Emergency Response Planning
```python
# For emergency response coordination
emergency_workflow = suggest_api_workflow("emergency response")

# Recommended sequence:
# 1. village_reverse_geocoding for rapid location ID
# 2. postal_hospital for nearest hospitals
# 3. routing for emergency routes
```

### 3. Urban Planning Project
```python
# For urban development planning
planning_workflow = suggest_api_workflow("urban planning")

# Comprehensive workflow:
# 1. geoid for administrative mapping
# 2. thematic_statistics for district data
# 3. lulc_aoi_statistics for detailed analysis
# 4. postal_hospital for infrastructure assessment
```

## 🔍 Agent Capabilities

### Intelligent Analysis
- **Coordinate Validation**: Automatically validates if coordinates are within India's boundaries
- **API Recommendations**: Suggests the most appropriate APIs based on location and use case
- **Performance Insights**: Provides real-time performance data and benchmarks

### Comprehensive Documentation
- **Detailed Guides**: Complete usage documentation for each API
- **Example Requests**: Ready-to-use request examples
- **Best Practices**: Recommendations for optimal API usage

### Workflow Optimization
- **Multi-API Workflows**: Suggests optimal sequences of API calls
- **Time Estimation**: Provides estimated response times for workflows
- **Use Case Matching**: Matches user requirements to proven workflows

## 🌐 Integration with Site Analysis Backend

The agent is designed to work seamlessly with the Site Analysis Backend project:

- **API Endpoint Knowledge**: Knows all Flask application endpoints
- **Data Format Understanding**: Understands request/response formats
- **Error Handling**: Provides guidance on handling API errors
- **Performance Optimization**: Suggests ways to optimize API usage

## 🚀 Running with Google ADK

To run the agent using Google ADK:

```powershell
# Start ADK development server
adk web

# The agent will be available for interaction
# Use the ADK interface to chat with the agent
```

## 📊 Performance Characteristics

- **Response Time**: Near-instantaneous for tool calls
- **Accuracy**: 100% accuracy for API information and documentation
- **Coverage**: Complete knowledge of all 7 Bhuvan APIs
- **Reliability**: Built on production-tested API data

## 🔧 Customization

### Adding New Tools
To extend the agent with additional tools:

1. Create new tool functions in `agent.py`
2. Add them to the `tools` list in the Agent initialization
3. Update the agent's instruction to include new capabilities

### Modifying API Knowledge
Update the API information in the tool functions:
- `get_api_overview()` for performance data
- `get_api_usage_guide()` for usage documentation
- `suggest_api_workflow()` for workflow patterns

## 📁 File Structure

```
multi_tool_agent/
│
├── agent.py              # Main agent implementation with tools
├── README.md             # This documentation
└── venv/                 # Virtual environment (after setup)
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```powershell
   # Ensure virtual environment is activated
   venv\Scripts\activate
   pip install google-adk
   ```

2. **Agent Not Responding**:
   - Check Google ADK configuration
   - Verify agent model availability
   - Check tool function syntax

3. **API Information Outdated**:
   - Update tool functions with latest API data
   - Refresh performance benchmarks
   - Update endpoint information

### Performance Issues

- Tool functions are designed for fast response
- All data is pre-computed and stored in functions
- No external API calls from agent tools

## 🔗 Related Projects

- **Site Analysis Backend**: Main Flask application with Bhuvan API integrations
- **Benchmark Suite**: Comprehensive API testing and performance monitoring
- **Environmental Analysis**: Django-based environmental data processing

## 📄 License

This project is part of the Site Analysis Backend suite. See the main project repository for license details.

## 🤝 Contributing

This agent is designed specifically for the Site Analysis Backend project. For contributions:

1. Focus on improving API knowledge accuracy
2. Add new workflow patterns based on real use cases
3. Enhance geographical analysis capabilities
4. Improve tool function performance

## 📞 Support

For questions about the agent or the Site Analysis Backend project:
- Check the main project documentation
- Review API benchmark results
- Consult the comprehensive API guides provided by the agent tools

---

**Note**: This agent is specifically designed for the Site Analysis Backend project and provides expert knowledge about Indian geospatial data through Bhuvan APIs. It's optimized for site analysis, urban planning, navigation, and emergency response use cases within India.
