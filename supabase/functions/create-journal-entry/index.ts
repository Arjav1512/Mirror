import { createClient } from 'npm:@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Info, Apikey',
};

interface SentimentScore {
  score: number;
  valence: number;
  label: string;
}

interface Bias {
  type: string;
  pattern: string;
  explanation: string;
}

function analyzeSentiment(text: string): SentimentScore {
  const lowerText = text.toLowerCase();
  
  const positiveWords = ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'love', 'good', 'better', 'best', 'excellent', 'fantastic', 'grateful', 'thankful', 'blessed', 'proud', 'accomplished', 'confident', 'optimistic', 'hopeful'];
  const negativeWords = ['sad', 'angry', 'upset', 'bad', 'worse', 'worst', 'terrible', 'awful', 'horrible', 'hate', 'depressed', 'anxious', 'worried', 'scared', 'afraid', 'lonely', 'hurt', 'pain', 'disappointed', 'frustrated'];
  
  let positiveCount = 0;
  let negativeCount = 0;
  
  positiveWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    const matches = text.match(regex);
    if (matches) positiveCount += matches.length;
  });
  
  negativeWords.forEach(word => {
    const regex = new RegExp(`\\b${word}\\b`, 'gi');
    const matches = text.match(regex);
    if (matches) negativeCount += matches.length;
  });
  
  const totalWords = text.split(/\s+/).length;
  const score = (positiveCount - negativeCount) / Math.max(totalWords, 1);
  const normalizedScore = Math.max(-1, Math.min(1, score * 10));
  
  let label = 'Neutral';
  if (normalizedScore > 0.2) label = 'Positive';
  else if (normalizedScore < -0.2) label = 'Negative';
  
  return {
    score: normalizedScore,
    valence: normalizedScore,
    label
  };
}

function detectBiases(text: string, valence: number): Bias[] {
  const biases: Bias[] = [];
  const lowerText = text.toLowerCase();
  
  const catastrophizingPatterns = [
    /\b(always|never|everything|nothing|everyone|no one)\b.*(terrible|awful|horrible|worst|disaster|ruined)/i,
    /\b(can't|cannot|couldn't|won't|wouldn't)\b.*(anything|ever|never|always)/i,
  ];
  
  const blackWhitePatterns = [
    /\b(all|none|every|nothing|everything)\b/i,
    /\b(always|never)\b/i,
    /\b(completely|totally|absolutely)\s+(wrong|right|bad|good)/i,
  ];
  
  const emotionalReasoningPatterns = [
    /\b(i feel|feels like).*\b(so|therefore|that means|this proves)/i,
    /\b(i feel|feeling).*\b(it's|it is|that's|they are)/i,
  ];
  
  const fortuneTellingPatterns = [
    /\b(will|going to)\b.*\b(bad|terrible|fail|wrong)/i,
    /\b(know|certain|sure)\b.*\b(will|going to)\b.*\b(bad|fail)/i,
  ];
  
  const overgeneralizationPatterns = [
    /\b(always|never|every|all)\b.*\b(happens|happened)/i,
    /\b(every time|whenever)\b/i,
  ];
  
  if (valence < -0.2) {
    for (const pattern of catastrophizingPatterns) {
      if (pattern.test(text)) {
        biases.push({
          type: 'Catastrophizing',
          pattern: 'Absolutist negative language detected',
          explanation: 'You may be magnifying negative events and expecting the worst possible outcomes.'
        });
        break;
      }
    }
  }
  
  let blackWhiteCount = 0;
  blackWhitePatterns.forEach(pattern => {
    if (pattern.test(text)) blackWhiteCount++;
  });
  if (blackWhiteCount >= 2) {
    biases.push({
      type: 'Black-and-white Thinking',
      pattern: 'Binary language patterns detected',
      explanation: 'You may be thinking in extremes without considering nuances or middle ground.'
    });
  }
  
  for (const pattern of emotionalReasoningPatterns) {
    if (pattern.test(text)) {
      biases.push({
        type: 'Emotional Reasoning',
        pattern: 'Treating feelings as facts',
        explanation: 'You may be treating your feelings as facts, assuming that negative emotions reflect reality.'
      });
      break;
    }
  }
  
  if (valence < -0.1) {
    for (const pattern of fortuneTellingPatterns) {
      if (pattern.test(text)) {
        biases.push({
          type: 'Fortune Telling',
          pattern: 'Predicting negative outcomes',
          explanation: 'You may be predicting negative outcomes without evidence, assuming things will go badly.'
        });
        break;
      }
    }
  }
  
  for (const pattern of overgeneralizationPatterns) {
    if (pattern.test(text)) {
      biases.push({
        type: 'Overgeneralization',
        pattern: 'Universal patterns from isolated incidents',
        explanation: 'You may be treating isolated incidents as universal patterns or rules.'
      });
      break;
    }
  }
  
  return biases;
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
        { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    const { userId, entryText } = await req.json();

    if (!userId || !entryText) {
      return new Response(
        JSON.stringify({ error: 'userId and entryText are required' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    const sentiment = analyzeSentiment(entryText);
    const biases = detectBiases(entryText, sentiment.valence);

    const { data: entry, error: entryError } = await supabase
      .from('journal_entries')
      .insert({
        user_id: userId,
        entry_text: entryText,
        sentiment_score: sentiment.score,
        valence: sentiment.valence,
      })
      .select()
      .single();

    if (entryError) {
      console.error('Error creating entry:', entryError);
      return new Response(
        JSON.stringify({ error: 'Failed to create entry: ' + entryError.message }),
        { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (biases.length > 0) {
      const biasRecords = biases.map(bias => ({
        entry_id: entry.id,
        bias_type: bias.type,
        detected_pattern: bias.pattern,
        explanation: bias.explanation,
      }));

      const { error: biasError } = await supabase
        .from('biases')
        .insert(biasRecords);

      if (biasError) {
        console.error('Error creating biases:', biasError);
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        entry: {
          ...entry,
          sentiment,
          biases,
        },
      }),
      { status: 201, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Error in create-journal-entry:', error);
    return new Response(
      JSON.stringify({ error: error.message || 'Internal server error' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});