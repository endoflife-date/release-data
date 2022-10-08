# release-data

Common Release Data for various projects in a consumable format. Current format is:

* `filename` matches the corresponding filename in the products/ directory in endoflife.date repository.
* Top-level keys are version strings.
* Non-stable versions are not included (nightly, beta, RC etc)
* Values are release dates in YYYY-MM-DD format
* Wherever possible, dates are as per the release-timezone.

## Guiding Principles

* Scripts that update this information should be stand-alone and simple.
* Code should not rely on existing data, and built it from scratch. (In case upstream information changes, we should reflect this change)
* It should be easy to add a new script in any language.
* Run everything on GitHub Actions.

## Currently Updated

As of Oct-2022, 83 of the 136 products tracked by endoflife.date have automatically tracked releases:

- almalinux
- alpinelinux
- amazon-linux
- angular
- ansible
- api-platform
- blender
- bootstrap
- composer
- consul
- couchbase-server
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
- gitlab
- godot
- go
- haproxy
- hashicorp-vault
- hbase
- ios
- ipados
- jquery
- kotlin
- kubernetes
- laravel
- linuxkernel
- log4j
- macos
- magento
- mariadb
- mediawiki
- mongodb
- mysql
- nextcloud
- nginx
- nix
- nodejs
- nomad
- opensearch
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
- rabbitmq
- react
- redis
- redmine
- rockylinux
- roundcube
- ruby
- ruby-on-rails
- solr
- spring-framework
- symfony
- tarantool
- terraform
- tomcat
- ubuntu
- unrealircd
- varnish
- vue
- wagtail
- watchos
- wordpress
- zabbix
- zookeeper
