import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Heart, Zap, ArrowRight } from 'lucide-react';

interface ResultCardsProps {
  actionPlan: string[];
  wellnessReset: string;
  motivationBoost: string;
  isVisible: boolean;
}

export const ResultCards = ({ actionPlan, wellnessReset, motivationBoost, isVisible }: ResultCardsProps) => {
  if (!isVisible) return null;

  return (
    <div className="w-full max-w-5xl mx-auto space-y-8">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-bold text-black mb-4">
          Your Stress to Success Transformation
        </h2>
        <p className="text-xl text-gray-700">Here's your personalized roadmap to feeling better</p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8">
        {/* Action Plan Card */}
        <Card className="p-8 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-purple-600 rounded-3xl flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-2xl md:text-3xl font-bold text-black">Action Plan</h3>
                <Badge className="bg-purple-100 text-purple-800 border-purple-200">Step by step</Badge>
              </div>
            </div>
            <div className="space-y-4">
              {actionPlan.map((step, index) => (
                <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-2xl">
                  <span className="bg-purple-600 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    {index + 1}
                  </span>
                  <p className="text-lg leading-relaxed text-gray-800">{step}</p>
                </div>
              ))}
            </div>
          </div>
        </Card>

        {/* Wellness Reset Card */}
        <Card className="p-8 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-blue-600 rounded-3xl flex items-center justify-center">
                <Heart className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-2xl md:text-3xl font-bold text-black">Wellness Reset</h3>
                <Badge className="bg-blue-100 text-blue-800 border-blue-200">Quick fix</Badge>
              </div>
            </div>
            <div className="p-6 bg-gray-50 rounded-2xl">
              <p className="text-lg leading-relaxed text-gray-800 mb-4">{wellnessReset}</p>
              <div className="flex items-center text-blue-600 font-semibold">
                <ArrowRight className="w-5 h-5 mr-2" />
                Takes 2-5 minutes
              </div>
            </div>
          </div>
        </Card>

        {/* Motivation Card */}
        <Card className="p-8 hover:shadow-lg transition-all duration-300 border-gray-200 bg-white">
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-green-600 rounded-3xl flex items-center justify-center">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-2xl md:text-3xl font-bold text-black">Motivation</h3>
                <Badge className="bg-green-100 text-green-800 border-green-200">Mind shift</Badge>
              </div>
            </div>
            <div className="p-6 bg-gray-50 rounded-2xl">
              <p className="text-lg leading-relaxed font-medium italic text-gray-800 mb-4">"{motivationBoost}"</p>
              <div className="text-center">
                <div className="inline-flex items-center text-green-600 font-bold">
                  <Zap className="w-5 h-5 mr-2" />
                  You've got this!
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};