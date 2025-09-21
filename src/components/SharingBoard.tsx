import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Heart, MessageCircle, Send, Users } from 'lucide-react';

interface ShareEntry {
  id: string;
  text: string;
  reactions: { type: string; count: number }[];
  timestamp: string;
}

export const SharingBoard = () => {
  const [entries, setEntries] = useState<ShareEntry[]>([
    {
      id: '1',
      text: "Just bombed my midterm and my laptop crashed with my project on it 😭",
      reactions: [
        { type: 'metoo', count: 12 },
        { type: 'support', count: 8 }
      ],
      timestamp: '2h ago'
    },
    {
      id: '2',
      text: "Interview tomorrow and I haven't slept in 30 hours",
      reactions: [
        { type: 'metoo', count: 5 },
        { type: 'support', count: 15 }
      ],
      timestamp: '4h ago'
    },
    {
      id: '3',
      text: "Parents asking about grades while I'm just trying to survive",
      reactions: [
        { type: 'metoo', count: 23 },
        { type: 'support', count: 7 }
      ],
      timestamp: '6h ago'
    }
  ]);
  
  const [newEntry, setNewEntry] = useState('');

  const addReaction = (entryId: string, reactionType: string) => {
    setEntries(prev => prev.map(entry => {
      if (entry.id === entryId) {
        const existingReaction = entry.reactions.find(r => r.type === reactionType);
        if (existingReaction) {
          return {
            ...entry,
            reactions: entry.reactions.map(r => 
              r.type === reactionType ? { ...r, count: r.count + 1 } : r
            )
          };
        } else {
          return {
            ...entry,
            reactions: [...entry.reactions, { type: reactionType, count: 1 }]
          };
        }
      }
      return entry;
    }));
  };

  const submitEntry = () => {
    if (newEntry.trim()) {
      const entry: ShareEntry = {
        id: Date.now().toString(),
        text: newEntry.trim(),
        reactions: [],
        timestamp: 'now'
      };
      setEntries(prev => [entry, ...prev]);
      setNewEntry('');
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Users className="w-5 h-5 text-primary" />
          Anonymous Stress Board
          <span className="text-sm font-normal text-muted-foreground">- You're not alone</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Add new entry */}
        <div className="flex gap-2">
          <Input
            value={newEntry}
            onChange={(e) => setNewEntry(e.target.value)}
            placeholder="Share your stress anonymously... (one-liner)"
            maxLength={100}
            onKeyPress={(e) => e.key === 'Enter' && submitEntry()}
            className="flex-1"
          />
          <Button onClick={submitEntry} size="sm" disabled={!newEntry.trim()}>
            <Send className="w-4 h-4" />
          </Button>
        </div>

        {/* Entries */}
        <div className="space-y-3 max-h-60 overflow-y-auto">
          {entries.map((entry) => (
            <div
              key={entry.id}
              className="p-3 bg-muted/30 rounded-lg border border-muted/50 animate-fade-in"
            >
              <p className="text-sm mb-2">{entry.text}</p>
              <div className="flex items-center justify-between">
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => addReaction(entry.id, 'metoo')}
                    className="h-6 px-2 text-xs hover:bg-accent/20"
                  >
                    <MessageCircle className="w-3 h-3 mr-1" />
                    Me too {entry.reactions.find(r => r.type === 'metoo')?.count || 0}
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => addReaction(entry.id, 'support')}
                    className="h-6 px-2 text-xs hover:bg-primary/20"
                  >
                    <Heart className="w-3 h-3 mr-1" />
                    You got this {entry.reactions.find(r => r.type === 'support')?.count || 0}
                  </Button>
                </div>
                <span className="text-xs text-muted-foreground">{entry.timestamp}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};