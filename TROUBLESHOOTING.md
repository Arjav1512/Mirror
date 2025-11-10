# Mirror - Troubleshooting Guide

## Features Not Displaying

If the Emotional Timeline, Cognitive Bias Detection, or other features appear as "Coming Soon" or empty:

### Solution: Create New Journal Entries

The features require journal entries created through the **new system** (stored in Supabase database, not browser localStorage).

**Steps to activate features:**

1. **Sign in to your dashboard** at `/dashboard`
2. **Go to the Journal tab** (should be the default view)
3. **Write a journal entry** - Try writing something with emotional content, for example:
   ```
   Today was really challenging. Everything seems to be going wrong and I feel like
   nothing I do is ever good enough. I'm worried things will never get better.
   ```
4. **Click "Save & Analyze Entry"**
5. **Wait for confirmation** - You should see "Entry saved and analyzed successfully!"
6. **Check the Timeline tab** - Your emotional pattern should now appear
7. **Check the Biases tab** - Any detected cognitive biases will be displayed

### How the Features Work

#### Emotional Timeline
- **Requirements:** At least 1 journal entry
- **What you'll see:**
  - Bar chart showing sentiment over time
  - Color-coded emotions (green=positive, yellow=neutral, red=negative)
  - Statistics: Average mood, positive days, neutral days, challenging days

#### Cognitive Bias Detection
- **Requirements:** At least 1 journal entry with detectable patterns
- **What you'll see:**
  - List of detected biases by type
  - Frequency of each bias
  - Explanations and tips for reframing
  - Recent detections with context

#### Example Entry That Triggers Biases

To test the bias detection, try writing an entry like this:

```
I always mess everything up. Nothing ever goes right for me. I feel like a complete
failure, which means I probably am. I know things will never get better. Every time
I try something, it ends badly. Everyone else has it figured out except me.
```

This should detect multiple biases:
- Catastrophizing ("always", "never", "complete failure")
- Black-and-white Thinking ("everything", "nothing")
- Emotional Reasoning ("I feel like a failure, which means I probably am")
- Fortune Telling ("things will never get better")
- Overgeneralization ("always", "every time")

## Sign-In Issues

If you see "User does not exist" when signing in:

### Verify Email
- Make sure you're using the **exact email** you signed up with
- Check for typos or extra spaces

### Create New Account
- If you signed up before the latest updates, you may need to create a fresh account
- The new system stores users in Supabase database
- Go to the landing page and complete the signup form again

## Data Not Persisting

If your entries disappear after refresh:

### Check Session
- Journal entries are tied to your user session
- Make sure you're signed in
- Don't clear your browser's sessionStorage

### Verify Supabase Connection
- Check browser console (F12) for any error messages
- Look for messages like "Load entries response:" and "Create entry response:"
- Contact support if you see connection errors

## Browser Console Logging

For debugging, the dashboard logs important information:

1. Open browser console (F12 or right-click → Inspect → Console)
2. Create or view entries
3. Look for log messages:
   - `Load entries response:` - Shows entries fetched from database
   - `Loaded entries:` - Shows the actual entry data
   - `Create entry response:` - Shows result of creating an entry

## Still Having Issues?

Contact support:
- Email: arjav.jain1512@icloud.com
- Include:
  - Browser console logs (F12 → Console tab)
  - Description of what you're experiencing
  - Steps you've already tried

## Quick Test

To quickly verify everything is working:

1. Sign up with a new account
2. Write this test entry: "I feel amazing today! Everything is going great and I'm so happy with my progress."
3. Click "Save & Analyze Entry"
4. You should see:
   - Success message
   - Entry appears in "Recent Entries" with a happy emoji
   - Sentiment labeled as "Positive"
5. Click "Timeline" tab - You should see a green bar
6. Click "Biases" tab - Should show "No biases detected yet" (this entry is positive and balanced)
7. Create another entry with negative patterns to see bias detection in action

## Feature Checklist

Use this to verify all features are working:

- [ ] Can sign up with email
- [ ] Can sign in with email
- [ ] Can create journal entry
- [ ] Entry appears in "Recent Entries"
- [ ] Entry shows sentiment emoji and label
- [ ] Timeline tab shows bar chart
- [ ] Timeline shows statistics
- [ ] Biases tab shows detected patterns (if applicable)
- [ ] Statistics cards update (Total Entries, Streak, Biases)
- [ ] Can sign out and sign back in
- [ ] Entries persist after signing back in
