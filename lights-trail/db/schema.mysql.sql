-- Llanwrtyd Lights — MySQL schema (GoDaddy cPanel)
-- Run once via cPanel > phpMyAdmin > Import, or paste into the SQL tab.

CREATE TABLE IF NOT EXISTS houses (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  stop_no       INT NOT NULL,
  name          VARCHAR(120) NOT NULL,
  address       VARCHAR(160) NOT NULL,
  blurb_en      TEXT NOT NULL,
  blurb_cy      TEXT NULL,
  note_en       VARCHAR(160) NULL,
  note_cy       VARCHAR(160) NULL,
  walk_en       VARCHAR(80) NULL,
  walk_cy       VARCHAR(80) NULL,
  lat           DECIMAL(9,6) NULL,
  lng           DECIMAL(9,6) NULL,
  token         VARCHAR(24) NOT NULL,
  active        TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uniq_token (token),
  UNIQUE KEY uniq_stop (stop_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categories (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  slug          VARCHAR(32) NOT NULL,
  label_en      VARCHAR(120) NOT NULL,
  label_cy      VARCHAR(120) NOT NULL,
  sort_order    INT NOT NULL DEFAULT 0,
  UNIQUE KEY uniq_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- One row per device per house. The UNIQUE key is what makes a repeat
-- scan harmless rather than a duplicate.
CREATE TABLE IF NOT EXISTS checkins (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  device_id     CHAR(32) NOT NULL,
  house_id      INT NOT NULL,
  created_at    DATETIME NOT NULL,
  ip_hash       CHAR(64) NULL,
  UNIQUE KEY uniq_device_house (device_id, house_id),
  KEY idx_house (house_id),
  CONSTRAINT fk_checkin_house FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- One vote per device per category. Changing your mind updates the row.
CREATE TABLE IF NOT EXISTS votes (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  device_id     CHAR(32) NOT NULL,
  category_id   INT NOT NULL,
  house_id      INT NOT NULL,
  created_at    DATETIME NOT NULL,
  updated_at    DATETIME NOT NULL,
  ip_hash       CHAR(64) NULL,
  UNIQUE KEY uniq_device_category (device_id, category_id),
  KEY idx_cat_house (category_id, house_id),
  CONSTRAINT fk_vote_house FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
  CONSTRAINT fk_vote_cat FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
