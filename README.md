# toggl2redmine
Script to synchronize toggle track and redmine. By default, it syncs for today.

## Installation
Create .env file and set values
```bash
touch .env
```
```
TOGGL_API_KEY=
REDMINE_API_KEY=
```
Build service
```bash
docker compose build
```

## Usage

```bash
docker compose up
```

### todo
- [x] Add docker
- [ ] Add command line arguments (date range)
