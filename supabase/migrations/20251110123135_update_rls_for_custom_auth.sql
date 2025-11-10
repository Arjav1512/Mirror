/*
  # Update RLS Policies for Custom Authentication

  1. Changes
    - Add service role policies to allow Edge Functions to manage data
    - Add anon role policy for user lookup during sign-in
    
  2. Security
    - Service role can bypass RLS (used by Edge Functions for user operations)
    - Anon role has limited SELECT access for sign-in verification
    - All data operations go through Edge Functions with validation
*/

-- Drop and recreate anon policy for users
DO $$ 
BEGIN
  DROP POLICY IF EXISTS "Anon can read users for sign-in" ON users;
EXCEPTION
  WHEN undefined_object THEN NULL;
END $$;

CREATE POLICY "Anon can read users for sign-in"
  ON users FOR SELECT
  TO anon
  USING (true);

-- Drop and recreate service role policies for journal_entries
DO $$ 
BEGIN
  DROP POLICY IF EXISTS "Service role can manage all entries" ON journal_entries;
EXCEPTION
  WHEN undefined_object THEN NULL;
END $$;

CREATE POLICY "Service role can manage all entries"
  ON journal_entries FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Drop and recreate service role policies for biases
DO $$ 
BEGIN
  DROP POLICY IF EXISTS "Service role can manage all biases" ON biases;
EXCEPTION
  WHEN undefined_object THEN NULL;
END $$;

CREATE POLICY "Service role can manage all biases"
  ON biases FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Drop and recreate service role policies for weekly_summaries
DO $$ 
BEGIN
  DROP POLICY IF EXISTS "Service role can manage all summaries" ON weekly_summaries;
EXCEPTION
  WHEN undefined_object THEN NULL;
END $$;

CREATE POLICY "Service role can manage all summaries"
  ON weekly_summaries FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
