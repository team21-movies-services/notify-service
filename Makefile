
BASE_DOCKER_COMPOSES = -f docker-compose.yml -f docker-compose.override.yml

LOCAL_DOCKER_COMPOSES = -f docker-compose.local.yml \
	-f docker-compose.override.yml

.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create_network:
	@docker network create notify-service-network 2>/dev/null || echo "notify-service-network is up-to-date"

# prod start
.PHONY: up
up: create_network ## up services
	@docker-compose $(BASE_DOCKER_COMPOSES) up -d

.PHONY: logs
logs: ## tail logs services
	@docker-compose $(BASE_DOCKER_COMPOSES) logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose $(BASE_DOCKER_COMPOSES) down

.PHONY: build
build: ## build services
	@docker-compose $(BASE_DOCKER_COMPOSES) build

.PHONY: restart
restart: down up ## restart services

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose $(BASE_DOCKER_COMPOSES) down --remove-orphans --volumes
# prod end

# local start
.PHONY: up-local
up-local: create_network ## up local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) up --build

.PHONY: up-local-d
up-local-d: create_network ## up all local services in daemon mode
	@docker-compose $(LOCAL_DOCKER_COMPOSES) up --build -d

.PHONY: down-local
down-local: ## down local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) down

.PHONY: build-local
build-local: ## build local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) build --force-rm

.PHONY: build-force-local
build-force-local: ## build force services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) build --no-cache

.PHONY: logs-local
logs-local: ## logs local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) logs -f $(serv)

.PHONY: restart-local
restart-local: down-local up-local ## logs local services

.PHONY: uninstall-local
uninstall-local: ## uninstall local services
	@docker-compose $(LOCAL_DOCKER_COMPOSES) down --remove-orphans --volumes
# local end
