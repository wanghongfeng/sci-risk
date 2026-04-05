FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY backend/pom.xml .
COPY backend/risk-basic-service/pom.xml ./risk-basic-service/
RUN mvn dependency:go-offline -B -f risk-basic-service/pom.xml
COPY backend/risk-basic-service/src ./risk-basic-service/src
RUN mvn package -DskipTests -B -f risk-basic-service/pom.xml

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/risk-basic-service/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
