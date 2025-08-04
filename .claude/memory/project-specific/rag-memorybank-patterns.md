# RAG MemoryBank MCP Project-Specific Agent Patterns

## Project Intelligence Context
Specialized agent coordination patterns for the RAG MemoryBank MCP system with memory and requirements management capabilities.

## Project Architecture Context

### Core System Components
- **Hybrid RAG Pipeline**: BM25S keyword search + Qdrant vector similarity search
- **MCP Server Implementation**: FastMCP-based Model Context Protocol server
- **Vector Database Integration**: Qdrant for document storage and vector operations
- **Evaluation Framework**: TruLens integration for RAG pipeline assessment
- **Testing Standards**: ≥82% coverage requirement with comprehensive testing infrastructure

### Technical Stack Intelligence
- **FastMCP**: Official MCP server implementation patterns and SDK compliance
- **TruLens**: RAG evaluation and feedback loop integration
- **Qdrant Client**: Vector database operations and optimization
- **BM25S Library**: Keyword search and text processing
- **Python Architecture**: Type hints, descriptive naming, quality standards

## Agent Selection Intelligence for RAG MemoryBank MCP

### Project-Specific Agent Expertise

#### **Infrastructure Agents + RAG MemoryBank Context**
```
infrastructure-engineer + RAG MemoryBank MCP Context:
- **MCP Server Deployment**: FastMCP server containerization and orchestration
- **Qdrant Integration**: Vector database container coordination and health monitoring
- **Service Networking**: MCP server ↔ Qdrant communication optimization
- **Performance Monitoring**: MCP response times and vector search latency
- **Commands**: make docker-up, make start-mcp, make mcp-status
```

#### **Testing Agents + RAG MemoryBank Context**
```
test-specialist + RAG MemoryBank MCP Context:
- **Coverage Requirements**: ≥82% coverage validation and gap analysis
- **MCP Server Testing**: FastMCP server endpoint testing and integration validation
- **Vector Search Testing**: Qdrant client testing and vector similarity validation
- **Hybrid Pipeline Testing**: BM25S + vector search integration testing
- **Evaluation Testing**: TruLens evaluation framework testing and validation
- **Commands**: make test-coverage, ./scripts/ci-modular-runner.sh fast
```

#### **Code Quality Agents + RAG MemoryBank Context**
```
code-quality-specialist + RAG MemoryBank MCP Context:
- **SDK Compliance**: FastMCP, TruLens, Qdrant, BM25S official pattern compliance
- **Security Scanning**: Semgrep integration with MCP server security validation
- **Quality Standards**: 750 lines max per file, 50 lines max per function
- **Type Safety**: Type hints required for all functions, descriptive variable naming
- **Performance Standards**: MCP server response time optimization
- **Commands**: make lint-ci, make pre-commit-staged
```

### Hybrid RAG Pipeline Coordination

#### **Search Architecture Intelligence**
```
RAG Pipeline Coordination Pattern:
User Query → BM25S Keyword Search + Qdrant Vector Search → Hybrid Result Fusion → Response Generation

Agent Coordination for Pipeline Issues:
- **performance-optimizer**: Pipeline response time optimization and bottleneck analysis
- **infrastructure-engineer**: Qdrant scaling and BM25S index optimization
- **test-specialist**: Pipeline accuracy testing and evaluation validation
- **code-quality-specialist**: Search algorithm quality and pattern compliance
```

#### **Vector Database Operations**
```
Qdrant Integration Patterns:
- **Collection Management**: Vector collection creation, indexing, and optimization
- **Search Operations**: Similarity search, filtering, and result ranking
- **Performance Tuning**: Vector dimension optimization and search latency reduction
- **Data Management**: Document ingestion, vector embedding, and storage optimization

Agent Coordination for Qdrant Issues:
- **infrastructure-engineer**: Qdrant container orchestration and resource allocation
- **performance-optimizer**: Vector search performance and index optimization
- **integration-validator**: End-to-end vector pipeline validation
- **docker-specialist**: Qdrant container troubleshooting and configuration
```

### MCP Server Development Patterns

#### **FastMCP Implementation Intelligence**
```
MCP Server Development Coordination:
- **FastMCP SDK Patterns**: Official MCP server implementation following FastMCP guidelines
- **Tool Integration**: MCP tool definitions and handler implementation
- **Resource Management**: MCP resource serving and protocol compliance
- **Error Handling**: MCP protocol error handling and client communication
- **Performance**: MCP server response time optimization and concurrent handling

Agent Coordination for MCP Development:
- **intelligent-enhancer**: SDK pattern compliance and MCP best practices
- **code-quality-specialist**: MCP server quality and security validation
- **test-specialist**: MCP server testing and protocol compliance validation
- **performance-optimizer**: MCP server performance tuning and optimization
```

#### **TruLens Integration Patterns**
```
RAG Evaluation Framework Coordination:
- **Evaluation Metrics**: RAG pipeline accuracy, relevance, and performance metrics
- **Feedback Loops**: Continuous improvement based on evaluation results
- **Quality Assessment**: Response quality evaluation and optimization
- **Performance Tracking**: Evaluation framework performance and efficiency

Agent Coordination for TruLens Integration:
- **test-specialist**: TruLens evaluation testing and framework validation
- **performance-optimizer**: Evaluation performance optimization and efficiency
- **code-quality-specialist**: TruLens integration quality and compliance
- **integration-validator**: End-to-end evaluation pipeline validation
```

## Project-Specific Quality Standards

### Development Standards Intelligence
```
RAG MemoryBank MCP Quality Requirements:
- **File Size Limits**: 750 lines implementation, 1000 lines tests
- **Function Complexity**: Maximum 50 lines per function
- **Variable Naming**: Descriptive names, avoid data/result/temp
- **Type Annotations**: Required for all functions
- **Indentation**: 2-space YAML, 4-space Python
- **Coverage Requirements**: ≥82% test coverage mandatory
```

### SDK-First Development Approach
```
Official SDK Integration Patterns:
- **FastMCP**: Use official FastMCP patterns for MCP server implementation
- **TruLens**: Follow official TruLens patterns for RAG evaluation
- **Qdrant**: Use official Qdrant client for vector operations
- **BM25S**: Use BM25S library for keyword search implementation

Agent Selection for SDK Issues:
- **intelligent-enhancer**: SDK pattern compliance and best practices
- **code-quality-specialist**: SDK security and quality validation
- **pattern-analyzer**: SDK architectural pattern consistency
- **integration-validator**: SDK integration testing and validation
```

### Performance Intelligence for RAG MemoryBank MCP

#### **System Performance Patterns**
```
Performance Optimization Priorities:
1. **MCP Server Response Time**: <500ms for standard operations
2. **Vector Search Latency**: <200ms for similarity search operations
3. **Hybrid Search Performance**: <300ms for combined BM25S + vector search
4. **Pipeline Throughput**: >100 queries/second under normal load
5. **Memory Efficiency**: Optimal RAM usage for vector embeddings and search indices

Agent Coordination for Performance:
- **performance-optimizer**: System-wide performance analysis and optimization
- **resource-optimizer**: Memory and CPU optimization for vector operations
- **infrastructure-engineer**: Container resource allocation and scaling
- **docker-specialist**: Container performance tuning and optimization
```

#### **Integration Performance Patterns**
```
Cross-System Performance Intelligence:
- **MCP ↔ Qdrant Communication**: Minimize network latency and optimize data transfer
- **BM25S ↔ Vector Search Coordination**: Parallel execution and result fusion optimization
- **TruLens Evaluation Performance**: Efficient evaluation without impacting search performance
- **Container Orchestration**: Optimal resource allocation for multi-service architecture

Performance Monitoring Commands:
- **Service Health**: make mcp-status for real-time performance monitoring
- **Load Testing**: ./scripts/ci-modular-runner.sh comprehensive for performance validation
- **Resource Monitoring**: Container resource usage and optimization analysis
```

### CI/CD Integration Patterns

#### **GitHub Actions Workflow Intelligence**
```
CI/CD Pipeline Coordination for RAG MemoryBank MCP:
- **Fast Validation**: ./scripts/ci-modular-runner.sh fast (≤4 min target)
- **Standard Testing**: ./scripts/ci-modular-runner.sh standard (≤9 min target)
- **Comprehensive Analysis**: ./scripts/ci-modular-runner.sh comprehensive (≤15 min target)
- **Manual Triggers**: gh workflow run ci-modular.yml -f test_scope=[fast|standard|comprehensive]

Agent Coordination for CI/CD:
- **ci-specialist**: GitHub Actions workflow optimization and troubleshooting
- **workflow-optimizer**: CI/CD pipeline performance optimization and caching
- **test-specialist**: CI testing validation and coverage verification
- **infrastructure-engineer**: CI environment Docker coordination and optimization
```

This project-specific memory provides deep RAG MemoryBank MCP context for intelligent agent selection and coordination, ensuring agents have sophisticated understanding of the system architecture, requirements, and performance standards.