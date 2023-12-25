# toggl2redmine

Script to synchronize Toggl Track and Redmine

https://user-images.githubusercontent.com/65816996/220307639-3ed4b024-3d11-47e2-bfb6-dd3007e95308.mov

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
ROUND_COSTS=
DAYS_OFFSET=
```

#### Build the service
```bash
docker compose build
```

### Usage
```bash
docker compose up
```