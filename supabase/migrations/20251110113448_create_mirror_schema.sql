/*
  # Mirror App Database Schema
  
  ## Overview
  Creates the complete database schema for the Mirror journaling application with proper security.
  
  ## Tables Created
  
  ### 1. users
  - id (uuid, primary key)
  - email (text, unique) - User's email address
  - name (text) - User's full name
  - created_at (timestamptz) - Account creation timestamp
  - onboarding_data (jsonb) - User profile data including age, occupation, goals, etc.
  
  ### 2. journal_entries
  - id (uuid, primary key)
  - user_id (uuid, foreign key) - References users table
  - entry_text (text) - The actual journal entry content
  - timestamp (timestamptz) - When the entry was created
  - sentiment_score (real) - VADER sentiment compound score (-1 to 1)
  - valence (real) - Combined sentiment valence (-1 to 1)
  
  ### 3. biases
  - id (uuid, primary key)
  - entry_id (uuid, foreign key) - References journal_entries table
  - bias_type (text) - Type of cognitive bias detected
  - detected_pattern (text) - The pattern that triggered detection
  - explanation (text) - Explanation of the bias
  
  ### 4. weekly_summaries
  - id (uuid, primary key)
  - user_id (uuid, foreign key) - References users table
  - week_start (date) - Start date of the week (Monday)
  - summary_text (text) - AI-generated summary text
  - themes (jsonb) - Array of themes detected
  - emotions (jsonb) - Array of emotions detected
  
  ## Security
  - RLS enabled on all tables
  - Policies enforce user-specific data access
  - Users can only read/write their own data
  - No public access without authentication
  
  ## Indexes
  - Performance indexes on frequently queried columns
  - Foreign key indexes for join operations
*/

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email text UNIQUE NOT NULL,
  name text NOT NULL,
  created_at timestamptz DEFAULT now(),
  onboarding_data jsonb DEFAULT '{}'::jsonb
);

-- Create journal_entries table
CREATE TABLE IF NOT EXISTS journal_entries (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  entry_text text NOT NULL,
  timestamp timestamptz DEFAULT now(),
  sentiment_score real,
  valence real
);

-- Create biases table
CREATE TABLE IF NOT EXISTS biases (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  entry_id uuid NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
  bias_type text NOT NULL,
  detected_pattern text DEFAULT '',
  explanation text DEFAULT ''
);

-- Create weekly_summaries table
CREATE TABLE IF NOT EXISTS weekly_summaries (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  week_start date NOT NULL,
  summary_text text NOT NULL,
  themes jsonb DEFAULT '[]'::jsonb,
  emotions jsonb DEFAULT '[]'::jsonb,
  UNIQUE(user_id, week_start)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_journal_entries_user_timestamp 
  ON journal_entries(user_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_journal_entries_user_id 
  ON journal_entries(user_id);

CREATE INDEX IF NOT EXISTS idx_biases_entry_id 
  ON biases(entry_id);

CREATE INDEX IF NOT EXISTS idx_weekly_summaries_user_week 
  ON weekly_summaries(user_id, week_start DESC);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE journal_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE biases ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_summaries ENABLE ROW LEVEL SECURITY;

-- Users table policies
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Journal entries policies
CREATE POLICY "Users can view own entries"
  ON journal_entries FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own entries"
  ON journal_entries FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own entries"
  ON journal_entries FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own entries"
  ON journal_entries FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- Biases policies (access through entry ownership)
CREATE POLICY "Users can view biases for own entries"
  ON biases FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM journal_entries
      WHERE journal_entries.id = biases.entry_id
      AND journal_entries.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can create biases for own entries"
  ON biases FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM journal_entries
      WHERE journal_entries.id = biases.entry_id
      AND journal_entries.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete biases for own entries"
  ON biases FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM journal_entries
      WHERE journal_entries.id = biases.entry_id
      AND journal_entries.user_id = auth.uid()
    )
  );

-- Weekly summaries policies
CREATE POLICY "Users can view own summaries"
  ON weekly_summaries FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own summaries"
  ON weekly_summaries FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own summaries"
  ON weekly_summaries FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own summaries"
  ON weekly_summaries FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());