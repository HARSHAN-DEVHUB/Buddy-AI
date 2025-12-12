import { io, Socket } from 'socket.io-client';
import type { PriceUpdate, Prediction } from '@/types';

type SubscriptionCallback<T> = (data: T) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private subscriptions: Map<string, Set<SubscriptionCallback<unknown>>> = new Map();
  private isConnecting = false;

  constructor() {
    this.url = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
  }

  /**
   * Connect to WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.socket?.connected) {
        resolve();
        return;
      }

      if (this.isConnecting) {
        reject(new Error('Connection already in progress'));
        return;
      }

      this.isConnecting = true;

      this.socket = io(this.url, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectDelay,
        reconnectionDelayMax: 5000,
        timeout: 10000,
        auth: {
          token: localStorage.getItem('auth_token'),
        },
      });

      this.socket.on('connect', () => {
        console.log('✅ WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.resubscribeAll();
        resolve();
      });

      this.socket.on('disconnect', (reason) => {
        console.warn('⚠️ WebSocket disconnected:', reason);
        this.isConnecting = false;
      });

      this.socket.on('connect_error', (error) => {
        console.error('❌ WebSocket connection error:', error.message);
        this.isConnecting = false;
        
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          reject(new Error('Max reconnection attempts reached'));
        } else {
          this.reconnectAttempts++;
        }
      });

      this.socket.on('error', (error) => {
        console.error('❌ WebSocket error:', error);
      });

      // Handle message types
      this.socket.on('price_update', (data: PriceUpdate) => {
        this.emit('price_update', data);
      });

      this.socket.on('prediction_update', (data: Prediction) => {
        this.emit('prediction_update', data);
      });

      this.socket.on('alert', (data: unknown) => {
        this.emit('alert', data);
      });
    });
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.subscriptions.clear();
      console.log('🔌 WebSocket disconnected');
    }
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.socket?.connected || false;
  }

  /**
   * Subscribe to price updates for a symbol
   */
  subscribeToPrice(symbol: string, callback: SubscriptionCallback<PriceUpdate>): () => void {
    const event = `price:${symbol}`;
    
    if (!this.subscriptions.has(event)) {
      this.subscriptions.set(event, new Set());
      // Send subscription request to server
      this.socket?.emit('subscribe', { type: 'price', symbol });
    }

    this.subscriptions.get(event)!.add(callback as SubscriptionCallback<unknown>);

    // Return unsubscribe function
    return () => this.unsubscribeFromPrice(symbol, callback);
  }

  /**
   * Unsubscribe from price updates
   */
  unsubscribeFromPrice(symbol: string, callback: SubscriptionCallback<PriceUpdate>): void {
    const event = `price:${symbol}`;
    const callbacks = this.subscriptions.get(event);

    if (callbacks) {
      callbacks.delete(callback as SubscriptionCallback<unknown>);
      
      if (callbacks.size === 0) {
        this.subscriptions.delete(event);
        // Send unsubscription request to server
        this.socket?.emit('unsubscribe', { type: 'price', symbol });
      }
    }
  }

  /**
   * Subscribe to prediction updates
   */
  subscribeToPredictions(callback: SubscriptionCallback<Prediction>): () => void {
    const event = 'prediction_update';
    
    if (!this.subscriptions.has(event)) {
      this.subscriptions.set(event, new Set());
    }

    this.subscriptions.get(event)!.add(callback as SubscriptionCallback<unknown>);

    return () => {
      const callbacks = this.subscriptions.get(event);
      if (callbacks) {
        callbacks.delete(callback as SubscriptionCallback<unknown>);
      }
    };
  }

  /**
   * Subscribe to alerts
   */
  subscribeToAlerts(callback: SubscriptionCallback<unknown>): () => void {
    const event = 'alert';
    
    if (!this.subscriptions.has(event)) {
      this.subscriptions.set(event, new Set());
    }

    this.subscriptions.get(event)!.add(callback);

    return () => {
      const callbacks = this.subscriptions.get(event);
      if (callbacks) {
        callbacks.delete(callback);
      }
    };
  }

  /**
   * Subscribe to order book updates
   */
  subscribeToOrderBook(symbol: string, callback: SubscriptionCallback<unknown>): () => void {
    const event = `orderbook:${symbol}`;
    
    if (!this.subscriptions.has(event)) {
      this.subscriptions.set(event, new Set());
      this.socket?.emit('subscribe', { type: 'orderbook', symbol });
    }

    this.subscriptions.get(event)!.add(callback);

    return () => {
      const callbacks = this.subscriptions.get(event);
      if (callbacks) {
        callbacks.delete(callback);
        if (callbacks.size === 0) {
          this.subscriptions.delete(event);
          this.socket?.emit('unsubscribe', { type: 'orderbook', symbol });
        }
      }
    };
  }

  /**
   * Emit event to all subscribers
   */
  private emit<T>(event: string, data: T): void {
    const callbacks = this.subscriptions.get(event);
    if (callbacks) {
      callbacks.forEach((callback) => {
        try {
          (callback as SubscriptionCallback<T>)(data);
        } catch (error) {
          console.error(`Error in subscription callback for ${event}:`, error);
        }
      });
    }
  }

  /**
   * Resubscribe to all previous subscriptions (after reconnect)
   */
  private resubscribeAll(): void {
    this.subscriptions.forEach((_callbacks, event) => {
      if (event.startsWith('price:')) {
        const symbol = event.split(':')[1];
        this.socket?.emit('subscribe', { type: 'price', symbol });
      } else if (event.startsWith('orderbook:')) {
        const symbol = event.split(':')[1];
        this.socket?.emit('subscribe', { type: 'orderbook', symbol });
      }
    });
  }

  /**
   * Send custom message to server
   */
  send<T>(event: string, data: T): void {
    if (!this.socket?.connected) {
      console.warn('WebSocket not connected. Message not sent.');
      return;
    }
    this.socket.emit(event, data);
  }
}

// Export singleton instance
export const wsService = new WebSocketService();
