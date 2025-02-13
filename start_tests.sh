#!/usr/bin/env bash
# -*- coding: utf-8 -*-
export ENVIRONMENT=tests
export PYTHONDONTWRITEBYTECODE=1
template_tests_env=.env.template.tests
main_env_tests=src/.env.tests

if [[ ! -e ${main_env_tests} ]]
then
    cp "${template_tests_env}"  "${main_env_tests}"
fi

docker compose -f docker/docker-compose-tests.yml up -d --build
docker compose -f docker/docker-compose-tests.yml run --rm task-management-tests pytest -x
docker compose -f docker/docker-compose-tests.yml down
