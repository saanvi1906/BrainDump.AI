import { useState, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Camera, RotateCcw, Sparkles } from 'lucide-react';

interface MoodAnalysis {
  stressLevel: number;
  fatigueLevel: number;
  suggestions: string[];
}

export const SelfieAnalyzer = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<MoodAnalysis | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [photo, setPhoto] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 300, height: 300, facingMode: 'user' } 
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error('Camera access denied:', error);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      const ctx = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      if (ctx) {
        ctx.drawImage(video, 0, 0);
        const photoData = canvas.toDataURL('image/jpeg');
        setPhoto(photoData);
        stopCamera();
        analyzeMood();
      }
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const analyzeMood = async () => {
    setIsAnalyzing(true);
    
    // Simulate facial analysis
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock analysis results
    const mockAnalysis: MoodAnalysis = {
      stressLevel: Math.floor(Math.random() * 5) + 1,
      fatigueLevel: Math.floor(Math.random() * 5) + 1,
      suggestions: [
        "Try the 4-7-8 breathing technique",
        "Drink a glass of water - you look dehydrated",
        "Take a 5-minute walk outside",
        "Do some gentle neck stretches"
      ]
    };
    
    setAnalysis(mockAnalysis);
    setIsAnalyzing(false);
  };

  const reset = () => {
    setPhoto(null);
    setAnalysis(null);
    stopCamera();
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-center">
          <Camera className="w-5 h-5 text-primary" />
          Selfie Mood Mirror
          <span className="text-sm font-normal text-muted-foreground">(Optional)</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {!stream && !photo && (
          <div className="text-center space-y-4">
            <p className="text-sm text-muted-foreground">
              Let AI analyze your stress levels and get instant relief tips
            </p>
            <Button onClick={startCamera} className="w-full">
              <Camera className="w-4 h-4 mr-2" />
              Start Camera
            </Button>
          </div>
        )}

        {stream && !photo && (
          <div className="space-y-4">
            <div className="relative rounded-lg overflow-hidden bg-muted">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-48 object-cover"
              />
              <canvas ref={canvasRef} className="hidden" />
            </div>
            <div className="flex gap-2">
              <Button onClick={capturePhoto} className="flex-1">
                <Sparkles className="w-4 h-4 mr-2" />
                Analyze My Mood
              </Button>
              <Button onClick={stopCamera} variant="outline">
                Cancel
              </Button>
            </div>
          </div>
        )}

        {photo && !analysis && isAnalyzing && (
          <div className="text-center space-y-4">
            <img src={photo} alt="Captured selfie" className="w-32 h-32 rounded-full mx-auto object-cover" />
            <div className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
              <span className="text-sm">Analyzing your mood...</span>
            </div>
          </div>
        )}

        {analysis && (
          <div className="space-y-4 animate-fade-in">
            <img src={photo!} alt="Analyzed selfie" className="w-20 h-20 rounded-full mx-auto object-cover" />
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm">Stress Level</span>
                <div className="flex gap-1">
                  {[1,2,3,4,5].map(i => (
                    <div
                      key={i}
                      className={`w-3 h-3 rounded-full ${
                        i <= analysis.stressLevel ? 'bg-red-400' : 'bg-muted'
                      }`}
                    />
                  ))}
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Fatigue Level</span>
                <div className="flex gap-1">
                  {[1,2,3,4,5].map(i => (
                    <div
                      key={i}
                      className={`w-3 h-3 rounded-full ${
                        i <= analysis.fatigueLevel ? 'bg-orange-400' : 'bg-muted'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="font-medium text-sm">Quick Fixes:</h4>
              <ul className="space-y-1">
                {analysis.suggestions.slice(0, 2).map((suggestion, i) => (
                  <li key={i} className="text-xs text-muted-foreground flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-primary" />
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>

            <Button onClick={reset} variant="outline" size="sm" className="w-full">
              <RotateCcw className="w-4 h-4 mr-2" />
              Try Again
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};