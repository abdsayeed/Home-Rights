import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { ChatService } from '../../core/services/chat.service';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="chat-container">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2>HomeRights AI</h2>
        </div>
        
        <nav class="nav-menu">
          <a routerLink="/chat" class="nav-item active">
            <span class="material-icons">chat</span>
            Chat
          </a>
          <a routerLink="/topics" class="nav-item">
            <span class="material-icons">menu_book</span>
            Topics
          </a>
          <a routerLink="/documents" class="nav-item">
            <span class="material-icons">upload_file</span>
            Documents
          </a>
          <a routerLink="/support" class="nav-item">
            <span class="material-icons">support_agent</span>
            Support
          </a>
        </nav>

        <div class="sidebar-footer">
          <div class="user-info">
            <span class="material-icons">account_circle</span>
            <span>{{ authService.currentUser()?.firstName }}</span>
          </div>
          <button (click)="authService.logout()" class="logout-btn">
            <span class="material-icons">logout</span>
          </button>
        </div>
      </aside>

      <main class="chat-main">
        <div class="messages-container" #messagesContainer>
          <div class="welcome-message" *ngIf="messages().length === 0">
            <h1>Welcome to HomeRights AI</h1>
            <p>I'm here to help you understand your housing rights in the UK.</p>
            <div class="suggestions">
              <button (click)="sendSuggestion('My landlord is asking for a £3,000 non-refundable deposit. Is this legal?')" class="suggestion">
                Is a non-refundable deposit legal?
              </button>
              <button (click)="sendSuggestion('My tenancy agreement says I am responsible for all repairs including structural repairs. Is this fair?')" class="suggestion">
                Who's responsible for repairs?
              </button>
              <button (click)="sendSuggestion('I received a Section 21 eviction notice. What should I do?')" class="suggestion">
                I received a Section 21 notice
              </button>
              <button (click)="sendSuggestion('My landlord wants to increase my rent by 20%. Can they do this?')" class="suggestion">
                Can my landlord increase rent by 20%?
              </button>
              <button (click)="sendSuggestion('What are my rights as a tenant in the UK?')" class="suggestion">
                What are my tenant rights?
              </button>
            </div>
          </div>

          <div class="message" *ngFor="let message of messages()" [class.user]="message.role === 'user'">
            <div class="message-avatar">
              <span class="material-icons">
                {{ message.role === 'user' ? 'person' : 'smart_toy' }}
              </span>
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>

          <div class="message" *ngIf="isLoading()">
            <div class="message-avatar">
              <span class="material-icons">smart_toy</span>
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="input-container">
          <div class="input-wrapper">
            <textarea
              [(ngModel)]="userInput"
              (keydown.enter)="onEnter($event)"
              placeholder="Ask about your housing rights..."
              rows="1"
            ></textarea>
            <button (click)="sendMessage()" [disabled]="!userInput.trim() || isLoading()">
              <span class="material-icons">send</span>
            </button>
          </div>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .chat-container {
      display: flex;
      height: 100vh;
      background: var(--bg);
    }

    .sidebar {
      width: 260px;
      background: #fff;
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
    }

    .sidebar-header {
      padding: 20px;
      border-bottom: 1px solid var(--border);
    }

    .sidebar-header h2 {
      font-family: 'Instrument Serif', serif;
      font-size: 18px;
      font-weight: 400;
      color: var(--ink);
    }

    .sidebar-header h2::after {
      content: ' AI';
      color: var(--teal);
      font-style: italic;
    }

    .nav-menu {
      flex: 1;
      padding: 16px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      border-radius: var(--r-sm);
      color: var(--ink3);
      text-decoration: none;
      margin-bottom: 4px;
      transition: all 0.2s;
      font-size: 14px;
      font-weight: 500;
    }

    .nav-item:hover {
      background: var(--bg2);
      color: var(--ink);
    }

    .nav-item.active {
      background: var(--teal-lt);
      color: var(--teal);
      border: 1px solid var(--teal-mid);
    }

    .sidebar-footer {
      padding: 16px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--ink);
      font-size: 14px;
      font-weight: 500;
    }

    .logout-btn {
      background: none;
      border: none;
      color: var(--ink3);
      cursor: pointer;
      padding: 8px;
      border-radius: 6px;
      transition: all 0.2s;
    }

    .logout-btn:hover {
      background: var(--red-lt);
      color: var(--red);
    }

    .chat-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      max-width: 900px;
      margin: 0 auto;
      width: 100%;
    }

    .messages-container {
      flex: 1;
      overflow-y: auto;
      padding: 32px 24px;
    }

    .welcome-message {
      text-align: center;
      padding: 80px 20px;
    }

    .welcome-message h1 {
      font-family: 'Instrument Serif', serif;
      font-size: 40px;
      font-weight: 400;
      letter-spacing: -1px;
      color: var(--ink);
      margin-bottom: 16px;
      line-height: 1.1;
    }

    .welcome-message p {
      color: var(--ink3);
      font-size: 17px;
      margin-bottom: 48px;
      font-weight: 300;
    }

    .suggestions {
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-width: 560px;
      margin: 0 auto;
    }

    .suggestion {
      padding: 18px 20px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--r);
      cursor: pointer;
      transition: all 0.2s;
      text-align: left;
      color: var(--ink2);
      font-size: 14px;
      line-height: 1.5;
      box-shadow: var(--shadow-sm);
    }

    .suggestion:hover {
      border-color: var(--teal);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
      color: var(--ink);
    }

    .message {
      display: flex;
      gap: 16px;
      margin-bottom: 28px;
      animation: fadeUp 0.3s ease;
    }

    .message-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: var(--teal-lt);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      border: 1px solid var(--teal-mid);
    }

    .message.user .message-avatar {
      background: #edf4ff;
      border: 1px solid #b8d4f7;
    }

    .message-avatar .material-icons {
      font-size: 20px;
      color: var(--teal);
    }

    .message.user .message-avatar .material-icons {
      color: #3b7dd8;
    }

    .message-content {
      flex: 1;
    }

    .message-text {
      background: #fff;
      padding: 14px 18px;
      border-radius: var(--r);
      color: var(--ink);
      line-height: 1.7;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-size: 14px;
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
    }

    .message-text strong,
    .message-text b {
      font-weight: 600;
      color: var(--ink);
    }

    .message.user .message-text {
      background: var(--teal-lt);
      border-color: var(--teal-mid);
    }

    .message-time {
      font-size: 12px;
      color: var(--ink4);
      margin-top: 6px;
      padding-left: 4px;
    }

    .typing-indicator {
      display: flex;
      gap: 4px;
      padding: 14px 18px;
    }

    .typing-indicator span {
      width: 8px;
      height: 8px;
      background: var(--teal-mid);
      border-radius: 50%;
      animation: typing 1.4s infinite;
    }

    .typing-indicator span:nth-child(2) {
      animation-delay: 0.2s;
    }

    .typing-indicator span:nth-child(3) {
      animation-delay: 0.4s;
    }

    @keyframes typing {
      0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
      }
      30% {
        transform: translateY(-10px);
        opacity: 1;
      }
    }

    .input-container {
      padding: 24px;
      background: #fff;
      border-top: 1px solid var(--border);
    }

    .input-wrapper {
      display: flex;
      gap: 12px;
      max-width: 900px;
      margin: 0 auto;
    }

    textarea {
      flex: 1;
      padding: 14px 18px;
      border: 1.5px solid var(--border);
      border-radius: var(--r);
      font-family: inherit;
      font-size: 14px;
      resize: none;
      max-height: 120px;
      transition: border-color 0.2s;
    }

    textarea:focus {
      outline: none;
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0, 168, 138, 0.1);
    }

    .input-wrapper button {
      width: 48px;
      height: 48px;
      background: var(--teal);
      border: none;
      border-radius: var(--r);
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      box-shadow: 0 2px 12px rgba(0, 168, 138, 0.28);
    }

    .input-wrapper button:hover:not(:disabled) {
      background: #009a7e;
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(0, 168, 138, 0.35);
    }

    .input-wrapper button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    @media (max-width: 768px) {
      .sidebar {
        display: none;
      }

      .chat-main {
        width: 100%;
      }
    }
  `]
})
export class ChatComponent {
  messages = signal<Message[]>([]);
  userInput = '';
  isLoading = signal(false);
  sessionId = signal<string | null>(null);

  constructor(
    public authService: AuthService,
    private chatService: ChatService
  ) {
    // Create a new chat session when component loads
    this.initializeSession();
  }

  initializeSession(): void {
    this.chatService.createSession().subscribe({
      next: (response) => {
        this.sessionId.set(response.session_id);
      },
      error: (err) => {
        console.error('Failed to create chat session:', err);
      }
    });
  }

  sendMessage(): void {
    if (!this.userInput.trim() || this.isLoading() || !this.sessionId()) return;

    const userMessage: Message = {
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    };

    this.messages.update(msgs => [...msgs, userMessage]);
    const messageText = this.userInput;
    this.userInput = '';
    this.isLoading.set(true);

    // Send to intelligent chat service with session context
    this.chatService.sendMessage(this.sessionId()!, messageText).subscribe({
      next: (response) => {
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.assistant_message.content || 'I apologize, but I had trouble processing that. Could you rephrase your question?',
          timestamp: new Date(response.assistant_message.timestamp)
        };
        
        this.messages.update(msgs => [...msgs, assistantMessage]);
        this.isLoading.set(false);
        
        // Auto-scroll to bottom
        setTimeout(() => this.scrollToBottom(), 100);
      },
      error: (err) => {
        const assistantMessage: Message = {
          role: 'assistant',
          content: 'I apologize, but I encountered an error. Please try again or contact support if the issue persists.',
          timestamp: new Date()
        };
        this.messages.update(msgs => [...msgs, assistantMessage]);
        this.isLoading.set(false);
      }
    });
  }

  sendSuggestion(text: string): void {
    this.userInput = text;
    this.sendMessage();
  }

  onEnter(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;
    if (keyboardEvent.key === 'Enter' && !keyboardEvent.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  formatTime(date: Date): string {
    return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
  }

  scrollToBottom(): void {
    // Scroll chat to bottom after new message
    const container = document.querySelector('.messages-container');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }
}
