import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  attachments?: any[];
  metadata?: any;
}

export interface ChatSession {
  id: string;
  lastMessage: string;
  updatedAt: string;
  messageCount: number;
}

export interface ChatResponse {
  response: string;
  intent?: string;
  needs_followup?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  sendQuickMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.apiUrl}/message`, { message });
  }

  getSessions(): Observable<{ sessions: ChatSession[] }> {
    return this.http.get<{ sessions: ChatSession[] }>(`${this.apiUrl}/sessions`);
  }

  createSession(): Observable<{ session_id: string }> {
    return this.http.post<{ session_id: string }>(`${this.apiUrl}/sessions`, {});
  }

  getSession(sessionId: string): Observable<{ id: string; messages: ChatMessage[]; createdAt: string; updatedAt: string }> {
    return this.http.get<any>(`${this.apiUrl}/sessions/${sessionId}`);
  }

  sendMessage(sessionId: string, content: string): Observable<{ user_message: ChatMessage; assistant_message: ChatMessage }> {
    return this.http.post<any>(`${this.apiUrl}/sessions/${sessionId}/messages`, { content });
  }
}
