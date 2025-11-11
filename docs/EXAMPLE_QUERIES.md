# 11 Example Questions for Your Hybrid RAG Redmine Chatbot

## 🎯 Organized by Query Type

### 📦 Layer 1: Metadata Cache Questions (< 1ms - Lightning Fast!)

**1. "What projects do I have?"**
```
Route: redmine_tools → JSON cache
Tool: list_all_available_resources
Speed: < 1ms
Result: Lists all 5 projects with IDs and names
```

**2. "What is the project ID for Ni-kshay Setu Revamp?"**
```
Route: redmine_tools → JSON cache
Tool: get_project_info_by_name
Speed: < 1ms
Result: Project ID: 37, identifier: ni-kshay-setu-revamp
```

**3. "What statuses are available in Redmine?"**
```
Route: redmine_tools → JSON cache
Tool: list_all_available_resources
Speed: < 1ms
Result: New, In Progress, Resolved, Feedback, Closed, Rejected
```

---

### 🧠 Layer 2: Semantic Search Questions (~100ms - AI-Powered!)

**4. "Find issues similar to authentication problems"**
```
Route: vector_search → ChromaDB
Tool: semantic_search_issues
Speed: ~100ms
Result: Issues about login, OAuth, credentials, SSO (semantic match!)
```

**5. "Show me issues related to database performance"**
```
Route: vector_search → ChromaDB
Tool: semantic_search_issues
Speed: ~100ms
Result: Issues about queries, indexing, optimization, slow responses
```

**6. "What issues mention payment gateway?"**
```
Route: vector_search → ChromaDB
Tool: semantic_search_issues
Speed: ~100ms
Result: Issues about transactions, checkout, billing, payment API
```

---

### 📡 Layer 3: Real-Time API Questions (~500ms - Current Data!)

**7. "Show me all open issues in Ni-kshay Setu Revamp project"**
```
Route: redmine_tools → API call
Tool: get_redmine_issues (project_id=37, status="open")
Speed: ~500ms
Result: Current list of all open issues with latest status
```

**8. "What are the details of issue #22812?"**
```
Route: redmine_tools → API call
Tool: get_redmine_issue_details (issue_id=22812)
Speed: ~500ms
Result: Full issue details, status, assignee, description, updates
```

**9. "Search for issues with subject containing 'API'"**
```
Route: redmine_tools → API call
Tool: search_redmine_issues (query="API")
Speed: ~500ms
Result: All issues with "API" in subject or description
```

---

### 💬 Layer 4: Direct Answer Questions (~200ms - No Tools!)

**10. "What is Redmine?"**
```
Route: direct_answer → LLM
Tool: None (direct response)
Speed: ~200ms
Result: "Redmine is an open-source project management tool..."
```

**11. "Hello! What can you help me with?"**
```
Route: direct_answer → LLM
Tool: None (direct response)
Speed: ~200ms
Result: Greeting + capabilities explanation
```

---

## 🚀 Quick Test Commands

### Test All 11 Questions:

```bash
# 1. Metadata - Projects list
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What projects do I have?"}'

# 2. Metadata - Project ID lookup
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the project ID for Ni-kshay Setu Revamp?"}'

# 3. Metadata - Available statuses
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What statuses are available in Redmine?"}'

# 4. Semantic - Similar to authentication
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find issues similar to authentication problems"}'

# 5. Semantic - Database performance
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me issues related to database performance"}'

# 6. Semantic - Payment gateway
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What issues mention payment gateway?"}'

# 7. API - Open issues in project
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all open issues in Ni-kshay Setu Revamp project"}'

# 8. API - Issue details
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the details of issue #22812?"}'

# 9. API - Search issues
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Search for issues with subject containing API"}'

# 10. Direct - General question
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Redmine?"}'

# 11. Direct - Greeting
curl -X POST http://localhost:8000/api/v1/redmine/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! What can you help me with?"}'
```

---

## 🎯 More Advanced Questions

### Combined Queries (Using Multiple Layers):

**12. "In the Ni-kshay project, find issues similar to API integration problems"**
```
Step 1: Get project ID from cache (< 1ms)
Step 2: Semantic search in that project (~100ms)
Total: ~100ms
```

**13. "Show me high priority open issues in project 37"**
```
Step 1: Get priority ID from cache (< 1ms)
Step 2: API call with filters (~500ms)
Total: ~500ms
```

**14. "What issues are in Resolved status in Digiflux projects?"**
```
Step 1: Get status ID from cache (< 1ms)
Step 2: Get project IDs from cache (< 1ms)
Step 3: API call with filters (~500ms)
Total: ~500ms
```

---

## 💡 Pro Tips

### For Fastest Results:
✅ Ask about projects, statuses, priorities (< 1ms)
✅ Use project names directly ("Ni-kshay Setu Revamp")
✅ Ask for lists of resources

### For Semantic Discovery:
✅ Use phrases like "similar to", "related to", "about"
✅ Ask content-based questions
✅ Find issues by concept, not exact keywords

### For Current Data:
✅ Ask for "open" or "closed" issues
✅ Request specific issue details by ID
✅ Search with exact keywords

### For Quick Answers:
✅ Ask general questions about Redmine
✅ Request capability information
✅ Use greetings and conversation

---

## 📊 Expected Response Times

| Question Type | Speed | Layer Used |
|--------------|-------|------------|
| Q1-Q3 (Metadata) | < 1ms | JSON Cache ⚡ |
| Q4-Q6 (Semantic) | ~100ms | Vector DB 🧠 |
| Q7-Q9 (Real-time) | ~500ms | API Call 📡 |
| Q10-Q11 (Direct) | ~200ms | LLM Only 💬 |

---

## 🎊 What Makes These Questions Work?

### Metadata Questions (Q1-Q3):
- ✅ Pre-loaded data in JSON
- ✅ No API calls needed
- ✅ Instant results

### Semantic Questions (Q4-Q6):
- ✅ Understand meaning, not just words
- ✅ Find related concepts
- ✅ Content-based discovery

### API Questions (Q7-Q9):
- ✅ Real-time current data
- ✅ Filtered and specific
- ✅ Always up-to-date

### Direct Questions (Q10-Q11):
- ✅ LLM knowledge
- ✅ No tools needed
- ✅ Conversational

---

## 🧪 Test Scenario

Run all 11 questions in sequence and observe:

1. **Speed Variation**: Notice how Q1-Q3 are instant, Q4-Q6 take ~100ms, Q7-Q9 take ~500ms
2. **Routing Decisions**: Check logs to see which layer each question routes to
3. **Accuracy**: Semantic search finds related issues even with different words
4. **Intelligence**: Router automatically picks the best datasource

---

## 🎯 Success Criteria

For each question, you should see:

✅ Correct routing decision in logs
✅ Appropriate tools called
✅ Relevant results returned
✅ Expected response time
✅ Quality answer generated

---

Happy testing! 🚀

Try these questions to experience the full power of your hybrid RAG system!
