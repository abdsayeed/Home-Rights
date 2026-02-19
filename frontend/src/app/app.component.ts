import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, CommonModule],
  template: `
    <div class="app-container">
      <nav class="main-nav" *ngIf="authService.isAuthenticated()">
        <div class="nav-content">
          <div class="nav-logo">
            <div class="logo-icon">
              <span>H</span>
            </div>
            <span class="logo-text serif">HomeRights <span class="logo-ai">AI</span></span>
          </div>
          
          <div class="nav-links">
            <a routerLink="/dashboard" routerLinkActive="active" class="nav-link">Dashboard</a>
            <a routerLink="/documents" routerLinkActive="active" class="nav-link">Documents</a>
            <a routerLink="/chat" routerLinkActive="active" class="nav-link">Assistant</a>
            <a routerLink="/topics" routerLinkActive="active" class="nav-link">Topics</a>
            <a routerLink="/support" routerLinkActive="active" class="nav-link">Support</a>
          </div>

          <div class="nav-actions">
            <span class="user-name">{{ authService.currentUser()?.firstName }}</span>
            <button (click)="logout()" class="btn-ghost" style="padding: 8px 18px; font-size: 13px">
              Sign out
            </button>
          </div>
        </div>
      </nav>
      
      <main class="main-content" [class.with-nav]="authService.isAuthenticated()">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      background: var(--bg);
    }

    .main-nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 100;
      background: rgba(250, 250, 248, 0.95);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      height: 64px;
    }

    .nav-content {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 48px;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 32px;
    }

    .nav-logo {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }

    .logo-icon {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--teal);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(0, 168, 138, 0.3);
    }

    .logo-icon span {
      color: #fff;
      font-weight: 800;
      font-size: 16px;
      font-family: 'Instrument Serif', serif;
    }

    .logo-text {
      font-size: 17px;
      color: var(--ink);
      letter-spacing: -0.3px;
    }

    .logo-ai {
      color: var(--teal);
      font-style: italic;
    }

    .nav-links {
      display: flex;
      gap: 28px;
      align-items: center;
      flex: 1;
      justify-content: center;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 16px;
      flex-shrink: 0;
    }

    .user-name {
      font-size: 14px;
      font-weight: 500;
      color: var(--ink2);
    }

    .main-content {
      min-height: 100vh;
    }

    .main-content.with-nav {
      padding-top: 64px;
    }

    @media (max-width: 768px) {
      .nav-content {
        padding: 0 24px;
      }

      .nav-links {
        display: none;
      }

      .user-name {
        display: none;
      }
    }
  `]
})
export class AppComponent {
  title = 'HomeRights AI';

  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
