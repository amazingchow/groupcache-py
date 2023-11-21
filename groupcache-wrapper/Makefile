
GROUPCACHE_GIT_HASH := $(shell cd ../groupcache && git rev-parse --short HEAD)

.PHONY: help
help: ### Display this help screen.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

ifeq ($(race), 1)
	BUILD_FLAGS := -race
endif

ifeq ($(gc_debug), 1)
	BUILD_FLAGS += -gcflags=all="-N -l"
endif

.PHONY: build
build: ## Build groupcache dynamic library.
	@(GOOS=linux GOARCH=amd64 go build -buildmode=c-shared -o ../libs/groupcache_$(GROUPCACHE_GIT_HASH).so main.go)
	@(ln -sf ../libs/groupcache_$(GROUPCACHE_GIT_HASH).h ../libs/groupcache.h)
	@(ln -sf ../libs/groupcache_$(GROUPCACHE_GIT_HASH).so ../libs/groupcache.so)

.PHONY: clean
clean: ## Clean all objects.
	@(rm -f ../libs/groupcache_$(GROUPCACHE_GIT_HASH).h)
	@(rm -f ../libs/groupcache_$(GROUPCACHE_GIT_HASH).so)
