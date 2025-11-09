# Architecture Overview

## System Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FastAPI Server                       │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │ Middleware │  │   Router   │  │Dependencies│       │
│  └────────────┘  └────────────┘  └────────────┘       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│                   Agent Layer                            │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │  States  │   │  Nodes   │   │  Graphs  │           │
│  └──────────┘   └──────────┘   └──────────┘           │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│                    LLM Layer                             │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │   Groq   │   │  OpenAI  │   │  Custom  │           │
│  └──────────┘   └──────────┘   └──────────┘           │
└──────────────────────────────────────────────────────────┘
```

## Core Components

### 1. LLM Layer (`src/llms/`)

**Responsibility**: Manage LLM providers and interactions

**Key Classes**:
- `BaseLLM`: Abstract interface for all LLM providers
- `GroqLLM`: Groq implementation
- `OpenAILLM`: OpenAI implementation
- `LLMFactory`: Factory for creating LLM instances

**Design Pattern**: Factory + Strategy Pattern

### 2. Agent Layer (`src/agents/`)

#### States (`states/`)
- Define workflow state schemas using TypedDict
- Type-safe state management
- Support for message reducers

#### Nodes (`nodes/`)
- Pure functions that process state
- Implement business logic
- Return partial state updates

#### Graphs (`graphs/`)
- Build LangGraph workflows
- Connect nodes with edges
- Handle conditional routing

### 3. API Layer (`src/api/`)

#### Routers (`v1/`)
- Define REST endpoints
- Handle request/response
- Use dependency injection

#### Middlewares
- `LoggingMiddleware`: Request/response logging
- `ErrorHandlerMiddleware`: Global exception handling
- `RateLimitMiddleware`: Rate limiting
- `CORSHeadersMiddleware`: Security headers

## Data Flow

### Request Flow

```
1. Client → HTTP Request
         ↓
2. Middleware Layer (logging, rate limiting)
         ↓
3. FastAPI Router (endpoint handling)
         ↓
4. Dependency Injection (get LLM, build graph)
         ↓
5. Agent Graph Execution
         ↓
6. LLM Provider (Groq/OpenAI)
         ↓
7. Response Processing
         ↓
8. Middleware Layer (headers, logging)
         ↓
9. Client ← HTTP Response
```

### Agent Workflow

```
Input State → Node 1 → Node 2 → ... → Node N → Output State
              ↓        ↓              ↓
            Tool    Condition      Decision
```

## Design Patterns

### 1. Factory Pattern
Used for creating LLMs and Graphs dynamically based on configuration.

### 2. Dependency Injection
FastAPI's DI system provides LLMs and other dependencies to endpoints.

### 3. Strategy Pattern
Different agent strategies (chatbot, research, writer) with same interface.

### 4. Middleware Pattern
Cross-cutting concerns (logging, auth, rate limiting) handled by middlewares.

### 5. Builder Pattern
Graph builders construct complex workflows step by step.

## State Management

### Message Reducer
```python
messages: Annotated[List[BaseMessage], add_messages]
```
Automatically appends new messages instead of replacing.

### State Updates
Nodes return partial state updates that merge with existing state.

## Error Handling

### Exception Hierarchy
```
AgenticAIException (Base)
├── LLMException
├── ToolException
├── GraphException
├── ConfigurationException
├── AuthenticationException
├── ValidationException
└── RateLimitException
```

### Error Flow
1. Exception raised in node/LLM
2. Caught by ErrorHandlerMiddleware
3. Logged with context
4. Returned as JSON error response

## Configuration Management

### Environment-Based Settings
- `.env` file for sensitive data
- `Settings` class with Pydantic validation
- Cached settings with `@lru_cache`

### Multi-Environment Support
- Development
- Staging
- Production

## Logging Strategy

### Log Levels
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

### Log Destinations
- Console: Colored output for development
- Files: Rotating daily logs
- Error logs: Separate file for errors

## Security

### API Security
- API key authentication (optional)
- JWT token support
- Rate limiting
- CORS configuration

### Input Validation
- Pydantic models for all inputs
- Length limits
- Type checking
- Sanitization

## Performance Considerations

### Caching
- Settings cached with `@lru_cache`
- LLM clients reused across requests

### Async Operations
- FastAPI endpoints are async
- LLM clients support async invocation

### Resource Management
- Connection pooling for HTTP clients
- Proper cleanup in lifespan handler

## Extensibility

### Adding New LLM Provider
1. Create class extending `BaseLLM`
2. Implement `get_client()`
3. Register with `LLMFactory`

### Adding New Agent Type
1. Define state in `states/`
2. Create nodes in `nodes/`
3. Build graph in `graphs/`
4. Create API endpoint

### Adding New Tool
1. Create tool function
2. Register in `tools/base.py`
3. Update `get_available_tools()`

## Testing Strategy

### Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Fast execution

### Integration Tests
- Test API endpoints
- Use test client
- Verify workflows

### Test Coverage
- Aim for >80% coverage
- Focus on critical paths
- Use `pytest-cov`

## Deployment

### Docker (Recommended)
- Containerize application
- Multi-stage build
- Environment-specific configs

### Cloud Platforms
- AWS (ECS, Lambda)
- Google Cloud (Cloud Run)
- Azure (App Service)

### Monitoring
- Health check endpoint
- Structured logging
- Error tracking (Sentry)
- Performance monitoring

## Future Enhancements

1. **Streaming Support**: Real-time response streaming
2. **Multi-Agent**: Agent collaboration and handoffs
3. **Persistence**: Database for conversations and state
4. **Caching**: Redis for response caching
5. **WebSockets**: Real-time communication
6. **Authentication**: Full OAuth2 implementation
7. **Rate Limiting**: Distributed rate limiting
8. **Observability**: Metrics and tracing
