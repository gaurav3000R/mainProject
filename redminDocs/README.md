# Redmine API Metadata

## 📦 Files

### 1. `api_details.json`
Original API documentation with endpoint definitions for both internal and external APIs.

### 2. `redmine_metadata.json` ✨ NEW
**Complete snapshot of all Redmine data** fetched from the live API.

**Contents:**
- Current user information
- All projects (5 projects)
- All issues (100 most recent)
- Time entries (100 most recent)
- Issue statuses (6 statuses)
- Priorities (6 priority levels)
- Trackers (6 trackers)

**File Size:** 213 KB  
**Fetched At:** 2025-11-11T07:54:15

## 🚀 How to Refresh Metadata

Run the fetch script to update the metadata:

```bash
python scripts/fetch_redmine_metadata.py
```

This will:
1. Connect to Redmine API
2. Call all 7 endpoints
3. Fetch current data
4. Save to `redmine_metadata.json`

## 📊 Data Structure

```json
{
  "fetched_at": "timestamp",
  "base_url": "https://mgt.digiflux.io/",
  "endpoints": {
    "validateConnection": {
      "url": "...",
      "method": "GET",
      "description": "...",
      "status": "success",
      "data": { ... },
      "fetched_at": "timestamp"
    },
    "getProjects": { ... },
    "getIssues": { ... },
    "getTimeEntries": { ... },
    "getIssueStatuses": { ... },
    "getPriorities": { ... },
    "getTrackers": { ... }
  }
}
```

## 🎯 Use Cases

### 1. Development Reference
Use the metadata to understand available:
- Projects and their IDs
- Issue statuses
- Priority levels
- Tracker types

### 2. Testing
Use actual data for:
- Testing chatbot responses
- Validating tool outputs
- Creating test cases

### 3. Documentation
Reference the metadata when:
- Writing user guides
- Creating examples
- Training the AI model

### 4. Analytics
Analyze the data for:
- Project statistics
- Issue distributions
- Time tracking patterns

## 📋 Endpoints Called

| Endpoint | Method | Description | Items |
|----------|--------|-------------|-------|
| `/users/current.json` | GET | Current user | 1 user |
| `/projects.json` | GET | All projects | 5 projects |
| `/issues.json` | GET | All issues | 100 issues |
| `/time_entries.json` | GET | Time logs | 100 entries |
| `/issue_statuses.json` | GET | Statuses | 6 statuses |
| `/enumerations/issue_priorities.json` | GET | Priorities | 6 priorities |
| `/trackers.json` | GET | Trackers | 6 trackers |

## 🔧 Script Features

The `fetch_redmine_metadata.py` script:
- ✅ Calls all external API endpoints
- ✅ Handles errors gracefully
- ✅ Stores complete responses
- ✅ Includes timestamps
- ✅ Shows progress and summary
- ✅ Validates connection first

## 📈 What's Included

### User Info
- Login, name, admin status
- Created/updated timestamps
- Last login time

### Projects
- Project names and IDs
- Identifiers (slugs)
- Full descriptions
- Status and visibility

### Issues
- Issue numbers and titles
- Project associations
- Status, priority, tracker
- Assigned users
- Descriptions
- Created/updated dates

### Time Entries
- Hours logged
- Users who logged time
- Activities
- Comments
- Dates

### Metadata
- All available statuses (Open, In Progress, Closed, etc.)
- Priority levels (Low, Normal, High, Urgent, Immediate)
- Tracker types (Bug, Feature, Support, Task, etc.)

## 🎉 Ready to Use!

The metadata file is now available for:
- Training the Adaptive RAG chatbot
- Testing tool responses
- Documentation examples
- Development reference

**Access it at:** `redminDocs/redmine_metadata.json`
