# Terragrunt Agent Quick Reference

> Краткий справочник для AI-агентов при работе с Terragrunt конфигурациями.

---

## Роли и Ответственности

### 🏛️ Architect Role

**Задачи:**
- Проектирование структуры репозиториев (live/catalog)
- Определение стратегии тегирования
- Архитектура multi-account/multi-region
- Стандарты безопасности и compliance

**При создании новой инфраструктуры:**
```
1. Определить account-структуру (prod/non-prod/mgmt)
2. Спроектировать иерархию тегов
3. Выбрать regions и AZ strategy
4. Определить blast radius для stacks
5. Задокументировать dependency graph
```

### 🔧 DevOps Role

**Задачи:**
- Создание и поддержка terragrunt конфигураций
- CI/CD пайплайны для деплоя
- Мониторинг state drift
- Управление секретами

**При деплое:**
```bash
# Порядок операций
terragrunt stack generate      # Сначала генерируем units
terragrunt run --all validate  # Валидируем
terragrunt run --all plan      # Планируем
terragrunt run --all apply     # Применяем (после review)
```

### 🤖 Terragrunt-Agent Role

**Задачи:**
- Автоматическая генерация конфигураций
- Валидация синтаксиса и best practices
- Автоматизация рутинных операций

**Правила генерации кода:**
```
✅ ВСЕГДА использовать labeled includes
✅ ВСЕГДА пинить версии модулей  
✅ ВСЕГДА добавлять mock_outputs
✅ ВСЕГДА использовать jsonencode для tags
❌ НИКОГДА не хардкодить секреты
❌ НИКОГДА не использовать latest/main в prod
```

---

## Шаблоны Быстрого Создания

### Новый Account

```hcl
# {account}/account.hcl
locals {
  account_name   = "ACCOUNT_NAME"        # prod, non-prod, mgmt
  aws_account_id = "123456789012"
  environment    = "production"          # production, staging, development
  
  # Tagging
  owner               = "platform-team"
  team                = "infrastructure"
  cost_center         = "CC-XXXX"
  data_classification = "internal"       # public, internal, confidential
  
  # Settings
  enable_deletion_protection = true
  log_retention_days         = 365
}
```

### Новый Region

```hcl
# {account}/{region}/region.hcl
locals {
  aws_region         = "us-east-1"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  project            = "main-platform"
}
```

### Новый Unit

```hcl
# {account}/{region}/{service}/terragrunt.hcl
include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

terraform {
  source = "git::git@github.com:COMPANY/infrastructure-catalog.git//modules/MODULE?ref=vX.Y.Z"
}

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

dependency "DEPENDENCY_NAME" {
  config_path = "../DEPENDENCY_PATH"
  
  mock_outputs = {
    output_name = "mock-value"
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

inputs = {
  # Inputs here
}
```

### Новый Stack

```hcl
# {account}/{region}/{stack}/terragrunt.stack.hcl
locals {
  name = "STACK_NAME"
}

unit "UNIT_NAME" {
  source = "git::git@github.com:COMPANY/infrastructure-catalog.git//units/UNIT?ref=vX.Y.Z"
  path   = "UNIT_PATH"

  values = {
    name = local.name
    # Values here
  }
}
```

---

## Стратегия Тегов

### Обязательные теги (REQUIRED)

| Tag | Источник | Пример |
|-----|----------|--------|
| `Environment` | account.hcl | `production` |
| `ManagedBy` | root.hcl | `Terragrunt` |
| `Owner` | account.hcl | `platform-team` |
| `Team` | account.hcl | `infrastructure` |
| `CostCenter` | account.hcl | `CC-1001` |
| `Project` | region.hcl | `main-platform` |

### Автоматические теги (AUTO)

| Tag | Источник | Пример |
|-----|----------|--------|
| `TerragruntPath` | root.hcl | `prod/us-east-1/vpc` |
| `Repository` | root.hcl | `infrastructure-live` |

### Опциональные теги (в tags.yml)

```yaml
# {unit}/tags.yml
DataClassification: confidential
Compliance: SOC2
BackupPolicy: daily
```

---

## Паттерны Provider Generation

### Базовый AWS Provider

```hcl
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    provider "aws" {
      region = "${local.aws_region}"
      
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }
  EOF
}
```

### Multi-Region Provider

```hcl
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    provider "aws" {
      region = "${local.aws_region}"
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }

    provider "aws" {
      alias  = "us_east_1"
      region = "us-east-1"
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }

    provider "aws" {
      alias  = "eu_west_1"  
      region = "eu-west-1"
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }
  EOF
}
```

### Cross-Account Provider (Assume Role)

```hcl
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<-EOF
    provider "aws" {
      region = "${local.aws_region}"
      
      assume_role {
        role_arn     = "arn:aws:iam::${local.account_id}:role/TerragruntDeployRole"
        session_name = "terragrunt-${local.account_name}"
      }
      
      default_tags {
        tags = ${jsonencode(local.tags)}
      }
    }
  EOF
}
```

---

## Команды

### Ежедневные операции

```bash
# Форматирование
terragrunt hclfmt

# Валидация
terragrunt run --all validate

# Планирование
terragrunt run --all plan

# Применение
terragrunt run --all apply

# Уничтожение (ОСТОРОЖНО!)
terragrunt run --all destroy
```

### Stacks

```bash
# Генерация units
terragrunt stack generate

# План стека
terragrunt stack run plan

# Применение стека
terragrunt stack run apply

# Outputs стека
terragrunt stack output
```

### Дебаг

```bash
# Подробный лог
terragrunt plan --terragrunt-log-level debug

# Показать inputs
terragrunt render-json

# Граф зависимостей
terragrunt graph-dependencies

# Очистка кэша
terragrunt clean
```

---

## Чеклист для Code Review

### Структура
- [ ] Используется labeled include (`include "root" {}`)
- [ ] Версия модуля запинена (`?ref=v1.2.3`)
- [ ] account.hcl существует и заполнен
- [ ] region.hcl существует и заполнен

### Зависимости
- [ ] dependency блоки имеют mock_outputs
- [ ] mock_outputs_allowed_terraform_commands указан
- [ ] Нет циклических зависимостей

### Теги
- [ ] Обязательные теги присутствуют
- [ ] jsonencode используется для tags в generate блоках
- [ ] tags.yml используется для переопределений (если нужно)

### Безопасность
- [ ] Нет хардкода credentials
- [ ] Нет секретов в inputs
- [ ] deletion_protection включен для prod

### Naming
- [ ] Имена ресурсов следуют конвенции
- [ ] State key уникален (`path_relative_to_include()`)
- [ ] Bucket name уникален

---

## Антипаттерны (НЕ ДЕЛАТЬ)

```hcl
# ❌ Bare include
include {
  path = find_in_parent_folders()
}

# ✅ Labeled include
include "root" {
  path = find_in_parent_folders("root.hcl")
}
```

```hcl
# ❌ Unpinned version
terraform {
  source = "git::git@github.com:company/modules.git//vpc"
}

# ✅ Pinned version
terraform {
  source = "git::git@github.com:company/modules.git//vpc?ref=v1.2.0"
}
```

```hcl
# ❌ Hardcoded tags
default_tags {
  tags = {
    Environment = "prod"
  }
}

# ✅ Dynamic tags
default_tags {
  tags = ${jsonencode(local.tags)}
}
```

```hcl
# ❌ No mock outputs
dependency "vpc" {
  config_path = "../vpc"
}

# ✅ With mock outputs
dependency "vpc" {
  config_path = "../vpc"
  mock_outputs = {
    vpc_id = "vpc-mock"
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}
```

---

## Ссылки

- [Terragrunt Docs](https://terragrunt.gruntwork.io/docs/)
- [Gruntwork Live Example](https://github.com/gruntwork-io/terragrunt-infrastructure-live-stacks-example)
- [Gruntwork Catalog Example](https://github.com/gruntwork-io/terragrunt-infrastructure-catalog-example)
