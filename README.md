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

As of 2024-01-07, 213 of the 281 products tracked by endoflife.date have automatically tracked releases:

| Product                                       | Permalink                                                                              | Auto | Method          |
|-----------------------------------------------|----------------------------------------------------------------------------------------|------|-----------------|
| Adobe ColdFusion                              | [`/coldfusion`](https://endoflife.date/coldfusion)                                     | ✔️   | custom          |
| Akeneo PIM                                    | [`/akeneo-pim`](https://endoflife.date/akeneo-pim)                                     | ✔️   | git             |
| Alibaba Dragonwell                            | [`/alibaba-dragonwell`](https://endoflife.date/alibaba-dragonwell)                     | ✔️   | git             |
| AlmaLinux OS                                  | [`/almalinux`](https://endoflife.date/almalinux)                                       | ✔️   | distrowatch     |
| Alpine Linux                                  | [`/alpine`](https://endoflife.date/alpine)                                             | ✔️   | git             |
| Amazon CDK                                    | [`/amazon-cdk`](https://endoflife.date/amazon-cdk)                                     | ✔️   | git             |
| Amazon Corretto                               | [`/amazon-corretto`](https://endoflife.date/amazon-corretto)                           | ✔️   | github_releases |
| Amazon EKS                                    | [`/amazon-eks`](https://endoflife.date/amazon-eks)                                     | ✔️   | custom          |
| Amazon Glue                                   | [`/amazon-glue`](https://endoflife.date/amazon-glue)                                   | ❌    | n/a             |
| Amazon Kindle                                 | [`/kindle`](https://endoflife.date/kindle)                                             | ❌    | n/a             |
| Amazon Linux                                  | [`/amazon-linux`](https://endoflife.date/amazon-linux)                                 | ✔️   | docker_hub      |
| Amazon Neptune                                | [`/amazon-neptune`](https://endoflife.date/amazon-neptune)                             | ✔️   | custom          |
| Amazon RDS for MySQL                          | [`/amazon-rds-mysql`](https://endoflife.date/amazon-rds-mysql)                         | ✔️   | custom          |
| Amazon RDS for PostgreSQL                     | [`/amazon-rds-postgresql`](https://endoflife.date/amazon-rds-postgresql)               | ✔️   | custom          |
| Android OS                                    | [`/android`](https://endoflife.date/android)                                           | ❌    | n/a             |
| Angular                                       | [`/angular`](https://endoflife.date/angular)                                           | ✔️   | git             |
| AngularJS                                     | [`/angularjs`](https://endoflife.date/angularjs)                                       | ✔️   | npm             |
| Ansible                                       | [`/ansible`](https://endoflife.date/ansible)                                           | ✔️   | pypi            |
| Ansible-core                                  | [`/ansible-core`](https://endoflife.date/ansible-core)                                 | ✔️   | git             |
| antiX Linux                                   | [`/antix`](https://endoflife.date/antix)                                               | ✔️   | distrowatch     |
| Apache ActiveMQ                               | [`/apache-activemq`](https://endoflife.date/apache-activemq)                           | ✔️   | git             |
| Apache Airflow                                | [`/apache-airflow`](https://endoflife.date/apache-airflow)                             | ✔️   | pypi            |
| Apache Camel                                  | [`/apache-camel`](https://endoflife.date/apache-camel)                                 | ✔️   | maven           |
| Apache Cassandra                              | [`/apache-cassandra`](https://endoflife.date/apache-cassandra)                         | ✔️   | git             |
| Apache Groovy                                 | [`/apache-groovy`](https://endoflife.date/apache-groovy)                               | ✔️   | maven           |
| Apache Hadoop                                 | [`/apache-hadoop`](https://endoflife.date/apache-hadoop)                               | ✔️   | git             |
| Apache HBase                                  | [`/hbase`](https://endoflife.date/hbase)                                               | ✔️   | git             |
| Apache Hop                                    | [`/apache-hop`](https://endoflife.date/apache-hop)                                     | ✔️   | github_releases |
| Apache HTTP Server                            | [`/apache`](https://endoflife.date/apache)                                             | ✔️   | custom          |
| Apache Kafka                                  | [`/apache-kafka`](https://endoflife.date/apache-kafka)                                 | ✔️   | git             |
| Apache Log4j                                  | [`/log4j`](https://endoflife.date/log4j)                                               | ✔️   | maven           |
| Apache Maven                                  | [`/maven`](https://endoflife.date/maven)                                               | ✔️   | maven           |
| Apache Solr                                   | [`/solr`](https://endoflife.date/solr)                                                 | ✔️   | git             |
| Apache Spark                                  | [`/apache-spark`](https://endoflife.date/apache-spark)                                 | ✔️   | git             |
| Apache Tomcat                                 | [`/tomcat`](https://endoflife.date/tomcat)                                             | ✔️   | maven           |
| Apache ZooKeeper                              | [`/zookeeper`](https://endoflife.date/zookeeper)                                       | ✔️   | maven           |
| API Platform                                  | [`/api-platform`](https://endoflife.date/api-platform)                                 | ✔️   | git             |
| Apple iOS                                     | [`/ios`](https://endoflife.date/ios)                                                   | ✔️   | custom          |
| Apple iPad                                    | [`/ipad`](https://endoflife.date/ipad)                                                 | ❌    | n/a             |
| Apple iPadOS                                  | [`/ipados`](https://endoflife.date/ipados)                                             | ✔️   | custom          |
| Apple iPhone                                  | [`/iphone`](https://endoflife.date/iphone)                                             | ❌    | n/a             |
| Apple macOS                                   | [`/macos`](https://endoflife.date/macos)                                               | ✔️   | custom          |
| Apple Watch                                   | [`/apple-watch`](https://endoflife.date/apple-watch)                                   | ❌    | n/a             |
| Apple watchOS                                 | [`/watchos`](https://endoflife.date/watchos)                                           | ✔️   | custom          |
| ArangoDB                                      | [`/arangodb`](https://endoflife.date/arangodb)                                         | ✔️   | git             |
| Argo CD                                       | [`/argo-cd`](https://endoflife.date/argo-cd)                                           | ✔️   | git             |
| Artifactory                                   | [`/artifactory`](https://endoflife.date/artifactory)                                   | ✔️   | custom          |
| AWS Lambda                                    | [`/aws-lambda`](https://endoflife.date/aws-lambda)                                     | ✔️   | custom          |
| Azul Zulu                                     | [`/azul-zulu`](https://endoflife.date/azul-zulu)                                       | ❌    | n/a             |
| Azure DevOps Server                           | [`/azure-devops-server`](https://endoflife.date/azure-devops-server)                   | ❌    | n/a             |
| Azure Kubernetes Service                      | [`/azure-kubernetes-service`](https://endoflife.date/azure-kubernetes-service)         | ❌    | n/a             |
| Bazel                                         | [`/bazel`](https://endoflife.date/bazel)                                               | ✔️   | git             |
| Bellsoft Liberica JDK                         | [`/bellsoft-liberica`](https://endoflife.date/bellsoft-liberica)                       | ✔️   | github_releases |
| Blender                                       | [`/blender`](https://endoflife.date/blender)                                           | ✔️   | git             |
| Bootstrap                                     | [`/bootstrap`](https://endoflife.date/bootstrap)                                       | ✔️   | git             |
| CakePHP                                       | [`/cakephp`](https://endoflife.date/cakephp)                                           | ✔️   | git             |
| CentOS                                        | [`/centos`](https://endoflife.date/centos)                                             | ❌    | n/a             |
| CentOS Stream                                 | [`/centos-stream`](https://endoflife.date/centos-stream)                               | ❌    | n/a             |
| cert-manager                                  | [`/cert-manager`](https://endoflife.date/cert-manager)                                 | ✔️   | git             |
| CFEngine                                      | [`/cfengine`](https://endoflife.date/cfengine)                                         | ✔️   | git             |
| Citrix Virtual Apps and Desktops              | [`/citrix-vad`](https://endoflife.date/citrix-vad)                                     | ❌    | n/a             |
| ClamAV                                        | [`/clamav`](https://endoflife.date/clamav)                                             | ✔️   | git             |
| Composer                                      | [`/composer`](https://endoflife.date/composer)                                         | ✔️   | git             |
| Confluence                                    | [`/confluence`](https://endoflife.date/confluence)                                     | ✔️   | custom          |
| Contao                                        | [`/contao`](https://endoflife.date/contao)                                             | ✔️   | git             |
| Couchbase Server                              | [`/couchbase-server`](https://endoflife.date/couchbase-server)                         | ✔️   | custom          |
| Craft CMS                                     | [`/craft-cms`](https://endoflife.date/craft-cms)                                       | ✔️   | git             |
| dbt Core                                      | [`/dbt-core`](https://endoflife.date/dbt-core)                                         | ✔️   | git             |
| Debian                                        | [`/debian`](https://endoflife.date/debian)                                             | ✔️   | custom          |
| Dependency-Track                              | [`/dependency-track`](https://endoflife.date/dependency-track)                         | ✔️   | git             |
| Devuan                                        | [`/devuan`](https://endoflife.date/devuan)                                             | ✔️   | distrowatch     |
| Django                                        | [`/django`](https://endoflife.date/django)                                             | ✔️   | git             |
| Docker Engine                                 | [`/docker-engine`](https://endoflife.date/docker-engine)                               | ✔️   | git             |
| Drupal                                        | [`/drupal`](https://endoflife.date/drupal)                                             | ✔️   | git             |
| Drush                                         | [`/drush`](https://endoflife.date/drush)                                               | ✔️   | git             |
| Eclipse Jetty                                 | [`/eclipse-jetty`](https://endoflife.date/eclipse-jetty)                               | ✔️   | maven           |
| Eclipse Temurin                               | [`/eclipse-temurin`](https://endoflife.date/eclipse-temurin)                           | ✔️   | github_releases |
| Elastic Beats                                 | [`/beats`](https://endoflife.date/beats)                                               | ✔️   | git             |
| Elasticsearch                                 | [`/elasticsearch`](https://endoflife.date/elasticsearch)                               | ✔️   | git             |
| Electron                                      | [`/electron`](https://endoflife.date/electron)                                         | ✔️   | npm             |
| Elixir                                        | [`/elixir`](https://endoflife.date/elixir)                                             | ✔️   | git             |
| Ember                                         | [`/emberjs`](https://endoflife.date/emberjs)                                           | ✔️   | npm             |
| Envoy                                         | [`/envoy`](https://endoflife.date/envoy)                                               | ✔️   | git             |
| Erlang                                        | [`/erlang`](https://endoflife.date/erlang)                                             | ✔️   | git             |
| etcd                                          | [`/etcd`](https://endoflife.date/etcd)                                                 | ✔️   | git             |
| EuroLinux                                     | [`/eurolinux`](https://endoflife.date/eurolinux)                                       | ✔️   | distrowatch     |
| Exim                                          | [`/exim`](https://endoflife.date/exim)                                                 | ✔️   | git             |
| Fairphone                                     | [`/fairphone`](https://endoflife.date/fairphone)                                       | ❌    | n/a             |
| Fedora Linux                                  | [`/fedora`](https://endoflife.date/fedora)                                             | ✔️   | distrowatch     |
| FFmpeg                                        | [`/ffmpeg`](https://endoflife.date/ffmpeg)                                             | ✔️   | git             |
| FileMaker Platform                            | [`/filemaker`](https://endoflife.date/filemaker)                                       | ❌    | n/a             |
| Firefox                                       | [`/firefox`](https://endoflife.date/firefox)                                           | ✔️   | custom          |
| Flux                                          | [`/flux`](https://endoflife.date/flux)                                                 | ✔️   | git             |
| FortiOS                                       | [`/fortios`](https://endoflife.date/fortios)                                           | ❌    | n/a             |
| FreeBSD                                       | [`/freebsd`](https://endoflife.date/freebsd)                                           | ❌    | n/a             |
| Gerrit                                        | [`/gerrit`](https://endoflife.date/gerrit)                                             | ✔️   | git             |
| GitLab                                        | [`/gitlab`](https://endoflife.date/gitlab)                                             | ✔️   | git             |
| Go                                            | [`/go`](https://endoflife.date/go)                                                     | ✔️   | git             |
| Godot                                         | [`/godot`](https://endoflife.date/godot)                                               | ✔️   | git             |
| Google Container-Optimized OS (COS)           | [`/cos`](https://endoflife.date/cos)                                                   | ✔️   | custom          |
| Google Kubernetes Engine                      | [`/google-kubernetes-engine`](https://endoflife.date/google-kubernetes-engine)         | ✔️   | custom          |
| Google Pixel                                  | [`/pixel`](https://endoflife.date/pixel)                                               | ❌    | n/a             |
| Gorilla Toolkit                               | [`/gorilla`](https://endoflife.date/gorilla)                                           | ❌    | n/a             |
| GraalVM                                       | [`/graalvm`](https://endoflife.date/graalvm)                                           | ✔️   | custom          |
| Gradle                                        | [`/gradle`](https://endoflife.date/gradle)                                             | ✔️   | git             |
| Grafana                                       | [`/grafana`](https://endoflife.date/grafana)                                           | ✔️   | git             |
| Grails Framework                              | [`/grails`](https://endoflife.date/grails)                                             | ✔️   | git             |
| Graylog                                       | [`/graylog`](https://endoflife.date/graylog)                                           | ✔️   | git             |
| GStreamer                                     | [`/gstreamer`](https://endoflife.date/gstreamer)                                       | ✔️   | git             |
| HAProxy                                       | [`/haproxy`](https://endoflife.date/haproxy)                                           | ✔️   | custom          |
| Hashicorp Consul                              | [`/consul`](https://endoflife.date/consul)                                             | ✔️   | git             |
| Hashicorp Terraform                           | [`/terraform`](https://endoflife.date/terraform)                                       | ✔️   | git             |
| Hashicorp Vault                               | [`/hashicorp-vault`](https://endoflife.date/hashicorp-vault)                           | ✔️   | git             |
| IBM AIX                                       | [`/ibm-aix`](https://endoflife.date/ibm-aix)                                           | ✔️   | custom          |
| IBM Semeru Runtime                            | [`/ibm-semeru-runtime`](https://endoflife.date/ibm-semeru-runtime)                     | ✔️   | github_releases |
| Intel Processors                              | [`/intel-processors`](https://endoflife.date/intel-processors)                         | ❌    | n/a             |
| Internet Explorer                             | [`/internet-explorer`](https://endoflife.date/internet-explorer)                       | ❌    | n/a             |
| Ionic Framework                               | [`/ionic`](https://endoflife.date/ionic)                                               | ✔️   | git             |
| ISC DHCP                                      | [`/isc-dhcp`](https://endoflife.date/isc-dhcp)                                         | ❌    | n/a             |
| Istio                                         | [`/istio`](https://endoflife.date/istio)                                               | ✔️   | git             |
| Jekyll                                        | [`/jekyll`](https://endoflife.date/jekyll)                                             | ✔️   | git             |
| Jenkins                                       | [`/jenkins`](https://endoflife.date/jenkins)                                           | ✔️   | git             |
| JHipster                                      | [`/jhipster`](https://endoflife.date/jhipster)                                         | ✔️   | npm             |
| Jira Software                                 | [`/jira-software`](https://endoflife.date/jira-software)                               | ✔️   | custom          |
| Joomla!                                       | [`/joomla`](https://endoflife.date/joomla)                                             | ✔️   | git             |
| jQuery                                        | [`/jquery`](https://endoflife.date/jquery)                                             | ✔️   | git             |
| JReleaser                                     | [`/jreleaser`](https://endoflife.date/jreleaser)                                       | ✔️   | maven           |
| KDE Plasma                                    | [`/kde-plasma`](https://endoflife.date/kde-plasma)                                     | ✔️   | git             |
| KEDA                                          | [`/keda`](https://endoflife.date/keda)                                                 | ✔️   | git             |
| Keycloak                                      | [`/keycloak`](https://endoflife.date/keycloak)                                         | ✔️   | git             |
| Kibana                                        | [`/kibana`](https://endoflife.date/kibana)                                             | ✔️   | git             |
| Kirby                                         | [`/kirby`](https://endoflife.date/kirby)                                               | ✔️   | git             |
| Kong Gateway                                  | [`/kong-gateway`](https://endoflife.date/kong-gateway)                                 | ✔️   | git             |
| Kotlin                                        | [`/kotlin`](https://endoflife.date/kotlin)                                             | ✔️   | npm             |
| Kubernetes                                    | [`/kubernetes`](https://endoflife.date/kubernetes)                                     | ✔️   | git             |
| Laravel                                       | [`/laravel`](https://endoflife.date/laravel)                                           | ✔️   | git             |
| LibreOffice                                   | [`/libreoffice`](https://endoflife.date/libreoffice)                                   | ❌    | n/a             |
| LineageOS                                     | [`/lineageos`](https://endoflife.date/lineageos)                                       | ❌    | n/a             |
| Linux Kernel                                  | [`/linux`](https://endoflife.date/linux)                                               | ✔️   | cgit            |
| Linux Mint                                    | [`/linuxmint`](https://endoflife.date/linuxmint)                                       | ❌    | n/a             |
| Logstash                                      | [`/logstash`](https://endoflife.date/logstash)                                         | ✔️   | git             |
| Looker                                        | [`/looker`](https://endoflife.date/looker)                                             | ✔️   | custom          |
| Mageia                                        | [`/mageia`](https://endoflife.date/mageia)                                             | ✔️   | distrowatch     |
| Magento                                       | [`/magento`](https://endoflife.date/magento)                                           | ✔️   | git             |
| MariaDB                                       | [`/mariadb`](https://endoflife.date/mariadb)                                           | ✔️   | git             |
| Mastodon                                      | [`/mastodon`](https://endoflife.date/mastodon)                                         | ✔️   | git             |
| Mattermost                                    | [`/mattermost`](https://endoflife.date/mattermost)                                     | ✔️   | git             |
| MediaWiki                                     | [`/mediawiki`](https://endoflife.date/mediawiki)                                       | ✔️   | git             |
| Memcached                                     | [`/memcached`](https://endoflife.date/memcached)                                       | ✔️   | git             |
| Micronaut Framework                           | [`/micronaut`](https://endoflife.date/micronaut)                                       | ✔️   | git             |
| Microsoft .NET                                | [`/dotnet`](https://endoflife.date/dotnet)                                             | ✔️   | git             |
| Microsoft .NET Framework                      | [`/dotnetfx`](https://endoflife.date/dotnetfx)                                         | ❌    | n/a             |
| Microsoft Build of OpenJDK                    | [`/microsoft-build-of-openjdk`](https://endoflife.date/microsoft-build-of-openjdk)     | ✔️   | git             |
| Microsoft Exchange                            | [`/msexchange`](https://endoflife.date/msexchange)                                     | ❌    | n/a             |
| Microsoft Office                              | [`/office`](https://endoflife.date/office)                                             | ❌    | n/a             |
| Microsoft PowerShell                          | [`/powershell`](https://endoflife.date/powershell)                                     | ✔️   | git             |
| Microsoft SharePoint                          | [`/sharepoint`](https://endoflife.date/sharepoint)                                     | ❌    | n/a             |
| Microsoft SQL Server                          | [`/mssqlserver`](https://endoflife.date/mssqlserver)                                   | ❌    | n/a             |
| Microsoft Surface                             | [`/surface`](https://endoflife.date/surface)                                           | ❌    | n/a             |
| Microsoft Visual Studio                       | [`/visual-studio`](https://endoflife.date/visual-studio)                               | ✔️   | custom          |
| Microsoft Windows                             | [`/windows`](https://endoflife.date/windows)                                           | ❌    | n/a             |
| Microsoft Windows Embedded                    | [`/windows-embedded`](https://endoflife.date/windows-embedded)                         | ❌    | n/a             |
| Microsoft Windows Server                      | [`/windows-server`](https://endoflife.date/windows-server)                             | ❌    | n/a             |
| MongoDB Server                                | [`/mongodb`](https://endoflife.date/mongodb)                                           | ✔️   | git             |
| Moodle                                        | [`/moodle`](https://endoflife.date/moodle)                                             | ✔️   | git             |
| Mule Runtime                                  | [`/mulesoft-runtime`](https://endoflife.date/mulesoft-runtime)                         | ❌    | n/a             |
| MX Linux                                      | [`/mxlinux`](https://endoflife.date/mxlinux)                                           | ✔️   | distrowatch     |
| MySQL                                         | [`/mysql`](https://endoflife.date/mysql)                                               | ✔️   | git             |
| Neo4j                                         | [`/neo4j`](https://endoflife.date/neo4j)                                               | ✔️   | git             |
| NetBSD                                        | [`/netbsd`](https://endoflife.date/netbsd)                                             | ❌    | n/a             |
| Netgear ReadyNAS                              | [`/readynas`](https://endoflife.date/readynas)                                         | ❌    | n/a             |
| Next.js                                       | [`/nextjs`](https://endoflife.date/nextjs)                                             | ✔️   | npm             |
| Nextcloud                                     | [`/nextcloud`](https://endoflife.date/nextcloud)                                       | ✔️   | git             |
| Nexus Repository OSS                          | [`/nexus`](https://endoflife.date/nexus)                                               | ✔️   | git             |
| nginx                                         | [`/nginx`](https://endoflife.date/nginx)                                               | ✔️   | git             |
| nix                                           | [`/nix`](https://endoflife.date/nix)                                                   | ✔️   | git             |
| NixOS                                         | [`/nixos`](https://endoflife.date/nixos)                                               | ❌    | n/a             |
| Node.js                                       | [`/nodejs`](https://endoflife.date/nodejs)                                             | ✔️   | git             |
| Nokia Mobile                                  | [`/nokia`](https://endoflife.date/nokia)                                               | ❌    | n/a             |
| Nomad                                         | [`/nomad`](https://endoflife.date/nomad)                                               | ✔️   | git             |
| NumPy                                         | [`/numpy`](https://endoflife.date/numpy)                                               | ✔️   | pypi            |
| Nutanix AOS                                   | [`/nutanix-aos`](https://endoflife.date/nutanix-aos)                                   | ✔️   | custom          |
| Nutanix Files                                 | [`/nutanix-files`](https://endoflife.date/nutanix-files)                               | ✔️   | custom          |
| Nutanix Prism Central                         | [`/nutanix-prism`](https://endoflife.date/nutanix-prism)                               | ✔️   | custom          |
| Nuxt                                          | [`/nuxt`](https://endoflife.date/nuxt)                                                 | ✔️   | npm             |
| NVIDIA Driver                                 | [`/nvidia`](https://endoflife.date/nvidia)                                             | ❌    | n/a             |
| NVIDIA GPUs                                   | [`/nvidia-gpu`](https://endoflife.date/nvidia-gpu)                                     | ❌    | n/a             |
| OpenBSD                                       | [`/openbsd`](https://endoflife.date/openbsd)                                           | ❌    | n/a             |
| OpenJDK builds from Oracle                    | [`/openjdk-builds-from-oracle`](https://endoflife.date/openjdk-builds-from-oracle)     | ❌    | n/a             |
| OpenSearch                                    | [`/opensearch`](https://endoflife.date/opensearch)                                     | ✔️   | git             |
| OpenSSL                                       | [`/openssl`](https://endoflife.date/openssl)                                           | ✔️   | git             |
| openSUSE                                      | [`/opensuse`](https://endoflife.date/opensuse)                                         | ❌    | n/a             |
| OpenWrt                                       | [`/openwrt`](https://endoflife.date/openwrt)                                           | ✔️   | git             |
| OpenZFS                                       | [`/openzfs`](https://endoflife.date/openzfs)                                           | ✔️   | git             |
| Oracle APEX                                   | [`/oracle-apex`](https://endoflife.date/oracle-apex)                                   | ❌    | n/a             |
| Oracle Database                               | [`/oracle-database`](https://endoflife.date/oracle-database)                           | ❌    | n/a             |
| Oracle JDK                                    | [`/oracle-jdk`](https://endoflife.date/oracle-jdk)                                     | ✔️   | custom          |
| Oracle Linux                                  | [`/oracle-linux`](https://endoflife.date/oracle-linux)                                 | ✔️   | distrowatch     |
| Oracle Solaris                                | [`/oracle-solaris`](https://endoflife.date/oracle-solaris)                             | ❌    | n/a             |
| Palo Alto Networks Cortex XDR agent           | [`/cortex-xdr`](https://endoflife.date/cortex-xdr)                                     | ❌    | n/a             |
| Palo Alto Networks GlobalProtect App          | [`/pangp`](https://endoflife.date/pangp)                                               | ❌    | n/a             |
| Palo Alto Networks PAN-OS                     | [`/panos`](https://endoflife.date/panos)                                               | ❌    | n/a             |
| PCI-DSS                                       | [`/pci-dss`](https://endoflife.date/pci-dss)                                           | ❌    | n/a             |
| Perl                                          | [`/perl`](https://endoflife.date/perl)                                                 | ✔️   | git             |
| PHP                                           | [`/php`](https://endoflife.date/php)                                                   | ✔️   | custom          |
| phpBB                                         | [`/phpbb`](https://endoflife.date/phpbb)                                               | ✔️   | git             |
| phpMyAdmin                                    | [`/phpmyadmin`](https://endoflife.date/phpmyadmin)                                     | ✔️   | git             |
| Plesk                                         | [`/plesk`](https://endoflife.date/plesk)                                               | ✔️   | custom          |
| Pop!_OS                                       | [`/pop-os`](https://endoflife.date/pop-os)                                             | ❌    | n/a             |
| Postfix                                       | [`/postfix`](https://endoflife.date/postfix)                                           | ✔️   | git             |
| PostgreSQL                                    | [`/postgresql`](https://endoflife.date/postgresql)                                     | ✔️   | git             |
| Prometheus                                    | [`/prometheus`](https://endoflife.date/prometheus)                                     | ✔️   | git             |
| Protractor                                    | [`/protractor`](https://endoflife.date/protractor)                                     | ✔️   | npm             |
| Proxmox VE                                    | [`/proxmox-ve`](https://endoflife.date/proxmox-ve)                                     | ✔️   | distrowatch     |
| Puppet                                        | [`/puppet`](https://endoflife.date/puppet)                                             | ✔️   | git             |
| Python                                        | [`/python`](https://endoflife.date/python)                                             | ✔️   | git             |
| Qt                                            | [`/qt`](https://endoflife.date/qt)                                                     | ✔️   | git             |
| Quarkus                                       | [`/quarkus-framework`](https://endoflife.date/quarkus-framework)                       | ✔️   | github_releases |
| Quasar                                        | [`/quasar`](https://endoflife.date/quasar)                                             | ✔️   | npm             |
| RabbitMQ                                      | [`/rabbitmq`](https://endoflife.date/rabbitmq)                                         | ✔️   | git             |
| Rancher                                       | [`/rancher`](https://endoflife.date/rancher)                                           | ✔️   | git             |
| Raspberry Pi                                  | [`/raspberry-pi`](https://endoflife.date/raspberry-pi)                                 | ❌    | n/a             |
| React                                         | [`/react`](https://endoflife.date/react)                                               | ✔️   | npm             |
| Red Hat build of OpenJDK                      | [`/redhat-build-of-openjdk`](https://endoflife.date/redhat-build-of-openjdk)           | ❌    | n/a             |
| Red Hat Enterprise Linux                      | [`/rhel`](https://endoflife.date/rhel)                                                 | ❌    | n/a             |
| Red Hat JBoss Enterprise Application Platform | [`/redhat-jboss-eap`](https://endoflife.date/redhat-jboss-eap)                         | ❌    | n/a             |
| Red Hat OpenShift                             | [`/red-hat-openshift`](https://endoflife.date/red-hat-openshift)                       | ✔️   | custom          |
| Red Hat Satellite                             | [`/redhat-satellite`](https://endoflife.date/redhat-satellite)                         | ✔️   | custom          |
| Redis                                         | [`/redis`](https://endoflife.date/redis)                                               | ✔️   | git             |
| Redmine                                       | [`/redmine`](https://endoflife.date/redmine)                                           | ✔️   | git             |
| Rocket.Chat                                   | [`/rocket-chat`](https://endoflife.date/rocket-chat)                                   | ✔️   | git             |
| Rocky Linux                                   | [`/rocky-linux`](https://endoflife.date/rocky-linux)                                   | ✔️   | custom          |
| ROS                                           | [`/ros`](https://endoflife.date/ros)                                                   | ❌    | n/a             |
| ROS 2                                         | [`/ros-2`](https://endoflife.date/ros-2)                                               | ❌    | n/a             |
| Roundcube Webmail                             | [`/roundcube`](https://endoflife.date/roundcube)                                       | ✔️   | git             |
| Ruby                                          | [`/ruby`](https://endoflife.date/ruby)                                                 | ✔️   | git             |
| Ruby on Rails                                 | [`/rails`](https://endoflife.date/rails)                                               | ✔️   | git             |
| Rust                                          | [`/rust`](https://endoflife.date/rust)                                                 | ✔️   | git             |
| Salt                                          | [`/salt`](https://endoflife.date/salt)                                                 | ✔️   | git             |
| Samsung Mobile                                | [`/samsung-mobile`](https://endoflife.date/samsung-mobile)                             | ❌    | n/a             |
| SapMachine                                    | [`/sapmachine`](https://endoflife.date/sapmachine)                                     | ✔️   | github_releases |
| Scala                                         | [`/scala`](https://endoflife.date/scala)                                               | ✔️   | git             |
| Silverstripe CMS                              | [`/silverstripe`](https://endoflife.date/silverstripe)                                 | ✔️   | git             |
| Slackware Linux                               | [`/slackware`](https://endoflife.date/slackware)                                       | ✔️   | distrowatch     |
| SonarQube                                     | [`/sonar`](https://endoflife.date/sonar)                                               | ✔️   | git             |
| Splunk                                        | [`/splunk`](https://endoflife.date/splunk)                                             | ✔️   | custom          |
| Spring Boot                                   | [`/spring-boot`](https://endoflife.date/spring-boot)                                   | ✔️   | git             |
| Spring Framework                              | [`/spring-framework`](https://endoflife.date/spring-framework)                         | ✔️   | git             |
| SQLite                                        | [`/sqlite`](https://endoflife.date/sqlite)                                             | ✔️   | git             |
| Squid                                         | [`/squid`](https://endoflife.date/squid)                                               | ✔️   | git             |
| SUSE Linux Enterprise Server                  | [`/sles`](https://endoflife.date/sles)                                                 | ❌    | n/a             |
| Symfony                                       | [`/symfony`](https://endoflife.date/symfony)                                           | ✔️   | git             |
| Tails                                         | [`/tails`](https://endoflife.date/tails)                                               | ✔️   | distrowatch     |
| Tarantool                                     | [`/tarantool`](https://endoflife.date/tarantool)                                       | ✔️   | git             |
| Telegraf                                      | [`/telegraf`](https://endoflife.date/telegraf)                                         | ✔️   | git             |
| Traefik                                       | [`/traefik`](https://endoflife.date/traefik)                                           | ✔️   | git             |
| Twig                                          | [`/twig`](https://endoflife.date/twig)                                                 | ✔️   | git             |
| TYPO3                                         | [`/typo3`](https://endoflife.date/typo3)                                               | ✔️   | custom          |
| Ubuntu                                        | [`/ubuntu`](https://endoflife.date/ubuntu)                                             | ✔️   | distrowatch     |
| Umbraco CMS                                   | [`/umbraco`](https://endoflife.date/umbraco)                                           | ✔️   | git             |
| Unity                                         | [`/unity`](https://endoflife.date/unity)                                               | ✔️   | custom          |
| UnrealIRCd                                    | [`/unrealircd`](https://endoflife.date/unrealircd)                                     | ✔️   | custom          |
| Varnish                                       | [`/varnish`](https://endoflife.date/varnish)                                           | ✔️   | git             |
| Veeam Backup & Replication                    | [`/veeam-backup-and-replication`](https://endoflife.date/veeam-backup-and-replication) | ❌    | n/a             |
| Visual COBOL                                  | [`/visual-cobol`](https://endoflife.date/visual-cobol)                                 | ❌    | n/a             |
| VMware Cloud Foundation                       | [`/vmware-cloud-foundation`](https://endoflife.date/vmware-cloud-foundation)           | ❌    | n/a             |
| VMware ESXi                                   | [`/esxi`](https://endoflife.date/esxi)                                                 | ❌    | n/a             |
| VMware Harbor Registry                        | [`/vmware-harbor-registry`](https://endoflife.date/vmware-harbor-registry)             | ❌    | n/a             |
| VMware Horizon                                | [`/horizon`](https://endoflife.date/horizon)                                           | ❌    | n/a             |
| VMware Photon                                 | [`/photon`](https://endoflife.date/photon)                                             | ❌    | n/a             |
| VMware Site Recovery Manager                  | [`/vmware-srm`](https://endoflife.date/vmware-srm)                                     | ❌    | n/a             |
| VMware vCenter Server                         | [`/vcenter`](https://endoflife.date/vcenter)                                           | ❌    | n/a             |
| Vue                                           | [`/vue`](https://endoflife.date/vue)                                                   | ✔️   | npm             |
| Vuetify                                       | [`/vuetify`](https://endoflife.date/vuetify)                                           | ✔️   | npm             |
| Wagtail                                       | [`/wagtail`](https://endoflife.date/wagtail)                                           | ✔️   | pypi            |
| WeeChat                                       | [`/weechat`](https://endoflife.date/weechat)                                           | ✔️   | git             |
| WordPress                                     | [`/wordpress`](https://endoflife.date/wordpress)                                       | ✔️   | git             |
| XCP-ng                                        | [`/xcp-ng`](https://endoflife.date/xcp-ng)                                             | ✔️   | git             |
| Yarn                                          | [`/yarn`](https://endoflife.date/yarn)                                                 | ✔️   | npm             |
| Yocto Project                                 | [`/yocto`](https://endoflife.date/yocto)                                               | ✔️   | git             |
| Zabbix                                        | [`/zabbix`](https://endoflife.date/zabbix)                                             | ✔️   | git             |

This table has been generated by [report.py](/report.py).
