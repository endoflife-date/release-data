> [!CAUTION]
> Data in this repository is primarily used by the [endoflife.date](https://endoflife.date) website.
> Format is not guaranteed to be stable, and may change at any time.
> Consider using the [End of Life Date API](https://endoflife.date/docs/api/v1/) which provides a stable interface.

# release-data

Common Release Data for various projects in a consistent and easy-to-parse format. The format is as follows:

* `filename` matches the corresponding filename in the
  [products/](https://github.com/endoflife-date/endoflife.date/tree/master/products) directory
  in the endoflife.date repository.
* Top-level keys are version strings.
* Non-stable versions are not included (nightly, beta, RC, etc.)
* Values are release dates in the YYYY-MM-DD format
* Wherever possible, dates are as per the release's timezone.

## Guiding Principles

* Scripts that update this information should be stand-alone and simple.
* Code should not rely on existing data; instead it should build the project's release data from scratch.
  (In case the upstream information changes, we should reflect that change.)
* It should be easy to add a new script in any language.
* Everything should run on GitHub Actions.

## Currently Updated

As of 2026-04-19, 387 of the 452 products tracked by endoflife.date have automatically tracked releases:

| Product | Permalink | Auto | Method(s) |
|---------|-----------|------|-----------|
| AdonisJS | [`/adonisjs`](https://endoflife.date/adonisjs) | ✔️ | git |
| Akeneo PIM | [`/akeneo-pim`](https://endoflife.date/akeneo-pim) | ✔️ | git, release_table |
| Alibaba ACK | [`/alibaba-ack`](https://endoflife.date/alibaba-ack) | ✔️ | release_table |
| Alibaba Dragonwell | [`/alibaba-dragonwell`](https://endoflife.date/alibaba-dragonwell) | ✔️ | git, release_table |
| AlmaLinux OS | [`/almalinux`](https://endoflife.date/almalinux) | ✔️ | distrowatch |
| Alpine Linux | [`/alpine-linux`](https://endoflife.date/alpine-linux) | ✔️ | git, release_table |
| Amazon Aurora PostgreSQL | [`/amazon-aurora-postgresql`](https://endoflife.date/amazon-aurora-postgresql) | ✔️ | rds, release_table |
| Amazon CDK | [`/amazon-cdk`](https://endoflife.date/amazon-cdk) | ✔️ | git |
| Amazon Corretto | [`/amazon-corretto`](https://endoflife.date/amazon-corretto) | ✔️ | github_releases |
| Amazon DocumentDB | [`/amazon-documentdb`](https://endoflife.date/amazon-documentdb) | ✔️ | release_table |
| Amazon EKS | [`/amazon-eks`](https://endoflife.date/amazon-eks) | ✔️ | amazon-eks, release_table |
| Amazon ElastiCache for Redis OSS | [`/amazon-elasticache-redis`](https://endoflife.date/amazon-elasticache-redis) | ✔️ | release_table |
| Amazon Glue | [`/amazon-glue`](https://endoflife.date/amazon-glue) | ❌ |  |
| Amazon Linux | [`/amazon-linux`](https://endoflife.date/amazon-linux) | ✔️ | docker_hub |
| Amazon MSK | [`/amazon-msk`](https://endoflife.date/amazon-msk) | ❌ |  |
| Amazon Neptune | [`/amazon-neptune`](https://endoflife.date/amazon-neptune) | ✔️ | amazon-neptune, release_table |
| Amazon OpenSearch | [`/amazon-opensearch`](https://endoflife.date/amazon-opensearch) | ❌ |  |
| Amazon RDS for MariaDB | [`/amazon-rds-mariadb`](https://endoflife.date/amazon-rds-mariadb) | ✔️ | rds, release_table |
| Amazon RDS for MySQL | [`/amazon-rds-mysql`](https://endoflife.date/amazon-rds-mysql) | ✔️ | rds, release_table |
| Amazon RDS for PostgreSQL | [`/amazon-rds-postgresql`](https://endoflife.date/amazon-rds-postgresql) | ✔️ | rds, release_table |
| Android OS | [`/android`](https://endoflife.date/android) | ❌ |  |
| Angular | [`/angular`](https://endoflife.date/angular) | ✔️ | git, release_table |
| AngularJS | [`/angularjs`](https://endoflife.date/angularjs) | ✔️ | npm |
| Ansible | [`/ansible`](https://endoflife.date/ansible) | ✔️ | pypi |
| Ansible-core | [`/ansible-core`](https://endoflife.date/ansible-core) | ✔️ | git, release_table |
| Anthropic Claude | [`/claude`](https://endoflife.date/claude) | ❌ |  |
| antiX Linux | [`/antix`](https://endoflife.date/antix) | ✔️ | distrowatch |
| Apache ActiveMQ Classic | [`/apache-activemq`](https://endoflife.date/apache-activemq) | ✔️ | git |
| Apache Airflow | [`/apache-airflow`](https://endoflife.date/apache-airflow) | ✔️ | pypi, release_table |
| Apache Ant | [`/ant`](https://endoflife.date/ant) | ✔️ | maven |
| Apache APISIX | [`/apache-apisix`](https://endoflife.date/apache-apisix) | ✔️ | github_releases |
| Apache Artemis | [`/apache-artemis`](https://endoflife.date/apache-artemis) | ✔️ | git |
| Apache Camel | [`/apache-camel`](https://endoflife.date/apache-camel) | ✔️ | git |
| Apache Cassandra | [`/apache-cassandra`](https://endoflife.date/apache-cassandra) | ✔️ | git |
| Apache CouchDB | [`/apache-couchdb`](https://endoflife.date/apache-couchdb) | ✔️ | git |
| Apache Flink | [`/apache-flink`](https://endoflife.date/apache-flink) | ✔️ | git |
| Apache Groovy | [`/apache-groovy`](https://endoflife.date/apache-groovy) | ✔️ | maven |
| Apache Hadoop | [`/apache-hadoop`](https://endoflife.date/apache-hadoop) | ✔️ | git |
| Apache Hop | [`/apache-hop`](https://endoflife.date/apache-hop) | ✔️ | maven |
| Apache HTTP Server | [`/apache-http-server`](https://endoflife.date/apache-http-server) | ✔️ | apache-http-server |
| Apache Kafka | [`/apache-kafka`](https://endoflife.date/apache-kafka) | ✔️ | git, release_table |
| Apache Lucene | [`/apache-lucene`](https://endoflife.date/apache-lucene) | ✔️ | maven |
| Apache Maven | [`/apache-maven`](https://endoflife.date/apache-maven) | ✔️ | github_releases |
| Apache NiFi | [`/apache-nifi`](https://endoflife.date/apache-nifi) | ✔️ | git |
| Apache Pulsar | [`/apache-pulsar`](https://endoflife.date/apache-pulsar) | ✔️ | github_releases, release_table |
| Apache Spark | [`/apache-spark`](https://endoflife.date/apache-spark) | ✔️ | git |
| Apache Struts | [`/apache-struts`](https://endoflife.date/apache-struts) | ✔️ | maven |
| Apache Subversion | [`/apache-subversion`](https://endoflife.date/apache-subversion) | ✔️ | apache-subversion |
| API Platform | [`/api-platform`](https://endoflife.date/api-platform) | ✔️ | git |
| Apple tvOS | [`/tvos`](https://endoflife.date/tvos) | ✔️ | apple |
| Apple Watch | [`/apple-watch`](https://endoflife.date/apple-watch) | ❌ |  |
| ArangoDB | [`/arangodb`](https://endoflife.date/arangodb) | ✔️ | git |
| Argo CD | [`/argo-cd`](https://endoflife.date/argo-cd) | ✔️ | git |
| Argo Workflows | [`/argo-workflows`](https://endoflife.date/argo-workflows) | ✔️ | git |
| Artifactory | [`/artifactory`](https://endoflife.date/artifactory) | ✔️ | version_table |
| authentik | [`/authentik`](https://endoflife.date/authentik) | ✔️ | git |
| AWS Lambda | [`/aws-lambda`](https://endoflife.date/aws-lambda) | ✔️ | aws-lambda, declare |
| Azul Zulu | [`/azul-zulu`](https://endoflife.date/azul-zulu) | ❌ |  |
| Azure Database for MySQL | [`/azure-database-for-mysql`](https://endoflife.date/azure-database-for-mysql) | ✔️ | release_table |
| Azure Database for PostgreSQL | [`/azure-database-for-postgresql`](https://endoflife.date/azure-database-for-postgresql) | ✔️ | release_table |
| Azure DevOps Server | [`/azure-devops-server`](https://endoflife.date/azure-devops-server) | ❌ |  |
| Azure Kubernetes Service | [`/azure-kubernetes-service`](https://endoflife.date/azure-kubernetes-service) | ✔️ | declare, release_table |
| Backdrop | [`/backdrop`](https://endoflife.date/backdrop) | ✔️ | github_releases |
| Bamboo | [`/bamboo`](https://endoflife.date/bamboo) | ✔️ | atlassian_eol, atlassian_versions |
| Bazel | [`/bazel`](https://endoflife.date/bazel) | ✔️ | git, release_table |
| Elastic Beats | [`/beats`](https://endoflife.date/beats) | ✔️ | git |
| Behat | [`/behat`](https://endoflife.date/behat) | ✔️ | git |
| Bellsoft Liberica JDK | [`/bellsoft-liberica`](https://endoflife.date/bellsoft-liberica) | ✔️ | github_releases |
| BIG-IP | [`/big-ip`](https://endoflife.date/big-ip) | ✔️ | release_table, version_table |
| BigBlueButton | [`/bigbluebutton`](https://endoflife.date/bigbluebutton) | ✔️ | github_releases |
| Bitbucket | [`/bitbucket`](https://endoflife.date/bitbucket) | ✔️ | atlassian_eol, atlassian_versions |
| Bitcoin Core | [`/bitcoin-core`](https://endoflife.date/bitcoin-core) | ✔️ | github_releases, release_table |
| Blender | [`/blender`](https://endoflife.date/blender) | ✔️ | git |
| Bootstrap | [`/bootstrap`](https://endoflife.date/bootstrap) | ✔️ | git |
| Hashicorp Boundary | [`/boundary`](https://endoflife.date/boundary) | ✔️ | github_releases |
| Bun | [`/bun`](https://endoflife.date/bun) | ✔️ | git |
| Cachet | [`/cachet`](https://endoflife.date/cachet) | ✔️ | git |
| Caddy | [`/caddy`](https://endoflife.date/caddy) | ✔️ | git |
| CakePHP | [`/cakephp`](https://endoflife.date/cakephp) | ✔️ | git |
| Calico | [`/calico`](https://endoflife.date/calico) | ✔️ | git |
| CentOS | [`/centos`](https://endoflife.date/centos) | ❌ |  |
| CentOS Stream | [`/centos-stream`](https://endoflife.date/centos-stream) | ❌ |  |
| Centreon | [`/centreon`](https://endoflife.date/centreon) | ✔️ | git, release_table |
| cert-manager | [`/cert-manager`](https://endoflife.date/cert-manager) | ✔️ | git |
| CFEngine | [`/cfengine`](https://endoflife.date/cfengine) | ✔️ | git |
| Chef Infra Client | [`/chef-infra-client`](https://endoflife.date/chef-infra-client) | ✔️ | chef-versions |
| Chef Infra Server | [`/chef-infra-server`](https://endoflife.date/chef-infra-server) | ✔️ | chef-versions |
| Chef InSpec | [`/chef-inspec`](https://endoflife.date/chef-inspec) | ✔️ | chef-versions |
| Chef Supermarket | [`/chef-supermarket`](https://endoflife.date/chef-supermarket) | ✔️ | chef-versions |
| Chef Workstation | [`/chef-workstation`](https://endoflife.date/chef-workstation) | ✔️ | chef-versions |
| Google Chrome | [`/chrome`](https://endoflife.date/chrome) | ✔️ | chrome-releases |
| Cilium | [`/cilium`](https://endoflife.date/cilium) | ✔️ | git |
| Cisco IOS XE | [`/cisco-ios-xe`](https://endoflife.date/cisco-ios-xe) | ❌ |  |
| Citrix Virtual Apps and Desktops | [`/citrix-vad`](https://endoflife.date/citrix-vad) | ✔️ | citrix-vad-rss |
| CKEditor | [`/ckeditor`](https://endoflife.date/ckeditor) | ❌ |  |
| ClamAV | [`/clamav`](https://endoflife.date/clamav) | ✔️ | git |
| Clear Linux | [`/clear-linux`](https://endoflife.date/clear-linux) | ❌ |  |
| ClickHouse | [`/clickhouse`](https://endoflife.date/clickhouse) | ✔️ | git |
| Cloud SQL Auth Proxy | [`/cloud-sql-auth-proxy`](https://endoflife.date/cloud-sql-auth-proxy) | ✔️ | git |
| cnspec | [`/cnspec`](https://endoflife.date/cnspec) | ✔️ | github_releases |
| CockroachDB | [`/cockroachdb`](https://endoflife.date/cockroachdb) | ✔️ | git, release_table |
| Coder | [`/coder`](https://endoflife.date/coder) | ✔️ | github_releases |
| Adobe ColdFusion | [`/coldfusion`](https://endoflife.date/coldfusion) | ✔️ | coldfusion, declare |
| Commvault | [`/commvault`](https://endoflife.date/commvault) | ✔️ | release_table |
| Composer | [`/composer`](https://endoflife.date/composer) | ✔️ | git |
| Concrete CMS | [`/concrete-cms`](https://endoflife.date/concrete-cms) | ✔️ | git |
| Confluence | [`/confluence`](https://endoflife.date/confluence) | ✔️ | atlassian_versions |
| Hashicorp Consul | [`/consul`](https://endoflife.date/consul) | ✔️ | git |
| containerd | [`/containerd`](https://endoflife.date/containerd) | ✔️ | git, release_table |
| Contao | [`/contao`](https://endoflife.date/contao) | ✔️ | git |
| Contour | [`/contour`](https://endoflife.date/contour) | ✔️ | git |
| Control-M | [`/controlm`](https://endoflife.date/controlm) | ❌ |  |
| Google Container-Optimized OS (COS) | [`/cos`](https://endoflife.date/cos) | ✔️ | cos |
| Couchbase Server | [`/couchbase-server`](https://endoflife.date/couchbase-server) | ✔️ | couchbase-server, declare, release_table |
| Craft CMS | [`/craft-cms`](https://endoflife.date/craft-cms) | ✔️ | git, release_table |
| dbt Core | [`/dbt-core`](https://endoflife.date/dbt-core) | ✔️ | git |
| DaoCloud Enterprise | [`/dce`](https://endoflife.date/dce) | ❌ |  |
| Debian | [`/debian`](https://endoflife.date/debian) | ✔️ | debian, release_table |
| Deno | [`/deno`](https://endoflife.date/deno) | ✔️ | git |
| Dependency-Track | [`/dependency-track`](https://endoflife.date/dependency-track) | ✔️ | git |
| Devuan | [`/devuan`](https://endoflife.date/devuan) | ✔️ | distrowatch |
| Discourse | [`/discourse`](https://endoflife.date/discourse) | ✔️ | git |
| Django | [`/django`](https://endoflife.date/django) | ✔️ | git, release_table |
| Docker Engine | [`/docker-engine`](https://endoflife.date/docker-engine) | ✔️ | git |
| Microsoft .NET | [`/dotnet`](https://endoflife.date/dotnet) | ✔️ | git, release_table |
| Microsoft .NET Framework | [`/dotnetfx`](https://endoflife.date/dotnetfx) | ✔️ | release_table |
| Dovecot | [`/dovecot`](https://endoflife.date/dovecot) | ✔️ | git |
| Drupal | [`/drupal`](https://endoflife.date/drupal) | ✔️ | git |
| Drush | [`/drush`](https://endoflife.date/drush) | ✔️ | git, release_table |
| DuckDB | [`/duckdb`](https://endoflife.date/duckdb) | ✔️ | github_releases |
| Eclipse Jetty | [`/eclipse-jetty`](https://endoflife.date/eclipse-jetty) | ✔️ | github_releases |
| Eclipse Temurin | [`/eclipse-temurin`](https://endoflife.date/eclipse-temurin) | ✔️ | github_releases, release_table |
| Elasticsearch | [`/elasticsearch`](https://endoflife.date/elasticsearch) | ✔️ | git |
| Electron | [`/electron`](https://endoflife.date/electron) | ✔️ | npm, release_table |
| Elixir | [`/elixir`](https://endoflife.date/elixir) | ✔️ | git |
| Ember | [`/emberjs`](https://endoflife.date/emberjs) | ✔️ | npm, release_table |
| Envoy | [`/envoy`](https://endoflife.date/envoy) | ✔️ | git, release_table |
| Erlang | [`/erlang`](https://endoflife.date/erlang) | ✔️ | git |
| ESLint | [`/eslint`](https://endoflife.date/eslint) | ✔️ | npm, release_table |
| etcd | [`/etcd`](https://endoflife.date/etcd) | ✔️ | git |
| EuroLinux | [`/eurolinux`](https://endoflife.date/eurolinux) | ✔️ | distrowatch |
| Exim | [`/exim`](https://endoflife.date/exim) | ✔️ | git |
| Express | [`/express`](https://endoflife.date/express) | ✔️ | git |
| Fairphone | [`/fairphone`](https://endoflife.date/fairphone) | ❌ |  |
| Fedora Linux | [`/fedora`](https://endoflife.date/fedora) | ✔️ | distrowatch |
| FFmpeg | [`/ffmpeg`](https://endoflife.date/ffmpeg) | ✔️ | git |
| FileMaker Platform | [`/filemaker`](https://endoflife.date/filemaker) | ✔️ | release_table |
| Firefox | [`/firefox`](https://endoflife.date/firefox) | ✔️ | firefox |
| Fluent Bit | [`/fluent-bit`](https://endoflife.date/fluent-bit) | ✔️ | github_releases |
| Flux | [`/flux`](https://endoflife.date/flux) | ✔️ | git |
| Font Awesome | [`/font-awesome`](https://endoflife.date/font-awesome) | ✔️ | git |
| Foreman | [`/foreman`](https://endoflife.date/foreman) | ✔️ | git |
| Forgejo | [`/forgejo`](https://endoflife.date/forgejo) | ✔️ | git, release_table |
| FortiOS | [`/fortios`](https://endoflife.date/fortios) | ❌ |  |
| FreeBSD | [`/freebsd`](https://endoflife.date/freebsd) | ✔️ | declare, freebsd-releases, release_table |
| Freedesktop SDK | [`/freedesktop-sdk`](https://endoflife.date/freedesktop-sdk) | ✔️ | git |
| Gatekeeper | [`/gatekeeper`](https://endoflife.date/gatekeeper) | ✔️ | git |
| Gerrit | [`/gerrit`](https://endoflife.date/gerrit) | ✔️ | git |
| Glasgow Haskell Compiler (GHC) | [`/ghc`](https://endoflife.date/ghc) | ✔️ | ghc-wiki, git |
| GitHub Actions Runner Images | [`/github-actions-runner-images`](https://endoflife.date/github-actions-runner-images) | ✔️ | release_table |
| GitLab | [`/gitlab`](https://endoflife.date/gitlab) | ✔️ | git |
| Gleam | [`/gleam`](https://endoflife.date/gleam) | ✔️ | git |
| Go | [`/go`](https://endoflife.date/go) | ✔️ | git |
| GoAccess | [`/goaccess`](https://endoflife.date/goaccess) | ✔️ | git |
| Godot | [`/godot`](https://endoflife.date/godot) | ✔️ | git |
| Google Kubernetes Engine | [`/google-kubernetes-engine`](https://endoflife.date/google-kubernetes-engine) | ✔️ | google-kubernetes-engine |
| Google Nexus | [`/google-nexus`](https://endoflife.date/google-nexus) | ❌ |  |
| Gorilla Toolkit | [`/gorilla`](https://endoflife.date/gorilla) | ❌ |  |
| GraalVM Community Edition | [`/graalvm-ce`](https://endoflife.date/graalvm-ce) | ✔️ | graalvm |
| Gradle | [`/gradle`](https://endoflife.date/gradle) | ✔️ | git |
| Grafana | [`/grafana`](https://endoflife.date/grafana) | ✔️ | git, release_table |
| Grafana Loki | [`/grafana-loki`](https://endoflife.date/grafana-loki) | ✔️ | git |
| Apache Grails Framework | [`/grails`](https://endoflife.date/grails) | ✔️ | git |
| Graylog | [`/graylog`](https://endoflife.date/graylog) | ✔️ | git, release_table |
| Greenlight | [`/greenlight`](https://endoflife.date/greenlight) | ✔️ | git |
| GrumPHP | [`/grumphp`](https://endoflife.date/grumphp) | ✔️ | git |
| Grunt | [`/grunt`](https://endoflife.date/grunt) | ✔️ | git |
| GStreamer | [`/gstreamer`](https://endoflife.date/gstreamer) | ✔️ | git |
| Guzzle | [`/guzzle`](https://endoflife.date/guzzle) | ✔️ | git |
| HAProxy | [`/haproxy`](https://endoflife.date/haproxy) | ✔️ | haproxy |
| HAProxy Ingress | [`/haproxy-ingress`](https://endoflife.date/haproxy-ingress) | ✔️ | git |
| Harbor | [`/harbor`](https://endoflife.date/harbor) | ✔️ | github_releases |
| Hashicorp Packer | [`/hashicorp-packer`](https://endoflife.date/hashicorp-packer) | ✔️ | git |
| Hashicorp Vault | [`/hashicorp-vault`](https://endoflife.date/hashicorp-vault) | ✔️ | git |
| Apache HBase | [`/hbase`](https://endoflife.date/hbase) | ✔️ | git |
| Hibernate ORM | [`/hibernate-orm`](https://endoflife.date/hibernate-orm) | ✔️ | git |
| IBM AIX | [`/ibm-aix`](https://endoflife.date/ibm-aix) | ✔️ | ibm-aix, release_table |
| IBM Db2 | [`/ibm-db2`](https://endoflife.date/ibm-db2) | ✔️ | ibm-product-lifecycle |
| IBM iSeries | [`/ibm-i`](https://endoflife.date/ibm-i) | ✔️ | release_table |
| IBM MQ | [`/ibm-mq`](https://endoflife.date/ibm-mq) | ✔️ | ibm-product-lifecycle |
| IBM Semeru Runtime | [`/ibm-semeru-runtime`](https://endoflife.date/ibm-semeru-runtime) | ✔️ | github_releases, release_table |
| Icinga | [`/icinga`](https://endoflife.date/icinga) | ✔️ | git |
| Icinga Web | [`/icinga-web`](https://endoflife.date/icinga-web) | ✔️ | git |
| IDL | [`/idl`](https://endoflife.date/idl) | ❌ |  |
| InfluxDB | [`/influxdb`](https://endoflife.date/influxdb) | ✔️ | git |
| Intel Processors | [`/intel-processors`](https://endoflife.date/intel-processors) | ❌ |  |
| Internet Explorer | [`/internet-explorer`](https://endoflife.date/internet-explorer) | ❌ |  |
| Ionic Framework | [`/ionic`](https://endoflife.date/ionic) | ✔️ | git, release_table |
| Apple iOS | [`/ios`](https://endoflife.date/ios) | ✔️ | apple |
| Apple iPad | [`/ipad`](https://endoflife.date/ipad) | ❌ |  |
| Apple iPadOS | [`/ipados`](https://endoflife.date/ipados) | ✔️ | apple |
| Apple iPhone | [`/iphone`](https://endoflife.date/iphone) | ❌ |  |
| ISC DHCP | [`/isc-dhcp`](https://endoflife.date/isc-dhcp) | ❌ |  |
| Istio | [`/istio`](https://endoflife.date/istio) | ✔️ | git, release_table |
| Jaeger | [`/jaeger`](https://endoflife.date/jaeger) | ✔️ | git |
| Jekyll | [`/jekyll`](https://endoflife.date/jekyll) | ✔️ | git |
| Jenkins | [`/jenkins`](https://endoflife.date/jenkins) | ✔️ | git |
| JHipster | [`/jhipster`](https://endoflife.date/jhipster) | ✔️ | npm |
| Jira Software | [`/jira-software`](https://endoflife.date/jira-software) | ✔️ | atlassian_eol, atlassian_versions |
| Joomla! | [`/joomla`](https://endoflife.date/joomla) | ✔️ | git |
| jQuery | [`/jquery`](https://endoflife.date/jquery) | ✔️ | git |
| jQuery UI | [`/jquery-ui`](https://endoflife.date/jquery-ui) | ✔️ | git |
| JReleaser | [`/jreleaser`](https://endoflife.date/jreleaser) | ✔️ | maven |
| Julia | [`/julia`](https://endoflife.date/julia) | ✔️ | git |
| Karpenter | [`/karpenter`](https://endoflife.date/karpenter) | ✔️ | github_releases |
| KDE Plasma | [`/kde-plasma`](https://endoflife.date/kde-plasma) | ✔️ | git |
| KEDA | [`/keda`](https://endoflife.date/keda) | ✔️ | git |
| Keycloak | [`/keycloak`](https://endoflife.date/keycloak) | ✔️ | github_releases |
| Kibana | [`/kibana`](https://endoflife.date/kibana) | ✔️ | git |
| Amazon Kindle | [`/kindle`](https://endoflife.date/kindle) | ❌ |  |
| Kirby | [`/kirby`](https://endoflife.date/kirby) | ✔️ | git |
| Knative | [`/knative`](https://endoflife.date/knative) | ✔️ | git, release_table |
| Kong Gateway | [`/kong-gateway`](https://endoflife.date/kong-gateway) | ✔️ | git |
| Kotlin | [`/kotlin`](https://endoflife.date/kotlin) | ✔️ | github_releases |
| Kubernetes | [`/kubernetes`](https://endoflife.date/kubernetes) | ✔️ | git |
| Kubernetes CSI Node Driver Registrar | [`/kubernetes-csi-node-driver-registrar`](https://endoflife.date/kubernetes-csi-node-driver-registrar) | ✔️ | git |
| Kubernetes Node Feature Discovery | [`/kubernetes-node-feature-discovery`](https://endoflife.date/kubernetes-node-feature-discovery) | ✔️ | github_releases |
| Kuma | [`/kuma`](https://endoflife.date/kuma) | ✔️ | git, github_releases, kuma |
| Kyverno | [`/kyverno`](https://endoflife.date/kyverno) | ✔️ | git |
| Laravel | [`/laravel`](https://endoflife.date/laravel) | ✔️ | git, release_table |
| LDAP Account Manager | [`/ldap-account-manager`](https://endoflife.date/ldap-account-manager) | ✔️ | git |
| LibreOffice | [`/libreoffice`](https://endoflife.date/libreoffice) | ✔️ | libreoffice |
| LineageOS | [`/lineageos`](https://endoflife.date/lineageos) | ❌ |  |
| Linux Kernel | [`/linux`](https://endoflife.date/linux) | ✔️ | github_tags |
| Linux Mint | [`/linuxmint`](https://endoflife.date/linuxmint) | ✔️ | release_table |
| Liquibase | [`/liquibase`](https://endoflife.date/liquibase) | ✔️ | maven |
| Apache Log4j | [`/log4j`](https://endoflife.date/log4j) | ✔️ | maven |
| Logstash | [`/logstash`](https://endoflife.date/logstash) | ✔️ | git |
| Longhorn | [`/longhorn`](https://endoflife.date/longhorn) | ✔️ | git |
| Looker | [`/looker`](https://endoflife.date/looker) | ✔️ | looker, release_table |
| Lua | [`/lua`](https://endoflife.date/lua) | ✔️ | lua |
| Apple macOS | [`/macos`](https://endoflife.date/macos) | ✔️ | apple |
| Mageia | [`/mageia`](https://endoflife.date/mageia) | ✔️ | distrowatch |
| Magento | [`/magento`](https://endoflife.date/magento) | ✔️ | git |
| Mandrel | [`/mandrel`](https://endoflife.date/mandrel) | ✔️ | github_releases |
| MariaDB | [`/mariadb`](https://endoflife.date/mariadb) | ✔️ | git, release_table |
| Mastodon | [`/mastodon`](https://endoflife.date/mastodon) | ✔️ | git |
| Matomo | [`/matomo`](https://endoflife.date/matomo) | ✔️ | git |
| Mattermost | [`/mattermost`](https://endoflife.date/mattermost) | ✔️ | github_releases, release_table |
| Mautic | [`/mautic`](https://endoflife.date/mautic) | ✔️ | git, release_table |
| MediaWiki | [`/mediawiki`](https://endoflife.date/mediawiki) | ✔️ | git, release_table |
| Meilisearch | [`/meilisearch`](https://endoflife.date/meilisearch) | ✔️ | github_releases |
| Memcached | [`/memcached`](https://endoflife.date/memcached) | ✔️ | git |
| MetalLB | [`/metallb`](https://endoflife.date/metallb) | ✔️ | git |
| Micronaut Framework | [`/micronaut`](https://endoflife.date/micronaut) | ✔️ | git |
| Microsoft Build of OpenJDK | [`/microsoft-build-of-openjdk`](https://endoflife.date/microsoft-build-of-openjdk) | ✔️ | git, release_table |
| MongoDB Server | [`/mongodb`](https://endoflife.date/mongodb) | ✔️ | git, release_table |
| Moodle | [`/moodle`](https://endoflife.date/moodle) | ✔️ | git, release_table |
| Motorola Mobility | [`/motorola-mobility`](https://endoflife.date/motorola-mobility) | ✔️ | motorola-security |
| Microsoft Exchange | [`/msexchange`](https://endoflife.date/msexchange) | ❌ |  |
| Microsoft SQL Server | [`/mssqlserver`](https://endoflife.date/mssqlserver) | ❌ |  |
| Mule Runtime | [`/mulesoft-runtime`](https://endoflife.date/mulesoft-runtime) | ✔️ | release_table |
| MX Linux | [`/mxlinux`](https://endoflife.date/mxlinux) | ✔️ | distrowatch |
| MySQL | [`/mysql`](https://endoflife.date/mysql) | ✔️ | git |
| Neo4j | [`/neo4j`](https://endoflife.date/neo4j) | ✔️ | declare, git, release_table |
| Neos | [`/neos`](https://endoflife.date/neos) | ✔️ | git |
| NetApp ONTAP | [`/netapp-ontap`](https://endoflife.date/netapp-ontap) | ❌ |  |
| NetBackup Appliance OS | [`/netbackup-appliance-os`](https://endoflife.date/netbackup-appliance-os) | ❌ |  |
| NetBSD | [`/netbsd`](https://endoflife.date/netbsd) | ✔️ | netbsd |
| Nextcloud | [`/nextcloud`](https://endoflife.date/nextcloud) | ✔️ | git, release_table |
| Next.js | [`/nextjs`](https://endoflife.date/nextjs) | ✔️ | npm |
| Nexus Repository | [`/nexus`](https://endoflife.date/nexus) | ✔️ | git, release_table |
| nginx | [`/nginx`](https://endoflife.date/nginx) | ✔️ | git |
| nix | [`/nix`](https://endoflife.date/nix) | ✔️ | git |
| NixOS | [`/nixos`](https://endoflife.date/nixos) | ❌ |  |
| Node.js | [`/nodejs`](https://endoflife.date/nodejs) | ✔️ | git |
| Nokia Mobile | [`/nokia`](https://endoflife.date/nokia) | ❌ |  |
| Nomad | [`/nomad`](https://endoflife.date/nomad) | ✔️ | git |
| Notepad++ | [`/notepad-plus-plus`](https://endoflife.date/notepad-plus-plus) | ✔️ | git |
| NumPy | [`/numpy`](https://endoflife.date/numpy) | ✔️ | pypi |
| Nutanix AOS | [`/nutanix-aos`](https://endoflife.date/nutanix-aos) | ✔️ | nutanix |
| Nutanix Files | [`/nutanix-files`](https://endoflife.date/nutanix-files) | ✔️ | nutanix |
| Nutanix Prism Central | [`/nutanix-prism`](https://endoflife.date/nutanix-prism) | ✔️ | nutanix |
| Nuxt | [`/nuxt`](https://endoflife.date/nuxt) | ✔️ | npm, release_table |
| NVIDIA Driver | [`/nvidia`](https://endoflife.date/nvidia) | ✔️ | declare, nvidia-releases |
| NVIDIA GPUs | [`/nvidia-gpu`](https://endoflife.date/nvidia-gpu) | ❌ |  |
| nvm | [`/nvm`](https://endoflife.date/nvm) | ✔️ | git |
| Microsoft Office | [`/office`](https://endoflife.date/office) | ❌ |  |
| Omnissa Horizon | [`/horizon`](https://endoflife.date/horizon) | ❌ |  |
| OnePlus | [`/oneplus`](https://endoflife.date/oneplus) | ❌ |  |
| Oniguruma | [`/oniguruma`](https://endoflife.date/oniguruma) | ✔️ | git |
| OpenBao | [`/openbao`](https://endoflife.date/openbao) | ✔️ | git |
| OpenBSD | [`/openbsd`](https://endoflife.date/openbsd) | ❌ |  |
| OpenJDK builds from Oracle | [`/openjdk-builds-from-oracle`](https://endoflife.date/openjdk-builds-from-oracle) | ❌ |  |
| OpenSearch | [`/opensearch`](https://endoflife.date/opensearch) | ✔️ | github_releases, release_table |
| OpenSSL | [`/openssl`](https://endoflife.date/openssl) | ✔️ | git, release_table |
| openSUSE | [`/opensuse`](https://endoflife.date/opensuse) | ❌ |  |
| OpenTofu | [`/opentofu`](https://endoflife.date/opentofu) | ✔️ | git |
| OpenVPN | [`/openvpn`](https://endoflife.date/openvpn) | ✔️ | git |
| OpenWrt | [`/openwrt`](https://endoflife.date/openwrt) | ✔️ | git |
| OpenZFS | [`/openzfs`](https://endoflife.date/openzfs) | ✔️ | github_releases |
| OPNsense | [`/opnsense`](https://endoflife.date/opnsense) | ✔️ | git |
| Oracle APEX | [`/oracle-apex`](https://endoflife.date/oracle-apex) | ✔️ | release_table |
| Oracle Database | [`/oracle-database`](https://endoflife.date/oracle-database) | ✔️ | release_table |
| Oracle GraalVM | [`/oracle-graalvm`](https://endoflife.date/oracle-graalvm) | ✔️ | graalvm, release_table |
| Oracle JDK | [`/oracle-jdk`](https://endoflife.date/oracle-jdk) | ✔️ | oracle-jdk, release_table |
| Oracle Linux | [`/oracle-linux`](https://endoflife.date/oracle-linux) | ✔️ | distrowatch |
| Oracle Solaris | [`/oracle-solaris`](https://endoflife.date/oracle-solaris) | ❌ |  |
| OTOBO | [`/otobo`](https://endoflife.date/otobo) | ✔️ | git |
| oVirt | [`/ovirt`](https://endoflife.date/ovirt) | ✔️ | git |
| Palo Alto Networks Cortex XDR agent | [`/cortex-xdr`](https://endoflife.date/cortex-xdr) | ✔️ | release_table |
| Palo Alto Networks GlobalProtect App | [`/pangp`](https://endoflife.date/pangp) | ✔️ | release_table |
| Palo Alto Networks PAN-OS | [`/panos`](https://endoflife.date/panos) | ✔️ | release_table |
| PCI-DSS | [`/pci-dss`](https://endoflife.date/pci-dss) | ❌ |  |
| Perl | [`/perl`](https://endoflife.date/perl) | ✔️ | git |
| Phoenix Framework | [`/phoenix-framework`](https://endoflife.date/phoenix-framework) | ✔️ | git |
| PHP | [`/php`](https://endoflife.date/php) | ✔️ | php |
| phpBB | [`/phpbb`](https://endoflife.date/phpbb) | ✔️ | git |
| phpMyAdmin | [`/phpmyadmin`](https://endoflife.date/phpmyadmin) | ✔️ | git |
| Pigeonhole | [`/pigeonhole`](https://endoflife.date/pigeonhole) | ✔️ | git |
| Google Pixel | [`/pixel`](https://endoflife.date/pixel) | ❌ |  |
| Google Pixel Watch | [`/pixel-watch`](https://endoflife.date/pixel-watch) | ❌ |  |
| Plesk | [`/plesk`](https://endoflife.date/plesk) | ✔️ | plesk |
| Plone | [`/plone`](https://endoflife.date/plone) | ✔️ | git, release_table |
| pnpm | [`/pnpm`](https://endoflife.date/pnpm) | ✔️ | npm |
| Podman | [`/podman`](https://endoflife.date/podman) | ✔️ | git |
| Pop!_OS | [`/pop-os`](https://endoflife.date/pop-os) | ❌ |  |
| Postfix | [`/postfix`](https://endoflife.date/postfix) | ✔️ | git |
| PostgreSQL | [`/postgresql`](https://endoflife.date/postgresql) | ✔️ | git, release_table |
| postmarketOS | [`/postmarketos`](https://endoflife.date/postmarketos) | ✔️ | distrowatch |
| Microsoft PowerShell | [`/powershell`](https://endoflife.date/powershell) | ✔️ | git, release_table |
| PrivateBin | [`/privatebin`](https://endoflife.date/privatebin) | ✔️ | git |
| ProFTPD | [`/proftpd`](https://endoflife.date/proftpd) | ✔️ | git |
| Prometheus | [`/prometheus`](https://endoflife.date/prometheus) | ✔️ | git, release_table |
| Protractor | [`/protractor`](https://endoflife.date/protractor) | ✔️ | npm |
| Proxmox VE | [`/proxmox-ve`](https://endoflife.date/proxmox-ve) | ✔️ | distrowatch, release_table |
| Puppet | [`/puppet`](https://endoflife.date/puppet) | ✔️ | git |
| Python | [`/python`](https://endoflife.date/python) | ✔️ | git, release_table |
| Qt | [`/qt`](https://endoflife.date/qt) | ✔️ | git |
| Quarkus | [`/quarkus-framework`](https://endoflife.date/quarkus-framework) | ✔️ | github_releases |
| Quasar | [`/quasar`](https://endoflife.date/quasar) | ✔️ | npm, release_table |
| RabbitMQ | [`/rabbitmq`](https://endoflife.date/rabbitmq) | ✔️ | git |
| Rancher | [`/rancher`](https://endoflife.date/rancher) | ✔️ | git, release_table |
| Raspberry Pi | [`/raspberry-pi`](https://endoflife.date/raspberry-pi) | ❌ |  |
| React | [`/react`](https://endoflife.date/react) | ✔️ | npm |
| React Native | [`/react-native`](https://endoflife.date/react-native) | ✔️ | npm |
| Red Hat Ansible Automation Platform | [`/red-hat-ansible-automation-platform`](https://endoflife.date/red-hat-ansible-automation-platform) | ❌ |  |
| Red Hat build of OpenJDK | [`/redhat-build-of-openjdk`](https://endoflife.date/redhat-build-of-openjdk) | ✔️ | redhat_lifecycles |
| Red Hat JBoss Enterprise Application Platform | [`/redhat-jboss-eap`](https://endoflife.date/redhat-jboss-eap) | ✔️ | red-hat-jboss-eap-7, red-hat-jboss-eap-8, redhat_lifecycles |
| Red Hat OpenShift | [`/red-hat-openshift`](https://endoflife.date/red-hat-openshift) | ✔️ | red-hat-openshift |
| Red Hat Satellite | [`/redhat-satellite`](https://endoflife.date/redhat-satellite) | ✔️ | version_table |
| Redis | [`/redis`](https://endoflife.date/redis) | ✔️ | git |
| Redmine | [`/redmine`](https://endoflife.date/redmine) | ✔️ | git |
| Renovate CLI | [`/renovate`](https://endoflife.date/renovate) | ✔️ | git |
| Red Hat Enterprise Linux | [`/rhel`](https://endoflife.date/rhel) | ✔️ | redhat_lifecycles |
| Robo | [`/robo`](https://endoflife.date/robo) | ✔️ | git, release_table |
| Rocket.Chat | [`/rocket-chat`](https://endoflife.date/rocket-chat) | ✔️ | git |
| Rocky Linux | [`/rocky-linux`](https://endoflife.date/rocky-linux) | ✔️ | release_table, rocky-linux |
| ROS | [`/ros`](https://endoflife.date/ros) | ❌ |  |
| ROS 2 | [`/ros-2`](https://endoflife.date/ros-2) | ✔️ | release_table |
| Roundcube Webmail | [`/roundcube`](https://endoflife.date/roundcube) | ✔️ | git |
| RouterOS | [`/routeros`](https://endoflife.date/routeros) | ✔️ | routeros-versions |
| rtpengine | [`/rtpengine`](https://endoflife.date/rtpengine) | ✔️ | git, rtpengine-releases |
| Ruby | [`/ruby`](https://endoflife.date/ruby) | ✔️ | git |
| Ruby on Rails | [`/rails`](https://endoflife.date/rails) | ✔️ | git |
| Rust | [`/rust`](https://endoflife.date/rust) | ✔️ | git |
| Salt | [`/salt`](https://endoflife.date/salt) | ✔️ | git, release_table |
| Samsung Galaxy Tab | [`/samsung-galaxy-tab`](https://endoflife.date/samsung-galaxy-tab) | ✔️ | samsung-security |
| Samsung Galaxy Watch | [`/samsung-galaxy-watch`](https://endoflife.date/samsung-galaxy-watch) | ❌ |  |
| Samsung Mobile | [`/samsung-mobile`](https://endoflife.date/samsung-mobile) | ✔️ | samsung-security |
| SapMachine | [`/sapmachine`](https://endoflife.date/sapmachine) | ✔️ | github_releases |
| Scala | [`/scala`](https://endoflife.date/scala) | ✔️ | github_releases |
| Microsoft SharePoint | [`/sharepoint`](https://endoflife.date/sharepoint) | ❌ |  |
| Shopware | [`/shopware`](https://endoflife.date/shopware) | ✔️ | git |
| Silverstripe CMS | [`/silverstripe`](https://endoflife.date/silverstripe) | ✔️ | git, silverstripe |
| Slackware Linux | [`/slackware`](https://endoflife.date/slackware) | ✔️ | distrowatch |
| SUSE Linux Enterprise Server | [`/sles`](https://endoflife.date/sles) | ✔️ | release_table |
| Stormshield Firmware | [`/sns-firmware`](https://endoflife.date/sns-firmware) | ✔️ | release_table |
| Stormshield Firewall | [`/sns-hardware`](https://endoflife.date/sns-hardware) | ✔️ | release_table |
| Stormshield Management Center | [`/sns-smc`](https://endoflife.date/sns-smc) | ✔️ | declare, release_table |
| Apache Solr | [`/solr`](https://endoflife.date/solr) | ✔️ | git |
| SonarQube Community Build | [`/sonarqube-community`](https://endoflife.date/sonarqube-community) | ✔️ | github_releases |
| SonarQube Server | [`/sonarqube-server`](https://endoflife.date/sonarqube-server) | ✔️ | discourse |
| Sony Xperia | [`/sony-xperia`](https://endoflife.date/sony-xperia) | ✔️ | release_table |
| Sourcegraph | [`/sourcegraph`](https://endoflife.date/sourcegraph) | ✔️ | git |
| Splunk | [`/splunk`](https://endoflife.date/splunk) | ✔️ | splunk |
| Spring Boot | [`/spring-boot`](https://endoflife.date/spring-boot) | ✔️ | git, release_table |
| Spring Framework | [`/spring-framework`](https://endoflife.date/spring-framework) | ✔️ | git, release_table |
| SQLite | [`/sqlite`](https://endoflife.date/sqlite) | ✔️ | git |
| Squid | [`/squid`](https://endoflife.date/squid) | ✔️ | git |
| Statamic | [`/statamic`](https://endoflife.date/statamic) | ✔️ | declare, git, release_table |
| SteamOS | [`/steamos`](https://endoflife.date/steamos) | ❌ |  |
| Microsoft Surface | [`/surface`](https://endoflife.date/surface) | ✔️ | release_table |
| SUSE Linux Micro | [`/suse-linux-micro`](https://endoflife.date/suse-linux-micro) | ✔️ | release_table |
| SUSE Multi-Linux Manager | [`/suse-manager`](https://endoflife.date/suse-manager) | ❌ |  |
| Svelte | [`/svelte`](https://endoflife.date/svelte) | ✔️ | npm |
| Symfony | [`/symfony`](https://endoflife.date/symfony) | ✔️ | git |
| Tails | [`/tails`](https://endoflife.date/tails) | ✔️ | git |
| Tailwind CSS | [`/tailwind-css`](https://endoflife.date/tailwind-css) | ✔️ | npm |
| Tarantool | [`/tarantool`](https://endoflife.date/tarantool) | ✔️ | git |
| tarteaucitron | [`/tarteaucitron`](https://endoflife.date/tarteaucitron) | ✔️ | git |
| Telegraf | [`/telegraf`](https://endoflife.date/telegraf) | ✔️ | git |
| Teleport | [`/teleport`](https://endoflife.date/teleport) | ✔️ | git |
| Hashicorp Terraform | [`/terraform`](https://endoflife.date/terraform) | ✔️ | git |
| Thumbor | [`/thumbor`](https://endoflife.date/thumbor) | ✔️ | git |
| TLS | [`/tls`](https://endoflife.date/tls) | ❌ |  |
| Apache Tomcat | [`/tomcat`](https://endoflife.date/tomcat) | ✔️ | git |
| Traefik | [`/traefik`](https://endoflife.date/traefik) | ✔️ | git, release_table |
| Twig | [`/twig`](https://endoflife.date/twig) | ✔️ | git |
| TYPO3 | [`/typo3`](https://endoflife.date/typo3) | ✔️ | typo3 |
| Ubuntu | [`/ubuntu`](https://endoflife.date/ubuntu) | ✔️ | distrowatch |
| Umbraco CMS | [`/umbraco`](https://endoflife.date/umbraco) | ✔️ | git, release_table |
| Unity | [`/unity`](https://endoflife.date/unity) | ✔️ | unity |
| UnrealIRCd | [`/unrealircd`](https://endoflife.date/unrealircd) | ✔️ | release_table, unrealircd |
| Valkey | [`/valkey`](https://endoflife.date/valkey) | ✔️ | git |
| Veeam Backup & Replication | [`/veeam-backup-and-replication`](https://endoflife.date/veeam-backup-and-replication) | ✔️ | veeam |
| Veeam Backup for Microsoft 365 | [`/veeam-backup-for-microsoft-365`](https://endoflife.date/veeam-backup-for-microsoft-365) | ✔️ | veeam |
| Veeam ONE | [`/veeam-one`](https://endoflife.date/veeam-one) | ✔️ | veeam |
| Vinyl Cache | [`/vinyl-cache`](https://endoflife.date/vinyl-cache) | ✔️ | release_table, version_table |
| VirtualBox | [`/virtualbox`](https://endoflife.date/virtualbox) | ✔️ | virtualbox-releases, virtualbox-versions |
| Apple visionOS | [`/visionos`](https://endoflife.date/visionos) | ✔️ | apple |
| Visual COBOL | [`/visual-cobol`](https://endoflife.date/visual-cobol) | ✔️ | release_table |
| Microsoft Visual Studio | [`/visual-studio`](https://endoflife.date/visual-studio) | ✔️ | visual-studio |
| Vitess | [`/vitess`](https://endoflife.date/vitess) | ✔️ | git |
| VMware Cloud Foundation | [`/vmware-cloud-foundation`](https://endoflife.date/vmware-cloud-foundation) | ❌ |  |
| VMware ESXi | [`/esxi`](https://endoflife.date/esxi) | ❌ |  |
| VMware Harbor Registry | [`/vmware-harbor-registry`](https://endoflife.date/vmware-harbor-registry) | ❌ |  |
| VMware Photon | [`/photon`](https://endoflife.date/photon) | ❌ |  |
| VMware Site Recovery Manager | [`/vmware-srm`](https://endoflife.date/vmware-srm) | ❌ |  |
| VMware vCenter Server | [`/vcenter`](https://endoflife.date/vcenter) | ❌ |  |
| Vue | [`/vue`](https://endoflife.date/vue) | ✔️ | npm |
| Vuetify | [`/vuetify`](https://endoflife.date/vuetify) | ✔️ | npm, release_table |
| Wagtail | [`/wagtail`](https://endoflife.date/wagtail) | ✔️ | pypi, release_table |
| Apple watchOS | [`/watchos`](https://endoflife.date/watchos) | ✔️ | apple |
| Weakforced | [`/weakforced`](https://endoflife.date/weakforced) | ✔️ | git |
| WeeChat | [`/weechat`](https://endoflife.date/weechat) | ✔️ | git |
| Microsoft Windows | [`/windows`](https://endoflife.date/windows) | ❌ |  |
| Microsoft Windows Embedded | [`/windows-embedded`](https://endoflife.date/windows-embedded) | ❌ |  |
| Microsoft Nano Server | [`/windows-nano-server`](https://endoflife.date/windows-nano-server) | ❌ |  |
| Microsoft Windows PowerShell | [`/windows-powershell`](https://endoflife.date/windows-powershell) | ❌ |  |
| Microsoft Windows Server | [`/windows-server`](https://endoflife.date/windows-server) | ❌ |  |
| Microsoft Windows Server Core | [`/windows-server-core`](https://endoflife.date/windows-server-core) | ❌ |  |
| Wireshark | [`/wireshark`](https://endoflife.date/wireshark) | ✔️ | git |
| WordPress | [`/wordpress`](https://endoflife.date/wordpress) | ✔️ | git |
| XCP-ng | [`/xcp-ng`](https://endoflife.date/xcp-ng) | ✔️ | git, release_table |
| Yarn | [`/yarn`](https://endoflife.date/yarn) | ✔️ | npm |
| Yocto Project | [`/yocto`](https://endoflife.date/yocto) | ✔️ | git |
| YouTrack | [`/youtrack`](https://endoflife.date/youtrack) | ✔️ | docker_hub |
| Zabbix | [`/zabbix`](https://endoflife.date/zabbix) | ✔️ | git |
| Zentyal | [`/zentyal`](https://endoflife.date/zentyal) | ✔️ | release_table |
| HPE Zerto | [`/zerto`](https://endoflife.date/zerto) | ✔️ | release_table |
| Apache ZooKeeper | [`/zookeeper`](https://endoflife.date/zookeeper) | ✔️ | maven |

This table has been generated by [report.py](/report.py).
