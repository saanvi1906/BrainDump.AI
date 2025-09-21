import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, DumpRequest, DumpResponse } from './api';
import { useToast } from '@/hooks/use-toast';

// Query keys
export const queryKeys = {
  health: ['health'] as const,
  recentEntries: (userId: string, limit: number) => ['recent', userId, limit] as const,
};

// Health check hook
export const useHealthCheck = () => {
  return useQuery({
    queryKey: queryKeys.health,
    queryFn: () => apiClient.healthCheck(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });
};

// Create dump mutation
export const useCreateDump = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (dumpData: DumpRequest) => apiClient.createDump(dumpData),
    onSuccess: (data) => {
      // Invalidate recent entries queries
      queryClient.invalidateQueries({ queryKey: ['recent'] });
      
      toast({
        title: "Transformation Complete! ✨",
        description: "Your stress has been converted into actionable steps.",
      });
    },
    onError: (error) => {
      console.error('Failed to create dump:', error);
      toast({
        title: "Oops! Something went wrong",
        description: "Please try again in a moment.",
        variant: "destructive",
      });
    },
  });
};

// Get recent entries hook
export const useRecentEntries = (userId: string, limit: number = 5) => {
  return useQuery({
    queryKey: queryKeys.recentEntries(userId, limit),
    queryFn: () => apiClient.getRecentEntries(userId, limit),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};
