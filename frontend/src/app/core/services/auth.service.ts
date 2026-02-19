import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  currentUser = signal<User | null>(null);
  isAuthenticated = signal<boolean>(false);

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.checkAuth();
  }

  register(email: string, password: string, firstName: string, lastName: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/register`, {
      email,
      password,
      firstName,
      lastName
    }).pipe(
      tap(response => this.handleAuthSuccess(response))
    );
  }

  login(email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, {
      email,
      password
    }).pipe(
      tap(response => this.handleAuthSuccess(response))
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
    this.router.navigate(['/auth/login']);
  }

  private handleAuthSuccess(response: AuthResponse): void {
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    localStorage.setItem('current_user', JSON.stringify(response.user));
    this.currentUser.set(response.user);
    this.isAuthenticated.set(true);
  }

  private checkAuth(): void {
    const token = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('current_user');
    
    if (token && storedUser) {
      try {
        // First, set user from localStorage immediately for faster UI
        const user = JSON.parse(storedUser);
        this.currentUser.set(user);
        this.isAuthenticated.set(true);
        
        // Then verify token is still valid in background
        this.http.get<User>(`${this.apiUrl}/me`).subscribe({
          next: (user) => {
            this.currentUser.set(user);
            this.isAuthenticated.set(true);
            // Update stored user data
            localStorage.setItem('current_user', JSON.stringify(user));
          },
          error: () => {
            // Token expired or invalid, clear everything
            this.logout();
          }
        });
      } catch (e) {
        // Invalid stored data, clear everything
        this.logout();
      }
    }
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
}
