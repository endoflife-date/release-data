# release-data

Common Release Data for various projects in a consumable format. Current format is:

* `filename` matches the corresponding filename in the products/ directory in endoflife.date
  repository.
* Top-level keys are version strings.
* Non-stable versions are not included (nightly, beta, RC etc)
* Values are release dates in YYYY-MM-DD format
* Wherever possible, dates are as per the release-timezone.

## Guiding Principles

* Scripts that update this information should be stand-alone and simple.
* Code should not rely on existing data, and built it from scratch. (In case upstream information
  changes, we should reflect this change)
* It should be easy to add a new script in any language.
* Run everything on GitHub Actions.

## Currently Updated

As of Oct-2022, 119 of the 186 products tracked by endoflife.date have automatically tracked
releases:

- almalinux
- alpinelinux
- amazon-linux
- angular
- ansible
- ansible-core
- antixlinux
- apache-airflow
- apache-cassandra
- apache-groovy
- apache-maven
- api-platform
- blender
- bootstrap
- cakephp
- clamav
- composer
- consul
- contao
- cos
- couchbase-server
- debian
- devuan
- django
- docker-engine
- dotnet
- drupal
- drush
- eks
- elasticsearch
- electron
- elixir
- emberjs
- eurolinux
- fedora
- ffmpeg
- filebeat
- gitlab
- gke
- go
- godot
- gradle
- grafana
- grails
- haproxy
- hashicorp-vault
- hbase
- ios
- ipados
- jenkins
- jhipster
- joomla
- jquery
- jreleaser
- keycloak
- kibana
- kotlin
- kubernetes
- laravel
- linuxkernel
- log4j
- logstash
- macos
- magento
- mariadb
- mediawiki
- micronaut
- mongodb
- moodle
- mxlinux
- mysql
- nextcloud
- nginx
- nix
- nodejs
- nomad
- numpy
- opensearch
- openssl
- openzfs
- oraclelinux
- pan-gp
- perl
- php
- postfix
- postgresql
- powershell
- python
- qt
- quarkus
- rabbitmq
- react
- redis
- redmine
- rockylinux
- roundcube
- ruby
- ruby-on-rails
- slackware
- solr
- sonarqube
- spring-boot
- spring-framework
- symfony
- tarantool
- telegraf
- terraform
- tomcat
- twig
- typo3
- ubuntu
- unrealircd
- varnish
- vue
- wagtail
- watchos
- wordpress
- zabbix
- zookeeper
