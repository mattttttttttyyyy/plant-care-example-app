# H2 Database for Local Development

H2 Database is a lightweight, open-source relational database written in Java. It offers several advantages for local development and testing:

* **Embedded Mode:** H2 can run in embedded mode, operating directly within your Java application's JVM. No separate database server process is required.
* **No External Dependencies:** Users can simply clone the project and run it without installing any external database software.
* **File-Based Persistence:** Data can be stored in local files, ensuring persistence between application restarts.
* **In-Memory Option:** For rapid testing or scenarios where data persistence isn't needed, H2 can also run entirely in memory, with data being lost upon application shutdown.
* **SQL Compatibility:** H2 supports a large subset of standard SQL.

## Configuration Steps

Follow these steps to configure your project to use H2 Database:

### Step 1: Add H2 Dependency

In your `pom.xml` file, add:

```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

### Step 2: Configure H2 Connection

In your `src/main/resources/application.properties` file, set:

```properties
spring.datasource.url=jdbc:h2:file:./data/your_app_db
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=password
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```

- `jdbc:h2:file:./data/your_app_db` – the database will be stored as a file in the `data` directory.
- The H2 console will be available at `/h2-console`.

**Optionally, for testing you can use an in-memory database:**

```properties
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=password
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```

### Step 3: Schema and Data Initialization

If you want, you can add `schema.sql` and `data.sql` files to the `src/main/resources/` directory to automatically create tables and initial data at application startup. This is not required if your application creates tables via JPA/Hibernate.

### Step 4: Testing

Run your application and verify the connection to the H2 database. The H2 console will be available at [http://localhost:8080/h2-console](http://localhost:8080/h2-console).

---

**Note:**
Since the project has never been run before, you do not need to perform any migrations or data transfers. H2 will create a new database on the first application startup.
