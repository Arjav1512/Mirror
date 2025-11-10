/*
  # Add INSERT policy for users table

  1. Changes
    - Add policy to allow anon role to insert new users during signup
    - This enables the signup Edge Function to create user records
  
  2. Security
    - Policy allows anyone to create a user account
    - Edge Function validates all data before insertion
    - RLS still protects user data after creation
*/

-- Drop existing policy if it exists
DO $$ 
BEGIN
  DROP POLICY IF EXISTS "Anyone can create user during signup" ON users;
EXCEPTION
  WHEN undefined_object THEN NULL;
END $$;

-- Allow anon role to insert new users during signup
CREATE POLICY "Anyone can create user during signup"
  ON users
  FOR INSERT
  TO anon
  WITH CHECK (true);
