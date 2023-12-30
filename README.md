# toggl2redmine

Script to synchronize Toggl Track and Redmine

* Toggl project is Redmine task_id
* Toggl description is Redmine comment

### Installation

#### Dotenv

```bash
touch .env
```

```dotenv
TOGGL_API_KEY=
REDMINE_API_KEY=
REDMINE_URL=
REDMINE_ACTIVITY_ID=
```

#### Optional

```dotenv
TOGGL_DAYS_OFFSET=0
REDMINE_ROUND_COSTS=false
REDMINE_DEFAULT_COMMENT='Выполнение требований задачи'
```

#### Build the service

```bash
docker compose build
```

### Usage

```bash
docker compose up
```