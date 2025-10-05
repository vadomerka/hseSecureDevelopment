| NFR ID     | Story/Task                                             | Приоритет | Release/Milestone |
|------------|--------------------------------------------------------|-----------|-------------------|
| NFR-API-ERR| API: Единый формат ошибок и хэндлеры                   | High      | 2025.10           |
| NFR-PII    | API: Исключить поле password из ответов                | High      | 2025.10           |
| NFR-DTO    | API: Покрыть валидацию DTO тестами (422)               | High      | 2025.10           |
| NFR-P95    | Perf: Нагрузочный тест p95 для GET /tasks              | Medium    | 2025.11           |
| NFR-THRPUT | Perf: Подтвердить целевой RPS и ошибки ≤1%             | Medium    | 2025.11           |
| NFR-SCA    | CI: Настроить SCA (pip-audit/Dependabot)               | High      | 2025.10           |
| NFR-LOG    | Platform: Маскирование секретов и request_id в логах   | Medium    | 2025.11           |
| NFR-OPENAPI| API: Синхронизация OpenAPI с контрактом                | Medium    | 2025.11           |
Backlog/Roadmap ссылки:
- Issue: API-ERR — формат ошибок и обработчики (PR: #api-err) — владелец: Backend
- Issue: PII — убрать password из ответов (PR: #pii-mask) — владелец: Backend
- Issue: DTO — тесты 422 (PR: #dto-422) — владелец: QA/Backend
- Issue: Perf p95/Throughput — нагрузочные тесты (PR: #perf-tests) — владелец: QA/Perf
- Issue: SCA — включить pip-audit/Dependabot (PR: #sca-ci) — владелец: DevOps
- Issue: Логи — request_id и маскирование (PR: #logging-policy) — владелец: DevOps
- Issue: OpenAPI — выравнивание схем (PR: #openapi-lint) — владелец: Backend
