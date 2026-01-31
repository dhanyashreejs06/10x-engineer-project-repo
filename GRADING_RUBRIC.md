# PromptLab: Grading Rubric

## Total Score: 100 Points

| Week | Focus | Weight |
|------|-------|--------|
| 1 | Backend Foundation | 20% |
| 2 | Documentation & Specs | 25% |
| 3 | Testing & DevOps | 25% |
| 4 | Full-Stack Integration | 30% |

### Grading Scheme

| Grade | Requirement |
|-------|-------------|
| **Satisfactory (S)** | Total score ≥ 70% |
| **Unsatisfactory (U)** | Total score < 70% |

---

## Week 1: Backend Foundation (20 Points)

### Deliverables
- [ ] All 4 bugs fixed and working
- [ ] PATCH endpoint implemented for partial updates
- [ ] All provided tests pass
- [ ] Code committed with meaningful commit messages

### Bug Fixes (12 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Bug #1: GET /prompts/{id} 404 | 3 | Returns proper 404 for non-existent prompts |
| Bug #2: PUT timestamp update | 3 | `updated_at` correctly updates on PUT |
| Bug #3: Sorting order | 3 | Prompts sorted newest-first correctly |
| Bug #4: Collection deletion | 3 | Handles orphaned prompts appropriately |

### New Feature (6 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| PATCH endpoint exists | 2 | Route is defined and accessible |
| Partial update works | 2 | Only provided fields are updated |
| Timestamp updates | 1 | `updated_at` set on PATCH |
| Error handling | 1 | Returns 404 for non-existent prompt |

### Code Quality (2 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Tests pass | 1 | All provided tests pass |
| Clean commits | 1 | Meaningful commit messages |

---

## Week 2: Documentation & Specifications (25 Points)

### Deliverables
- [ ] Comprehensive `README.md` with project overview, setup, and usage
- [ ] Google-style docstrings on all functions in `models.py`, `api.py`, `storage.py`, `utils.py`
- [ ] `docs/API_REFERENCE.md` with full endpoint documentation
- [ ] `.github/copilot-instructions.md` or `.continuerules` for custom AI agent
- [ ] `specs/prompt-versions.md` feature specification
- [ ] `specs/tagging-system.md` feature specification

### README.md (5 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Project overview | 1 | Clear description of what PromptLab does |
| Installation guide | 1 | Step-by-step setup instructions |
| API summary | 1 | List of endpoints with descriptions |
| Usage examples | 1 | Code examples for common operations |
| Professional format | 1 | Well-organized, proper Markdown |

### Docstrings (8 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| models.py coverage | 2 | All models and fields documented |
| api.py coverage | 2 | All endpoints documented with Args/Returns |
| storage.py coverage | 2 | All storage methods documented |
| utils.py coverage | 1 | All utility functions documented |
| Google style format | 1 | Consistent formatting throughout |

### API Reference (4 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| All endpoints covered | 1 | Every endpoint documented |
| Request examples | 1 | curl/fetch examples for each |
| Response examples | 1 | Sample responses shown |
| Error documentation | 1 | Error codes and formats explained |

### Custom AI Agent (3 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| File exists | 1 | `.github/copilot-instructions.md` or `.continuerules` |
| Coding standards | 1 | Clear style guide for the project |
| Useful patterns | 1 | Helpful for AI to generate good code |

### Feature Specifications (5 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| prompt-versions.md | 2.5 | Complete spec with user stories, models, endpoints |
| tagging-system.md | 2.5 | Complete spec with user stories, models, endpoints |

**Spec completeness checklist (for each):**
- [ ] Overview and goals
- [ ] User stories with acceptance criteria
- [ ] Data model changes
- [ ] API endpoints with request/response
- [ ] Edge cases considered

---

## Week 3: Testing & DevOps (25 Points)

### Deliverables
- [ ] Comprehensive test suite with ≥80% code coverage
- [ ] One new feature implemented (Prompt Versions OR Tagging System) using TDD
- [ ] `.github/workflows/ci.yml` GitHub Actions pipeline
- [ ] `backend/Dockerfile` for containerization
- [ ] `docker-compose.yml` for local development
- [ ] Code refactored for quality improvements

### Test Suite (10 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Coverage ≥ 80% | 4 | Measured via pytest-cov |
| API tests complete | 2 | All endpoints tested |
| Edge cases covered | 2 | Error conditions, empty inputs, etc. |
| Tests are meaningful | 2 | Not just coverage padding |

### Feature Implementation (7 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Feature works | 3 | Meets spec requirements |
| TDD approach used | 2 | Evidence of test-first development |
| Tests for feature | 2 | New feature has comprehensive tests |

### CI/CD Pipeline (4 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Workflow file exists | 1 | `.github/workflows/ci.yml` |
| Runs on push/PR | 1 | Correct triggers configured |
| Runs tests | 1 | Tests execute in pipeline |
| Coverage check | 1 | Fails if coverage < 80% |

### Docker Configuration (3 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Dockerfile works | 1.5 | Can build and run container |
| docker-compose.yml | 1 | Local dev setup works |
| Documentation | 0.5 | README explains Docker usage |

### Code Quality (1 point)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Refactoring done | 1 | Visible improvements to code quality |

---

## Week 4: Full-Stack Integration (30 Points)

### Deliverables
- [ ] React frontend scaffolded with Vite
- [ ] Prompt list/grid displaying all prompts
- [ ] Create, edit, delete prompt functionality
- [ ] Collections management UI
- [ ] Frontend connected to backend API
- [ ] Loading states, error handling, and empty states
- [ ] Responsive design that works on mobile

### React Setup (4 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Project scaffolded | 1.5 | Vite + React properly initialized |
| Structure organized | 1.5 | Components, API, etc. in logical folders |
| Styling solution | 1 | CSS approach chosen and implemented |

### Core Components (9 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Prompt list/grid | 3 | Displays all prompts |
| Prompt form | 3 | Create/edit functionality |
| Collections UI | 2 | Can view and manage collections |
| Shared components | 1 | Buttons, modals, etc. |

### API Integration (7 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| API client setup | 1 | Clean API abstraction layer |
| CRUD for prompts | 4 | All operations work |
| CRUD for collections | 2 | All operations work |

### UX Polish (6 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Loading states | 1.5 | Spinners/skeletons during fetch |
| Error handling | 1.5 | User-friendly error messages |
| Empty states | 1 | Helpful UI when no data |
| Responsive design | 1 | Works on mobile |
| Visual design | 1 | Looks professional |

### Integration (4 points)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Frontend connects to backend | 2 | API calls work |
| End-to-end flow works | 2 | Can do full operations |

---

## Grading Scale

| Grade | Score | Description |
|-------|-------|-------------|
| **Satisfactory (S)** | ≥ 70 | Meets requirements, demonstrates competency |
| **Unsatisfactory (U)** | < 70 | Does not meet minimum requirements |

> **Note:** You need at least 70 points (70%) to pass the project.

---

## Automatic Deductions

| Issue | Deduction |
|-------|-----------|
| Tests don't pass | -5 points |
| Application doesn't run | -10 points |
| Missing week deliverable | -25 points (full week) |
| Plagiarism detected | -100 points |
| Late submission (per day) | -5 points |

---

## Bonus Points (Up to 10 extra)

| Bonus | Points | Description |
|-------|--------|-------------|
| Exceptional UI design | +3 | Goes beyond basic functionality |
| Extra features | +3 | Implemented both specs in Week 3 |
| 95%+ test coverage | +2 | Exceptional testing |
| Deployment | +2 | Actually deployed and accessible |

---

## Submission Requirements

Each week, submit:
1. GitHub repository link
2. Brief summary of what you completed
3. Any notes or known issues

**Repository must include:**
- All source code
- Working README with setup instructions
- Passing tests (where applicable)

---

## Questions?

Reach out to your instructor or post in the course forum.

Good luck! 🚀
