# Digital Krishna AI — Technical Architecture

## DSOC Summer Edition 2026

Digital Krishna AI uses a modular architecture that separates the
user interface, request validation, safety processing, scripture
retrieval, AI-generated interpretation, response validation, and
media delivery.

This document describes the public DSOC architecture. Components are
labelled according to their current development status.

## Status Labels

- **Implemented:** Working in the current product
- **Prototype:** Partially working or available for demonstration
- **Experimental:** Under technical testing
- **Planned:** Not implemented yet

---

## High-Level Architecture

```text
User
  │
  ▼
Digital Krishna Web Interface
  │
  ├── Text input
  ├── Voice input
  ├── Scripture library
  ├── Stories
  ├── Animations
  └── Reflection interface
  │
  ▼
Application Backend
  │
  ├── Request validation
  ├── Language detection
  ├── Concern classification
  ├── Safety screening
  └── Session handling
  │
  ▼
Scripture Retrieval Layer
  │
  ├── Curated scripture records
  ├── Theme matching
  ├── Source metadata
  └── Optional semantic retrieval
  │
  ▼
AI Guidance Layer
  │
  ├── Controlled context construction
  ├── Qwen-based model workflow
  ├── Structured generation
  └── Multilingual interpretation
  │
  ▼
Response Validation Layer
  │
  ├── Schema validation
  ├── Source-integrity checking
  ├── Safety validation
  ├── Relevance checking
  └── Fallback handling
  │
  ▼
Structured User Response
```

---

## 1. Frontend Layer

**Status: Implemented**

The frontend provides the primary Digital Krishna user experience.

### Main responsibilities

- Collect user input
- Display AI guidance
- Present scripture content
- Show stories and animations
- Support responsive desktop and mobile layouts
- Display loading, validation, and error states

### Technologies

- React
- JavaScript and JSX
- React Router
- Tailwind CSS
- Responsive CSS
- Radix UI
- Lucide icons
- Axios
- Zod or compatible schema validation

### Main interfaces

- Home page
- Saathi AI Companion
- Scripture library
- Verse-reading page
- Krishna story library
- Animation and narration experience
- Reflection tools
- Mobile-responsive navigation

---

## 2. Backend Layer

**Status: Prototype**

The backend coordinates guidance requests and connects the frontend
with retrieval, safety, model, and validation components.

### Responsibilities

- Receive user requests
- Validate request structure
- Detect input language
- Classify the user concern
- Apply safety checks
- Retrieve relevant scripture records
- Construct controlled model context
- Validate generated output
- Return a structured response

### Technologies

- Python
- HTTP API routes
- JSON-based prototype storage
- Environment-based configuration
- Contract and schema validation

No credentials or private production configuration are included in
this public repository.

---

## 3. Request Validation

**Status: Prototype**

Request validation checks whether an incoming request contains the
required fields and acceptable values.

Example request structure:

```json
{
  "message": "I am worried about my future.",
  "language": "en",
  "session_id": "anonymous-demo-session"
}
```

Validation may check:

- Message exists
- Message is not empty
- Input length is within limits
- Language value is supported
- Unexpected fields are rejected
- Unsafe file or command inputs are not accepted

---

## 4. Language Detection

**Status: Prototype**

Digital Krishna is designed to process:

- English
- Hindi
- Hinglish
- Romanised Hindi

Language detection supports:

- Response-language selection
- Concern classification
- Safety screening
- Scripture retrieval
- Multilingual explanation

Additional Indian languages are planned for future versions.

---

## 5. Concern Classification

**Status: Prototype**

The system identifies the general category of the user’s concern.

Possible categories include:

- Academic stress
- Career uncertainty
- Fear and anxiety
- Anger
- Motivation
- Relationships
- Loneliness
- Grief
- Self-discipline
- Decision-making
- Spiritual reflection

The classification result helps select relevant teachings and
response instructions.

---

## 6. Safety Screening

**Status: Prototype**

Safety checks are applied before and after response generation.

### Input screening

The system checks for language involving:

- Immediate danger
- Severe emotional distress
- Abuse or exploitation
- Threats toward another person
- Medical emergencies
- Illegal or dangerous requests

### Output screening

Generated responses may be checked for:

- Unsafe instructions
- Unsupported professional claims
- Excessive certainty
- Manipulative language
- Incorrect scripture attribution
- Invalid response structure

When a request falls outside the platform’s role, the system should
provide safe boundaries and encourage appropriate real-world support.

---

## 7. Scripture Retrieval Layer

**Status: Prototype**

The scripture retrieval layer connects a modern concern with relevant
reviewed teachings.

A scripture record may contain:

```json
{
  "id": "gita-2-47",
  "source": "Bhagavad Gita",
  "chapter": 2,
  "verse": 47,
  "original_text": "Reviewed source text",
  "hindi_translation": "Reviewed Hindi translation",
  "english_translation": "Reviewed English translation",
  "teaching": "Reviewed teaching summary",
  "themes": [
    "duty",
    "discipline",
    "detachment"
  ],
  "review_status": "reviewed"
}
```

### Retrieval process

```text
User concern
    ↓
Concern category
    ↓
Theme and keyword matching
    ↓
Candidate scripture records
    ↓
Relevance ranking
    ↓
Selected reviewed teaching
```

Semantic retrieval using a vector database is an experimental
extension and should not be described as fully deployed unless it is
connected in the working application.

---

## 8. Scripture Integrity

**Status: Prototype**

Verified scripture and AI-generated explanation are treated as
different content types.

The system should keep separate:

1. Original or reviewed scripture text
2. Reviewed translation
3. Reviewed teaching summary
4. AI-generated explanation
5. Practical reflection suggestions

The AI must not create new wording and present it as an authentic
scripture quotation.

When no verified record is available, the response should avoid
claiming that a specific verse was retrieved.

---

## 9. AI Guidance Layer

**Status: Experimental**

The AI guidance layer uses:

- User concern
- Language preference
- Concern category
- Retrieved teaching
- Safety instructions
- Required response structure

The project includes a Qwen-based model-development workflow. The
public repository may include sanitized examples and architecture
documentation, but no private model credentials or production
endpoints.

Example response structure:

```json
{
  "category": "Academic stress",
  "acknowledgement": "Empathetic acknowledgement",
  "source": {
    "reference": "Bhagavad Gita 2.47",
    "text": "Verified source text"
  },
  "explanation": "How the teaching relates to the concern",
  "practical_steps": [
    "Create a small study plan",
    "Focus on the next achievable task",
    "Reflect on effort rather than only results"
  ],
  "reflection_question": "What action is within your control today?",
  "safety_note": null
}
```

---

## 10. Response Validation

**Status: Prototype**

Before a response is shown, the system may verify:

- Required fields are present
- The response matches the expected schema
- The scripture reference matches the retrieved record
- Protected scripture text has not been altered
- Practical steps are understandable
- Unsafe claims are not included
- The response language matches the user preference

When validation fails, the application should return a safe fallback
rather than displaying an unverified response.

---

## 11. Data Storage

**Status: Prototype**

The project may use:

- JSON-based application records
- Curated scripture datasets
- Anonymous session identifiers
- Saved user preferences
- Optional vector-search storage

The public DSOC repository must not contain:

- Private conversations
- User passwords
- Personal contact details
- Authentication tokens
- Cloud credentials
- Production databases
- Private analytics exports

---

## 12. Media Layer

**Status: Implemented**

Digital Krishna includes educational and devotional media such as:

- Krishna stories
- Scene illustrations
- Animations
- Narration
- Audio playback
- Responsive video delivery

Media features are separated from the core guidance flow so that the
main experience can remain accessible on lower-powered devices.

Large copyrighted or privately licensed media files are not included
in the sanitized public repository unless redistribution is permitted.

---

## 13. Deployment Architecture

**Status: Prototype**

The platform is designed for cloud deployment using components such
as:

- Static or React frontend hosting
- Python backend service
- Environment variables
- Docker
- Render
- AWS Elastic Beanstalk
- Private model-serving endpoint

Example deployment flow:

```text
User Browser
    ↓
Public Web Frontend
    ↓
Secure Backend API
    ↓
Retrieval and Validation Services
    ↓
Private Model Provider
```

Secrets must be stored in the deployment platform’s environment
settings and never committed to GitHub.

---

## 14. Scalability

**Status: Planned**

Future scalability improvements may include:

- Dedicated production database
- Larger reviewed scripture collection
- Vector-search infrastructure
- Response caching
- Background job queues
- Horizontally scalable APIs
- Dedicated private model serving
- Content-delivery network for media
- Monitoring and logging
- Rate limiting
- Automated deployment pipelines

---

## 15. Development Tool Disclosure

Codex with GPT-5.6 supported engineering tasks such as:

- Repository analysis
- Architecture planning
- Implementation assistance
- Debugging
- Test preparation
- Dataset-format preparation
- Safety improvements
- Documentation
- Deployment planning

Codex and GPT-5.6 were used as development tools.

They are not presented as scripture sources, spiritual authorities, or
the voice of Krishna.

---

## 16. Current Limitations

The prototype may have limitations including:

- Limited reviewed scripture coverage
- Incomplete multilingual evaluation
- Experimental model-serving components
- Limited expert review
- Classification errors
- Retrieval of partially relevant teachings
- Dependence on reviewed source-data quality
- Limited production monitoring

These limitations are documented to maintain transparency.

---

## Architecture Principle

Digital Krishna separates:

```text
Verified source content
        ≠
AI-generated interpretation
```

This separation is central to the project’s safety, cultural
responsibility, and source integrity.
