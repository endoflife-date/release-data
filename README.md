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

As of 2023-06-25, 160 of the 232 products tracked by endoflife.date have automatically tracked releases:

| Product                              | Permalink                     | Auto | Method          |
|--------------------------------------|-------------------------------|------|-----------------|
| Adobe ColdFusion                     | `/coldfusion`                 | ❌    | n/a             |
| Alibaba Dragonwell                   | `/alibaba-dragonwell`         | ✔️   | git             |
| AlmaLinux OS                         | `/almalinux`                  | ✔️   | distrowatch     |
| Alpine Linux                         | `/alpine`                     | ✔️   | git             |
| Amazon Corretto                      | `/amazon-corretto`            | ✔️   | github_releases |
| Amazon EKS                           | `/amazon-eks`                 | ✔️   | custom          |
| Amazon Kindle                        | `/kindle`                     | ❌    | n/a             |
| Amazon Linux                         | `/amazon-linux`               | ✔️   | dockerhub       |
| Amazon RDS for MySQL                 | `/amazon-rds-mysql`           | ✔️   | custom          |
| Amazon RDS for PostgreSQL            | `/amazon-rds-postgresql`      | ✔️   | custom          |
| Android OS                           | `/android`                    | ❌    | n/a             |
| Angular                              | `/angular`                    | ✔️   | git             |
| Ansible                              | `/ansible`                    | ✔️   | pypi            |
| Ansible-core                         | `/ansible-core`               | ✔️   | git             |
| antiX Linux                          | `/antix`                      | ✔️   | distrowatch     |
| Apache Airflow                       | `/apache-airflow`             | ✔️   | pypi            |
| Apache Camel                         | `/apache-camel`               | ✔️   | maven           |
| Apache Cassandra                     | `/apache-cassandra`           | ✔️   | git             |
| Apache Groovy                        | `/apache-groovy`              | ✔️   | maven           |
| Apache HBase                         | `/hbase`                      | ✔️   | git             |
| Apache HTTP Server                   | `/apache`                     | ❌    | n/a             |
| Apache Kafka                         | `/apache-kafka`               | ✔️   | git             |
| Apache Log4j                         | `/log4j`                      | ✔️   | maven           |
| Apache Maven                         | `/maven`                      | ✔️   | maven           |
| Apache Solr                          | `/solr`                       | ✔️   | git             |
| Apache Tomcat                        | `/tomcat`                     | ✔️   | maven           |
| Apache ZooKeeper                     | `/zookeeper`                  | ✔️   | maven           |
| API Platform                         | `/api-platform`               | ✔️   | git             |
| Apple iOS                            | `/ios`                        | ✔️   | custom          |
| Apple iPad                           | `/ipad`                       | ❌    | n/a             |
| Apple iPadOS                         | `/ipados`                     | ✔️   | custom          |
| Apple iPhone                         | `/iphone`                     | ❌    | n/a             |
| Apple macOS                          | `/macos`                      | ✔️   | custom          |
| Apple watchOS                        | `/watchos`                    | ✔️   | custom          |
| Azul Zulu                            | `/azul-zulu`                  | ❌    | n/a             |
| Azure DevOps Server                  | `/azure-devops-server`        | ❌    | n/a             |
| Azure Kubernetes Service             | `/azure-kubernetes-service`   | ❌    | n/a             |
| Bellsoft Liberica JDK                | `/bellsoft-liberica`          | ✔️   | github_releases |
| Blender                              | `/blender`                    | ✔️   | git             |
| Bootstrap                            | `/bootstrap`                  | ✔️   | git             |
| CakePHP                              | `/cakephp`                    | ✔️   | git             |
| CentOS                               | `/centos`                     | ❌    | n/a             |
| CentOS Stream                        | `/centos-stream`              | ❌    | n/a             |
| CFEngine                             | `/cfengine`                   | ✔️   | git             |
| Citrix Virtual Apps and Desktops     | `/citrix-vad`                 | ❌    | n/a             |
| ClamAV                               | `/clamav`                     | ✔️   | git             |
| Composer                             | `/composer`                   | ✔️   | git             |
| Confluence                           | `/confluence`                 | ❌    | n/a             |
| Contao                               | `/contao`                     | ✔️   | git             |
| Couchbase Server                     | `/couchbase-server`           | ✔️   | dockerhub       |
| Craft CMS                            | `/craft-cms`                  | ✔️   | git             |
| Debian                               | `/debian`                     | ✔️   | custom          |
| Dependency-Track                     | `/dependency-track`           | ✔️   | git             |
| Devuan                               | `/devuan`                     | ✔️   | distrowatch     |
| Django                               | `/django`                     | ✔️   | git             |
| Docker Engine                        | `/docker-engine`              | ✔️   | git             |
| Drupal                               | `/drupal`                     | ✔️   | git             |
| Drush                                | `/drush`                      | ✔️   | git             |
| Eclipse Temurin                      | `/eclipse-temurin`            | ✔️   | github_releases |
| Elastic Beats                        | `/beats`                      | ✔️   | git             |
| Elasticsearch                        | `/elasticsearch`              | ✔️   | git             |
| Electron                             | `/electron`                   | ✔️   | npm             |
| Elixir                               | `/elixir`                     | ✔️   | git             |
| Ember                                | `/emberjs`                    | ✔️   | npm             |
| EuroLinux                            | `/eurolinux`                  | ✔️   | distrowatch     |
| Fairphone                            | `/fairphone`                  | ❌    | n/a             |
| Fedora Linux                         | `/fedora`                     | ✔️   | distrowatch     |
| FFmpeg                               | `/ffmpeg`                     | ✔️   | git             |
| FileMaker Platform                   | `/filemaker`                  | ❌    | n/a             |
| Firefox                              | `/firefox`                    | ✔️   | custom          |
| FortiOS                              | `/fortios`                    | ❌    | n/a             |
| FreeBSD                              | `/freebsd`                    | ❌    | n/a             |
| Gerrit                               | `/gerrit`                     | ✔️   | git             |
| GitLab                               | `/gitlab`                     | ✔️   | git             |
| Go                                   | `/go`                         | ✔️   | git             |
| Godot                                | `/godot`                      | ✔️   | git             |
| Google Container-Optimized OS (COS)  | `/cos`                        | ✔️   | custom          |
| Google Kubernetes Engine             | `/google-kubernetes-engine`   | ✔️   | custom          |
| Google Pixel                         | `/pixel`                      | ❌    | n/a             |
| Gorilla Toolkit                      | `/gorilla`                    | ❌    | n/a             |
| GraalVM                              | `/graalvm`                    | ❌    | n/a             |
| Gradle                               | `/gradle`                     | ✔️   | git             |
| Grafana                              | `/grafana`                    | ✔️   | git             |
| Grails Framework                     | `/grails`                     | ✔️   | git             |
| GStreamer                            | `/gstreamer`                  | ✔️   | git             |
| HAProxy                              | `/haproxy`                    | ✔️   | custom          |
| Hashicorp Consul                     | `/consul`                     | ✔️   | git             |
| Hashicorp Terraform                  | `/terraform`                  | ✔️   | git             |
| Hashicorp Vault                      | `/hashicorp-vault`            | ✔️   | git             |
| IBM AIX                              | `/ibm-aix`                    | ✔️   | custom          |
| Intel Processors                     | `/intel-processors`           | ❌    | n/a             |
| Internet Explorer                    | `/internet-explorer`          | ❌    | n/a             |
| Ionic Framework                      | `/ionic`                      | ✔️   | git             |
| ISC DHCP                             | `/isc-dhcp`                   | ❌    | n/a             |
| Istio                                | `/istio`                      | ✔️   | git             |
| Java/OpenJDK                         | `/java`                       | ✔️   | custom          |
| Jekyll                               | `/jekyll`                     | ✔️   | git             |
| Jenkins                              | `/jenkins`                    | ✔️   | git             |
| JHipster                             | `/jhipster`                   | ✔️   | npm             |
| Jira Software                        | `/jira-software`              | ❌    | n/a             |
| Joomla!                              | `/joomla`                     | ✔️   | git             |
| jQuery                               | `/jquery`                     | ✔️   | git             |
| JReleaser                            | `/jreleaser`                  | ✔️   | maven           |
| KDE Plasma                           | `/kde-plasma`                 | ✔️   | git             |
| Keycloak                             | `/keycloak`                   | ✔️   | git             |
| Kibana                               | `/kibana`                     | ✔️   | git             |
| Kotlin                               | `/kotlin`                     | ✔️   | npm             |
| Kubernetes                           | `/kubernetes`                 | ✔️   | git             |
| Laravel                              | `/laravel`                    | ✔️   | git             |
| LibreOffice                          | `/libreoffice`                | ❌    | n/a             |
| LineageOS                            | `/lineageos`                  | ❌    | n/a             |
| Linux Kernel                         | `/linux`                      | ✔️   | cgit            |
| Linux Mint                           | `/linuxmint`                  | ❌    | n/a             |
| Logstash                             | `/logstash`                   | ✔️   | git             |
| Looker                               | `/looker`                     | ❌    | n/a             |
| Mageia                               | `/mageia`                     | ✔️   | distrowatch     |
| Magento                              | `/magento`                    | ✔️   | git             |
| MariaDB                              | `/mariadb`                    | ✔️   | git             |
| Mastodon                             | `/mastodon`                   | ✔️   | git             |
| Mattermost                           | `/mattermost`                 | ✔️   | git             |
| MediaWiki                            | `/mediawiki`                  | ✔️   | git             |
| Micronaut Framework                  | `/micronaut`                  | ✔️   | git             |
| Microsoft .NET                       | `/dotnet`                     | ✔️   | git             |
| Microsoft .NET Framework             | `/dotnetfx`                   | ❌    | n/a             |
| Microsoft Build of OpenJDK           | `/microsoft-build-of-openjdk` | ✔️   | git             |
| Microsoft Exchange                   | `/msexchange`                 | ❌    | n/a             |
| Microsoft Office                     | `/office`                     | ❌    | n/a             |
| Microsoft PowerShell                 | `/powershell`                 | ✔️   | git             |
| Microsoft SharePoint                 | `/sharepoint`                 | ❌    | n/a             |
| Microsoft SQL Server                 | `/mssqlserver`                | ❌    | n/a             |
| Microsoft Surface                    | `/surface`                    | ❌    | n/a             |
| Microsoft Visual Studio              | `/visual-studio`              | ❌    | n/a             |
| Microsoft Windows                    | `/windows`                    | ❌    | n/a             |
| Microsoft Windows Embedded           | `/windows-embedded`           | ❌    | n/a             |
| Microsoft Windows Server             | `/windows-server`             | ❌    | n/a             |
| MongoDB Server                       | `/mongodb`                    | ✔️   | git             |
| Moodle                               | `/moodle`                     | ✔️   | git             |
| Mule Runtime                         | `/mulesoft-runtime`           | ❌    | n/a             |
| MX Linux                             | `/mxlinux`                    | ✔️   | distrowatch     |
| MySQL                                | `/mysql`                      | ✔️   | git             |
| Neo4j                                | `/neo4j`                      | ✔️   | git             |
| NetBSD                               | `/netbsd`                     | ❌    | n/a             |
| Netgear ReadyNAS                     | `/readynas`                   | ❌    | n/a             |
| Nextcloud                            | `/nextcloud`                  | ✔️   | git             |
| Nexus Repository OSS                 | `/nexus`                      | ✔️   | git             |
| nginx                                | `/nginx`                      | ✔️   | git             |
| nix                                  | `/nix`                        | ✔️   | git             |
| NixOS                                | `/nixos`                      | ❌    | n/a             |
| Node.js                              | `/nodejs`                     | ✔️   | git             |
| Nokia Mobile                         | `/nokia`                      | ❌    | n/a             |
| Nomad                                | `/nomad`                      | ✔️   | git             |
| NumPy                                | `/numpy`                      | ✔️   | pypi            |
| Nutanix AOS                          | `/nutanix-aos`                | ❌    | n/a             |
| Nutanix Files                        | `/nutanix-files`              | ❌    | n/a             |
| Nutanix Prism Central                | `/nutanix-prism`              | ❌    | n/a             |
| Nuxt                                 | `/nuxt`                       | ✔️   | npm             |
| NVIDIA Driver                        | `/nvidia`                     | ❌    | n/a             |
| NVIDIA GPUs                          | `/nvidia-gpu`                 | ❌    | n/a             |
| OpenBSD                              | `/openbsd`                    | ❌    | n/a             |
| OpenSearch                           | `/opensearch`                 | ✔️   | git             |
| OpenSSL                              | `/openssl`                    | ✔️   | git             |
| openSUSE                             | `/opensuse`                   | ❌    | n/a             |
| OpenWrt                              | `/openwrt`                    | ✔️   | git             |
| OpenZFS                              | `/openzfs`                    | ✔️   | git             |
| Oracle Database                      | `/oracle-database`            | ❌    | n/a             |
| Oracle Linux                         | `/oraclelinux`                | ✔️   | distrowatch     |
| Palo Alto Networks Cortex XDR agent  | `/cortex-xdr`                 | ❌    | n/a             |
| Palo Alto Networks GlobalProtect App | `/pangp`                      | ❌    | n/a             |
| Palo Alto Networks PAN-OS            | `/panos`                      | ❌    | n/a             |
| PCI-DSS                              | `/pci-dss`                    | ❌    | n/a             |
| Perl                                 | `/perl`                       | ✔️   | git             |
| PHP                                  | `/php`                        | ✔️   | custom          |
| phpBB                                | `/phpbb`                      | ✔️   | git             |
| phpMyAdmin                           | `/phpmyadmin`                 | ✔️   | git             |
| Plesk                                | `/plesk`                      | ✔️   | custom          |
| Pop!_OS                              | `/pop_os`                     | ❌    | n/a             |
| Postfix                              | `/postfix`                    | ✔️   | git             |
| PostgreSQL                           | `/postgresql`                 | ✔️   | git             |
| Proxmox VE                           | `/proxmox-ve`                 | ✔️   | distrowatch     |
| Python                               | `/python`                     | ✔️   | git             |
| Qt                                   | `/qt`                         | ✔️   | git             |
| Quarkus                              | `/quarkus-framework`          | ✔️   | git             |
| RabbitMQ                             | `/rabbitmq`                   | ✔️   | git             |
| Raspberry Pi                         | `/raspberry-pi`               | ❌    | n/a             |
| React                                | `/react`                      | ✔️   | npm             |
| Red Hat Enterprise Linux             | `/rhel`                       | ❌    | n/a             |
| Red Hat OpenShift                    | `/red-hat-openshift`          | ❌    | n/a             |
| Red Hat Satellite                    | `/redhat-satellite`           | ✔️   | custom          |
| Redis                                | `/redis`                      | ✔️   | git             |
| Redmine                              | `/redmine`                    | ✔️   | git             |
| Rocky Linux                          | `/rocky-linux`                | ✔️   | distrowatch     |
| ROS                                  | `/ros`                        | ❌    | n/a             |
| ROS2                                 | `/ros2`                       | ❌    | n/a             |
| Roundcube Webmail                    | `/roundcube`                  | ✔️   | git             |
| Ruby                                 | `/ruby`                       | ✔️   | git             |
| Ruby on Rails                        | `/rails`                      | ✔️   | git             |
| Samsung Mobile                       | `/samsung-mobile`             | ❌    | n/a             |
| Scala                                | `/scala`                      | ✔️   | git             |
| Silverstripe CMS                     | `/silverstripe`               | ✔️   | git             |
| Slackware Linux                      | `/slackware`                  | ✔️   | distrowatch     |
| SonarQube                            | `/sonar`                      | ✔️   | git             |
| Splunk                               | `/splunk`                     | ❌    | n/a             |
| Spring Boot                          | `/spring-boot`                | ✔️   | git             |
| Spring Framework                     | `/spring-framework`           | ✔️   | git             |
| SQLite                               | `/sqlite`                     | ✔️   | git             |
| Squid                                | `/squid`                      | ✔️   | git             |
| SUSE Linux Enterprise Server         | `/sles`                       | ❌    | n/a             |
| Symfony                              | `/symfony`                    | ✔️   | git             |
| Tails                                | `/tails`                      | ✔️   | distrowatch     |
| Tarantool                            | `/tarantool`                  | ✔️   | git             |
| Telegraf                             | `/telegraf`                   | ✔️   | git             |
| Twig                                 | `/twig`                       | ✔️   | git             |
| TYPO3                                | `/typo3`                      | ✔️   | git             |
| Ubuntu                               | `/ubuntu`                     | ✔️   | distrowatch     |
| Umbraco CMS                          | `/umbraco`                    | ✔️   | git             |
| Unity                                | `/unity`                      | ❌    | n/a             |
| UnrealIRCd                           | `/unrealircd`                 | ✔️   | custom          |
| Varnish                              | `/varnish`                    | ✔️   | git             |
| Visual COBOL                         | `/visual-cobol`               | ❌    | n/a             |
| VMware Cloud Foundation              | `/vmware-cloud-foundation`    | ❌    | n/a             |
| VMware ESXi                          | `/esxi`                       | ❌    | n/a             |
| VMware Horizon                       | `/horizon`                    | ❌    | n/a             |
| VMware Photon                        | `/photon`                     | ❌    | n/a             |
| VMware Site Recovery Manager         | `/vmware-srm`                 | ❌    | n/a             |
| VMware vCenter Server                | `/vcenter`                    | ❌    | n/a             |
| Vue                                  | `/vue`                        | ✔️   | npm             |
| Vuetify                              | `/vuetify`                    | ✔️   | npm             |
| Wagtail                              | `/wagtail`                    | ✔️   | git             |
| WordPress                            | `/wordpress`                  | ✔️   | git             |
| XCP-ng                               | `/xcp-ng`                     | ✔️   | git             |
| Yocto Project                        | `/yocto`                      | ✔️   | git             |
| Zabbix                               | `/zabbix`                     | ✔️   | git             |

This table has been generated by [report.py](/report.py).
