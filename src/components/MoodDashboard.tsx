import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Calendar, Smile } from 'lucide-react';

interface MoodEntry {
  date: string;
  emotion: 'stressed' | 'anxious' | 'tired' | 'calm' | 'motivated' | 'happy';
  intensity: number; // 1-5
}

interface MoodDashboardProps {
  entries: MoodEntry[];
}

const emotionColors = {
  stressed: 'bg-red-500',
  anxious: 'bg-orange-500', 
  tired: 'bg-blue-500',
  calm: 'bg-green-500',
  motivated: 'bg-purple-500',
  happy: 'bg-yellow-500'
};

const emotionLabels = {
  stressed: 'Stressed',
  anxious: 'Anxious',
  tired: 'Tired',
  calm: 'Calm',
  motivated: 'Motivated',
  happy: 'Happy'
};

export const MoodDashboard = ({ entries }: MoodDashboardProps) => {
  const recentEntries = entries.slice(-7); // Last 7 entries
  const avgIntensity = entries.length > 0 ? entries.reduce((sum, entry) => sum + entry.intensity, 0) / entries.length : 0;
  const trendingEmotion = entries.length > 0 ? 
    entries.reduce((prev, curr) => 
      entries.filter(e => e.emotion === curr.emotion).length > entries.filter(e => e.emotion === prev.emotion).length ? curr : prev
    ).emotion : 'calm';

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <Card className="border-0 shadow-lg">
        <CardHeader>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            <CardTitle>Your Emotional Journey</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Emotion Wave Visualization */}
          <div className="space-y-3">
            <h3 className="font-medium flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Recent Mood Flow
            </h3>
            <div className="flex items-end gap-2 h-20 p-4 bg-muted/30 rounded-lg">
              {recentEntries.map((entry, index) => (
                <div key={index} className="flex flex-col items-center gap-1 flex-1">
                  <div 
                    className={`${emotionColors[entry.emotion]} w-4 rounded-full transition-all duration-300 hover:scale-125`}
                    style={{ 
                      height: `${(entry.intensity / 5) * 60}px`
                    }}
                    title={`${emotionLabels[entry.emotion]} - ${entry.intensity}/5`}
                  />
                  <span className="text-xs text-muted-foreground">
                    {new Date(entry.date).toLocaleDateString('en', { weekday: 'short' })}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-muted/30 rounded-lg">
              <div className="text-2xl font-bold text-primary">{entries.length}</div>
              <div className="text-sm text-muted-foreground">Dumps</div>
            </div>
            <div className="text-center p-4 bg-muted/30 rounded-lg">
              <div className="text-2xl font-bold text-accent">{avgIntensity.toFixed(1)}/5</div>
              <div className="text-sm text-muted-foreground">Avg Intensity</div>
            </div>
            <div className="text-center p-4 bg-muted/30 rounded-lg">
              <Badge variant="secondary" className="text-sm">
                {emotionLabels[trendingEmotion]}
              </Badge>
              <div className="text-xs text-muted-foreground mt-1">Trending</div>
            </div>
          </div>

          {/* Progress Message */}
          {entries.length > 3 && (
            <div className="text-center p-4 bg-gray-100 rounded-lg">
              <p className="text-sm text-muted-foreground">
                You've been on this journey for {entries.length} sessions. Each dump is progress! 
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};