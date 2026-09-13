-- Llanwrtyd Lights — SQLite schema (local development only)
-- The live site uses schema.mysql.sql.

CREATE TABLE IF NOT EXISTS houses (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  stop_no       INT NOT NULL,
  name          TEXT NOT NULL,
  address       TEXT NOT NULL,
  blurb_en      TEXT NOT NULL,
  blurb_cy      TEXT NULL,
  note_en       TEXT NULL,
  note_cy       TEXT NULL,
  walk_en       TEXT NULL,
  walk_cy       TEXT NULL,
  lat           REAL NULL,
  lng           REAL NULL,
  token         TEXT NOT NULL,
  active        INTEGER NOT NULL DEFAULT 1,
  UNIQUE (token),
  UNIQUE (stop_no)
);

CREATE TABLE IF NOT EXISTS categories (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  slug          TEXT NOT NULL,
  label_en      TEXT NOT NULL,
  label_cy      TEXT NOT NULL,
  sort_order    INT NOT NULL DEFAULT 0,
  UNIQUE (slug)
);

-- One row per device per house. The UNIQUE key is what makes a repeat
-- scan harmless rather than a duplicate.
CREATE TABLE IF NOT EXISTS checkins (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id     TEXT NOT NULL,
  house_id      INT NOT NULL,
  created_at    TEXT NOT NULL,
  ip_hash       TEXT NULL,
  UNIQUE (device_id, house_id),
  FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE
);

-- One vote per device per category. Changing your mind updates the row.
CREATE TABLE IF NOT EXISTS votes (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id     TEXT NOT NULL,
  category_id   INT NOT NULL,
  house_id      INT NOT NULL,
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL,
  ip_hash       TEXT NULL,
  UNIQUE (device_id, category_id),
  FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
