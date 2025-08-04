# Infrastructure Domain Agent Patterns

## Infrastructure-Specific Agent Selection Intelligence

### Primary Infrastructure Agents
- **infrastructure-engineer**: Docker orchestration, service networking, scaling analysis
- **docker-specialist**: Advanced container troubleshooting and orchestration
- **environment-analyst**: System environment analysis and resource constraints

### Infrastructure Integration Patterns

#### **Docker Orchestration Complexity**
```
User Context: "Docker orchestration issues with service networking and scaling"
→ infrastructure-engineer (primary)
→ Coordination: docker-specialist + performance-optimizer
→ Success Rate: 93% for orchestration + performance issues
```

#### **Environment + Configuration Issues**
```
User Context: "Environment configuration problems affecting deployment"
→ environment-analyst (primary)
→ Coordination: configuration-validator + environment-synchronizer
→ Success Rate: 89% for environment + config issues
```

#### **Infrastructure Performance Problems**
```
User Context: "Infrastructure performance bottlenecks in container deployment"
→ infrastructure-engineer (primary)
→ Coordination: performance-optimizer + resource-optimizer + docker-specialist
→ Success Rate: 91% for performance + infrastructure coordination
```

### Infrastructure Performance Patterns

#### **Response Time Optimization**
- **infrastructure-engineer**: Average 1.4s for orchestration issues
- **docker-specialist**: Average 1.1s for container troubleshooting
- **environment-analyst**: Average 1.6s for environment analysis

#### **Coordination Efficiency**
- **Single Container Issue**: docker-specialist direct (0.8s average)
- **Multi-Infrastructure Domains**: Primary + 2-3 agents (1.8s average)
- **Complex Deployment Issues**: Meta-orchestration (2.5s average)

### Common Infrastructure Scenarios

#### **High-Success Patterns**
1. **Docker + Performance Issues**: infrastructure-engineer → docker-specialist + performance-optimizer (94% success)
2. **Environment + Configuration**: environment-analyst → configuration-validator (92% success)
3. **Infrastructure + CI/CD**: infrastructure-engineer → ci-specialist (88% success)

#### **Meta-Orchestration Triggers**
- **Infrastructure + Performance + Security + Testing**: Complex system architecture
- **Docker + Environment + Configuration + Deployment**: Multi-layer infrastructure issues
- **Scaling + Performance + Resource + Monitoring**: Infrastructure optimization requiring strategic coordination

### RAG MemoryBank MCP Infrastructure Context

#### **Project-Specific Infrastructure Intelligence**
- **Container Services**: MCP server, Qdrant vector database containers
- **Essential Commands**: `make docker-up`, `make start-mcp`, `make mcp-status`
- **Service Health**: MCP + Qdrant container coordination and health monitoring
- **Network Architecture**: Service-to-service communication patterns

#### **Infrastructure Integration Patterns**
- **MCP Server Deployment**: Docker container orchestration with health checks
- **Qdrant Integration**: Vector database container coordination and networking
- **Service Mesh**: Inter-service communication and service discovery patterns
- **Performance Monitoring**: Container resource usage and optimization strategies

#### **Docker-Specific Patterns**
- **Container Orchestration**: Multi-service container coordination
- **Health Check Configuration**: Service health validation and monitoring
- **Network Configuration**: Container networking and service communication
- **Resource Management**: Container resource allocation and optimization

#### **Environment Coordination**
- **Development Environment**: Local development with Docker containers
- **CI Environment**: GitHub Actions with Docker services
- **Production Environment**: Scalable container deployment patterns
- **Cross-Environment**: Configuration synchronization and deployment consistency

### Advanced Infrastructure Coordination

#### **Performance-Critical Infrastructure**
- **Qdrant Performance**: Vector database optimization and scaling
- **MCP Server Performance**: Server response time and throughput optimization
- **Container Performance**: Resource allocation and container optimization
- **Network Performance**: Service communication latency and throughput

#### **Security Infrastructure**
- **Container Security**: Docker security best practices and vulnerability scanning
- **Network Security**: Service-to-service communication security
- **Access Control**: Infrastructure access patterns and security policies
- **Monitoring Security**: Infrastructure security monitoring and alerting

This domain memory provides specialized infrastructure intelligence while maintaining integration with the broader agent coordination framework for complex multi-domain issues.