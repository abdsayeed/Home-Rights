import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="auth-container">
      <div class="auth-card">
        <h1>Welcome to HomeRights AI</h1>
        <p class="subtitle">Sign in to access your housing rights assistant</p>
        
        <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              type="email" 
              formControlName="email"
              placeholder="your@email.com"
            />
            <div class="error" *ngIf="loginForm.get('email')?.invalid && loginForm.get('email')?.touched">
              Please enter a valid email
            </div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input 
              id="password" 
              type="password" 
              formControlName="password"
              placeholder="••••••••"
            />
            <div class="error" *ngIf="loginForm.get('password')?.invalid && loginForm.get('password')?.touched">
              Password is required
            </div>
          </div>

          <div class="error" *ngIf="errorMessage">{{ errorMessage }}</div>

          <button type="submit" [disabled]="loginForm.invalid || isLoading">
            {{ isLoading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <p class="footer-text">
          Don't have an account? <a routerLink="/auth/register">Sign up</a>
        </p>
      </div>
    </div>
  `,
  styles: [`
    .auth-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--bg);
      padding: 20px;
      position: relative;
      overflow: hidden;
    }

    .auth-container::before {
      content: '';
      position: absolute;
      width: 500px;
      height: 500px;
      background: rgba(0, 168, 138, 0.08);
      border-radius: 50%;
      filter: blur(80px);
      top: -100px;
      left: -100px;
      pointer-events: none;
    }

    .auth-container::after {
      content: '';
      position: absolute;
      width: 400px;
      height: 400px;
      background: rgba(124, 106, 240, 0.06);
      border-radius: 50%;
      filter: blur(80px);
      bottom: -100px;
      right: -100px;
      pointer-events: none;
    }

    .auth-card {
      background: #fff;
      padding: 48px;
      border-radius: var(--r);
      box-shadow: var(--shadow-lg);
      max-width: 420px;
      width: 100%;
      border: 1px solid var(--border);
      position: relative;
      z-index: 1;
      animation: scaleIn 0.5s ease;
    }

    h1 {
      font-family: 'Instrument Serif', serif;
      font-size: 32px;
      font-weight: 400;
      letter-spacing: -0.8px;
      margin-bottom: 8px;
      color: var(--ink);
    }

    .subtitle {
      color: var(--ink3);
      margin-bottom: 36px;
      font-size: 15px;
    }

    .form-group {
      margin-bottom: 24px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--ink);
      font-size: 14px;
    }

    input {
      width: 100%;
      padding: 14px 16px;
      border: 1.5px solid var(--border);
      border-radius: var(--r-sm);
      font-size: 14px;
      transition: all 0.2s;
      font-family: 'Inter', sans-serif;
    }

    input:focus {
      outline: none;
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(0, 168, 138, 0.1);
    }

    .error {
      color: var(--red);
      font-size: 13px;
      margin-top: 8px;
      padding: 12px 16px;
      background: var(--red-lt);
      border-radius: var(--r-sm);
      border: 1px solid #f5b5b0;
    }

    button {
      width: 100%;
      padding: 14px;
      background: var(--teal);
      color: #fff;
      border: none;
      border-radius: var(--r-full);
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      box-shadow: 0 2px 12px rgba(0, 168, 138, 0.28);
      margin-top: 8px;
    }

    button:hover:not(:disabled) {
      background: #009a7e;
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(0, 168, 138, 0.35);
    }

    button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    .footer-text {
      text-align: center;
      margin-top: 28px;
      color: var(--ink3);
      font-size: 14px;
    }

    .footer-text a {
      color: var(--teal);
      text-decoration: none;
      font-weight: 600;
      transition: color 0.2s;
    }

    .footer-text a:hover {
      color: #009a7e;
    }
  `]
})
export class LoginComponent {
  loginForm: FormGroup;
  isLoading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';

      const { email, password } = this.loginForm.value;

      this.authService.login(email, password).subscribe({
        next: () => {
          // Redirect based on user role
          const user = this.authService.currentUser();
          if (user?.role === 'admin' || user?.role === 'super_admin') {
            this.router.navigate(['/admin']);
          } else {
            this.router.navigate(['/chat']);
          }
        },
        error: (error) => {
          this.isLoading = false;
          this.errorMessage = error.error?.error || 'Login failed. Please try again.';
        }
      });
    }
  }
}
