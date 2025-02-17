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

As of 2025-02-08, 282 of the 355 products tracked by endoflife.date have automatically tracked releases:

| Product                                       | Permalink                                                                                              | Auto | Method(s)                      |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------|------|--------------------------------|
| Akeneo PIM                                    | [`/akeneo-pim`](https://endoflife.date/akeneo-pim)                                                     | ✔️   | git, release_table             |
| Alibaba Dragonwell                            | [`/alibaba-dragonwell`](https://endoflife.date/alibaba-dragonwell)                                     | ✔️   | git, release_table             |
| AlmaLinux OS                                  | [`/almalinux`](https://endoflife.date/almalinux)                                                       | ✔️   | distrowatch                    |
| Alpine Linux                                  | [`/alpine`](https://endoflife.date/alpine)                                                             | ✔️   | git, release_table             |
| Amazon CDK                                    | [`/amazon-cdk`](https://endoflife.date/amazon-cdk)                                                     | ✔️   | git                            |
| Amazon Corretto                               | [`/amazon-corretto`](https://endoflife.date/amazon-corretto)                                           | ✔️   | github_releases, release_table |
| Amazon Glue                                   | [`/amazon-glue`](https://endoflife.date/amazon-glue)                                                   | ❌    |                                |
| Amazon Linux                                  | [`/amazon-linux`](https://endoflife.date/amazon-linux)                                                 | ✔️   | docker_hub                     |
| Amazon Neptune                                | [`/amazon-neptune`](https://endoflife.date/amazon-neptune)                                             | ✔️   | custom, release_table          |
| Amazon RDS for MariaDB                        | [`/amazon-rds-mariadb`](https://endoflife.date/amazon-rds-mariadb)                                     | ✔️   | custom, release_table          |
| Amazon RDS for MySQL                          | [`/amazon-rds-mysql`](https://endoflife.date/amazon-rds-mysql)                                         | ✔️   | custom, release_table          |
| Amazon RDS for PostgreSQL                     | [`/amazon-rds-postgresql`](https://endoflife.date/amazon-rds-postgresql)                               | ✔️   | custom, release_table          |
| Android OS                                    | [`/android`](https://endoflife.date/android)                                                           | ❌    |                                |
| Angular                                       | [`/angular`](https://endoflife.date/angular)                                                           | ✔️   | git, release_table             |
| AngularJS                                     | [`/angularjs`](https://endoflife.date/angularjs)                                                       | ✔️   | npm                            |
| Ansible-core                                  | [`/ansible-core`](https://endoflife.date/ansible-core)                                                 | ✔️   | git                            |
| Ansible                                       | [`/ansible`](https://endoflife.date/ansible)                                                           | ✔️   | pypi                           |
| antiX Linux                                   | [`/antix`](https://endoflife.date/antix)                                                               | ✔️   | distrowatch                    |
| Apache ActiveMQ                               | [`/apache-activemq`](https://endoflife.date/apache-activemq)                                           | ✔️   | git                            |
| Apache Airflow                                | [`/apache-airflow`](https://endoflife.date/apache-airflow)                                             | ✔️   | pypi, release_table            |
| Apache APISIX                                 | [`/apache-apisix`](https://endoflife.date/apache-apisix)                                               | ✔️   | github_releases                |
| Apache Camel                                  | [`/apache-camel`](https://endoflife.date/apache-camel)                                                 | ✔️   | maven                          |
| Apache Cassandra                              | [`/apache-cassandra`](https://endoflife.date/apache-cassandra)                                         | ✔️   | git                            |
| Apache CouchDB                                | [`/apache-couchdb`](https://endoflife.date/apache-couchdb)                                             | ✔️   | git                            |
| Apache Flink                                  | [`/apache-flink`](https://endoflife.date/apache-flink)                                                 | ✔️   | git                            |
| Apache Groovy                                 | [`/apache-groovy`](https://endoflife.date/apache-groovy)                                               | ✔️   | maven                          |
| Apache Hadoop                                 | [`/apache-hadoop`](https://endoflife.date/apache-hadoop)                                               | ✔️   | git                            |
| Apache Hop                                    | [`/apache-hop`](https://endoflife.date/apache-hop)                                                     | ✔️   | maven                          |
| Apache HTTP Server                            | [`/apache`](https://endoflife.date/apache)                                                             | ✔️   | custom                         |
| Apache Kafka                                  | [`/apache-kafka`](https://endoflife.date/apache-kafka)                                                 | ✔️   | git, release_table             |
| Apache Lucene                                 | [`/apache-lucene`](https://endoflife.date/apache-lucene)                                               | ✔️   | maven                          |
| Apache Maven                                  | [`/maven`](https://endoflife.date/maven)                                                               | ✔️   | maven                          |
| Apache Spark                                  | [`/apache-spark`](https://endoflife.date/apache-spark)                                                 | ✔️   | git                            |
| Apache Struts                                 | [`/apache-struts`](https://endoflife.date/apache-struts)                                               | ✔️   | maven                          |
| Apache Subversion                             | [`/subversion`](https://endoflife.date/subversion)                                                     | ✔️   | custom                         |
| API Platform                                  | [`/api-platform`](https://endoflife.date/api-platform)                                                 | ✔️   | git                            |
| Apple tvOS                                    | [`/tvos`](https://endoflife.date/tvos)                                                                 | ✔️   | apple                          |
| Apple Watch                                   | [`/apple-watch`](https://endoflife.date/apple-watch)                                                   | ❌    |                                |
| ArangoDB                                      | [`/arangodb`](https://endoflife.date/arangodb)                                                         | ✔️   | git                            |
| Argo CD                                       | [`/argo-cd`](https://endoflife.date/argo-cd)                                                           | ✔️   | git                            |
| Artifactory                                   | [`/artifactory`](https://endoflife.date/artifactory)                                                   | ✔️   | custom                         |
| AWS Lambda                                    | [`/aws-lambda`](https://endoflife.date/aws-lambda)                                                     | ✔️   | custom                         |
| Azul Zulu                                     | [`/azul-zulu`](https://endoflife.date/azul-zulu)                                                       | ❌    |                                |
| Azure DevOps Server                           | [`/azure-devops-server`](https://endoflife.date/azure-devops-server)                                   | ❌    |                                |
| Azure Kubernetes Service                      | [`/azure-kubernetes-service`](https://endoflife.date/azure-kubernetes-service)                         | ❌    |                                |
| Backdrop                                      | [`/backdrop`](https://endoflife.date/backdrop)                                                         | ❌    |                                |
| Bazel                                         | [`/bazel`](https://endoflife.date/bazel)                                                               | ✔️   | git, release_table             |
| Elastic Beats                                 | [`/beats`](https://endoflife.date/beats)                                                               | ✔️   | git                            |
| Bellsoft Liberica JDK                         | [`/bellsoft-liberica`](https://endoflife.date/bellsoft-liberica)                                       | ✔️   | github_releases                |
| BIG-IP                                        | [`/big-ip`](https://endoflife.date/big-ip)                                                             | ❌    |                                |
| Blender                                       | [`/blender`](https://endoflife.date/blender)                                                           | ✔️   | git                            |
| Bootstrap                                     | [`/bootstrap`](https://endoflife.date/bootstrap)                                                       | ✔️   | git                            |
| Bun                                           | [`/bun`](https://endoflife.date/bun)                                                                   | ✔️   | git                            |
| CakePHP                                       | [`/cakephp`](https://endoflife.date/cakephp)                                                           | ✔️   | git                            |
| Calico                                        | [`/calico`](https://endoflife.date/calico)                                                             | ✔️   | git                            |
| CentOS Stream                                 | [`/centos-stream`](https://endoflife.date/centos-stream)                                               | ❌    |                                |
| CentOS                                        | [`/centos`](https://endoflife.date/centos)                                                             | ❌    |                                |
| Centreon                                      | [`/centreon`](https://endoflife.date/centreon)                                                         | ✔️   | git, release_table             |
| cert-manager                                  | [`/cert-manager`](https://endoflife.date/cert-manager)                                                 | ✔️   | git                            |
| CFEngine                                      | [`/cfengine`](https://endoflife.date/cfengine)                                                         | ✔️   | git                            |
| Chef Infra Client                             | [`/chef-infra-client`](https://endoflife.date/chef-infra-client)                                       | ✔️   | custom                         |
| Chef Infra Server                             | [`/chef-infra-server`](https://endoflife.date/chef-infra-server)                                       | ✔️   | custom                         |
| Chef InSpec                                   | [`/chef-inspec`](https://endoflife.date/chef-inspec)                                                   | ✔️   | custom                         |
| Citrix Virtual Apps and Desktops              | [`/citrix-vad`](https://endoflife.date/citrix-vad)                                                     | ❌    |                                |
| CKEditor                                      | [`/ckeditor`](https://endoflife.date/ckeditor)                                                         | ❌    |                                |
| ClamAV                                        | [`/clamav`](https://endoflife.date/clamav)                                                             | ✔️   | git                            |
| cnspec                                        | [`/cnspec`](https://endoflife.date/cnspec)                                                             | ✔️   | github_releases                |
| CockroachDB                                   | [`/cockroachdb`](https://endoflife.date/cockroachdb)                                                   | ✔️   | git, release_table             |
| Coder                                         | [`/coder`](https://endoflife.date/coder)                                                               | ✔️   | git                            |
| Adobe ColdFusion                              | [`/coldfusion`](https://endoflife.date/coldfusion)                                                     | ❌    |                                |
| Composer                                      | [`/composer`](https://endoflife.date/composer)                                                         | ✔️   | git                            |
| Confluence                                    | [`/confluence`](https://endoflife.date/confluence)                                                     | ✔️   | atlassian_eol, custom          |
| Hashicorp Consul                              | [`/consul`](https://endoflife.date/consul)                                                             | ✔️   | git                            |
| containerd                                    | [`/containerd`](https://endoflife.date/containerd)                                                     | ✔️   | git, release_table             |
| Contao                                        | [`/contao`](https://endoflife.date/contao)                                                             | ✔️   | git                            |
| Contour                                       | [`/contour`](https://endoflife.date/contour)                                                           | ✔️   | git                            |
| Control-M                                     | [`/controlm`](https://endoflife.date/controlm)                                                         | ❌    |                                |
| Google Container-Optimized OS (COS)           | [`/cos`](https://endoflife.date/cos)                                                                   | ✔️   | custom                         |
| Couchbase Server                              | [`/couchbase-server`](https://endoflife.date/couchbase-server)                                         | ✔️   | custom, release_table          |
| Craft CMS                                     | [`/craft-cms`](https://endoflife.date/craft-cms)                                                       | ✔️   | git, release_table             |
| dbt Core                                      | [`/dbt-core`](https://endoflife.date/dbt-core)                                                         | ✔️   | git                            |
| DaoCloud Enterprise                           | [`/dce`](https://endoflife.date/dce)                                                                   | ❌    |                                |
| Debian                                        | [`/debian`](https://endoflife.date/debian)                                                             | ✔️   | custom, release_table          |
| Dependency-Track                              | [`/dependency-track`](https://endoflife.date/dependency-track)                                         | ✔️   | git                            |
| Devuan                                        | [`/devuan`](https://endoflife.date/devuan)                                                             | ✔️   | distrowatch                    |
| Django                                        | [`/django`](https://endoflife.date/django)                                                             | ✔️   | git, release_table             |
| Docker Engine                                 | [`/docker-engine`](https://endoflife.date/docker-engine)                                               | ✔️   | git                            |
| Microsoft .NET                                | [`/dotnet`](https://endoflife.date/dotnet)                                                             | ✔️   | git, release_table             |
| Microsoft .NET Framework                      | [`/dotnetfx`](https://endoflife.date/dotnetfx)                                                         | ✔️   | release_table                  |
| Drupal                                        | [`/drupal`](https://endoflife.date/drupal)                                                             | ✔️   | git                            |
| Drush                                         | [`/drush`](https://endoflife.date/drush)                                                               | ✔️   | git, release_table             |
| Eclipse Jetty                                 | [`/eclipse-jetty`](https://endoflife.date/eclipse-jetty)                                               | ✔️   | maven                          |
| Eclipse Temurin                               | [`/eclipse-temurin`](https://endoflife.date/eclipse-temurin)                                           | ✔️   | github_releases, release_table |
| Amazon EKS                                    | [`/amazon-eks`](https://endoflife.date/amazon-eks)                                                     | ✔️   | custom, release_table          |
| Elasticsearch                                 | [`/elasticsearch`](https://endoflife.date/elasticsearch)                                               | ✔️   | git                            |
| Electron                                      | [`/electron`](https://endoflife.date/electron)                                                         | ✔️   | npm, release_table             |
| Elixir                                        | [`/elixir`](https://endoflife.date/elixir)                                                             | ✔️   | git                            |
| Ember                                         | [`/emberjs`](https://endoflife.date/emberjs)                                                           | ✔️   | npm, release_table             |
| Envoy                                         | [`/envoy`](https://endoflife.date/envoy)                                                               | ✔️   | git, release_table             |
| Erlang                                        | [`/erlang`](https://endoflife.date/erlang)                                                             | ✔️   | git                            |
| ESLint                                        | [`/eslint`](https://endoflife.date/eslint)                                                             | ✔️   | npm, release_table             |
| etcd                                          | [`/etcd`](https://endoflife.date/etcd)                                                                 | ✔️   | git                            |
| EuroLinux                                     | [`/eurolinux`](https://endoflife.date/eurolinux)                                                       | ✔️   | distrowatch                    |
| Exim                                          | [`/exim`](https://endoflife.date/exim)                                                                 | ✔️   | git                            |
| Fairphone                                     | [`/fairphone`](https://endoflife.date/fairphone)                                                       | ❌    |                                |
| Fedora Linux                                  | [`/fedora`](https://endoflife.date/fedora)                                                             | ✔️   | distrowatch                    |
| FFmpeg                                        | [`/ffmpeg`](https://endoflife.date/ffmpeg)                                                             | ✔️   | git                            |
| FileMaker Platform                            | [`/filemaker`](https://endoflife.date/filemaker)                                                       | ✔️   | release_table                  |
| Firefox                                       | [`/firefox`](https://endoflife.date/firefox)                                                           | ✔️   | custom                         |
| Fluent Bit                                    | [`/fluent-bit`](https://endoflife.date/fluent-bit)                                                     | ✔️   | git                            |
| Flux                                          | [`/flux`](https://endoflife.date/flux)                                                                 | ✔️   | git                            |
| Forgejo                                       | [`/forgejo`](https://endoflife.date/forgejo)                                                           | ✔️   | git, release_table             |
| FortiOS                                       | [`/fortios`](https://endoflife.date/fortios)                                                           | ❌    |                                |
| FreeBSD                                       | [`/freebsd`](https://endoflife.date/freebsd)                                                           | ❌    |                                |
| Gerrit                                        | [`/gerrit`](https://endoflife.date/gerrit)                                                             | ✔️   | git                            |
| Glasgow Haskell Compiler (GHC)                | [`/ghc`](https://endoflife.date/ghc)                                                                   | ✔️   | git                            |
| GitLab                                        | [`/gitlab`](https://endoflife.date/gitlab)                                                             | ✔️   | git, release_table             |
| Google Kubernetes Engine                      | [`/google-kubernetes-engine`](https://endoflife.date/google-kubernetes-engine)                         | ✔️   | custom                         |
| Go                                            | [`/go`](https://endoflife.date/go)                                                                     | ✔️   | git                            |
| GoAccess                                      | [`/goaccess`](https://endoflife.date/goaccess)                                                         | ✔️   | git                            |
| Godot                                         | [`/godot`](https://endoflife.date/godot)                                                               | ✔️   | git                            |
| Google Nexus                                  | [`/google-nexus`](https://endoflife.date/google-nexus)                                                 | ❌    |                                |
| Gorilla Toolkit                               | [`/gorilla`](https://endoflife.date/gorilla)                                                           | ❌    |                                |
| GraalVM                                       | [`/graalvm`](https://endoflife.date/graalvm)                                                           | ✔️   | custom                         |
| Gradle                                        | [`/gradle`](https://endoflife.date/gradle)                                                             | ✔️   | git                            |
| Grafana Loki                                  | [`/grafana-loki`](https://endoflife.date/grafana-loki)                                                 | ✔️   | git                            |
| Grafana                                       | [`/grafana`](https://endoflife.date/grafana)                                                           | ✔️   | github_releases                |
| Grails Framework                              | [`/grails`](https://endoflife.date/grails)                                                             | ✔️   | git                            |
| Graylog                                       | [`/graylog`](https://endoflife.date/graylog)                                                           | ✔️   | git                            |
| GStreamer                                     | [`/gstreamer`](https://endoflife.date/gstreamer)                                                       | ✔️   | git                            |
| HAProxy                                       | [`/haproxy`](https://endoflife.date/haproxy)                                                           | ✔️   | custom                         |
| Harbor                                        | [`/harbor`](https://endoflife.date/harbor)                                                             | ✔️   | git                            |
| Hashicorp Packer                              | [`/hashicorp-packer`](https://endoflife.date/hashicorp-packer)                                         | ✔️   | git                            |
| Hashicorp Vault                               | [`/hashicorp-vault`](https://endoflife.date/hashicorp-vault)                                           | ✔️   | git                            |
| Apache HBase                                  | [`/hbase`](https://endoflife.date/hbase)                                                               | ✔️   | git                            |
| IBM AIX                                       | [`/ibm-aix`](https://endoflife.date/ibm-aix)                                                           | ✔️   | custom, release_table          |
| IBM iSeries                                   | [`/ibm-i`](https://endoflife.date/ibm-i)                                                               | ✔️   | release_table                  |
| IBM Semeru Runtime                            | [`/ibm-semeru-runtime`](https://endoflife.date/ibm-semeru-runtime)                                     | ✔️   | github_releases, release_table |
| Icinga Web                                    | [`/icinga-web`](https://endoflife.date/icinga-web)                                                     | ✔️   | git                            |
| Icinga                                        | [`/icinga`](https://endoflife.date/icinga)                                                             | ✔️   | git                            |
| Intel Processors                              | [`/intel-processors`](https://endoflife.date/intel-processors)                                         | ❌    |                                |
| Internet Explorer                             | [`/internet-explorer`](https://endoflife.date/internet-explorer)                                       | ❌    |                                |
| Ionic Framework                               | [`/ionic`](https://endoflife.date/ionic)                                                               | ✔️   | git, release_table             |
| Apple iOS                                     | [`/ios`](https://endoflife.date/ios)                                                                   | ✔️   | apple                          |
| Apple iPad                                    | [`/ipad`](https://endoflife.date/ipad)                                                                 | ❌    |                                |
| Apple iPadOS                                  | [`/ipados`](https://endoflife.date/ipados)                                                             | ✔️   | apple                          |
| Apple iPhone                                  | [`/iphone`](https://endoflife.date/iphone)                                                             | ❌    |                                |
| ISC DHCP                                      | [`/isc-dhcp`](https://endoflife.date/isc-dhcp)                                                         | ❌    |                                |
| Istio                                         | [`/istio`](https://endoflife.date/istio)                                                               | ✔️   | git, release_table             |
| Jekyll                                        | [`/jekyll`](https://endoflife.date/jekyll)                                                             | ✔️   | git                            |
| Jenkins                                       | [`/jenkins`](https://endoflife.date/jenkins)                                                           | ✔️   | git                            |
| JHipster                                      | [`/jhipster`](https://endoflife.date/jhipster)                                                         | ✔️   | npm                            |
| Jira Software                                 | [`/jira-software`](https://endoflife.date/jira-software)                                               | ✔️   | atlassian_eol, custom          |
| Joomla!                                       | [`/joomla`](https://endoflife.date/joomla)                                                             | ✔️   | git                            |
| jQuery UI                                     | [`/jquery-ui`](https://endoflife.date/jquery-ui)                                                       | ✔️   | git                            |
| jQuery                                        | [`/jquery`](https://endoflife.date/jquery)                                                             | ✔️   | git                            |
| JReleaser                                     | [`/jreleaser`](https://endoflife.date/jreleaser)                                                       | ✔️   | maven                          |
| Julia                                         | [`/julia`](https://endoflife.date/julia)                                                               | ✔️   | git                            |
| KDE Plasma                                    | [`/kde-plasma`](https://endoflife.date/kde-plasma)                                                     | ✔️   | git                            |
| KEDA                                          | [`/keda`](https://endoflife.date/keda)                                                                 | ✔️   | git                            |
| Keycloak                                      | [`/keycloak`](https://endoflife.date/keycloak)                                                         | ✔️   | github_releases                |
| Kibana                                        | [`/kibana`](https://endoflife.date/kibana)                                                             | ✔️   | git                            |
| Amazon Kindle                                 | [`/kindle`](https://endoflife.date/kindle)                                                             | ❌    |                                |
| Kirby                                         | [`/kirby`](https://endoflife.date/kirby)                                                               | ✔️   | git                            |
| Kong Gateway                                  | [`/kong-gateway`](https://endoflife.date/kong-gateway)                                                 | ✔️   | git                            |
| Kotlin                                        | [`/kotlin`](https://endoflife.date/kotlin)                                                             | ✔️   | npm                            |
| Kubernetes CSI Node Driver Registrar          | [`/kubernetes-csi-node-driver-registrar`](https://endoflife.date/kubernetes-csi-node-driver-registrar) | ✔️   | git                            |
| Kubernetes                                    | [`/kubernetes`](https://endoflife.date/kubernetes)                                                     | ✔️   | git                            |
| Kuma                                          | [`/kuma`](https://endoflife.date/kuma)                                                                 | ✔️   | git                            |
| Kyverno                                       | [`/kyverno`](https://endoflife.date/kyverno)                                                           | ✔️   | git                            |
| Laravel                                       | [`/laravel`](https://endoflife.date/laravel)                                                           | ✔️   | git, release_table             |
| LibreOffice                                   | [`/libreoffice`](https://endoflife.date/libreoffice)                                                   | ✔️   | custom                         |
| LineageOS                                     | [`/lineageos`](https://endoflife.date/lineageos)                                                       | ❌    |                                |
| Linux Kernel                                  | [`/linux`](https://endoflife.date/linux)                                                               | ✔️   | cgit                           |
| Linux Mint                                    | [`/linuxmint`](https://endoflife.date/linuxmint)                                                       | ✔️   | release_table                  |
| Apache Log4j                                  | [`/log4j`](https://endoflife.date/log4j)                                                               | ✔️   | maven                          |
| Logstash                                      | [`/logstash`](https://endoflife.date/logstash)                                                         | ✔️   | git                            |
| Looker                                        | [`/looker`](https://endoflife.date/looker)                                                             | ✔️   | custom                         |
| Lua                                           | [`/lua`](https://endoflife.date/lua)                                                                   | ✔️   | custom                         |
| Apple macOS                                   | [`/macos`](https://endoflife.date/macos)                                                               | ✔️   | apple                          |
| Mageia                                        | [`/mageia`](https://endoflife.date/mageia)                                                             | ✔️   | distrowatch                    |
| Magento                                       | [`/magento`](https://endoflife.date/magento)                                                           | ✔️   | git                            |
| Mandrel                                       | [`/mandrel`](https://endoflife.date/mandrel)                                                           | ✔️   | github_releases                |
| MariaDB                                       | [`/mariadb`](https://endoflife.date/mariadb)                                                           | ✔️   | git, release_table             |
| Mastodon                                      | [`/mastodon`](https://endoflife.date/mastodon)                                                         | ✔️   | git                            |
| Matomo                                        | [`/matomo`](https://endoflife.date/matomo)                                                             | ✔️   | git                            |
| Mattermost                                    | [`/mattermost`](https://endoflife.date/mattermost)                                                     | ✔️   | github_releases, release_table |
| Mautic                                        | [`/mautic`](https://endoflife.date/mautic)                                                             | ✔️   | git, release_table             |
| MediaWiki                                     | [`/mediawiki`](https://endoflife.date/mediawiki)                                                       | ✔️   | git, release_table             |
| Meilisearch                                   | [`/meilisearch`](https://endoflife.date/meilisearch)                                                   | ✔️   | github_releases                |
| Memcached                                     | [`/memcached`](https://endoflife.date/memcached)                                                       | ✔️   | git                            |
| Micronaut Framework                           | [`/micronaut`](https://endoflife.date/micronaut)                                                       | ✔️   | git                            |
| Microsoft Build of OpenJDK                    | [`/microsoft-build-of-openjdk`](https://endoflife.date/microsoft-build-of-openjdk)                     | ✔️   | git, release_table             |
| MongoDB Server                                | [`/mongodb`](https://endoflife.date/mongodb)                                                           | ✔️   | git, release_table             |
| Moodle                                        | [`/moodle`](https://endoflife.date/moodle)                                                             | ✔️   | git, release_table             |
| Motorola Mobility                             | [`/motorola-mobility`](https://endoflife.date/motorola-mobility)                                       | ❌    |                                |
| Microsoft Exchange                            | [`/msexchange`](https://endoflife.date/msexchange)                                                     | ❌    |                                |
| Microsoft SharePoint                          | [`/sharepoint`](https://endoflife.date/sharepoint)                                                     | ❌    |                                |
| Microsoft SQL Server                          | [`/mssqlserver`](https://endoflife.date/mssqlserver)                                                   | ❌    |                                |
| Mule Runtime                                  | [`/mulesoft-runtime`](https://endoflife.date/mulesoft-runtime)                                         | ❌    |                                |
| MX Linux                                      | [`/mxlinux`](https://endoflife.date/mxlinux)                                                           | ✔️   | distrowatch                    |
| MySQL                                         | [`/mysql`](https://endoflife.date/mysql)                                                               | ✔️   | git                            |
| Neo4j                                         | [`/neo4j`](https://endoflife.date/neo4j)                                                               | ✔️   | git, release_table             |
| Neos                                          | [`/neos`](https://endoflife.date/neos)                                                                 | ✔️   | git                            |
| NetBSD                                        | [`/netbsd`](https://endoflife.date/netbsd)                                                             | ✔️   | custom                         |
| Nextcloud                                     | [`/nextcloud`](https://endoflife.date/nextcloud)                                                       | ✔️   | git, release_table             |
| Next.js                                       | [`/nextjs`](https://endoflife.date/nextjs)                                                             | ✔️   | npm                            |
| Nexus Repository                              | [`/nexus`](https://endoflife.date/nexus)                                                               | ✔️   | git, release_table             |
| nginx                                         | [`/nginx`](https://endoflife.date/nginx)                                                               | ✔️   | git                            |
| nix                                           | [`/nix`](https://endoflife.date/nix)                                                                   | ✔️   | git                            |
| NixOS                                         | [`/nixos`](https://endoflife.date/nixos)                                                               | ❌    |                                |
| Kubernetes Node Feature Discovery             | [`/kubernetes-node-feature-discovery`](https://endoflife.date/kubernetes-node-feature-discovery)       | ✔️   | github_releases                |
| Node.js                                       | [`/nodejs`](https://endoflife.date/nodejs)                                                             | ✔️   | git                            |
| Nokia Mobile                                  | [`/nokia`](https://endoflife.date/nokia)                                                               | ❌    |                                |
| Nomad                                         | [`/nomad`](https://endoflife.date/nomad)                                                               | ✔️   | git                            |
| NumPy                                         | [`/numpy`](https://endoflife.date/numpy)                                                               | ✔️   | pypi                           |
| Nutanix AOS                                   | [`/nutanix-aos`](https://endoflife.date/nutanix-aos)                                                   | ✔️   | nutanix                        |
| Nutanix Files                                 | [`/nutanix-files`](https://endoflife.date/nutanix-files)                                               | ✔️   | nutanix                        |
| Nutanix Prism Central                         | [`/nutanix-prism`](https://endoflife.date/nutanix-prism)                                               | ✔️   | nutanix                        |
| Nuxt                                          | [`/nuxt`](https://endoflife.date/nuxt)                                                                 | ✔️   | npm, release_table             |
| NVIDIA Driver                                 | [`/nvidia`](https://endoflife.date/nvidia)                                                             | ❌    |                                |
| NVIDIA GPUs                                   | [`/nvidia-gpu`](https://endoflife.date/nvidia-gpu)                                                     | ❌    |                                |
| nvm                                           | [`/nvm`](https://endoflife.date/nvm)                                                                   | ✔️   | git                            |
| Microsoft Office                              | [`/office`](https://endoflife.date/office)                                                             | ❌    |                                |
| Omnissa Horizon                               | [`/horizon`](https://endoflife.date/horizon)                                                           | ❌    |                                |
| OnePlus                                       | [`/oneplus`](https://endoflife.date/oneplus)                                                           | ❌    |                                |
| OpenBSD                                       | [`/openbsd`](https://endoflife.date/openbsd)                                                           | ❌    |                                |
| OpenJDK builds from Oracle                    | [`/openjdk-builds-from-oracle`](https://endoflife.date/openjdk-builds-from-oracle)                     | ❌    |                                |
| OpenSearch                                    | [`/opensearch`](https://endoflife.date/opensearch)                                                     | ✔️   | git, release_table             |
| OpenSSL                                       | [`/openssl`](https://endoflife.date/openssl)                                                           | ✔️   | git                            |
| openSUSE                                      | [`/opensuse`](https://endoflife.date/opensuse)                                                         | ❌    |                                |
| OpenTofu                                      | [`/opentofu`](https://endoflife.date/opentofu)                                                         | ✔️   | git                            |
| OpenVPN                                       | [`/openvpn`](https://endoflife.date/openvpn)                                                           | ✔️   | git                            |
| OpenWrt                                       | [`/openwrt`](https://endoflife.date/openwrt)                                                           | ✔️   | git                            |
| OpenZFS                                       | [`/openzfs`](https://endoflife.date/openzfs)                                                           | ✔️   | git                            |
| OPNsense                                      | [`/opnsense`](https://endoflife.date/opnsense)                                                         | ✔️   | git                            |
| Oracle APEX                                   | [`/oracle-apex`](https://endoflife.date/oracle-apex)                                                   | ✔️   | release_table                  |
| Oracle Database                               | [`/oracle-database`](https://endoflife.date/oracle-database)                                           | ✔️   | release_table                  |
| Oracle JDK                                    | [`/oracle-jdk`](https://endoflife.date/oracle-jdk)                                                     | ✔️   | custom, release_table          |
| Oracle Linux                                  | [`/oracle-linux`](https://endoflife.date/oracle-linux)                                                 | ✔️   | distrowatch                    |
| Oracle Solaris                                | [`/oracle-solaris`](https://endoflife.date/oracle-solaris)                                             | ❌    |                                |
| oVirt                                         | [`/ovirt`](https://endoflife.date/ovirt)                                                               | ✔️   | git                            |
| Palo Alto Networks Cortex XDR agent           | [`/cortex-xdr`](https://endoflife.date/cortex-xdr)                                                     | ✔️   | release_table                  |
| Palo Alto Networks GlobalProtect App          | [`/pangp`](https://endoflife.date/pangp)                                                               | ✔️   | release_table                  |
| Palo Alto Networks PAN-OS                     | [`/panos`](https://endoflife.date/panos)                                                               | ✔️   | release_table                  |
| PCI-DSS                                       | [`/pci-dss`](https://endoflife.date/pci-dss)                                                           | ❌    |                                |
| Perl                                          | [`/perl`](https://endoflife.date/perl)                                                                 | ✔️   | git                            |
| PHP                                           | [`/php`](https://endoflife.date/php)                                                                   | ✔️   | custom                         |
| phpBB                                         | [`/phpbb`](https://endoflife.date/phpbb)                                                               | ✔️   | git                            |
| phpMyAdmin                                    | [`/phpmyadmin`](https://endoflife.date/phpmyadmin)                                                     | ✔️   | git                            |
| Google Pixel Watch                            | [`/pixel-watch`](https://endoflife.date/pixel-watch)                                                   | ❌    |                                |
| Google Pixel                                  | [`/pixel`](https://endoflife.date/pixel)                                                               | ❌    |                                |
| Plesk                                         | [`/plesk`](https://endoflife.date/plesk)                                                               | ✔️   | custom                         |
| pnpm                                          | [`/pnpm`](https://endoflife.date/pnpm)                                                                 | ✔️   | npm                            |
| Podman                                        | [`/podman`](https://endoflife.date/podman)                                                             | ✔️   | git                            |
| Pop!_OS                                       | [`/pop-os`](https://endoflife.date/pop-os)                                                             | ❌    |                                |
| Postfix                                       | [`/postfix`](https://endoflife.date/postfix)                                                           | ✔️   | git                            |
| PostgreSQL                                    | [`/postgresql`](https://endoflife.date/postgresql)                                                     | ✔️   | git, release_table             |
| postmarketOS                                  | [`/postmarketos`](https://endoflife.date/postmarketos)                                                 | ✔️   | distrowatch                    |
| Microsoft PowerShell                          | [`/powershell`](https://endoflife.date/powershell)                                                     | ✔️   | git, release_table             |
| PrivateBin                                    | [`/privatebin`](https://endoflife.date/privatebin)                                                     | ✔️   | git                            |
| Prometheus                                    | [`/prometheus`](https://endoflife.date/prometheus)                                                     | ✔️   | git, release_table             |
| Protractor                                    | [`/protractor`](https://endoflife.date/protractor)                                                     | ✔️   | npm                            |
| Proxmox VE                                    | [`/proxmox-ve`](https://endoflife.date/proxmox-ve)                                                     | ✔️   | distrowatch, release_table     |
| Puppet                                        | [`/puppet`](https://endoflife.date/puppet)                                                             | ✔️   | git                            |
| Python                                        | [`/python`](https://endoflife.date/python)                                                             | ✔️   | git, release_table             |
| Qt                                            | [`/qt`](https://endoflife.date/qt)                                                                     | ✔️   | git                            |
| Quarkus                                       | [`/quarkus-framework`](https://endoflife.date/quarkus-framework)                                       | ✔️   | github_releases                |
| Quasar                                        | [`/quasar`](https://endoflife.date/quasar)                                                             | ✔️   | npm, release_table             |
| RabbitMQ                                      | [`/rabbitmq`](https://endoflife.date/rabbitmq)                                                         | ✔️   | git                            |
| Rancher                                       | [`/rancher`](https://endoflife.date/rancher)                                                           | ✔️   | git                            |
| Raspberry Pi                                  | [`/raspberry-pi`](https://endoflife.date/raspberry-pi)                                                 | ❌    |                                |
| React Native                                  | [`/react-native`](https://endoflife.date/react-native)                                                 | ✔️   | npm                            |
| React                                         | [`/react`](https://endoflife.date/react)                                                               | ✔️   | npm                            |
| Netgear ReadyNAS                              | [`/readynas`](https://endoflife.date/readynas)                                                         | ❌    |                                |
| Red Hat build of OpenJDK                      | [`/redhat-build-of-openjdk`](https://endoflife.date/redhat-build-of-openjdk)                           | ❌    |                                |
| Red Hat JBoss Enterprise Application Platform | [`/redhat-jboss-eap`](https://endoflife.date/redhat-jboss-eap)                                         | ❌    |                                |
| Red Hat OpenShift                             | [`/red-hat-openshift`](https://endoflife.date/red-hat-openshift)                                       | ✔️   | custom                         |
| Red Hat Satellite                             | [`/redhat-satellite`](https://endoflife.date/redhat-satellite)                                         | ✔️   | custom                         |
| Redis                                         | [`/redis`](https://endoflife.date/redis)                                                               | ✔️   | git                            |
| Redmine                                       | [`/redmine`](https://endoflife.date/redmine)                                                           | ✔️   | git                            |
| Red Hat Enterprise Linux                      | [`/rhel`](https://endoflife.date/rhel)                                                                 | ❌    |                                |
| Robo                                          | [`/robo`](https://endoflife.date/robo)                                                                 | ✔️   | git, release_table             |
| Rocket.Chat                                   | [`/rocket-chat`](https://endoflife.date/rocket-chat)                                                   | ✔️   | git                            |
| Rocky Linux                                   | [`/rocky-linux`](https://endoflife.date/rocky-linux)                                                   | ✔️   | custom, release_table          |
| ROS 2                                         | [`/ros-2`](https://endoflife.date/ros-2)                                                               | ❌    |                                |
| ROS                                           | [`/ros`](https://endoflife.date/ros)                                                                   | ❌    |                                |
| Roundcube Webmail                             | [`/roundcube`](https://endoflife.date/roundcube)                                                       | ✔️   | git                            |
| Ruby on Rails                                 | [`/rails`](https://endoflife.date/rails)                                                               | ✔️   | git                            |
| Ruby                                          | [`/ruby`](https://endoflife.date/ruby)                                                                 | ✔️   | git                            |
| Rust                                          | [`/rust`](https://endoflife.date/rust)                                                                 | ✔️   | git                            |
| Salt                                          | [`/salt`](https://endoflife.date/salt)                                                                 | ✔️   | git, release_table             |
| Samsung Mobile                                | [`/samsung-mobile`](https://endoflife.date/samsung-mobile)                                             | ❌    |                                |
| SapMachine                                    | [`/sapmachine`](https://endoflife.date/sapmachine)                                                     | ✔️   | github_releases                |
| Scala                                         | [`/scala`](https://endoflife.date/scala)                                                               | ✔️   | github_releases                |
| Shopware                                      | [`/shopware`](https://endoflife.date/shopware)                                                         | ✔️   | git                            |
| Silverstripe CMS                              | [`/silverstripe`](https://endoflife.date/silverstripe)                                                 | ✔️   | git, release_table             |
| Slackware Linux                               | [`/slackware`](https://endoflife.date/slackware)                                                       | ✔️   | distrowatch                    |
| SUSE Linux Enterprise Server                  | [`/sles`](https://endoflife.date/sles)                                                                 | ❌    |                                |
| Apache Solr                                   | [`/solr`](https://endoflife.date/solr)                                                                 | ✔️   | git                            |
| SonarQube                                     | [`/sonar`](https://endoflife.date/sonar)                                                               | ✔️   | git                            |
| Sourcegraph                                   | [`/sourcegraph`](https://endoflife.date/sourcegraph)                                                   | ✔️   | git                            |
| Splunk                                        | [`/splunk`](https://endoflife.date/splunk)                                                             | ✔️   | custom                         |
| Spring Boot                                   | [`/spring-boot`](https://endoflife.date/spring-boot)                                                   | ✔️   | git, release_table             |
| Spring Framework                              | [`/spring-framework`](https://endoflife.date/spring-framework)                                         | ✔️   | git, release_table             |
| SQLite                                        | [`/sqlite`](https://endoflife.date/sqlite)                                                             | ✔️   | git                            |
| Squid                                         | [`/squid`](https://endoflife.date/squid)                                                               | ✔️   | git                            |
| SteamOS                                       | [`/steamos`](https://endoflife.date/steamos)                                                           | ❌    |                                |
| Microsoft Surface                             | [`/surface`](https://endoflife.date/surface)                                                           | ❌    |                                |
| SUSE Manager                                  | [`/suse-manager`](https://endoflife.date/suse-manager)                                                 | ❌    |                                |
| Svelte                                        | [`/svelte`](https://endoflife.date/svelte)                                                             | ✔️   | npm                            |
| Symfony                                       | [`/symfony`](https://endoflife.date/symfony)                                                           | ✔️   | git                            |
| Tails                                         | [`/tails`](https://endoflife.date/tails)                                                               | ✔️   | distrowatch                    |
| Tarantool                                     | [`/tarantool`](https://endoflife.date/tarantool)                                                       | ✔️   | git                            |
| Telegraf                                      | [`/telegraf`](https://endoflife.date/telegraf)                                                         | ✔️   | git                            |
| Hashicorp Terraform                           | [`/terraform`](https://endoflife.date/terraform)                                                       | ✔️   | git                            |
| Apache Tomcat                                 | [`/tomcat`](https://endoflife.date/tomcat)                                                             | ✔️   | maven                          |
| Traefik                                       | [`/traefik`](https://endoflife.date/traefik)                                                           | ✔️   | git, release_table             |
| Twig                                          | [`/twig`](https://endoflife.date/twig)                                                                 | ✔️   | git                            |
| TYPO3                                         | [`/typo3`](https://endoflife.date/typo3)                                                               | ✔️   | custom                         |
| Ubuntu                                        | [`/ubuntu`](https://endoflife.date/ubuntu)                                                             | ✔️   | distrowatch                    |
| Umbraco CMS                                   | [`/umbraco`](https://endoflife.date/umbraco)                                                           | ✔️   | git, release_table             |
| Unity                                         | [`/unity`](https://endoflife.date/unity)                                                               | ❌    |                                |
| UnrealIRCd                                    | [`/unrealircd`](https://endoflife.date/unrealircd)                                                     | ✔️   | custom, release_table          |
| Valkey                                        | [`/valkey`](https://endoflife.date/valkey)                                                             | ✔️   | git                            |
| Varnish                                       | [`/varnish`](https://endoflife.date/varnish)                                                           | ✔️   | git, release_table             |
| Veeam Backup & Replication                    | [`/veeam-backup-and-replication`](https://endoflife.date/veeam-backup-and-replication)                 | ✔️   | custom                         |
| Apple visionOS                                | [`/visionos`](https://endoflife.date/visionos)                                                         | ✔️   | apple                          |
| Visual COBOL                                  | [`/visual-cobol`](https://endoflife.date/visual-cobol)                                                 | ❌    |                                |
| Microsoft Visual Studio                       | [`/visual-studio`](https://endoflife.date/visual-studio)                                               | ✔️   | custom                         |
| VMware Cloud Foundation                       | [`/vmware-cloud-foundation`](https://endoflife.date/vmware-cloud-foundation)                           | ❌    |                                |
| VMware ESXi                                   | [`/esxi`](https://endoflife.date/esxi)                                                                 | ❌    |                                |
| VMware Harbor Registry                        | [`/vmware-harbor-registry`](https://endoflife.date/vmware-harbor-registry)                             | ❌    |                                |
| VMware Photon                                 | [`/photon`](https://endoflife.date/photon)                                                             | ❌    |                                |
| VMware Site Recovery Manager                  | [`/vmware-srm`](https://endoflife.date/vmware-srm)                                                     | ❌    |                                |
| VMware vCenter Server                         | [`/vcenter`](https://endoflife.date/vcenter)                                                           | ❌    |                                |
| Vue                                           | [`/vue`](https://endoflife.date/vue)                                                                   | ✔️   | npm                            |
| Vuetify                                       | [`/vuetify`](https://endoflife.date/vuetify)                                                           | ✔️   | npm, release_table             |
| Wagtail                                       | [`/wagtail`](https://endoflife.date/wagtail)                                                           | ✔️   | pypi, release_table            |
| Apple watchOS                                 | [`/watchos`](https://endoflife.date/watchos)                                                           | ✔️   | apple                          |
| WeeChat                                       | [`/weechat`](https://endoflife.date/weechat)                                                           | ✔️   | git                            |
| Microsoft Windows Embedded                    | [`/windows-embedded`](https://endoflife.date/windows-embedded)                                         | ❌    |                                |
| Microsoft Nano Server                         | [`/windows-nano-server`](https://endoflife.date/windows-nano-server)                                   | ❌    |                                |
| Microsoft Windows Server Core                 | [`/windows-server-core`](https://endoflife.date/windows-server-core)                                   | ❌    |                                |
| Microsoft Windows Server                      | [`/windows-server`](https://endoflife.date/windows-server)                                             | ❌    |                                |
| Microsoft Windows                             | [`/windows`](https://endoflife.date/windows)                                                           | ❌    |                                |
| Wireshark                                     | [`/wireshark`](https://endoflife.date/wireshark)                                                       | ✔️   | git                            |
| WordPress                                     | [`/wordpress`](https://endoflife.date/wordpress)                                                       | ✔️   | git                            |
| XCP-ng                                        | [`/xcp-ng`](https://endoflife.date/xcp-ng)                                                             | ✔️   | git, release_table             |
| Yarn                                          | [`/yarn`](https://endoflife.date/yarn)                                                                 | ✔️   | npm                            |
| Yocto Project                                 | [`/yocto`](https://endoflife.date/yocto)                                                               | ✔️   | git                            |
| Zabbix                                        | [`/zabbix`](https://endoflife.date/zabbix)                                                             | ✔️   | git, release_table             |
| Zentyal                                       | [`/zentyal`](https://endoflife.date/zentyal)                                                           | ✔️   | release_table                  |
| Zerto                                         | [`/zerto`](https://endoflife.date/zerto)                                                               | ❌    |                                |
| Apache ZooKeeper                              | [`/zookeeper`](https://endoflife.date/zookeeper)                                                       | ✔️   | maven                          |

This table has been generated by [report.py](/report.py).
