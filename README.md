# On-Demand Streaming Platform (Mini-Netflix)

## 1. Project Overview

**On-Demand Streaming Platform (Mini-Netflix)** is a database project that models a simplified online streaming platform.

The system is designed to manage:

* User accounts
* User profiles
* Subscription plans
* User subscriptions
* Movies
* TV series and episodes
* Watch history

The project focuses on applying **EER (Enhanced Entity-Relationship) modeling** to represent different types of streaming content and relationships between users, profiles, subscriptions, and content.

---

## 2. Project Objectives

The main objectives of this project are:

1. Design an EER diagram for an on-demand streaming platform.
2. Manage users and their profiles.
3. Manage subscription plans and user subscriptions.
4. Store movies and TV series episodes.
5. Track users' watch history.
6. Apply specialization/generalization to the `CONTENT` entity.
7. Convert the EER model into a relational database schema.
8. Apply database normalization principles.

---

## 3. System Scope

The system contains the following main functions:

### User Management

The system stores user account information, including:

* User ID
* Username
* Password
* Email
* Role

Each user can create multiple profiles.

---

### Profile Management

A profile represents an individual viewing profile created by a user.

Each profile contains:

* Profile ID
* User ID
* Profile name
* Birthdate

A user can create multiple profiles, while each profile belongs to exactly one user.

**Relationship:**

```text
USERS 1 ───── creates ───── N PROFILE
```

---

### Subscription Management

The system allows users to subscribe to a subscription plan.

A subscription contains:

* Subscription ID
* User ID
* Plan ID
* Status
* Start date
* End date

A subscription uses one subscription plan.

**Relationship:**

```text
USERS 1 ───── subscribes to ───── N SUBSCRIPTION
                                      |
                                      N
                                      |
                                    uses
                                      |
                                      1
                                      |
                              SUBSCRIPTION_PLAN
```

---

### Subscription Plans

The system provides different subscription plans.

Each plan contains:

* Plan ID
* Plan name
* Price
* Quality
* Maximum number of profiles

Example plans could include:

```text
Basic
Standard
Premium
```

The actual plans can be changed according to the project's requirements.

---

## 4. Content Management

`CONTENT` is the main entity used to represent streaming content.

Each content item contains:

* Content ID
* Title
* Description
* Release date
* Duration
* Content type

The EER model specializes `CONTENT` into two subtypes:

```text
                 CONTENT
                    |
                 is a
                /     \
               /       \
          MOVIES      EPISODE
```

---

## 5. Movie

`MOVIES` represents movie content.

It uses:

* Content ID

`CONTENT_ID` is both the primary key of `MOVIES` and a reference to the corresponding `CONTENT`.

Example:

```text
CONTENT
   |
   └── MOVIES
```

A movie inherits the common content information from `CONTENT`.

---

## 6. TV Series and Episodes

The system also supports TV series.

### TV_SERIES

`TV_SERIES` represents a television series.

Attributes:

* Series ID
* Series name

### EPISODE

`EPISODE` represents an individual episode of a TV series.

Attributes:

* Content ID
* Series ID
* Episode number
* Season number

Each episode belongs to exactly one TV series.

One TV series can contain many episodes.

**Relationship:**

```text
TV_SERIES 1 ───── belongs to ───── N EPISODE
```

---

## 7. Watch History

The `WATCH_HISTORY` entity records the content watched by profiles.

It contains:

* Watch History ID
* Profile ID
* Content ID
* Watch duration
* Completed status

The relationships are:

```text
PROFILE 1 ───── watches ───── N WATCH_HISTORY

WATCH_HISTORY N ───── on ───── 1 CONTENT
```

This means:

* One profile can have many watch history records.
* Each watch history record belongs to one profile.
* One content item can appear in many watch history records.
* Each watch history record refers to one content item.

This allows the system to track what content a profile has watched and whether the content was completed.

---

## 8. Main Entities

| Entity                | Description                                       |
| --------------------- | ------------------------------------------------- |
| **USERS**             | Stores user account information                   |
| **PROFILE**           | Stores viewing profiles created by users          |
| **SUBSCRIPTION**      | Stores user subscription information              |
| **SUBSCRIPTION_PLAN** | Stores available subscription plans               |
| **WATCH_HISTORY**     | Records content watched by profiles               |
| **CONTENT**           | Stores common information about streaming content |
| **MOVIES**            | Represents movie content                          |
| **EPISODE**           | Represents individual TV series episodes          |
| **TV_SERIES**         | Stores TV series information                      |

---

## 9. Entity Relationships

The main relationships in the EER diagram are:

| Relationship                     | Cardinality        | Description                                      |
| -------------------------------- | ------------------ | ------------------------------------------------ |
| USERS → PROFILE                  | 1:N                | One user can create multiple profiles            |
| USERS → SUBSCRIPTION             | 1:N                | One user can have multiple subscription records  |
| SUBSCRIPTION → SUBSCRIPTION_PLAN | N:1                | Many subscriptions can use the same plan         |
| PROFILE → WATCH_HISTORY          | 1:N                | One profile can have many watch history records  |
| WATCH_HISTORY → CONTENT          | N:1                | Many watch records can refer to the same content |
| CONTENT → MOVIES/EPISODE         | 1:1 specialization | Content is specialized into movie or episode     |
| TV_SERIES → EPISODE              | 1:N                | One TV series can contain many episodes          |

---

## 10. EER Specialization

One of the main database challenges is modeling different types of content.

The `CONTENT` entity acts as a **superclass**.

Its subtypes are:

* `MOVIES`
* `EPISODE`

```text
                       CONTENT
                          |
                    Specialization
                     /           \
                    /             \
                MOVIES          EPISODE
                                  |
                                  |
                              belongs to
                                  |
                                  N
                                  |
                              TV_SERIES
```

Common attributes such as title, description, release date, and duration are stored in `CONTENT`.

Specific information is stored in the corresponding subtype.

---

## 11. Business Rules

The following business rules are derived from the EER diagram:

1. Each user must have a unique `USER_ID`.
2. A user can create multiple profiles.
3. Each profile belongs to one user.
4. A user can have multiple subscription records.
5. Each subscription belongs to one user.
6. Each subscription uses one subscription plan.
7. A subscription plan can be used by multiple subscriptions.
8. Each profile can have multiple watch history records.
9. Each watch history record belongs to one profile.
10. Each watch history record refers to one content item.
11. One content item can appear in multiple watch history records.
12. Content can be classified as a movie or an episode.
13. Each episode belongs to one TV series.
14. One TV series can contain multiple episodes.
15. `CONTENT_ID`, `USER_ID`, `PROFILE_ID`, `SUBSCRIPTION_ID`, `PLAN_ID`, `WATCH_HISTORY_ID`, and `SERIES_ID` uniquely identify their respective records.

---

## 12. Database Constraints

### Primary Key Constraints

Each main entity has a unique primary key:

```text
USERS              → USER_ID
PROFILE            → PROFILE_ID
SUBSCRIPTION       → SUBSCRIPTION_ID
SUBSCRIPTION_PLAN  → PLAN_ID
WATCH_HISTORY      → WATCH_HISTORY_ID
CONTENT            → CONTENT_ID
TV_SERIES          → SERIES_ID
```

`MOVIES` and `EPISODE` use `CONTENT_ID` to identify their corresponding content.

---

### Foreign Key Constraints

Examples:

```text
PROFILE.USER_ID
        ↓
USERS.USER_ID
```

```text
SUBSCRIPTION.USER_ID
        ↓
USERS.USER_ID
```

```text
SUBSCRIPTION.PLAN_ID
        ↓
SUBSCRIPTION_PLAN.PLAN_ID
```

```text
WATCH_HISTORY.PROFILE_ID
        ↓
PROFILE.PROFILE_ID
```

```text
WATCH_HISTORY.CONTENT_ID
        ↓
CONTENT.CONTENT_ID
```

```text
EPISODE.SERIES_ID
        ↓
TV_SERIES.SERIES_ID
```

These constraints maintain referential integrity between related tables.

---

## 13. Logical Schema

The EER diagram can be mapped into the following relational schema:

```text
USERS(
    USER_ID PK,
    USERNAME,
    PASSWORD,
    EMAIL,
    ROLE
)

PROFILE(
    PROFILE_ID PK,
    USER_ID FK,
    PROFILE_NAME,
    BIRTHDATE
)

SUBSCRIPTION_PLAN(
    PLAN_ID PK,
    PLAN_NAME,
    PRICE,
    QUALITY,
    MAX_PROFILES
)

SUBSCRIPTION(
    SUBSCRIPTION_ID PK,
    USER_ID FK,
    PLAN_ID FK,
    STATUS,
    START_DATE,
    END_DATE
)

CONTENT(
    CONTENT_ID PK,
    TITLE,
    DESCRIPTION,
    RELEASE_DATE,
    DURATION,
    CONTENT_TYPE
)

MOVIES(
    CONTENT_ID PK, FK
)

TV_SERIES(
    SERIES_ID PK,
    SERIES_NAME
)

EPISODE(
    CONTENT_ID PK, FK,
    SERIES_ID FK,
    EPISODE_NUMBER,
    SEASON_NUMBER
)

WATCH_HISTORY(
    WATCH_HISTORY_ID PK,
    PROFILE_ID FK,
    CONTENT_ID FK,
    WATCH_DURATION,
    COMPLETED
)
```

---

## 14. Database Design Flow

The project follows this development process:

```text
Requirements
     ↓
Business Rules
     ↓
EER Diagram
     ↓
Logical Schema Mapping
     ↓
Normalization
     ↓
SQL Implementation
     ↓
Testing
```

---

## 15. Normalization

The database design should be checked using:

* **1NF – First Normal Form**
* **2NF – Second Normal Form**
* **3NF – Third Normal Form**
* **BCNF – Boyce-Codd Normal Form**, where applicable

Normalization helps:

* Reduce data redundancy
* Prevent update anomalies
* Maintain data consistency
* Improve database organization

---

## 16. Suggested Project Structure

```text
Mini-Netflix/
│
├── README.md
│
├── docs/
│   ├── EER_Diagram.png
│   ├── Logical_Schema.png
│   └── Project_Report.docx
│
├── database/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   └── queries.sql
│
└── presentation/
    └── Mini_Netflix_Presentation.pptx
```

---

## 17. Technologies

The project can be implemented using:

* **EER Diagram** – Conceptual database design
* **SQL** – Database implementation
* **MySQL / SQL Server / PostgreSQL** – Database Management System
* **Git & GitHub** – Version control
* **Microsoft Word** – Project report
* **Microsoft PowerPoint** – Presentation

---

## 18. Project Deliverables

The project includes:

* [x] Project description
* [x] Business rules and constraints
* [x] EER diagram
* [x] EER specialization/generalization
* [x] Logical schema mapping
* [x] Normalization analysis
* [x] Data dictionary
* [x] SQL table creation
* [x] Sample data
* [x] SQL queries
* [x] Project report
* [x] Presentation

---

## 19. Conclusion

The **On-Demand Streaming Platform (Mini-Netflix)** project demonstrates the design of a relational database for a simplified streaming service.

The EER model manages users, profiles, subscriptions, subscription plans, content, movies, TV series, episodes, and watch history.

The most important database concepts demonstrated in this project are:

* **Entity-Relationship modeling**
* **1:N relationships**
* **Specialization / Generalization**
* **Primary and foreign keys**
* **Referential integrity**
* **Logical schema mapping**
* **Database normalization**

The final database provides a structured foundation for managing an on-demand streaming platform.
