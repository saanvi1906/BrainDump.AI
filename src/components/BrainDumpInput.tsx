import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Mic, Send, Sparkles } from 'lucide-react';

interface BrainDumpInputProps {
  onSubmit: (text: string) => void;
  isLoading: boolean;
}

export const BrainDumpInput = ({ onSubmit, isLoading }: BrainDumpInputProps) => {
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleSubmit = () => {
    if (input.trim()) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const startVoiceInput = () => {
    if ('speechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).speechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = true;
      recognition.interimResults = true;
      
      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      
      recognition.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          setInput(prev => prev + finalTranscript);
        }
      };
      
      recognition.start();
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-4">
      <div className="text-center mb-4">
        <h3 className="text-xl md:text-2xl font-bold text-black mb-2">Ready to Transform Your Stress?</h3>
        <p className="text-base text-gray-700">Dump everything that's weighing you down and watch it turn into clarity, action, and motivation</p>
      </div>
      
      <div className="relative">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Dump all your stress here... exams, deadlines, relationship drama, whatever's eating at you 😮‍💨"
          className="min-h-[100px] text-base p-4 resize-none border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all duration-300 bg-white text-center"
          disabled={isLoading}
        />
        
        {input && !isLoading && (
          <div className="absolute top-4 right-4">
            <Sparkles className="w-5 h-5 text-purple-500 animate-pulse" />
          </div>
        )}
      </div>
      
      <div className="flex gap-3 justify-center">
        <Button
          onClick={startVoiceInput}
          variant="outline"
          size="lg"
          className="border-2 border-gray-300 hover:border-blue-600 hover:bg-blue-50 text-base px-6 py-3 rounded-lg font-semibold transition-all duration-300"
          disabled={isLoading || isListening}
        >
          <Mic className={`w-5 h-5 mr-2 ${isListening ? 'animate-pulse text-red-500' : 'text-purple-500'}`} />
          {isListening ? 'Listening...' : 'Speak It'}
        </Button>
        
        <Button
          onClick={handleSubmit}
          size="lg"
          disabled={!input.trim() || isLoading}
          className="bg-blue-600 hover:bg-blue-700 text-white transition-all duration-300 text-lg px-8 py-3 rounded-lg font-bold"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
          ) : (
            <Send className="w-5 h-5 mr-2" />
          )}
          {isLoading ? 'Transforming...' : 'Transform My Chaos'}
        </Button>
      </div>
    </div>
  );
};