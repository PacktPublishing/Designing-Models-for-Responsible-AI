# Atlas setup on any Linux VM

## _Atlas on Linux VM Deployment Guide_


- The first step is to install Apache Atlas (>= 2.x.x) from GitHub

	```sh
     wget  http://mirrors.estointernet.in/apache/atlas/2.0.0/apache-atlas-2.0.0-sources.tar.gz
	```

- The next step is to build Apache Atlas and package it, using the following steps.

	```sh
	tar xvfz apache-atlas-2.0.0-sources.tar.gz 
	cd apache-atlas-sources-1.0.0/ 
	export MAVEN_OPTS="-Xms2g -Xmx2g" 
	mvn clean -DskipTests install
	mvn clean -DskipTests package -Pdist
	mvn clean -DskipTests package -Pdist,embedded-hbase-solr
	mvn clean package -Pdist,embedded-cassandra-solr
	```
- Apache Atlas packages are created at

	```
	distro/target/apache-atlas-2.0.0-bin.tar.gz 
	distro/target/apache-atlas-2.0.0-hbase-hook.tar.gz
	distro/target/apache-atlas--2.0.0--hive-hook.gz 
	distro/target/apache-atlas--2.0.0--kafka-hook.gz
	distro/target/apache-atlas--2.0.0--sources.tar.gz 
	distro/target/apache-atlas-2.0.0--sqoop-hook.tar.gz
	distro/target/apache-atlas--2.0.0--storm-hook.tar.gz
	```

- Installing and running Apache Atlas

	```
	tar -xzvf apache-atlas-2.0.0-server.tar.gz  
 	cd atlas-2.0.0-server
 	```

- To run Apache Atlas with Solr and HBase we use the following
 	
 	```
 	export MANAGE_LOCAL_HBASE=true 
 	export MANAGE_LOCAL_SOLR=true 
 	```

-  When you are building with embedded Apache HBase & Apache Solr , remember to add JAVA_HOME. in conf/atlas-env.sh, and execute it as ./conf/	   atlas-env.sh, before starting Atlas server.

- To start and stop Apache Atlas server

	```
	bin/atlas_start.py
	bin/atlas_stop.py
	```
- To verify Apache Atlas server is running

	```
	curl -u admin:admin http://localhost:21000/api/atlas/admin/version 
	```

- Call Apacge Atlas using REST API

	```
	 curl -u admin:admin http://localhost:21000/api/atlas/v2/types/typedefs/headers 
	```

- Receive the response as
	```
	[ {"guid":"fa421be8-c21b-4cf8-a226-fdde559ad598","name":"Referenceable","category":"ENTITY"}, {"guid":"7f3f5712-521d-450d-9bb2-ba996b6f2a4e","name":"Asset","category":"ENTITY"}, {"guid":"84b02fa0-e2f4-4cc4-8b24-d2371cd00375","name":"DataSet","category":"ENTITY"}, {"guid":"f93975d5-5a5c-41da-ad9d-eb7c4f91a093","name":"Process","category":"ENTITY"}, {"guid":"79dcd1f9-f350-4f7b-b706-5bab416f8206","name":"Infrastructure","category":"ENTITY"} ]
	```
