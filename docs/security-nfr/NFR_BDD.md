Feature: Нефункциональные требования API Task Tracker

  Scenario: Контракт ошибок единый для not_found (NFR-API-ERR)
    Given развернут сервис FastAPI Task Tracker
    When клиент запрашивает GET /tasks/999
    Then статус ответа равен 404
    And тело содержит объект error с code "not_found" и message

  Scenario: Валидация DTO при отсутствии обязательных полей (NFR-DTO)
    Given развернут сервис FastAPI Task Tracker
    When клиент делает POST /users без обязательных полей
    Then статус ответа равен 422
    And тело содержит поле detail со списком ошибок

  Scenario: PII не попадает в ответы API (NFR-PII)
    Given в системе есть пользователи
    When клиент запрашивает GET /users
    Then ни один элемент ответа не содержит поле password

  Scenario: Производительность GET /tasks p95 (NFR-P95)
    Given сервис развернут на stage и нагрузка 50 RPS
    When запускается 5-минутный нагрузочный тест на GET /tasks
    Then p95 времени ответа ≤ 200 ms

  Scenario: Негативный — деградация при нагрузке (NFR-THRPUT)
    Given целевой RPS = 50
    When в течение 5 минут поддерживается 50 RPS равномерной нагрузкой
    Then процент ошибок 5xx ≤ 1%
