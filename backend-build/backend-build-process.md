# Backend Service Docker Builds
The following backend services are written using Spring Boot with Maven and are configured to be built as Docker images:
1. Authentication Service
2. Customers service
3. Flights service
4. Tickets service
5. Orchestration service (to be migrated to API Gateway and AWS Lambda)
6. Eureka Service Discovery server
7. Cloud Configuration Service (provides runtime configuration properties to above)


## Image Repository (AWS ECR)
Each of these services are containerized and pushed to AWS Elastic Container Registry at `247293358719.dkr.ecr.us-east-1.amazonaws.com`.

For building and pushing Docker images, we are using the [fabric8io/docker-maven-plugin](https://dmp.fabric8.io/) for a very simple, overall process. This plugin allows us to use Maven for the entire build and image deploy process with a single command:

```sh
mvn clean package docker:build docker:push
```

## Image Push Authorization
In order for images to be pushed to the ECR registry, the host machine performing the build must have AWS ECR IAM permissions configured either through the `aws-cli` tool, or with an IAM role (for EC2 instances) that allows pushes to the repository. Additionally, the Docker client must be logged into ECR to allow a push.

This can be accomplished with the following command:
```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 247293358719.dkr.ecr.us-east-1.amazonaws.com
```

## Dockerfile
The fabric8 plugin requires the Dockerfile to live within the Maven configured source paths, notably `${root_project_dir}/src/main/docker/Dockerfile`, where `root_project_dir` is the location of the project on the local machine.

The Dockerfile is configured for layered builds, increasing the efficiency of image builds and storage overall. It builds the required libraries and source within the Maven build context and the compiled bytecode is copied to and used for running each individual service.

The following is an example Dockerfile that can be used for all services:
```dockerfile
FROM openjdk:11-jre-slim as builder
WORKDIR application
ADD maven/${project.build.finalName}.jar ${project.build.finalName}.jar
RUN java -Djarmode=layertools -jar ${project.build.finalName}.jar extract

FROM openjdk:11-jre-slim
LABEL PROJECT_NAME=${project.artifactId} \
      PROJECT=${project.id}

EXPOSE 8080

WORKDIR application
COPY --from=builder application/dependencies/ ./
COPY --from=builder application/spring-boot-loader/ ./
COPY --from=builder application/snapshot-dependencies/ ./
COPY --from=builder application/application/ ./
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "org.springframework.boot.loader.JarLauncher"]
```

Dependent on the service, a port exposure may differ (ie `8888` for the configuration server and `8761` for the Eureka service). These ports can be mapped as appropriate by the controlling layer (AWS ECS or Docker-Compose).

## Required Maven Dependencies
To accomplish this simple build process, some configuration properties must be set in the project `pom.xml`. Notably, project properties must be set for the `docker.image.name` and `docker.image.prefix` as such:
```xml
<properties>
    ... other properties
    <docker.image.prefix>ss-utopia</docker.image.prefix>
    <docker.image.name>SERVICE NAME</docker.image.name>
  </properties>
```
In the above example, `SERVICE NAME` should be the only thing differing between projects.

Additionally, the following plugin must be added:
```xml
  <build>
    <plugins>
      ... other plugins

      <plugin>
        <groupId>pl.project13.maven</groupId>
        <artifactId>git-commit-id-plugin</artifactId>
        <version>4.0.0</version>
        <executions>
          <execution>
            <id>get-the-git-infos</id>
            <goals>
              <goal>revision</goal>
            </goals>
            <phase>initialize</phase>
          </execution>
        </executions>
        <configuration>
          <generateGitPropertiesFile>true</generateGitPropertiesFile>
          <generateGitPropertiesFilename>${project.build.outputDirectory}/git.properties
          </generateGitPropertiesFilename>
          <includeOnlyProperties>
            <includeOnlyProperty>^git.branch$</includeOnlyProperty>
            <includeOnlyProperty>^git.commit.id.abbrev$</includeOnlyProperty>
          </includeOnlyProperties>
          <commitIdGenerationMode>full</commitIdGenerationMode>
        </configuration>
      </plugin>

      <plugin>
        <groupId>io.fabric8</groupId>
        <artifactId>docker-maven-plugin</artifactId>
        <version>0.33.0</version>
        <configuration>
          <verbose>true</verbose>
          <images>
            <image>
              <name>${docker.image.prefix}/${docker.image.name}</name>
              <alias>${project.artifactId}</alias>
              <registry>247293358719.dkr.ecr.us-east-1.amazonaws.com</registry>
              <build>
                <assembly>
                  <descriptorRef>artifact</descriptorRef>
                </assembly>
                <dockerFile>Dockerfile</dockerFile>
                <tags>
                  <tag>latest</tag>
                  <tag>${git.branch}.${git.commit.id.abbrev}.${project.version}</tag>
                </tags>
              </build>
            </image>
          </images>
        </configuration>
      </plugin>

    </plugins>
  </build>
```
This plugin should be as-is with no modifications.

## Build Tags
Build tags are provided by the [Maven Git Commit ID Plugin](https://github.com/git-commit-id/git-commit-id-maven-plugin). As seen in the `pom.xml` snippet above, in the `fabric8` plugin, all build tags will be structured as `branch.commit.version`. As an example, on the `dev` branch with abbreviated commit ID of `a22559b` on version `1.1-SNAPSHOT`, the tag will be parsed as `dev.a22559b.1.1-SNAPSHOT`.


An additional tag of `latest` will be used to keep the repository updated with the latest builds anytime a build/push occurs.
