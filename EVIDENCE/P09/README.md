# P09 - SBOM & SCA Evidence

Этот каталог содержит артефакты, сгенерированные workflow `Security - SBOM & SCA`.

## Файлы

- **sbom.json** — Software Bill of Materials в формате CycloneDX JSON, сгенерированный с помощью Syft
- **sca_report.json** — отчёт о сканировании уязвимостей (SCA) от Grype на основе SBOM
- **sca_summary.md** — краткая сводка по уязвимостям с группировкой по severity

## Генерация

Артефакты автоматически генерируются при:
- Push изменений в `**/*.py`, `requirements*.txt` или сам workflow
- Ручном запуске через `workflow_dispatch`

## Использование

Артефакты доступны через GitHub Actions artifacts (`P09_EVIDENCE`) и также сохраняются локально в этом каталоге.

Для просмотра результатов:
1. Перейдите в Actions → выберите последний запуск workflow "Security - SBOM & SCA"
2. Скачайте артефакт `P09_EVIDENCE`
3. Изучите `sca_summary.md` для быстрого обзора, `sca_report.json` для деталей

## Политика управления уязвимостями

См. `policy/waivers.yml` для исключений (waivers) по уязвимостям.
