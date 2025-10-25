# System Diagrams for AI Code Generator

## 1. Data Flow Diagram
```mermaid
flowchart TD
    User[User/Client] --> |Sends prompt| Frontend[Frontend UI]
    Frontend --> |HTTP Request| Backend[Backend API]
    Backend --> |Generate Request| Ollama[Ollama LLM]
    Ollama --> |Generated Code| Backend
    Backend --> |Store| DB[(SQLite Database)]
    Backend --> |Code Response| Frontend
    User --> |Feedback| Frontend
    Frontend --> |Submit Feedback| Backend
    Backend --> |Store Feedback| DB
    DB --> |Learning Patterns| Backend
    Backend --> |Suggestions| Frontend
```

## 2. Use Case Diagram
```mermaid
graph TD
    subgraph Users
        Developer[Developer]
        Administrator[System Administrator]
        AIEngineer[AI Engineer]
    end
    
    subgraph AI_Code_Generator
        GC[Generate Code]
        PF[Provide Feedback]
        VS[View Statistics]
        DL[Detect Language]
        LP[Learning Patterns]
        SP[Stream Progress]
        CM[Configure Models]
        MA[Monitor Analytics]
    end
    
    Developer --> GC
    Developer --> PF
    Developer --> VS
    Developer --> DL
    
    Administrator --> CM
    Administrator --> MA
    
    AIEngineer --> LP
    AIEngineer --> CM
    
    GC --> LP
    PF --> LP
```

## 3. System Architecture Block Diagram
```mermaid
graph TB
    subgraph Frontend
        UI[React UI]
        Prism[Prism.js Syntax Highlighting]
        WebSocket[WebSocket Client]
    end
    
    subgraph Backend
        API[FastAPI Server]
        Learning[Learning Engine]
        OllamaService[Ollama Service]
        DBService[Database Service]
    end
    
    subgraph Database
        SQLite[(SQLite DB)]
    end
    
    subgraph AI
        Ollama[Ollama LLM]
    end
    
    UI --> |HTTP/WS| API
    API --> |Generate| OllamaService
    OllamaService --> Ollama
    API --> |Store/Query| DBService
    DBService --> SQLite
    API --> |Analysis| Learning
    Learning --> DBService
    WebSocket --> API
```

## 4. Class Diagram
```mermaid
classDiagram
    class UserProfile {
        +id: Integer
        +username: String
        +created_at: DateTime
        +prompts: List[Prompt]
        +feedbacks: List[Feedback]
    }
    
    class Prompt {
        +id: Integer
        +user_id: Integer
        +prompt_text: String
        +detected_language: String
        +created_at: DateTime
        +outputs: List[ModelOutput]
    }
    
    class ModelOutput {
        +id: Integer
        +prompt_id: Integer
        +model_name: String
        +generated_code: String
        +raw_output: String
        +language: String
        +generation_time_ms: Integer
        +temperature: Float
        +success: Boolean
        +error_message: String
        +created_at: DateTime
        +feedback: List[Feedback]
    }
    
    class Feedback {
        +id: Integer
        +output_id: Integer
        +user_id: Integer
        +rating: Integer
        +feedback_type: String
        +comments: String
        +created_at: DateTime
    }
    
    class LearningPattern {
        +id: Integer
        +language: String
        +pattern_type: String
        +pattern_description: String
        +avg_rating: Float
        +confidence_score: Float
        +occurrence_count: Integer
        +created_at: DateTime
    }
    
    UserProfile "1" -- "*" Prompt : has
    Prompt "1" -- "*" ModelOutput : generates
    ModelOutput "1" -- "*" Feedback : receives
    UserProfile "1" -- "*" Feedback : provides
```

## 5. Main Pipeline
```mermaid
graph LR
    A[User Input] --> B[Language Detection]
    B --> C[Code Generation]
    C --> D[Syntax Highlighting]
    D --> E[Display Output]
    E --> F[Collect Feedback]
    F --> G[Update Learning Patterns]
```

## 6. Performance Pipeline
```mermaid
graph LR
    A[Request] --> B[Request Validation]
    B --> C[Cache Check]
    C --> |Cache Miss| D[Generate Code]
    C --> |Cache Hit| G[Return Cached]
    D --> E[Process Result]
    E --> F[Cache Result]
    F --> G[Return Response]
    G --> H[Log Metrics]
```

## 7. Error Handling Pipeline
```mermaid
graph TD
    A[Input] --> B{Validate Request}
    B --> |Invalid| C[Return 400]
    B --> |Valid| D{Check Ollama}
    D --> |Not Running| E[Return 503]
    D --> |Running| F{Generate Code}
    F --> |Error| G[Return 500]
    F --> |Success| H[Process Output]
    H --> |Invalid| I[Return 422]
    H --> |Valid| J[Return 200]
    
    subgraph Error Types
        C
        E
        G
        I
    end
```

## 8. Learning Feedback Pipeline
```mermaid
graph TD
    A[Receive Feedback] --> B[Validate Rating]
    B --> C[Store in Database]
    C --> D[Update Statistics]
    D --> E[Analyze Patterns]
    E --> F[Extract Success Patterns]
    E --> G[Extract Error Patterns]
    F --> H[Update Learning Model]
    G --> H
    H --> I[Generate Suggestions]
```