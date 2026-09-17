# Database Project Report

**Project ID & Title:** On-Demand Streaming Platform (Mini-Netflix)

---

## A. Project Identity

**Team Name:** Group 3 – CHANG LINH NGU LAM

**Team Members:**

1. **Lê Ngọc Dũng** — n24dece065@student.ptithcm.edu.vn
2. **Lê Phạm Khánh Huy** — n24dece072@student.ptithcm.edu.vn
3. **Phan Giảng Bình** — n24dece056@student.ptithcm.edu.vn

**Project Title:** On-Demand Streaming Platform (Mini-Netflix)

---

## B. Report Structure

### 1. Introduction & Project Scope

*(Adapted from ISO/IEC/IEEE 29148)*

An on-demand streaming platform needs to manage a large amount of information every day, including user accounts, user profiles, subscription plans, subscriptions, movies, TV series episodes, and watch histories. If this information is not organized properly, it may lead to duplicated data, inconsistent records, or difficulties in tracking users' viewing activities.

The **On-Demand Streaming Platform (Mini-Netflix)** is designed as a centralized database system for managing the basic operations of a streaming service. The system focuses on managing users, profiles, subscriptions, subscription plans, content, movies, TV series, episodes, and watch history.

The database also uses an **EER specialization** for the `CONTENT` entity. Content is divided into two subtypes: `MOVIES` and `EPISODE`. This allows common content information to be stored in the `CONTENT` entity while specific information is stored in the corresponding subtype.

---

### 1.1 System Objective

The main objective of the system is to provide a structured database for storing and managing essential information of an on-demand streaming platform.

The system is designed to:

* Store and manage user account information.
* Store and manage user profiles.
* Allow users to create multiple profiles.
* Manage subscription information.
* Manage different subscription plans.
* Store plan price, quality, and maximum number of profiles.
* Store and manage streaming content.
* Classify content into Movies and Episodes.
* Store TV series information.
* Associate episodes with their corresponding TV series.
* Maintain users' watch history.
* Store watch duration and completion status.
* Maintain relationships between profiles and watched content.
* Maintain data consistency through primary keys and foreign keys.

---

### 1.2 Business Rules & Constraints

#### 1.2.1 User and Profile

* **BR1:** Each User must have a unique `USER_ID`.
* **BR2:** A User may create many Profiles.
* **BR3:** Each Profile must belong to exactly one User.
* **BR4:** Each Profile must have a unique `PROFILE_ID`.
* **BR5:** A Profile contains a profile name and birthdate.

#### 1.2.2 Subscription and Subscription Plan

* **BR6:** Each Subscription must have a unique `SUBSCRIPTION_ID`.
* **BR7:** A User may have many Subscription records.
* **BR8:** Each Subscription must belong to exactly one User.
* **BR9:** Each Subscription must use exactly one Subscription Plan.
* **BR10:** One Subscription Plan may be used by many Subscriptions.
* **BR11:** Each Subscription Plan must have a unique `PLAN_ID`.
* **BR12:** A Subscription Plan stores the plan name, price, quality, and maximum number of profiles.
* **BR13:** Each Subscription must contain a status, start date, and end date.

#### 1.2.3 Content

* **BR14:** Each Content item must have a unique `CONTENT_ID`.
* **BR15:** Each Content item stores a title, description, release date, duration, and content type.
* **BR16:** Content is specialized into Movies and Episodes.
* **BR17:** Each Movie references one existing Content item.
* **BR18:** Each Episode references one existing Content item.

#### 1.2.4 TV Series and Episode

* **BR19:** Each TV Series must have a unique `SERIES_ID`.
* **BR20:** Each TV Series must have a series name.
* **BR21:** An Episode must belong to exactly one TV Series.
* **BR22:** One TV Series may contain many Episodes.
* **BR23:** Each Episode must have an episode number and season number.
* **BR24:** `EPISODE.SERIES_ID` must reference an existing `TV_SERIES.SERIES_ID`.

#### 1.2.5 Watch History

* **BR25:** Each Watch History record must have a unique `WATCH_HISTORY_ID`.
* **BR26:** A Profile may have many Watch History records.
* **BR27:** Each Watch History record must belong to exactly one Profile.
* **BR28:** One Content item may appear in many Watch History records.
* **BR29:** Each Watch History record must reference exactly one Content item.
* **BR30:** Watch History stores the watch duration and whether the content was completed.
* **BR31:** `WATCH_HISTORY.PROFILE_ID` must reference an existing Profile.
* **BR32:** `WATCH_HISTORY.CONTENT_ID` must reference an existing Content item.

---

### 1.2.6 Main Constraints

The database design applies the following major constraints:

* `USER_ID` must be unique.
* `PROFILE_ID` must be unique.
* `SUBSCRIPTION_ID` must be unique.
* `PLAN_ID` must be unique.
* `WATCH_HISTORY_ID` must be unique.
* `CONTENT_ID` must be unique.
* `SERIES_ID` must be unique.
* `PROFILE.USER_ID` must reference an existing User.
* `SUBSCRIPTION.USER_ID` must reference an existing User.
* `SUBSCRIPTION.PLAN_ID` must reference an existing Subscription Plan.
* `WATCH_HISTORY.PROFILE_ID` must reference an existing Profile.
* `WATCH_HISTORY.CONTENT_ID` must reference an existing Content.
* `MOVIES.CONTENT_ID` must reference an existing Content.
* `EPISODE.CONTENT_ID` must reference an existing Content.
* `EPISODE.SERIES_ID` must reference an existing TV Series.
* An Episode cannot belong to a non-existing TV Series.
* A Subscription cannot use a non-existing Subscription Plan.

These constraints help maintain **referential integrity and data consistency** throughout the database.

---

## 2. Database Design

*(ISO/IEC 19505 / IE Standards)*

### 2.1 Conceptual Model (ER/EER Diagram)

The conceptual database model is represented using an **Enhanced Entity-Relationship (EER) diagram**.

The main entities in the system are:

* `USERS`
* `PROFILE`
* `SUBSCRIPTION`
* `SUBSCRIPTION_PLAN`
* `WATCH_HISTORY`
* `CONTENT`
* `MOVIES`
* `EPISODE`
* `TV_SERIES`

The EER model contains several important relationships:

```text
USERS 1 ───── creates ───── N PROFILE

USERS 1 ───── subscribes to ───── N SUBSCRIPTION

SUBSCRIPTION N ───── uses ───── 1 SUBSCRIPTION_PLAN

PROFILE 1 ───── watches ───── N WATCH_HISTORY

WATCH_HISTORY N ───── on ───── 1 CONTENT

CONTENT 1 ───── is a ───── MOVIES
                    \
                     └──── EPISODE

EPISODE N ───── belongs to ───── 1 TV_SERIES
```

#### EER Specialization

The `CONTENT` entity is the superclass of two specialized entities:

```text
                    CONTENT
                       |
                      is a
                    /     \
                   /       \
              MOVIES      EPISODE
                            |
                         belongs to
                            |
                        TV_SERIES
```

`CONTENT` stores attributes common to streaming content:

* `CONTENT_ID`
* `TITLE`
* `DESCRIPTION`
* `RELEASE_DATE`
* `DURATION`
* `CONTENT_TYPE`

`MOVIES` represents movie content and uses `CONTENT_ID`.

`EPISODE` represents TV series episodes and contains:

* `CONTENT_ID`
* `SERIES_ID`
* `EPISODE_NUMBER`
* `SEASON_NUMBER`

---

### Entity Overview

| **Entity**            | **Primary Key (PK)** | **Purpose**                                        |
| --------------------- | -------------------- | -------------------------------------------------- |
| **USERS**             | `USER_ID`            | Stores user account information.                   |
| **PROFILE**           | `PROFILE_ID`         | Stores profiles created by users.                  |
| **SUBSCRIPTION**      | `SUBSCRIPTION_ID`    | Stores user subscription information.              |
| **SUBSCRIPTION_PLAN** | `PLAN_ID`            | Stores available subscription plans.               |
| **WATCH_HISTORY**     | `WATCH_HISTORY_ID`   | Stores records of content watched by profiles.     |
| **CONTENT**           | `CONTENT_ID`         | Stores common information about streaming content. |
| **MOVIES**            | `CONTENT_ID` (FK)    | Represents movie content as a subtype of Content.  |
| **EPISODE**           | `CONTENT_ID` (FK)    | Represents an episode as a subtype of Content.     |
| **TV_SERIES**         | `SERIES_ID`          | Stores TV series information.                      |

---

### Entity Attributes

#### USERS

| Attribute  | Data Type   | Description                  |
| ---------- | ----------- | ---------------------------- |
| `USER_ID`  | varchar(20) | Unique identifier of a user. |
| `USERNAME` | varchar(20) | User's username.             |
| `PASSWORD` | varchar(20) | User's password.             |
| `EMAIL`    | varchar(25) | User's email address.        |

#### PROFILE

| Attribute      | Data Type   | Description                          |
| -------------- | ----------- | ------------------------------------ |
| `PROFILE_ID`   | varchar(20) | Unique identifier of a profile.      |
| `USER_ID`      | varchar(20) | References the owner of the profile. |
| `PROFILE_NAME` | varchar(20) | Name of the profile.                 |
| `BIRTHDATE`    | date        | Profile's birthdate.                 |

#### SUBSCRIPTION

| Attribute         | Data Type   | Description                       |
| ----------------- | ----------- | --------------------------------- |
| `SUBSCRIPTION_ID` | varchar(20) | Unique subscription identifier.   |
| `USER_ID`         | varchar(20) | References the subscribed user.   |
| `PLAN_ID`         | varchar(20) | References the subscription plan. |
| `STATUS`          | varchar(10) | Current subscription status.      |
| `START_DATE`      | date        | Subscription start date.          |
| `END_DATE`        | date        | Subscription end date.            |

#### SUBSCRIPTION_PLAN

| Attribute      | Data Type   | Description                             |
| -------------- | ----------- | --------------------------------------- |
| `PLAN_ID`      | varchar(20) | Unique identifier of a plan.            |
| `PLAN_NAME`    | varchar(20) | Name of the subscription plan.          |
| `PRICE`        | int         | Price of the plan.                      |
| `QUALITY`      | varchar(15) | Streaming quality provided by the plan. |
| `MAX_PROFILES` | int         | Maximum number of profiles allowed.     |

#### CONTENT

| Attribute      | Data Type   | Description                                |
| -------------- | ----------- | ------------------------------------------ |
| `CONTENT_ID`   | varchar(20) | Unique identifier of content.              |
| `TITLE`        | varchar(20) | Title of the content.                      |
| `DESCRIPTION`  | text        | Description of the content.                |
| `RELEASE_DATE` | date        | Content release date.                      |
| `DURATION`     | int         | Duration of the content.                   |
| `CONTENT_TYPE` | varchar(10) | Type of content, such as Movie or Episode. |

#### MOVIES

| Attribute    | Data Type   | Description                                      |
| ------------ | ----------- | ------------------------------------------------ |
| `CONTENT_ID` | varchar(20) | Primary key and foreign key referencing Content. |

#### TV_SERIES

| Attribute     | Data Type   | Description                       |
| ------------- | ----------- | --------------------------------- |
| `SERIES_ID`   | varchar(20) | Unique identifier of a TV series. |
| `SERIES_NAME` | varchar(50) | Name of the TV series.            |

#### EPISODE

| Attribute        | Data Type   | Description                                      |
| ---------------- | ----------- | ------------------------------------------------ |
| `CONTENT_ID`     | varchar(20) | Primary key and foreign key referencing Content. |
| `SERIES_ID`      | varchar(20) | Foreign key referencing TV Series.               |
| `EPISODE_NUMBER` | int         | Episode number within a series/season.           |
| `SEASON_NUMBER`  | int         | Season number of the episode.                    |

#### WATCH_HISTORY

| Attribute          | Data Type   | Description                                      |
| ------------------ | ----------- | ------------------------------------------------ |
| `WATCH_HISTORY_ID` | varchar(20) | Unique identifier of a watch history record.     |
| `PROFILE_ID`       | varchar(20) | References the profile that watched the content. |
| `CONTENT_ID`       | varchar(20) | References the watched content.                  |
| `WATCH_DURATION`   | int         | Amount of content watched.                       |
| `COMPLETED`        | boolean     | Indicates whether the content was completed.     |

---

### 2.2 Logical Schema Mapping

The EER model is mapped into the following relational schema:

```text
USERS(
    USER_ID PK,
    USERNAME,
    PASSWORD,
    EMAIL
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

### 2.3 Normalization Verification

The database design should be verified according to the following normalization levels:

#### First Normal Form (1NF)

Each table contains atomic values, and each record is uniquely identified by a primary key.

#### Second Normal Form (2NF)

The tables should have no partial dependency of non-key attributes on part of a composite primary key.

#### Third Normal Form (3NF)

Non-key attributes should depend only on the primary key and not on other non-key attributes.

#### BCNF

Where applicable, every determinant should be a candidate key.

Normalization is used to:

* Reduce data redundancy.
* Prevent update anomalies.
* Improve data consistency.
* Maintain a clear database structure.

---

## 3. Project Structure

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

## 4. Technologies

* **EER Diagram** – Conceptual database modeling
* **SQL** – Database implementation
* **MySQL / SQL Server / PostgreSQL** – Database Management System
* **Git & GitHub** – Version control and project management
* **Microsoft Word** – Project documentation
* **Microsoft PowerPoint** – Project presentation

---

## 5. Conclusion

The **On-Demand Streaming Platform (Mini-Netflix)** project demonstrates how an EER model can be used to design a database for an online streaming service.

The system manages users, profiles, subscriptions, subscription plans, content, movies, TV series, episodes, and watch history.

The project demonstrates important database concepts including:

* Entity-Relationship Modeling
* EER Specialization
* One-to-Many Relationships
* Primary Keys and Foreign Keys
* Referential Integrity
* Logical Schema Mapping
* Database Normalization

The resulting database provides a structured foundation for managing the core operations of a simplified on-demand streaming platform.

---

**Project:** On-Demand Streaming Platform (Mini-Netflix)
**Team:** Group 3 – CHANG LINH NGU LAM
