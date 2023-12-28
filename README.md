# toggl2redmine

Script to synchronize Toggl Track and Redmine

* Project is redmine task id
* Description is comment

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
```

#### Build the service

```bash
docker compose build
```

### Usage

```bash
docker compose up
```