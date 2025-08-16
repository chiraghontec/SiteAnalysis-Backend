# KGIS API Testing Suite - Karthik's Implementation

This repository contains a comprehensive testing suite for Karnataka Geographic Information System (KGIS) APIs, developed as part of the spike work by Karthik.

## 🎯 Overview

This testing suite evaluates 12 different KGIS APIs that provide geographic, administrative, and location-based services for Karnataka state. The APIs cover everything from administrative hierarchy lookup to geometric calculations and distance measurements.

## 📊 Test Results Summary

**Test Date:** August 16, 2025  
**Total APIs Tested:** 12  
**Working APIs:** 12 (100%)  
**APIs with Data:** 9 (75%)  
**Average Response Time:** 180.8ms

---

## 🗺️ API Catalog & Use Cases

### 1. **Admin Hierarchy API**
- **Purpose:** Fetch complete administrative hierarchy based on department and application codes
- **Use Cases:** 
  - Government data integration
  - Administrative boundary mapping
  - Hierarchical location services
- **Test File:** `adminhierarchytest.py`

### 2. **District Code Lookup API**
- **Purpose:** Get district codes and names based on district name input
- **Use Cases:**
  - District validation and standardization
  - Administrative code mapping
  - Location normalization
- **Test File:** `districtcode.py`

### 3. **Taluk Code Lookup API**
- **Purpose:** Retrieve taluk information including district hierarchy
- **Use Cases:**
  - Sub-district administrative mapping
  - Regional planning and analysis
  - Government service delivery
- **Test File:** `talukcode.py`

### 4. **Hobli Code Lookup API**
- **Purpose:** Fetch hobli (revenue circle) information with complete hierarchy
- **Use Cases:**
  - Revenue administration
  - Land record management
  - Rural area governance
- **Test File:** `hoblicodetest.py`

### 5. **Survey Number Lookup API**
- **Purpose:** Find survey numbers based on coordinates and village information
- **Use Cases:**
  - Land parcel identification
  - Property mapping
  - Revenue survey management
- **Test File:** `surveynumbertest.py`

### 6. **Nearby Admin Hierarchy API**
- **Purpose:** Get administrative boundaries near specific coordinates
- **Use Cases:**
  - Location-based services
  - Proximity analysis
  - Administrative jurisdiction determination
- **Test File:** `nearbyadminhierarchy.py`

### 7. **Nearby Assets API**
- **Purpose:** Find nearby infrastructure and assets based on location
- **Use Cases:**
  - Asset management
  - Infrastructure planning
  - Service delivery optimization
- **Test File:** `nearbyassetstest.py`

### 8. **Geometric Polygon Area API**
- **Purpose:** Retrieve geometric boundaries for survey numbers
- **Use Cases:**
  - Land area calculation
  - Boundary mapping
  - GIS visualization
- **Test File:** `geometricpolygonareatest.py`

### 9. **PIN Code Distance API**
- **Purpose:** Calculate distance between Karnataka PIN codes
- **Use Cases:**
  - Logistics and delivery planning
  - Distance-based service pricing
  - Regional connectivity analysis
- **Test File:** `pincodedistancetest.py`

### 10. **Election Jurisdiction Hierarchy API**
- **Purpose:** Get election, police, education, and health jurisdiction boundaries
- **Use Cases:**
  - Electoral boundary management
  - Service jurisdiction mapping
  - Administrative planning
- **Test File:** `electionjhtest.py`

### 11. **Nearby Location Details API**
- **Purpose:** Provide urban/rural classification and administrative details
- **Use Cases:**
  - Urban planning
  - Service categorization
  - Development planning
- **Test File:** `nearbylocationtest.py`

### 12. **Zonation Data API**
- **Purpose:** Comprehensive administrative and election data with POST method
- **Use Cases:**
  - Batch location processing
  - Electoral data management
  - Administrative analytics
- **Test File:** `zoning.py`

---

## 🔗 API Endpoints Reference

| API Name | Method | Endpoint |
|----------|--------|----------|
| Admin Hierarchy | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/kgisadminhierarchy` |
| District Code | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/districtcode` |
| Taluk Code | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/talukcode` |
| Hobli Code | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/hoblicode` |
| Survey Number | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/surveyno` |
| Nearby Admin Hierarchy | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/nearbyadminhierarchy` |
| Nearby Assets | GET | `https://kgis.ksrsac.in:9000/NearbyAssets/ws/getNearbyAssetData` |
| Geometric Polygon | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/geomForSurveyNum` |
| PIN Code Distance | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/getDistanceBtwPincode` |
| Election Jurisdiction | GET | `https://kgis.ksrsac.in:9000/boundarywebservices/ws/getJurisdictionBoundary` |
| Location Details | GET | `https://kgis.ksrsac.in:9000/genericwebservices/ws/getlocationdetails` |
| Zonation Data | POST | `https://kgis.ksrsac.in:9000/genericwebservices/ws/getKGISAdminCodes2` |

---

## 📈 Performance Benchmark Results

### Response Time Analysis
| API Name | Response Time (ms) | Status | Data Available |
|----------|-------------------|--------|----------------|
| Nearby Assets | 30 | ✅ Working | ❌ No Data |
| District Code | 120 | ✅ Working | ✅ Has Data |
| Admin Hierarchy | 150 | ✅ Working | ✅ Has Data |
| Location Details | 150 | ✅ Working | ✅ Has Data |
| Hobli Code | 160 | ✅ Working | ✅ Has Data |
| Taluk Code | 180 | ✅ Working | ✅ Has Data |
| PIN Code Distance | 180 | ✅ Working | ✅ Has Data |
| Nearby Admin Hierarchy | 200 | ✅ Working | ✅ Has Data |
| Election Jurisdiction | 220 | ✅ Working | ❌ No Data |
| Survey Number | 250 | ✅ Working | ❌ No Data |
| Geometric Polygon | 267 | ✅ Working | ✅ Has Data |
| Zonation Data | 300 | ✅ Working | ✅ Has Data |

### API Status Summary
| Metric | Count | Percentage |
|--------|-------|------------|
| **Total APIs** | 12 | 100% |
| **Working APIs** | 12 | 100% |
| **APIs with Data** | 9 | 75% |
| **APIs with Issues** | 3 | 25% |
| **Average Response Time** | 180.8ms | - |

### Fully Functional APIs ✅
- Admin Hierarchy
- District Code Lookup
- Taluk Code Lookup
- Hobli Code Lookup
- Nearby Admin Hierarchy
- Geometric Polygon Area
- PIN Code Distance
- Location Details
- Zonation Data

### APIs with Issues ⚠️
| API Name | Issue Description |
|----------|------------------|
| **Survey Number** | Returns empty survey data - possible data availability or parameter issues |
| **Nearby Assets** | Layer code '1312130' from documentation appears invalid |
| **Election Jurisdiction** | Documentation coordinates appear out of Karnataka bounds |

---

## 🛠️ Technical Implementation

### Test Environment
- **Platform:** Windows PowerShell
- **SSL Verification:** Disabled for testing
- **Request Timeout:** 30 seconds
- **Retry Attempts:** 1
- **Concurrent Requests:** False

### Key Features
- ✅ Comprehensive error handling
- ✅ Response time measurement
- ✅ Data validation
- ✅ Multiple parameter testing
- ✅ Performance benchmarking
- ✅ Detailed logging

---

## 📋 Recommendations

### Documentation Updates Needed
1. **Nearby Assets API**: Update layer code examples (current code '1312130' is invalid)
2. **Election Jurisdiction API**: Verify coordinate examples (current coordinates out of Karnataka bounds)
3. **Survey Number API**: Check data availability and parameter requirements

### Performance Insights
- **Overall Performance**: Good with average response time under 200ms
- **Reliability**: 75% of APIs return meaningful data
- **Connectivity**: 100% of APIs are accessible and responding

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install requests urllib3
```

### Running Individual Tests
```bash
# Test Admin Hierarchy API
python adminhierarchytest.py

# Test District Code API
python districtcode.py

# Test all APIs
python benchmark_all_apis.py
```

### Sample Usage
```python
from adminhierarchytest import KGISAdminHierarchyTester

tester = KGISAdminHierarchyTester()
result = tester.test_api_with_all_parameters("1", "102", "lgd", "604199")
print(result)
```

---

## 📁 Repository Structure

```
Karthik/
├── README.md                           # This documentation
├── kgis_api_benchmark_results.json     # Detailed benchmark results
├── adminhierarchytest.py              # Admin hierarchy testing
├── districtcode.py                    # District code testing
├── talukcode.py                       # Taluk code testing
├── hoblicodetest.py                   # Hobli code testing
├── surveynumbertest.py                # Survey number testing
├── nearbyadminhierarchy.py            # Nearby admin hierarchy testing
├── nearbyassetstest.py                # Nearby assets testing
├── geometricpolygonareatest.py        # Geometric polygon testing
├── pincodedistancetest.py             # PIN code distance testing
├── electionjhtest.py                  # Election jurisdiction testing
├── nearbylocationtest.py              # Location details testing
└── zoning.py                          # Zonation data testing
```

---

## 📊 Detailed Benchmark Data

For complete benchmark results including sample requests, responses, and detailed performance metrics, see: [`kgis_api_benchmark_results.json`](./kgis_api_benchmark_results.json)

---

## 👥 Contributing

This is part of the SiteAnalysis-Backend spike implementation. For questions or contributions, please refer to the main project repository.

**Author:** Karthik  
**Last Updated:** August 16, 2025  
**Version:** 1.0
