import { useState, useEffect, useCallback, useRef } from 'react';
import { wsService } from '@services/websocket';
import type { PriceUpdate } from '@/types';

/**
 * Hook for real-time price updates via WebSocket
 */
export function useRealTimePrice(symbol: string) {
  const [price, setPrice] = useState<PriceUpdate | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let unsubscribe: (() => void) | null = null;

    const connectAndSubscribe = async () => {
      try {
        if (!wsService.isConnected()) {
          await wsService.connect();
        }
        
        setIsConnected(true);
        setError(null);

        unsubscribe = wsService.subscribeToPrice(symbol, (data) => {
          setPrice(data);
        });
      } catch (err) {
        setError(err as Error);
        setIsConnected(false);
      }
    };

    connectAndSubscribe();

    return () => {
      if (unsubscribe) {
        unsubscribe();
      }
    };
  }, [symbol]);

  return { price, isConnected, error };
}

/**
 * Hook for WebSocket connection management
 */
export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const connect = async () => {
      try {
        if (!wsService.isConnected()) {
          await wsService.connect();
          setIsConnected(true);
          setError(null);
        }
      } catch (err) {
        setError(err as Error);
        setIsConnected(false);
      }
    };

    connect();

    return () => {
      wsService.disconnect();
      setIsConnected(false);
    };
  }, []);

  const reconnect = useCallback(async () => {
    try {
      wsService.disconnect();
      await wsService.connect();
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setError(err as Error);
      setIsConnected(false);
    }
  }, []);

  return { isConnected, error, reconnect };
}

/**
 * Hook for debounced value
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook for interval execution
 */
export function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef<() => void>();

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const tick = () => {
      savedCallback.current?.();
    };

    const id = setInterval(tick, delay);
    return () => clearInterval(id);
  }, [delay]);
}

/**
 * Hook for previous value
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

/**
 * Hook for local storage with TypeScript support
 */
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`Error loading ${key} from localStorage:`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error saving ${key} to localStorage:`, error);
    }
  };

  return [storedValue, setValue];
}

/**
 * Hook for window size
 */
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}

/**
 * Hook for media query
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

/**
 * Hook for click outside detection
 */
export function useClickOutside<T extends HTMLElement>(
  callback: () => void
): React.RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const handleClick = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        callback();
      }
    };

    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [callback]);

  return ref;
}

/**
 * Hook for async operation with loading/error states
 */
export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async () => {
    setLoading(true);
    setData(null);
    setError(null);

    try {
      const result = await asyncFunction();
      setData(result);
      return result;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [asyncFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { loading, data, error, execute };
}

/**
 * Hook for copying to clipboard
 */
export function useCopyToClipboard() {
  const [copiedText, setCopiedText] = useState<string | null>(null);

  const copy = async (text: string) => {
    if (!navigator?.clipboard) {
      console.warn('Clipboard not supported');
      return false;
    }

    try {
      await navigator.clipboard.writeText(text);
      setCopiedText(text);
      setTimeout(() => setCopiedText(null), 2000);
      return true;
    } catch (error) {
      console.error('Failed to copy:', error);
      setCopiedText(null);
      return false;
    }
  };

  return { copiedText, copy };
}
