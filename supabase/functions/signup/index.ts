import { createClient } from 'npm:@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Info, Apikey',
};

interface SignupRequest {
  email: string;
  name: string;
  ageGroup: string;
  occupation: string;
  journalingExperience: string;
  primaryGoal: string;
  emotionalChallenges?: string;
  preferredReflectionTime: string;
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    if (req.method !== 'POST') {
      return new Response(
        JSON.stringify({ error: 'Method not allowed' }),
        {
          status: 405,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    const data: SignupRequest = await req.json();

    if (!data.email || !data.name) {
      return new Response(
        JSON.stringify({ error: 'Email and name are required' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    if (!data.ageGroup || !data.occupation) {
      return new Response(
        JSON.stringify({ error: 'Age group and occupation are required' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    if (!data.journalingExperience || !data.primaryGoal || !data.preferredReflectionTime) {
      return new Response(
        JSON.stringify({ error: 'Please complete all required fields' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    const onboardingData = {
      age_group: data.ageGroup,
      occupation: data.occupation,
      journaling_experience: data.journalingExperience,
      primary_goal: data.primaryGoal,
      emotional_challenges: data.emotionalChallenges || '',
      preferred_reflection_time: data.preferredReflectionTime,
      profile_completed_at: new Date().toISOString(),
    };

    const { data: existingUser } = await supabaseClient
      .from('users')
      .select('id, email, name')
      .eq('email', data.email)
      .maybeSingle();

    if (existingUser) {
      return new Response(
        JSON.stringify({
          success: true,
          user_id: existingUser.id,
          email: existingUser.email,
          name: existingUser.name,
          message: 'Welcome back! Redirecting to your dashboard...',
        }),
        {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    const { data: newUser, error: insertError } = await supabaseClient
      .from('users')
      .insert({
        email: data.email,
        name: data.name,
        onboarding_data: onboardingData,
      })
      .select('id, email, name')
      .single();

    if (insertError) {
      console.error('Error creating user:', insertError);
      return new Response(
        JSON.stringify({ error: 'Failed to create user: ' + insertError.message }),
        {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    return new Response(
      JSON.stringify({
        success: true,
        user_id: newUser.id,
        email: newUser.email,
        name: newUser.name,
        message: 'Profile created successfully! Redirecting to your dashboard...',
      }),
      {
        status: 201,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('Error in signup function:', error);
    return new Response(
      JSON.stringify({ error: error.message || 'Internal server error' }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});