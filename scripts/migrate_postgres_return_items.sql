-- Neon / PostgreSQL: return_items tablosunu app/models/models.py ile hizala.
-- Neon SQL Editor'da calistir (veya psql ile bu dosyayi ver).

ALTER TABLE return_items ADD COLUMN IF NOT EXISTS ai_verdict VARCHAR(64);
ALTER TABLE return_items ADD COLUMN IF NOT EXISTS ai_reasoning TEXT;

-- Bazi eski kurulumlarda eksik olabilir:
ALTER TABLE return_items ADD COLUMN IF NOT EXISTS ai_risk_score DOUBLE PRECISION DEFAULT 0.0;
