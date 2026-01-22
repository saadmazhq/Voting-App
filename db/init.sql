CREATE TABLE IF NOT EXISTS votes (
  id SERIAL PRIMARY KEY,
  choice VARCHAR(8) NOT NULL CHECK (choice IN ('YES', 'NO')),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Optional: aggregate table for faster reads
CREATE TABLE IF NOT EXISTS vote_totals (
  id BOOLEAN PRIMARY KEY DEFAULT TRUE,
  yes_count BIGINT NOT NULL DEFAULT 0,
  no_count BIGINT NOT NULL DEFAULT 0
);

INSERT INTO vote_totals (id, yes_count, no_count)
VALUES (TRUE, 0, 0)
ON CONFLICT (id) DO NOTHING;