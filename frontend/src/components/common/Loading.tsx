import { cn } from '@utils/helpers';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className }: LoadingSpinnerProps) {
  return (
    <div
      className={cn(
        'inline-block animate-spin rounded-full border-4 border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]',
        {
          'h-4 w-4 border-2': size === 'sm',
          'h-8 w-8 border-4': size === 'md',
          'h-12 w-12 border-4': size === 'lg',
        },
        className
      )}
      role="status"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}

interface LoadingProps {
  text?: string;
  fullScreen?: boolean;
}

export default function Loading({ text = 'Loading...', fullScreen = false }: LoadingProps) {
  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
        <div className="flex flex-col items-center gap-4">
          <LoadingSpinner size="lg" className="text-primary" />
          <p className="text-sm text-muted-foreground">{text}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <LoadingSpinner size="md" className="text-primary" />
      <p className="mt-4 text-sm text-muted-foreground">{text}</p>
    </div>
  );
}
