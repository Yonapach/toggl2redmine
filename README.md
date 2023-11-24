# toggl2redmine

Script to synchronize Toggl Track and Redmine

https://user-images.githubusercontent.com/65816996/220307639-3ed4b024-3d11-47e2-bfb6-dd3007e95308.mov

## Installation

Create a `.env` file and set values:

```bash
touch .env
```

```
TOGGL_API_KEY=
REDMINE_API_KEY=
REDMINE_URL=
REDMINE_ACTIVITY_ID=
```

Build the service:

```bash
docker compose build
```

### Additional Options

You can use the `days_offset` parameter to specify how many days ago the program should synchronize. Add the following
line to your `.env` file:

```
DAYS_OFFSET=1
```

In this example, yesterday's data will be synchronized.

## Usage

```bash
docker compose up
```