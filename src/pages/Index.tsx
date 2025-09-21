import { useState } from 'react';
import { BrainDumpInput } from '@/components/BrainDumpInput';
import { ResultCards } from '@/components/ResultCards';
import { MoodDashboard } from '@/components/MoodDashboard';
import { SharingBoard } from '@/components/SharingBoard';
import { SelfieAnalyzer } from '@/components/SelfieAnalyzer';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Brain, Sparkles, Heart, Target, Users, Camera } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useCreateDump, useHealthCheck } from '@/hooks/use-api';
import { DumpResponse } from '@/lib/api';

interface DumpResult {
  actionPlan: string[];
  wellnessReset: string;
  motivationBoost: string;
}

interface MoodEntry {
  date: string;
  emotion: 'stressed' | 'anxious' | 'tired' | 'calm' | 'motivated' | 'happy';
  intensity: number;
}

const Index = () => {
  const [result, setResult] = useState<DumpResult | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [moodEntries, setMoodEntries] = useState<MoodEntry[]>([
    { date: '2024-01-15', emotion: 'stressed', intensity: 4 },
    { date: '2024-01-16', emotion: 'anxious', intensity: 3 },
    { date: '2024-01-17', emotion: 'tired', intensity: 5 },
    { date: '2024-01-18', emotion: 'calm', intensity: 2 },
    { date: '2024-01-19', emotion: 'motivated', intensity: 4 },
    { date: '2024-01-20', emotion: 'happy', intensity: 3 },
    { date: '2024-01-21', emotion: 'calm', intensity: 2 },
  ]);
  
  const { toast } = useToast();
  const createDumpMutation = useCreateDump();
  const { data: healthData, isLoading: isHealthLoading } = useHealthCheck();

  const handleBrainDump = async (text: string) => {
    setShowResult(false);
    
    try {
      const response = await createDumpMutation.mutateAsync({
        user_input: text,
        user_id: 'anonymous', // For now, use anonymous user
        tags: extractTags(text)
      });
      
      // Convert backend response to frontend format
      const transformedResult: DumpResult = {
        actionPlan: response.plan,
        wellnessReset: response.reset_tip,
        motivationBoost: response.motivation
      };
      
      setResult(transformedResult);
      setShowResult(true);
      
      // Add mood entry based on stress score
      const emotion = response.stress_score < 0.3 ? 'calm' : 
                     response.stress_score < 0.5 ? 'motivated' :
                     response.stress_score < 0.7 ? 'tired' : 'stressed';
      const intensity = Math.ceil(response.stress_score * 5);
      
      setMoodEntries(prev => [...prev, {
        date: new Date().toISOString(),
        emotion,
        intensity: Math.min(intensity, 5)
      }]);
      
    } catch (error) {
      console.error('Failed to process brain dump:', error);
      // Error handling is done in the mutation hook
    }
  };

  // Helper function to extract tags from text
  const extractTags = (text: string): string[] => {
    const tags: string[] = [];
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('exam') || lowerText.includes('test')) tags.push('academic');
    if (lowerText.includes('deadline') || lowerText.includes('due')) tags.push('deadline');
    if (lowerText.includes('relationship') || lowerText.includes('friend')) tags.push('social');
    if (lowerText.includes('work') || lowerText.includes('job')) tags.push('work');
    if (lowerText.includes('family') || lowerText.includes('parent')) tags.push('family');
    if (lowerText.includes('money') || lowerText.includes('financial')) tags.push('financial');
    
    return tags;
  };

  const handleNewDump = () => {
    setResult(null);
    setShowResult(false);
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="px-0 py-0">
        <img
          src="/logo.png"
          alt="BrainDump logo"
          className="object-contain"
          style={{ maxWidth: '280px', maxHeight: '120px' }}
        />
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-6 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-black max-w-4xl mx-auto mb-4 leading-tight">
          Turn Your{' '}
          <span 
            className="font-bold"
            style={{
              background: 'linear-gradient(135deg, #ff6b9d, #8b5cf6)',
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              color: 'transparent'
            }}
          >
            Stress
          </span>
          {' '}Into{' '}
          <span 
            className="font-bold"
            style={{
              background: 'linear-gradient(135deg, #3b82f6, #10b981)',
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              color: 'transparent'
            }}
          >
            Success
          </span>
        </h1>
        <p className="text-base md:text-lg font-medium text-gray-700 max-w-4xl mx-auto leading-relaxed">
          Dump your racing thoughts, overwhelming feelings, and daily chaos. Our AI instantly transforms your mental clutter into clarity, actionable plans, and emotional support, designed specifically for students.
        </p>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 space-y-6">
        {!showResult ? (
          <>
            {/* Features Section */}
            <section className="text-center space-y-4">
              <h2 className="text-2xl md:text-3xl font-bold text-black mb-6">How It Works</h2>
              <div className="grid md:grid-cols-3 gap-4 max-w-4xl mx-auto mb-6">
                <Card className="p-6 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                      <Target className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-left">
                      <h3 className="text-lg md:text-xl font-bold text-black mb-2">Action Plan</h3>
                      <p className="text-sm text-gray-700 leading-relaxed">A step-by-step set of tiny, doable tasks that actually work</p>
                    </div>
                  </div>
                </Card>
                <Card className="p-6 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                      <Heart className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-left">
                      <h3 className="text-lg md:text-xl font-bold text-black mb-2">Wellness Reset</h3>
                      <p className="text-sm text-gray-700 leading-relaxed">A quick nudge for your body or mind (stretch, hydrate, breathe)</p>
                    </div>
                  </div>
                </Card>
                <Card className="p-6 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-green-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                      <Sparkles className="w-8 h-8 text-white" />
                    </div>
                    <div className="text-left">
                      <h3 className="text-lg md:text-xl font-bold text-black mb-2">Motivation</h3>
                      <p className="text-sm text-gray-700 leading-relaxed">Affirmation, reframing, or encouragement that hits different</p>
                    </div>
                  </div>
                </Card>
              </div>
              
              <BrainDumpInput onSubmit={handleBrainDump} isLoading={createDumpMutation.isPending} />
            </section>

            {/* Community & Tools */}
            <section className="py-8">
              <h2 className="text-2xl md:text-3xl font-bold text-black text-center mb-8">Explore More</h2>
              <Tabs defaultValue="mood" className="w-full">
                <TabsList className="grid w-full grid-cols-3 max-w-xl mx-auto bg-gray-100 p-2 rounded-2xl">
                  <TabsTrigger value="mood" className="flex items-center gap-3 text-base font-semibold py-3 px-4 rounded-xl data-[state=active]:bg-white data-[state=active]:text-black data-[state=active]:shadow-lg">
                    <Sparkles className="w-4 h-4" />
                    Mood Dashboard
                  </TabsTrigger>
                  <TabsTrigger value="community" className="flex items-center gap-3 text-base font-semibold py-3 px-4 rounded-xl data-[state=active]:bg-white data-[state=active]:text-black data-[state=active]:shadow-lg">
                    <Users className="w-4 h-4" />
                    Community
                  </TabsTrigger>
                  <TabsTrigger value="selfie" className="flex items-center gap-3 text-base font-semibold py-3 px-4 rounded-xl data-[state=active]:bg-white data-[state=active]:text-black data-[state=active]:shadow-lg">
                    <Camera className="w-4 h-4" />
                    Selfie Analysis
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="mood" className="mt-4">
                  {moodEntries.length > 0 && <MoodDashboard entries={moodEntries} />}
                </TabsContent>
                
                <TabsContent value="community" className="mt-4">
                  <SharingBoard />
                </TabsContent>
                
                <TabsContent value="selfie" className="mt-4">
                  <div className="flex justify-center">
                    <SelfieAnalyzer />
                  </div>
                </TabsContent>
              </Tabs>
            </section>

          </>
        ) : (
          <>
            {/* Results */}
            <section>
              <ResultCards 
                actionPlan={result!.actionPlan}
                wellnessReset={result!.wellnessReset}
                motivationBoost={result!.motivationBoost}
                isVisible={showResult}
              />
            </section>

            {/* New Dump Button */}
            <section className="text-center py-16">
              <Button 
                onClick={handleNewDump}
                size="lg"
                className="bg-gradient-to-r from-pink-500 via-purple-600 to-blue-600 text-white hover:shadow-2xl hover:shadow-purple-500/30 transition-all duration-300 text-xl px-12 py-6 rounded-2xl font-bold"
              >
                <Brain className="w-6 h-6 mr-3" />
                Dump More Stress
              </Button>
            </section>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-4 mt-8">
        <div className="text-center">
          <p className="text-base font-semibold text-gray-800 mb-2">Your stress is valid. Your feelings matter. You've got this.</p>
          <p className="text-sm text-gray-600">BrainDump: AI Stress to Success Hub</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
