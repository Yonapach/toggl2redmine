# toggl2redmine
Script to synchronize toggle track and redmine. By default, it syncs for today.


https://user-images.githubusercontent.com/65816996/220307639-3ed4b024-3d11-47e2-bfb6-dd3007e95308.mov


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
